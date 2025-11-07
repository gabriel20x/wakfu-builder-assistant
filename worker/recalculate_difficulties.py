"""
Recalculate item difficulties using the improved algorithm

This script recalculates all item difficulties using:
1. Real drop rates from monster_drops table
2. Recipe complexity with ingredient quantities
3. Harvest resource costs
4. Item flags, rarity, and level

Run this after loading drop rates or recipe data to update difficulties.
"""

import os
import sys
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import time

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Database connection
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://wakfu:wakfu123@db:5432/wakfu_builder"
)

# Import models - try different paths for Docker vs local
try:
    from fetch_and_load import Item, Recipe, HarvestResource, MonsterDrop, Base
except ModuleNotFoundError:
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from worker.fetch_and_load import Item, Recipe, HarvestResource, MonsterDrop, Base

import math
from typing import Optional

# ============================================================================
# DIFFICULTY CALCULATION FUNCTIONS (copied from api/app/services/difficulty.py)
# ============================================================================

DROP_RATE_BASE_DIFFICULTY = 20.0
DROP_RATE_MAX_DIFFICULTY = 95.0
HARVEST_PERCENTILE_95 = 100.0

def calculate_harvest_cost(item: Item, db) -> float:
    """Calculate harvest cost for collectible items"""
    harvest = db.query(HarvestResource).filter(
        HarvestResource.item_id == item.item_id
    ).first()
    
    if not harvest:
        return 0.0
    
    time_cost = harvest.collection_time * harvest.visibility
    consumption = 1.0
    harvest_cost = (time_cost + consumption) / (harvest.drop_rate * harvest.quantity)
    normalized = min(100.0, (harvest_cost / HARVEST_PERCENTILE_95) * 100.0)
    
    return normalized

def calculate_recipe_cost(item: Item, db, visited: Optional[set] = None) -> float:
    """Calculate recipe cost recursively"""
    if visited is None:
        visited = set()
    
    if item.item_id in visited:
        return 0.0
    
    visited.add(item.item_id)
    
    recipe = db.query(Recipe).filter(
        Recipe.result_item_id == item.item_id
    ).first()
    
    if not recipe:
        return 0.0
    
    total_cost = recipe.craft_cost * 10.0
    num_ingredients = len(recipe.ingredients)
    total_ingredient_quantity = 0
    
    for ingredient in recipe.ingredients:
        ingredient_item = db.query(Item).filter(
            Item.item_id == ingredient["item_id"]
        ).first()
        
        quantity = ingredient["quantity"]
        total_ingredient_quantity += quantity
        
        if ingredient_item:
            ingredient_difficulty = calculate_item_difficulty(
                ingredient_item, db, visited.copy()
            )
            
            if quantity <= 10:
                quantity_factor = quantity
            else:
                quantity_factor = 10 + math.log10(quantity) * 3
            
            total_cost += ingredient_difficulty * (quantity_factor / 10.0)
    
    if num_ingredients >= 7:
        complexity_penalty = 30.0
    elif num_ingredients >= 5:
        complexity_penalty = 20.0
    elif num_ingredients >= 3:
        complexity_penalty = 10.0
    else:
        complexity_penalty = 0.0
    
    total_cost += complexity_penalty
    
    if total_ingredient_quantity > 100:
        batch_penalty = min(20.0, (total_ingredient_quantity - 100) / 10.0)
        total_cost += batch_penalty
    
    normalized = min(100.0, total_cost)
    return normalized

def calculate_drop_difficulty(item: Item, db) -> float:
    """Calculate drop difficulty based on actual drop rates"""
    drops = db.query(MonsterDrop).filter(
        MonsterDrop.item_id == item.item_id
    ).all()
    
    if drops:
        best_drop_rate = max(drop.drop_rate for drop in drops)
        
        if best_drop_rate >= 1.0:
            difficulty = DROP_RATE_BASE_DIFFICULTY
        elif best_drop_rate <= 0.0001:
            difficulty = DROP_RATE_MAX_DIFFICULTY
        else:
            log_rate = -math.log10(best_drop_rate)
            normalized_log = min(4.0, log_rate) / 4.0
            difficulty = DROP_RATE_BASE_DIFFICULTY + (DROP_RATE_MAX_DIFFICULTY - DROP_RATE_BASE_DIFFICULTY) * normalized_log
        
        return min(DROP_RATE_MAX_DIFFICULTY, difficulty)
    
    if item.manual_drop_difficulty is not None:
        return item.manual_drop_difficulty
    
    return 70.0

def calculate_flag_score(item: Item) -> float:
    """Calculate difficulty score from item flags"""
    score = 0.0
    
    if item.is_epic:
        score += 20.0
    if item.is_relic:
        score += 30.0
    if item.has_gem_slot:
        score += 10.0
    
    return score

def calculate_rarity_score(item: Item) -> float:
    """Calculate difficulty score from rarity"""
    rarity_map = {
        0: 10.0,
        1: 15.0,
        2: 20.0,
        3: 30.0,
        4: 40.0,
        5: 35.0,
        6: 25.0,
        7: 35.0,
    }
    
    return rarity_map.get(item.rarity, 10.0)

