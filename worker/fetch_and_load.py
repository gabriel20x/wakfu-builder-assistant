"""
Worker script to fetch and load Wakfu game data

This script:
1. Waits for database to be ready
2. Loads game data from local JSON files
3. Normalizes and inserts into database
"""

import os
import sys
import time
import json
import logging
from pathlib import Path
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, JSON, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://wakfu:wakfu123@db:5432/wakfu_builder")
GAMEDATA_PATH = os.getenv("GAMEDATA_PATH", "/wakfu_data/gamedata_1.90.1.43")

Base = declarative_base()

# Define models (must match API models)
class Item(Base):
    __tablename__ = "items"
    
    item_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    level = Column(Integer, nullable=False, index=True)
    rarity = Column(Integer, default=0)
    slot = Column(String, index=True)
    is_epic = Column(Boolean, default=False, index=True)
    is_relic = Column(Boolean, default=False, index=True)
    has_gem_slot = Column(Boolean, default=False)
    source_type = Column(String, index=True)
    difficulty = Column(Float, default=0.0, index=True)
    manual_drop_difficulty = Column(Float, nullable=True)
    stats = Column(JSON, default=dict)
    raw_data = Column(JSON, default=dict)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Recipe(Base):
    __tablename__ = "recipes"
    
    recipe_id = Column(Integer, primary_key=True, index=True)
    result_item_id = Column(Integer, index=True)
    ingredients = Column(JSON, nullable=False)
    craft_cost = Column(Float, default=1.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class HarvestResource(Base):
    __tablename__ = "harvest_resources"
    
    item_id = Column(Integer, primary_key=True, index=True)  # Changed to use item_id as PK
    resource_id = Column(Integer, index=True)
    collection_time = Column(Float, default=1.0)
    visibility = Column(Float, default=1.0)
    drop_rate = Column(Float, default=1.0)
    quantity = Column(Integer, default=1)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class GameDataVersion(Base):
    __tablename__ = "gamedata_versions"
    
    id = Column(Integer, primary_key=True, index=True)
    version_string = Column(String, nullable=False, unique=True)
    loaded_items = Column(Integer, default=0)
    status = Column(String, default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Build(Base):
    __tablename__ = "builds"
    
    id = Column(Integer, primary_key=True, index=True)
    params = Column(JSON, nullable=False)
    result = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

def wait_for_db(engine, max_retries=30):
    """Wait for database to be ready"""
    for i in range(max_retries):
        try:
            connection = engine.connect()
            connection.close()
            logger.info("Database is ready!")
            return True
        except Exception as e:
            logger.info(f"Waiting for database... ({i+1}/{max_retries})")
            time.sleep(2)
    
    logger.error("Could not connect to database")
    return False

def load_json(file_path: Path):
    """Load and parse JSON file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading {file_path}: {e}")
        return []

def extract_equipment_stats(item_data: dict) -> dict:
    """Extract stats from item equipment effects"""
    stats = {}
    
    if "equipEffects" not in item_data.get("definition", {}):
        return stats
    
    effects = item_data["definition"]["equipEffects"]
    
    for effect in effects:
        effect_def = effect.get("effect", {}).get("definition", {})
        action_id = effect_def.get("actionId")
        params = effect_def.get("params", [])
        
        # Map action IDs to stat names
        stat_map = {
            20: "HP",
            31: "AP",
            41: "MP",
            80: "Critical_Hit",
            120: "Damage_Inflicted",
            160: "Resistance",
            171: "Mastery",
            180: "Lock",
            181: "Dodge",
            184: "Initiative",
            191: "Wisdom",
            192: "Prospecting",
        }
        
        stat_name = stat_map.get(action_id)
        if stat_name and len(params) > 0:
            stat_value = params[0]
            stats[stat_name] = stats.get(stat_name, 0) + stat_value
    
    return stats

def calculate_difficulty(item, recipes_map, harvest_map):
    """Simple difficulty calculation"""
    difficulty = 0.0
    
    # Base on level
    difficulty += min(30.0, item.level / 230.0 * 30.0)
    
    # Base on rarity
    rarity_scores = {0: 5, 1: 10, 2: 15, 3: 20, 4: 25, 5: 30, 6: 20, 7: 30}
    difficulty += rarity_scores.get(item.rarity, 5)
    
    # Flags
    if item.is_epic:
        difficulty += 15
    if item.is_relic:
        difficulty += 20
    
    # Source type
    if item.source_type == "harvest":
        difficulty += 5
    elif item.source_type == "recipe":
        difficulty += 10
    elif item.source_type == "drop":
        difficulty += 20
    
    return min(100.0, difficulty)

def main():
    """Main worker function"""
    logger.info("Starting Wakfu data worker...")
    logger.info(f"Database URL: {DATABASE_URL}")
    logger.info(f"Game data path: {GAMEDATA_PATH}")
    
    # Create engine and session
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)
    
    # Wait for database
    if not wait_for_db(engine):
        logger.error("Failed to connect to database")
        sys.exit(1)
    
    # Create tables
    logger.info("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # Check if data already loaded
        version = session.query(GameDataVersion).filter(
            GameDataVersion.version_string == "1.90.1.43"
        ).first()
        
        if version and version.status == "completed":
            logger.info("Data already loaded, skipping...")
            return
        
        # Create version entry
        if not version:
            version = GameDataVersion(
                version_string="1.90.1.43",
                status="loading"
            )
            session.add(version)
            session.commit()
        else:
            version.status = "loading"
            session.commit()
        
        data_path = Path(GAMEDATA_PATH)
        
        # Load JSON files
        logger.info("Loading JSON files...")
        items_data = load_json(data_path / "items.json")
        equipment_types = load_json(data_path / "equipmentItemTypes.json")
        recipes_data = load_json(data_path / "recipes.json")
        recipe_results = load_json(data_path / "recipeResults.json")
        recipe_ingredients = load_json(data_path / "recipeIngredients.json")
        harvest_loots = load_json(data_path / "harvestLoots.json")
        collectible_resources = load_json(data_path / "collectibleResources.json")
        
        logger.info(f"Loaded {len(items_data)} items from JSON")
        
        # Build lookup maps
        equipment_types_map = {
            et["definition"]["id"]: et for et in equipment_types
        }
        
        recipes_map = {}
        for result in recipe_results:
            result_id = result.get("itemId")
            recipe_id = result.get("recipeId")
            if result_id and recipe_id:
                recipes_map[result_id] = recipe_id
        
        harvest_map = {}
        for loot in harvest_loots:
            item_id = loot.get("itemId")
            if item_id:
                harvest_map[item_id] = loot
        
        collectible_map = {}
        for resource in collectible_resources:
            resource_id = resource.get("definition", {}).get("id")
            if resource_id:
                collectible_map[resource_id] = resource
        
        # Clear existing data
        logger.info("Clearing existing data...")
        session.query(Item).delete()
        session.query(Recipe).delete()
        session.query(HarvestResource).delete()
        session.commit()
        
        # Process items
        logger.info("Processing items...")
        loaded_count = 0
        
        for item_data in items_data:
            try:
                definition = item_data.get("definition", {})
                item_def = definition.get("item", {})
                item_id = item_def.get("id")
                
                if not item_id:
                    continue
                
                # Get item type info
                item_type_id = item_def.get("baseParameters", {}).get("itemTypeId")
                
                # Skip if no item type
                if not item_type_id:
                    continue
                    
                equipment_type = equipment_types_map.get(item_type_id, {})
                equipment_def = equipment_type.get("definition", {})
                
                # Determine equipment slot
                equipment_positions = equipment_def.get("equipmentPositions", [])
                slot = equipment_positions[0] if equipment_positions else None
                
                # Skip non-equipment items (no slot defined)
                if not slot or slot == "":
                    continue
                
                # Extract basic info
                level = item_def.get("level", 0)
                rarity = item_def.get("baseParameters", {}).get("rarity", 0)
                
                # Determine flags
                properties = item_def.get("baseParameters", {}).get("properties", [])
                is_epic = 21 in properties  # EPIC property ID
                is_relic = rarity == 5
                has_gem_slot = False
                
                # Get item name
                title = item_data.get("title", {})
                name = title.get("en", title.get("fr", f"Item {item_id}"))
                
                # Extract stats
                stats = extract_equipment_stats(item_data)
                
                # Determine source type
                if item_id in harvest_map:
                    source_type = "harvest"
                elif item_id in recipes_map:
                    source_type = "recipe"
                elif item_id < 10000:
                    source_type = "special"
                else:
                    source_type = "drop"
                
                # Create item object for difficulty calculation
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
                    stats=stats,
                    raw_data=item_data
                )
                
                # Calculate difficulty
                item.difficulty = calculate_difficulty(item, recipes_map, harvest_map)
                
                session.add(item)
                loaded_count += 1
                
                if loaded_count % 100 == 0:
                    logger.info(f"Processed {loaded_count} items...")
                    session.commit()
            
            except Exception as e:
                logger.error(f"Error processing item: {e}")
                continue
        
        session.commit()
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
            session.add(recipe)
        
        session.commit()
        logger.info(f"Loaded {len(recipes_map)} recipes")
        
        # Process harvest resources
        logger.info("Processing harvest resources...")
        for item_id, loot_data in harvest_map.items():
            resource_id = loot_data.get("linkedCursorId")
            collectible = collectible_map.get(resource_id, {})
            collectible_def = collectible.get("definition", {})
            
            harvest = HarvestResource(
                item_id=item_id,  # Now using item_id as primary key
                resource_id=resource_id or 0,
                collection_time=collectible_def.get("duration", 1000) / 1000.0,
                visibility=collectible_def.get("visibility", 100) / 100.0,
                drop_rate=loot_data.get("dropRate", 100) / 100.0,
                quantity=loot_data.get("quantity", 1)
            )
            session.add(harvest)
        
        session.commit()
        logger.info(f"Loaded {len(harvest_map)} harvest resources")
        
        # Update version status
        version.status = "completed"
        version.loaded_items = loaded_count
        session.commit()
        
        logger.info("✅ Game data loading complete!")
    
    except Exception as e:
        logger.error(f"❌ Error loading game data: {e}")
        if version:
            version.status = "failed"
            session.commit()
        raise
    
    finally:
        session.close()

if __name__ == "__main__":
    main()

