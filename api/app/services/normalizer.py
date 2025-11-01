"""
Data normalizer for loading Wakfu game data from JSON files

Reads JSON files from the CDN and normalizes into database models
"""

import json
import logging
from pathlib import Path
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.db.models import Item, Recipe, HarvestResource, GameDataVersion
from app.core.config import settings
from app.services.difficulty import calculate_item_difficulty

logger = logging.getLogger(__name__)

def load_json(file_path: Path):
    """Load and parse JSON file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading {file_path}: {e}")
        return []

def extract_equipment_stats(item_data: dict) -> dict:
    """
    Extract stats from item equipment effects
    
    Returns dict like {"HP": 100, "AP": 1, ...}
    """
    stats = {}
    
    # Look for equipment effects
    if "equipEffects" not in item_data.get("definition", {}):
        return stats
    
    effects = item_data["definition"]["equipEffects"]
    
    for effect in effects:
        effect_def = effect.get("effect", {}).get("definition", {})
        action_id = effect_def.get("actionId")
        params = effect_def.get("params", [])
        
        # Map action IDs to stat names (common Wakfu action IDs)
        stat_map = {
            20: "HP",  # Health points
            31: "AP",  # Action points
            41: "MP",  # Movement points
            80: "Critical_Hit",
            120: "Damage_Inflicted",
            160: "Resistance",
            171: "Mastery",
            180: "Lock",
            181: "Dodge",
            184: "Initiative",
            191: "Wisdom",
            192: "Prospecting",
            # Add more as needed
        }
        
        stat_name = stat_map.get(action_id)
        if stat_name and len(params) > 0:
            # First param is usually the stat value
            stat_value = params[0]
            stats[stat_name] = stats.get(stat_name, 0) + stat_value
    
    return stats

def determine_source_type(item_id: int, recipes_map: dict, harvest_map: dict) -> str:
    """
    Determine how an item is obtained
    
    Returns: 'harvest', 'recipe', 'drop', or 'special'
    """
    if item_id in harvest_map:
        return "harvest"
    elif item_id in recipes_map:
        return "recipe"
    elif item_id < 10000:  # Heuristic: low IDs are often special items
        return "special"
    else:
        return "drop"

def load_gamedata(version_id: int):
    """
    Main function to load all game data
    
    Called as background task from API
    """
    db = SessionLocal()
    
    try:
        version = db.query(GameDataVersion).filter(
            GameDataVersion.id == version_id
        ).first()
        
        if not version:
            logger.error(f"Version {version_id} not found")
            return
        
        version.status = "loading"
        db.commit()
        
        data_path = Path(settings.GAMEDATA_PATH)
        
        # Load all JSON files
        logger.info("Loading JSON files...")
        items_data = load_json(data_path / "items.json")
        equipment_types = load_json(data_path / "equipmentItemTypes.json")
        recipes_data = load_json(data_path / "recipes.json")
        recipe_results = load_json(data_path / "recipeResults.json")
        recipe_ingredients = load_json(data_path / "recipeIngredients.json")
        harvest_loots = load_json(data_path / "harvestLoots.json")
        collectible_resources = load_json(data_path / "collectibleResources.json")
        
        logger.info(f"Loaded {len(items_data)} items")
        
        # Build lookup maps
        equipment_types_map = {
            et["definition"]["id"]: et for et in equipment_types
        }
        
        # Map recipe results
        recipes_map = {}
        for result in recipe_results:
            result_id = result.get("itemId")
            recipe_id = result.get("recipeId")
            if result_id and recipe_id:
                recipes_map[result_id] = recipe_id
        
        # Map harvest loots
        harvest_map = {}
        for loot in harvest_loots:
            item_id = loot.get("itemId")
            if item_id:
                harvest_map[item_id] = loot
        
        # Map collectible resources
        collectible_map = {}
        for resource in collectible_resources:
            resource_id = resource.get("definition", {}).get("id")
            if resource_id:
                collectible_map[resource_id] = resource
        
        # Clear existing data
        logger.info("Clearing existing data...")
        db.query(Item).delete()
        db.query(Recipe).delete()
        db.query(HarvestResource).delete()
        db.commit()
        
        # Process items
        logger.info("Processing items...")
        loaded_count = 0
        
        for item_data in items_data:
            try:
                definition = item_data.get("definition", {})
                item_id = definition.get("id")
                
                if not item_id:
                    continue
                
                # Get item type info
                item_type_id = definition.get("item", {}).get("baseParameters", {}).get("itemTypeId")
                equipment_type = equipment_types_map.get(item_type_id, {})
                equipment_def = equipment_type.get("definition", {})
                
                # Determine equipment slot
                equipment_positions = equipment_def.get("equipmentPositions", [])
                slot = equipment_positions[0] if equipment_positions else None
                
                # Skip non-equipment items
                if not slot:
                    continue
                
                # Extract basic info
                level = definition.get("item", {}).get("level", 0)
                rarity = definition.get("item", {}).get("baseParameters", {}).get("rarity", 0)
                
                # Determine flags
                is_epic = "epic" in definition.get("item", {}).get("baseParameters", {}).get("properties", [])
                is_relic = rarity == 5
                has_gem_slot = False  # TODO: detect gem slots
                
                # Get item name
                title = item_data.get("title", {})
                name = title.get("en", title.get("fr", f"Item {item_id}"))
                
                # Extract stats
                stats = extract_equipment_stats(item_data)
                
                # Determine source type
                source_type = determine_source_type(item_id, recipes_map, harvest_map)
                
                # Create item
                item = Item(
                    item_id=item_id,
                    name=name,
                    level=level,
                    rarity=rarity,
                    slot=slot,
                    is_epic=is_epic,
                    is_relic=is_relic,
                    has_gem_slot=has_gem_slot,
                    source_type=source_type,
                    difficulty=0.0,  # Will be calculated later
                    stats=stats,
                    raw_data=item_data
                )
                
                db.add(item)
                loaded_count += 1
                
                if loaded_count % 100 == 0:
                    logger.info(f"Processed {loaded_count} items...")
                    db.commit()
            
            except Exception as e:
                logger.error(f"Error processing item {item_data.get('definition', {}).get('id')}: {e}")
                continue
        
        db.commit()
        logger.info(f"Loaded {loaded_count} equipment items")
        
        # Process recipes
        logger.info("Processing recipes...")
        recipe_ingredients_map = {}
        for ingredient in recipe_ingredients:
            recipe_id = ingredient.get("recipeId")
            if recipe_id not in recipe_ingredients_map:
                recipe_ingredients_map[recipe_id] = []
            recipe_ingredients_map[recipe_id].append({
                "item_id": ingredient.get("itemId"),
                "quantity": ingredient.get("quantity", 1)
            })
        
        for result_item_id, recipe_id in recipes_map.items():
            ingredients = recipe_ingredients_map.get(recipe_id, [])
            
            recipe = Recipe(
                recipe_id=recipe_id,
                result_item_id=result_item_id,
                ingredients=ingredients,
                craft_cost=1.0
            )
            db.add(recipe)
        
        db.commit()
        logger.info(f"Loaded {len(recipes_map)} recipes")
        
        # Process harvest resources
        logger.info("Processing harvest resources...")
        for item_id, loot_data in harvest_map.items():
            # Find corresponding collectible resource
            resource_id = loot_data.get("linkedCursorId")
            collectible = collectible_map.get(resource_id, {})
            collectible_def = collectible.get("definition", {})
            
            harvest = HarvestResource(
                resource_id=resource_id or 0,
                item_id=item_id,
                collection_time=collectible_def.get("duration", 1000) / 1000.0,  # ms to seconds
                visibility=collectible_def.get("visibility", 100) / 100.0,
                drop_rate=loot_data.get("dropRate", 100) / 100.0,
                quantity=loot_data.get("quantity", 1)
            )
            db.add(harvest)
        
        db.commit()
        logger.info(f"Loaded {len(harvest_map)} harvest resources")
        
        # Calculate difficulties
        logger.info("Calculating item difficulties...")
        items = db.query(Item).all()
        for item in items:
            item.difficulty = calculate_item_difficulty(item, db)
        
        db.commit()
        logger.info("Difficulty calculation complete")
        
        # Update version status
        version.status = "completed"
        version.loaded_items = loaded_count
        db.commit()
        
        logger.info("Game data loading complete!")
    
    except Exception as e:
        logger.error(f"Error loading game data: {e}")
        if version:
            version.status = "failed"
            db.commit()
    
    finally:
        db.close()

