"""
Difficulty calculation service for Wakfu items

Difficulty is calculated based on:
1. Harvest cost (if item is from collection)
2. Recipe cost (if item is from crafting, recursive)
3. Drop difficulty (manual input for mob drops)
4. Item flags (epic, relic, gem slots)
5. Rarity
6. Level
"""

from sqlalchemy.orm import Session
from app.db.models import Item, Recipe, HarvestResource
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)

# Normalization percentiles (will be calculated from actual data)
HARVEST_PERCENTILE_95 = 100.0
RECIPE_PERCENTILE_95 = 100.0

def calculate_harvest_cost(item: Item, db: Session) -> float:
    """
    Calculate harvest cost for collectible items
    
    Formula: (collection_time * visibility + consumption) / (drop_rate * quantity)
    Normalized by 95th percentile
    """
    harvest = db.query(HarvestResource).filter(
        HarvestResource.item_id == item.item_id
    ).first()
    
    if not harvest:
        return 0.0
    
    # Base harvest calculation
    time_cost = harvest.collection_time * harvest.visibility
    consumption = 1.0  # Base consumption cost
    
    harvest_cost = (time_cost + consumption) / (harvest.drop_rate * harvest.quantity)
    
    # Normalize by percentile (0-100 scale)
    normalized = min(100.0, (harvest_cost / HARVEST_PERCENTILE_95) * 100.0)
    
    return normalized

def calculate_recipe_cost(item: Item, db: Session, visited: Optional[set] = None) -> float:
    """
    Calculate recipe cost recursively
    
    Formula: Σ(difficulty(ingredient) * quantity) + craft_cost
    """
    if visited is None:
        visited = set()
    
    # Prevent infinite recursion
    if item.item_id in visited:
        return 0.0
    
    visited.add(item.item_id)
    
    recipe = db.query(Recipe).filter(
        Recipe.result_item_id == item.item_id
    ).first()
    
    if not recipe:
        return 0.0
    
    total_cost = recipe.craft_cost
    
    # Recursively calculate ingredient costs
    for ingredient in recipe.ingredients:
        ingredient_item = db.query(Item).filter(
            Item.item_id == ingredient["item_id"]
        ).first()
        
        if ingredient_item:
            ingredient_difficulty = calculate_item_difficulty(
                ingredient_item, db, visited.copy()
            )
            total_cost += ingredient_difficulty * ingredient["quantity"]
    
    # Normalize
    normalized = min(100.0, (total_cost / RECIPE_PERCENTILE_95) * 100.0)
    
    return normalized

def calculate_drop_difficulty(item: Item) -> float:
    """
    Get drop difficulty from manual input
    
    Returns manual_drop_difficulty if set, otherwise default value
    """
    if item.manual_drop_difficulty is not None:
        return item.manual_drop_difficulty
    
    # Default difficulty for drops without manual value
    return 70.0

def calculate_flag_score(item: Item) -> float:
    """
    Calculate difficulty score from item flags
    
    - Epic: +20
    - Relic: +30
    - Gem slot: +10
    """
    score = 0.0
    
    if item.is_epic:
        score += 20.0
    if item.is_relic:
        score += 30.0
    if item.has_gem_slot:
        score += 10.0
    
    return score

def calculate_rarity_score(item: Item) -> float:
    """
    Calculate difficulty score from rarity
    
    Scale: 0 (common) to 40 (legendary)
    """
    # Rarity: 0=common, 1=unusual, 2=rare, 3=mythical, 4=legendary, 5=relic, 6=souvenir, 7=epic
    rarity_map = {
        0: 10.0,  # common
        1: 15.0,  # unusual
        2: 20.0,  # rare
        3: 30.0,  # mythical
        4: 40.0,  # legendary
        5: 35.0,  # relic
        6: 25.0,  # souvenir
        7: 35.0,  # epic
    }
    
    return rarity_map.get(item.rarity, 10.0)

def calculate_level_score(item: Item) -> float:
    """
    Calculate difficulty score from item level
    
    Scale: 0-100 based on level (0-230)
    """
    max_level = 230.0
    return min(100.0, (item.level / max_level) * 100.0)

def calculate_item_difficulty(
    item: Item,
    db: Session,
    visited: Optional[set] = None
) -> float:
    """
    Calculate total difficulty for an item
    
    Weighted formula:
    difficulty = 0.3 * harvest_cost +
                 0.3 * recipe_cost +
                 0.2 * flag_score +
                 0.1 * rarity_score +
                 0.1 * level_score
    """
    harvest_cost = 0.0
    recipe_cost = 0.0
    drop_cost = 0.0
    
    # Calculate source-specific costs
    if item.source_type == "harvest":
        harvest_cost = calculate_harvest_cost(item, db)
    elif item.source_type == "recipe":
        recipe_cost = calculate_recipe_cost(item, db, visited)
    elif item.source_type == "drop":
        drop_cost = calculate_drop_difficulty(item)
    
    # Calculate modifier scores
    flag_score = calculate_flag_score(item)
    rarity_score = calculate_rarity_score(item)
    level_score = calculate_level_score(item)
    
    # Weighted combination
    difficulty = (
        0.3 * harvest_cost +
        0.3 * recipe_cost +
        0.2 * drop_cost +
        0.1 * flag_score +
        0.1 * rarity_score +
        0.1 * level_score
    )
    
    return min(100.0, difficulty)

def recalculate_all_difficulties(db: Session):
    """
    Recalculate difficulties for all items
    
    Useful after updating harvest/recipe data or manual drop difficulties
    """
    items = db.query(Item).all()
    
    for item in items:
        item.difficulty = calculate_item_difficulty(item, db)
    
    db.commit()
    
    logger.info(f"Recalculated difficulties for {len(items)} items")