def calculate_level_score(item: Item) -> float:
    """Calculate difficulty score from item level"""
    max_level = 230.0
    return min(100.0, (item.level / max_level) * 100.0)

def calculate_item_difficulty(item: Item, db, visited: Optional[set] = None) -> float:
    """Calculate total difficulty for an item"""
    harvest_cost = 0.0
    recipe_cost = 0.0
    drop_cost = 0.0
    
    if item.source_type == "harvest":
        harvest_cost = calculate_harvest_cost(item, db)
    elif item.source_type == "recipe":
        recipe_cost = calculate_recipe_cost(item, db, visited)
    elif item.source_type == "drop":
        drop_cost = calculate_drop_difficulty(item, db)
    
    flag_score = calculate_flag_score(item)
    rarity_score = calculate_rarity_score(item)
    level_score = calculate_level_score(item)
    
    difficulty = (
        0.4 * max(harvest_cost, recipe_cost, drop_cost) +
        0.2 * flag_score +
        0.2 * rarity_score +
        0.2 * level_score
    )
    
    return min(100.0, difficulty)

def recalculate_all_difficulties(db):
    """Recalculate difficulties for all items"""
    items = db.query(Item).all()
    
    for item in items:
        item.difficulty = calculate_item_difficulty(item, db)
    
    db.commit()
    logger.info(f"Recalculated difficulties for {len(items)} items")

def main():
    """Recalculate all item difficulties"""
    logger.info("Starting difficulty recalculation...")
    logger.info(f"Database URL: {DATABASE_URL}")
    
    # Create database connection
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        start_time = time.time()
        
        # Get total item count
        total_items = session.query(Item).count()
        logger.info(f"Found {total_items} items to process")
        
        # Recalculate all difficulties
        logger.info("Recalculating difficulties...")
        recalculate_all_difficulties(session)
        
        elapsed_time = time.time() - start_time
        logger.info(f"✅ Successfully recalculated difficulties for {total_items} items in {elapsed_time:.2f}s")
        
        # Show some statistics
        logger.info("\n" + "=" * 80)
        logger.info("DIFFICULTY STATISTICS")
        logger.info("=" * 80)
        
        # Difficulty ranges
        ranges = [
            ("Very Easy (0-20)", 0, 20),
            ("Easy (20-40)", 20, 40),
            ("Medium (40-60)", 40, 60),
            ("Hard (60-80)", 60, 80),
            ("Very Hard (80-100)", 80, 100),
        ]
        
        for label, min_diff, max_diff in ranges:
            count = session.query(Item).filter(
                Item.difficulty >= min_diff,
                Item.difficulty < max_diff
            ).count()
            percentage = (count / total_items * 100) if total_items > 0 else 0
            logger.info(f"{label}: {count} items ({percentage:.1f}%)")
        
        # Top 10 most difficult items
        logger.info("\n" + "=" * 80)
        logger.info("TOP 10 MOST DIFFICULT ITEMS")
        logger.info("=" * 80)
        
        top_difficult = session.query(Item).order_by(
            Item.difficulty.desc()
        ).limit(10).all()
        
        for i, item in enumerate(top_difficult, 1):
            logger.info(
                f"{i}. {item.name} (ID: {item.item_id}) - "
                f"Difficulty: {item.difficulty:.1f} - "
                f"Source: {item.source_type} - "
                f"Level: {item.level}"
            )
        
        # Top 10 easiest items
        logger.info("\n" + "=" * 80)
        logger.info("TOP 10 EASIEST ITEMS")
        logger.info("=" * 80)
        
        top_easy = session.query(Item).filter(
            Item.difficulty > 0
        ).order_by(
            Item.difficulty.asc()
        ).limit(10).all()
        
        for i, item in enumerate(top_easy, 1):
            logger.info(
                f"{i}. {item.name} (ID: {item.item_id}) - "
                f"Difficulty: {item.difficulty:.1f} - "
                f"Source: {item.source_type} - "
                f"Level: {item.level}"
            )
        
        # Statistics by source type
        logger.info("\n" + "=" * 80)
        logger.info("AVERAGE DIFFICULTY BY SOURCE TYPE")
        logger.info("=" * 80)
        
        from sqlalchemy import func
        
        source_stats = session.query(
            Item.source_type,
            func.count(Item.item_id).label('count'),
            func.avg(Item.difficulty).label('avg_difficulty'),
            func.min(Item.difficulty).label('min_difficulty'),
            func.max(Item.difficulty).label('max_difficulty')
        ).group_by(Item.source_type).all()
        
        for stat in source_stats:
            logger.info(
                f"{stat.source_type}: "
                f"Count={stat.count}, "
                f"Avg={stat.avg_difficulty:.1f}, "
                f"Min={stat.min_difficulty:.1f}, "
                f"Max={stat.max_difficulty:.1f}"
            )
        
        logger.info("=" * 80)
        
    except Exception as e:
        logger.error(f"❌ Error recalculating difficulties: {e}", exc_info=True)
        session.rollback()
        sys.exit(1)
    finally:
        session.close()

if __name__ == "__main__":
    main()

