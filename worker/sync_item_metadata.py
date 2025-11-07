"""
Sync item_metadata.json with database drop rates

This script:
1. Reads existing item_metadata.json
2. Queries database for all items with drop sources
3. Updates metadata with drop rates from database
4. Generates statistics about coverage
5. Saves updated metadata file
"""

import os
import sys
import json
import logging
from pathlib import Path
from datetime import datetime, timezone
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from collections import defaultdict

# Import models - works both in Docker and locally
try:
    # Try Docker path first (when running in container)
    from fetch_and_load import Item, MonsterDrop, Recipe
except ModuleNotFoundError:
    # Fallback to local development path
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from worker.fetch_and_load import Item, MonsterDrop, Recipe

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://wakfu:wakfu123@db:5432/wakfu_builder")
METADATA_PATH = os.getenv("METADATA_PATH", "/wakfu_data/item_metadata.json")

def load_existing_metadata(metadata_path: Path) -> dict:
    """Load existing metadata file or create new structure"""
    if metadata_path.exists():
        try:
            with open(metadata_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Could not load existing metadata: {e}")
    
    # Return empty structure
    return {
        "version": "2.0.0",
        "last_updated": datetime.now(timezone.utc).isoformat(),
        "description": "Manual metadata for items - Ultra simplified: only acquisition methods (booleans) and drop rates",
        "items": {}
    }

def sync_metadata_from_database(session, existing_metadata: dict) -> dict:
    """Sync metadata with database information"""
    
    logger.info("Querying database for all equipment items...")
    
    # Query ALL equipment items (not just drops)
    all_items = session.query(Item.item_id, Item.name, Item.source_type).all()
    
    logger.info(f"Found {len(all_items)} total equipment items")
    
    # Query all drop rates grouped by item
    drop_rates_query = session.query(
        MonsterDrop.item_id,
        func.array_agg(MonsterDrop.drop_rate_percent).label('rates')
    ).group_by(MonsterDrop.item_id).all()
    
    drop_rates_map = {item_id: rates for item_id, rates in drop_rates_query}
    logger.info(f"Found drop rates for {len(drop_rates_map)} items in monster_drops table")
    
    # Query all recipes with ingredient details
    recipes_query = session.query(Recipe).all()
    recipes_map = {}
    for recipe in recipes_query:
        recipes_map[recipe.result_item_id] = {
            "recipe_id": recipe.recipe_id,
            "ingredients": recipe.ingredients,  # Already a JSON with item_id and quantity
            "craft_cost": recipe.craft_cost
        }
    logger.info(f"Found {len(recipes_map)} items with recipes")
    
    # Stats
    stats = {
        "total_items_processed": 0,
        "items_with_drops": 0,
        "items_with_recipes": 0,
        "items_with_both": 0,
        "items_with_drop_only": 0,
        "items_with_recipe_only": 0,
        "items_with_neither": 0,
        "items_updated": 0,
        "items_created": 0,
        "items_unchanged": 0
    }
    
    # Get existing items from metadata
    existing_items = existing_metadata.get("items", {})
    updated_items = {}
    
    # Process all items
    for item_id, item_name, source_type in all_items:
        stats["total_items_processed"] += 1
        item_id_str = str(item_id)
        
        # Get existing metadata for this item
        existing_item = existing_items.get(item_id_str, {})
        
        # Check if item exists in metadata
        is_new = item_id_str not in existing_items
        
        # Build acquisition methods
        has_drops = item_id in drop_rates_map
        has_recipe = item_id in recipes_map
        
        drop_rates = []
        if has_drops:
            stats["items_with_drops"] += 1
            # Get drop rates and sort them (highest first)
            rates = sorted(drop_rates_map[item_id], reverse=True)
            drop_rates = rates
        
        recipe_info = {}
        if has_recipe:
            stats["items_with_recipes"] += 1
            recipe_data = recipes_map[item_id]
            recipe_info = {
                "recipe_id": recipe_data["recipe_id"],
                "ingredients": recipe_data["ingredients"],
                "craft_cost": recipe_data["craft_cost"]
            }
        
        # Count combinations
        if has_drops and has_recipe:
            stats["items_with_both"] += 1
        elif has_drops:
            stats["items_with_drop_only"] += 1
        elif has_recipe:
            stats["items_with_recipe_only"] += 1
        else:
            stats["items_with_neither"] += 1
        
        # Build new item metadata (only include enabled methods)
        acquisition_methods = {}
        
        # Only add drop if it has drop rates
        if has_drops:
            acquisition_methods["drop"] = {
                "enabled": True,
                "drop_rates": drop_rates
            }
        
        # Only add recipe if it exists
        if has_recipe:
            acquisition_methods["recipe"] = {
                "enabled": True,
                "recipe_id": recipe_info.get("recipe_id"),
                "ingredients": recipe_info.get("ingredients", []),
                "craft_cost": recipe_info.get("craft_cost", 1.0)
            }
        
        # Preserve manual entries (fragments, crupier, etc.)
        fragments_data = existing_item.get("acquisition_methods", {}).get("fragments", {})
        if fragments_data.get("enabled"):
            acquisition_methods["fragments"] = fragments_data
        
        crupier_enabled = existing_item.get("acquisition_methods", {}).get("crupier", {}).get("enabled", False)
        if crupier_enabled:
            acquisition_methods["crupier"] = {"enabled": True}
        
        challenge_enabled = existing_item.get("acquisition_methods", {}).get("challenge_reward", {}).get("enabled", False)
        if challenge_enabled:
            acquisition_methods["challenge_reward"] = {"enabled": True}
        
        quest_enabled = existing_item.get("acquisition_methods", {}).get("quest", {}).get("enabled", False)
        if quest_enabled:
            acquisition_methods["quest"] = {"enabled": True}
        
        other_enabled = existing_item.get("acquisition_methods", {}).get("other", {}).get("enabled", False)
        if other_enabled:
            acquisition_methods["other"] = {"enabled": True}
        
        new_item = {
            "item_id": item_id,
            "name": item_name,
            "acquisition_methods": acquisition_methods
        }
        
        # Add timestamps
        if is_new:
            new_item["added_date"] = datetime.now(timezone.utc).isoformat()
            stats["items_created"] += 1
        else:
            new_item["added_date"] = existing_item.get("added_date", datetime.now(timezone.utc).isoformat())
            
            # Check if anything changed
            old_drops = existing_item.get("acquisition_methods", {}).get("drop", {})
            old_recipe = existing_item.get("acquisition_methods", {}).get("recipe", {})
            
            drops_changed = (old_drops.get("enabled") != has_drops or 
                           old_drops.get("drop_rates") != drop_rates)
            
            recipe_changed = (old_recipe.get("enabled") != has_recipe or
                            old_recipe.get("ingredients") != recipe_info.get("ingredients", []))
            
            if drops_changed or recipe_changed:
                new_item["updated_date"] = datetime.now(timezone.utc).isoformat()
                stats["items_updated"] += 1
            else:
                stats["items_unchanged"] += 1
        
        updated_items[item_id_str] = new_item
    
    # Preserve existing items that weren't processed (manual entries)
    for item_id_str, item_data in existing_items.items():
        if item_id_str not in updated_items:
            updated_items[item_id_str] = item_data
    
    return updated_items, stats

def generate_coverage_report(items: dict) -> dict:
    """Generate coverage statistics"""
    total_items = len(items)
    
    items_with_any_method = 0
    items_with_drop_rates = 0
    items_with_recipe = 0
    items_with_fragments = 0
    items_with_crupier = 0
    items_with_quest = 0
    
    for item in items.values():
        methods = item.get("acquisition_methods", {})
        
        has_any = False
        if methods.get("drop", {}).get("enabled"):
            has_any = True
            if methods["drop"].get("drop_rates"):
                items_with_drop_rates += 1
        
        if methods.get("recipe", {}).get("enabled"):
            has_any = True
            items_with_recipe += 1
        
        if methods.get("fragments", {}).get("enabled"):
            has_any = True
            items_with_fragments += 1
        
        if methods.get("crupier", {}).get("enabled"):
            has_any = True
            items_with_crupier += 1
        
        if methods.get("quest", {}).get("enabled"):
            has_any = True
            items_with_quest += 1
        
        if has_any:
            items_with_any_method += 1
    
    coverage = {
        "total_items": total_items,
        "items_with_any_method": items_with_any_method,
        "coverage_percentage": round((items_with_any_method / total_items * 100) if total_items > 0 else 0, 2),
        "breakdown": {
            "drop_rates": items_with_drop_rates,
            "recipe": items_with_recipe,
            "fragments": items_with_fragments,
            "crupier": items_with_crupier,
            "quest": items_with_quest
        }
    }
    
    return coverage

def main():
    """Main sync function"""
    logger.info("Starting metadata sync from database...")
    logger.info(f"Database URL: {DATABASE_URL}")
    logger.info(f"Metadata path: {METADATA_PATH}")
    
    # Create engine and session
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # Resolve metadata path
        metadata_path = Path(METADATA_PATH)
        logger.info(f"Using metadata path: {metadata_path}")
        
        # Load existing metadata
        logger.info("Loading existing metadata...")
        existing_metadata = load_existing_metadata(metadata_path)
        logger.info(f"Loaded {len(existing_metadata.get('items', {}))} existing items")
        
        # Sync with database
        updated_items, stats = sync_metadata_from_database(session, existing_metadata)
        
        # Generate coverage report
        coverage = generate_coverage_report(updated_items)
        
        # Build final metadata structure
        final_metadata = {
            "version": "2.0.0",
            "last_updated": datetime.now(timezone.utc).isoformat(),
            "description": "Manual metadata for items - Ultra simplified: only acquisition methods (booleans) and drop rates",
            "stats": {
                "sync_stats": stats,
                "coverage": coverage
            },
            "items": updated_items
        }
        
        # Save updated metadata
        logger.info(f"Saving updated metadata to {metadata_path}...")
        metadata_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(final_metadata, f, indent=2, ensure_ascii=False)
        
        # Print summary
        logger.info("=" * 80)
        logger.info("SYNC COMPLETE")
        logger.info("=" * 80)
        logger.info(f"Total items processed: {stats['total_items_processed']}")
        logger.info(f"Items created: {stats['items_created']}")
        logger.info(f"Items updated: {stats['items_updated']}")
        logger.info(f"Items unchanged: {stats['items_unchanged']}")
        logger.info(f"Items with drop rates: {stats['items_with_drops']}")
        logger.info(f"Items with recipes: {stats['items_with_recipes']}")
        logger.info(f"Items with BOTH (drop + recipe): {stats['items_with_both']}")
        logger.info(f"Items with ONLY drops: {stats['items_with_drop_only']}")
        logger.info(f"Items with ONLY recipes: {stats['items_with_recipe_only']}")
        logger.info(f"Items with NEITHER: {stats['items_with_neither']}")
        logger.info("")
        logger.info("COVERAGE REPORT")
        logger.info("=" * 80)
        logger.info(f"Total items in metadata: {coverage['total_items']}")
        logger.info(f"Items with acquisition methods: {coverage['items_with_any_method']}")
        logger.info(f"Coverage: {coverage['coverage_percentage']}%")
        logger.info("")
        logger.info("Breakdown:")
        logger.info(f"  - Drop rates: {coverage['breakdown']['drop_rates']}")
        logger.info(f"  - Recipes: {coverage['breakdown']['recipe']}")
        logger.info(f"  - Fragments: {coverage['breakdown']['fragments']}")
        logger.info(f"  - Crupier: {coverage['breakdown']['crupier']}")
        logger.info(f"  - Quest: {coverage['breakdown']['quest']}")
        logger.info("=" * 80)
        
    except Exception as e:
        logger.error(f"Error during sync: {e}", exc_info=True)
        raise
    
    finally:
        session.close()

if __name__ == "__main__":
    main()

