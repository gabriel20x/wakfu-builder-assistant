"""
Difficulty calculation service for Wakfu items

Difficulty is calculated based on:
1. Harvest cost (if item is from collection)
2. Recipe cost (if item is from crafting, recursive)
3. Drop difficulty (based on actual drop rates from monster_drops)
4. Item flags (epic, relic, gem slots)
5. Rarity
6. Level
"""

from sqlalchemy.orm import Session
from app.db.models import Item, Recipe, HarvestResource, MonsterDrop
from typing import Dict, Optional
import logging
import math

logger = logging.getLogger(__name__)

# Normalization percentiles (will be calculated from actual data)
HARVEST_PERCENTILE_95 = 100.0
RECIPE_PERCENTILE_95 = 100.0

# Drop rate difficulty curve parameters
# Lower drop rates = higher difficulty
DROP_RATE_BASE_DIFFICULTY = 20.0  # Minimum difficulty for 100% drop rate
DROP_RATE_MAX_DIFFICULTY = 95.0   # Maximum difficulty for very rare drops

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
    
    Formula: 
    - Base cost from craft_cost
    - Ingredient cost: Σ(difficulty(ingredient) * quantity_factor)
    - Complexity penalty: Based on number of different ingredients
    - Large quantity penalty: Extra cost for ingredients requiring many units
    
    Examples:
    - Simple recipe (2 ingredients, low qty): Low difficulty
    - Complex recipe (5+ ingredients): Medium difficulty
    - High quantity recipe (75+ units of something): High difficulty
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
    
    # Base crafting cost
    total_cost = recipe.craft_cost * 10.0  # Scale up craft_cost impact
    
    # Track recipe complexity
    num_ingredients = len(recipe.ingredients)
    total_ingredient_quantity = 0
    
    # Recursively calculate ingredient costs
    for ingredient in recipe.ingredients:
        ingredient_item = db.query(Item).filter(
            Item.item_id == ingredient["item_id"]
        ).first()
        
        quantity = ingredient["quantity"]
        total_ingredient_quantity += quantity
        
        if ingredient_item:
            # Get base difficulty of ingredient
            ingredient_difficulty = calculate_item_difficulty(
                ingredient_item, db, visited.copy()
            )
            
            # Quantity scaling factor
            # Linear for 1-10, then logarithmic for larger quantities
            if quantity <= 10:
                quantity_factor = quantity
            else:
                # Log scale: 10=10, 20=13, 50=17, 100=20, 200=23
                quantity_factor = 10 + math.log10(quantity) * 3
            
            # Add weighted ingredient cost
            total_cost += ingredient_difficulty * (quantity_factor / 10.0)
    
    # Complexity penalty based on number of different ingredients
    # 1-2 ingredients: no penalty
    # 3-4 ingredients: +10
    # 5-6 ingredients: +20
    # 7+ ingredients: +30
    if num_ingredients >= 7:
        complexity_penalty = 30.0
    elif num_ingredients >= 5:
        complexity_penalty = 20.0
    elif num_ingredients >= 3:
        complexity_penalty = 10.0
    else:
        complexity_penalty = 0.0
    
    total_cost += complexity_penalty
    
    # Large batch penalty (if total quantity > 100)
    if total_ingredient_quantity > 100:
        batch_penalty = min(20.0, (total_ingredient_quantity - 100) / 10.0)
        total_cost += batch_penalty
    
    # Normalize to 0-100 scale
    normalized = min(100.0, total_cost)
    
    return normalized

def calculate_drop_difficulty(item: Item, db: Session) -> float:
    """
    Calculate drop difficulty based on actual drop rates from monster_drops
    
    Formula: Logarithmic scale based on best (highest) drop rate
    - 100% drop rate = 20 difficulty (very easy)
    - 50% drop rate = 35 difficulty (easy)
    - 10% drop rate = 55 difficulty (medium)
    - 1% drop rate = 75 difficulty (hard)
    - 0.1% drop rate = 95 difficulty (very hard)
    
    Falls back to manual_drop_difficulty if no drop data exists
    """
    # Check if we have actual drop data
    drops = db.query(MonsterDrop).filter(
        MonsterDrop.item_id == item.item_id
    ).all()
    
    if drops:
        # Use the BEST (highest) drop rate for difficulty calculation
        # This represents the "easiest" way to farm the item
        best_drop_rate = max(drop.drop_rate for drop in drops)
        
        # Logarithmic difficulty curve
        # Higher drop rate = lower difficulty
        if best_drop_rate >= 1.0:
            # 100%+ drop rate (very easy)
            difficulty = DROP_RATE_BASE_DIFFICULTY
        elif best_drop_rate <= 0.0001:
            # 0.01% or less (extremely rare)
            difficulty = DROP_RATE_MAX_DIFFICULTY
        else:
            # Logarithmic scale: difficulty = base + (max - base) * (-log10(rate) / 4)
            # rate=1.0 (100%) -> log=0 -> difficulty=20
            # rate=0.1 (10%) -> log=1 -> difficulty=38.75
            # rate=0.01 (1%) -> log=2 -> difficulty=57.5
            # rate=0.001 (0.1%) -> log=3 -> difficulty=76.25
            # rate=0.0001 (0.01%) -> log=4 -> difficulty=95
            log_rate = -math.log10(best_drop_rate)
            normalized_log = min(4.0, log_rate) / 4.0  # Normalize to 0-1
            difficulty = DROP_RATE_BASE_DIFFICULTY + (DROP_RATE_MAX_DIFFICULTY - DROP_RATE_BASE_DIFFICULTY) * normalized_log
        
        return min(DROP_RATE_MAX_DIFFICULTY, difficulty)
    
    # Fallback to manual difficulty if set
    if item.manual_drop_difficulty is not None:
        return item.manual_drop_difficulty
    
    # Default difficulty for drops without any data
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
    difficulty = 0.4 * source_cost +
                 0.2 * flag_score +
                 0.2 * rarity_score +
                 0.2 * level_score
    
    Where source_cost is one of:
    - harvest_cost: Based on collection time, visibility, drop rate
    - recipe_cost: Based on ingredients, quantities, and their difficulties
    - drop_cost: Based on actual drop rates from monsters
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
        drop_cost = calculate_drop_difficulty(item, db)
    
    # Calculate modifier scores
    flag_score = calculate_flag_score(item)
    rarity_score = calculate_rarity_score(item)
    level_score = calculate_level_score(item)
    
    # Weighted combination
    # Increased weight on source cost (0.4) since it's now data-driven
    difficulty = (
        0.4 * max(harvest_cost, recipe_cost, drop_cost) +
        0.2 * flag_score +
        0.2 * rarity_score +
        0.2 * level_score
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

