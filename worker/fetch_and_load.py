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
    name = Column(String, nullable=False)  # Default name (English)
    name_es = Column(String)  # Spanish name
    name_en = Column(String)  # English name  
    name_fr = Column(String)  # French name
    level = Column(Integer, nullable=False, index=True)
    rarity = Column(Integer, default=0)
    slot = Column(String, index=True)
    is_epic = Column(Boolean, default=False, index=True)
    is_relic = Column(Boolean, default=False, index=True)
    has_gem_slot = Column(Boolean, default=False)
    blocks_second_weapon = Column(Boolean, default=False, index=True)
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

def extract_equipment_stats(item_data: dict, slot: str = None) -> dict:
    """Extract stats from item equipment effects"""
    stats = {}
    
    if "equipEffects" not in item_data.get("definition", {}):
        return stats
    
    effects = item_data["definition"]["equipEffects"]
    
    # Get item type info for contextual mapping
    item_def = item_data.get("definition", {}).get("item", {})
    item_type_id = item_def.get("baseParameters", {}).get("itemTypeId")
    
    for effect in effects:
        effect_def = effect.get("effect", {}).get("definition", {})
        action_id = effect_def.get("actionId")
        params = effect_def.get("params", [])
        
        # Complete map of Wakfu action IDs to stat names
        # Based on Wakfu game data analysis and CORAZAS_REVIEW corrections
        stat_map = {
            # Core stats
            20: "HP",
            31: "AP",
            41: "MP",
            57: "MP_Penalty",  # ✅ FIXED - -MP (Movement Points penalty, e.g., Sello fulgurante)
            1020: "WP",
            191: "WP",  # ✅ CORRECTED - Wakfu Points (alternative)
            
            # Critical
            150: "Critical_Hit",  # Critical Hit % (valores 3-10%)
            96: "Critical_Mastery",
            97: "Critical_Mastery",  # Critical Mastery (alternativo)
            149: "Critical_Mastery",  # ✅ CORRECTED - Dominio crítico (was Kit_Skill)
            162: "Critical_Resistance",
            988: "Critical_Resistance",  # ✅ CORRECTED - Resistencia crítica (was Block)
            
            # Damage and healing
            122: "Healing_Mastery",
            1023: "Healing_Mastery",  # ✅ FIXED - Dominio cura (alternative Action ID)
            1058: "Heals_Performed",
            
            # Elemental Masteries
            120: "Elemental_Mastery",  # ✅ FIXED - Dominio elemental (was Damage_Inflicted)
            130: "Fire_Mastery",
            131: "Water_Mastery",
            132: "Earth_Mastery",
            133: "Air_Mastery",
            171: "Initiative",  # ✅ FIXED - Iniciativa (was Elemental_Mastery)
            1068: "Multi_Element_Mastery",  # ✅ CORRECTED - Dominio en N elementos (was Random_Elemental_Mastery)
            
            # Elemental Resistances
            80: "Elemental_Resistance",  # Elemental Resistance (valores bajos 5-10)
            82: "Fire_Resistance",
            83: "Water_Resistance",
            84: "Earth_Resistance",
            85: "Air_Resistance",
            151: "Water_Resistance",  # Alternative
            152: "Earth_Resistance",  # Alternative
            153: "Air_Resistance",  # Alternative
            160: "Elemental_Resistance",  # Alternative
            1069: "Random_Elemental_Resistance",  # Special: params[2] = number of elements
            
            # Position Masteries
            166: "Rear_Mastery",
            1052: "Melee_Mastery",  # Melee Mastery (principal)
            175: "Dodge_or_Berserk",  # ✅ IMPROVED - Contextual: Dodge (<50) or Berserk_Mastery (>=50)
            1053: "Distance_Mastery",  # Distance Mastery (principal)
            1055: "Armor_or_Berserk",  # Contextual: Armor_Given (≤50) o Berserk_Mastery (>50)
            
            # Resistances
            167: "Rear_Resistance",
            71: "Rear_Resistance",  # ✅ CORRECTED - Resistencia por la espalda (was Critical_Resistance)
            
            # Movement and positioning
            173: "Lock",  # Lock (Placaje)
            180: "Lock_or_Rear_Mastery",  # ✅ FIXED - Contextual: Rear_Mastery en NECK, Lock en otros
            181: "Rear_Mastery_Penalty",  # -Rear_Mastery (Dominio espalda negativo)
            184: "Control",  # Control (antes era Initiative, pero es Control en todos los casos)
            875: "Block",  # ✅ CORRECTED - % de anticipación/Block (simplified contextual)
            832: "Control",  # Control (alternativo)
            160: "Range_or_Elemental_Res",  # Contextual: Range en armas, Elemental_Res en armaduras
            
            # Penalties (negative stats) - estos suelen tener valores que deben ser negativos
            21: "HP_Penalty",  # -HP
            168: "Critical_Hit_Penalty",  # -Critical Hit %
            174: "Lock_Penalty",  # -Lock (en armaduras)
            176: "Dodge_Penalty",  # -Dodge (en armaduras)
            192: "WP_Penalty",  # ✅ FIXED - -WP (Wakfu Points penalty, positive value → negative stat)
            
            # Other
            193: "Prospecting",  # Prospecting (if it exists on different Action ID)
            
            # Armor
            1056: "Armor_Received",
            26: "Armor_Received",  # Alternative
            
            # Force of Will
            177: "Force_Of_Will",
            
            # Percentages
            39: "Heals_Received_or_Armor_Given",  # ✅ FIXED - Contextual: Armor_Given en NECK, Heals_Received en otros
            
            # Special effects (usually ignored for stats)
            304: None,  # State effects - skip
            400: None,  # Special mechanics - skip
            168: "Indirect_Damage",
            
            # Additional
            123: "Dodge",  # Alternative
            124: "Lock",  # Alternative
            125: "Initiative",  # Alternative
        }
        
        # Handle special action IDs with multiple parameters
        if action_id == 1068 and len(params) >= 3:
            # ✅ CORRECTED - Multi-Element Mastery (Dominio en N elementos)
            # params[0] = mastery value, params[2] = number of elements (2 or 3)
            mastery_value = params[0]
            num_elements = int(params[2]) if len(params) > 2 else 0
            stat_key = f"Multi_Element_Mastery_{num_elements}"
            stats[stat_key] = stats.get(stat_key, 0) + mastery_value
        elif action_id == 1069 and len(params) >= 3:
            # Random Elemental Resistance - show resistance value and number of elements
            resist_value = params[0]
            num_elements = int(params[2]) if len(params) > 2 else 0
            stat_key = f"Random_Elemental_Resistance_{num_elements}"
            stats[stat_key] = stats.get(stat_key, 0) + resist_value
        else:
            # Normal stats
            stat_name = stat_map.get(action_id)
            # Skip if stat_name is None (special effects we don't track as stats)
            if stat_name is not None and stat_name and len(params) > 0:
                stat_value = params[0]
                
                # Handle contextual stats (depend on item type, slot, and value)
                if stat_name == "Range_or_Elemental_Res":
                    # ✅ FIXED - Incluir NECK y SHOULDERS para Range
                    # Use slot to determine: weapons/head/neck/shoulders = Range, other armors = Elemental_Resistance
                    range_slots = ["FIRST_WEAPON", "SECOND_WEAPON", "HEAD", "NECK", "SHOULDERS"]
                    if slot in range_slots:
                        stat_name = "Range"
                    else:
                        stat_name = "Elemental_Resistance"
                
                elif stat_name == "Heals_Received_or_Armor_Given":
                    # ✅ FIXED - Contextual: En NECK y SHOULDERS es Armor_Given, en otros es Heals_Received
                    if slot in ["NECK", "SHOULDERS"]:
                        stat_name = "Armor_Given"
                    else:
                        stat_name = "Heals_Received"
                
                elif stat_name == "Lock_or_Rear_Mastery":
                    # ✅ FIXED - Contextual: En amuletos (NECK) es Rear_Mastery, en otros es Lock
                    if slot == "NECK":
                        stat_name = "Rear_Mastery"
                    else:
                        stat_name = "Lock"
                
                elif stat_name == "Dodge_or_Berserk":
                    # ✅ IMPROVED: Use value and slot to determine stat type
                    # Different slots have different Dodge value ranges:
                    # - FIRST_WEAPON: Dodge can go up to 200+ (e.g., Pepepew Sword: 170 Dodge)
                    # - HEAD: Dodge can go up to 100+ (e.g., Screechcut: 80 Dodge)
                    # - SHOULDERS, SECOND_WEAPON: Dodge can go up to 200+
                    # Berserk_Mastery typically starts from very low values (not mixed with Dodge)
                    
                    # For most equipment slots, action ID 175 with ANY value should be Dodge
                    # Only specific cases with extremely high values (250+) might be Berserk
                    if slot in ["FIRST_WEAPON", "HEAD", "SHOULDERS", "SECOND_WEAPON"]:
                        # These slots commonly have Dodge; only treat as Berserk if extremely high
                        if stat_value < 250:
                            stat_name = "Dodge"
                        else:
                            stat_name = "Berserk_Mastery"
                    else:
                        # Other slots: use lower threshold (chest, belt, etc.)
                        if stat_value < 100:
                            stat_name = "Dodge"
                        else:
                            stat_name = "Berserk_Mastery"
                        
                elif stat_name == "Armor_or_Berserk":
                    # Use value to determine: low values (≤50) = Armor_Given %, high values = Berserk_Mastery
                    if stat_value <= 50:
                        stat_name = "Armor_Given"
                    else:
                        stat_name = "Berserk_Mastery"
                
                # Handle penalties (make negative and change to base stat name)
                if stat_name == "HP_Penalty":
                    stat_name = "HP"
                    stat_value = -stat_value
                elif stat_name == "Critical_Hit_Penalty":
                    stat_name = "Critical_Hit"
                    stat_value = -stat_value
                elif stat_name == "Lock_Penalty":
                    stat_name = "Lock"
                    stat_value = -stat_value
                elif stat_name == "Dodge_Penalty":
                    stat_name = "Dodge"
                    stat_value = -stat_value
                elif stat_name == "Rear_Mastery_Penalty":
                    stat_name = "Rear_Mastery"
                    stat_value = -stat_value
                elif stat_name == "WP_Penalty":
                    stat_name = "WP"
                    stat_value = -stat_value
                elif stat_name == "MP_Penalty":
                    stat_name = "MP"
                    stat_value = -stat_value
                
                stats[stat_name] = stats.get(stat_name, 0) + stat_value
    
    return stats

def calculate_difficulty(item, recipes_map, harvest_map):
    """
    Calculate difficulty based on rarity, level, and source
    
    Rarity drop rates (approximate):
    - Común (1-2): ~5% drop rate
    - Raro (3): ~0.2% drop rate → difficulty +15
    - Mítico (4): ~0.1% drop rate (2x más difícil) → difficulty +30
    - Legendario (5): ~0.05% drop rate (4x más difícil) → difficulty +50
    - Épico (7): Muy raro → difficulty +40
    - Reliquia (6): Muy raro → difficulty +45
    """
    difficulty = 0.0
    
    # Base on level (max 20 points)
    difficulty += min(20.0, item.level / 245.0 * 20.0)
    
    # Base on rarity (exponential scaling)
    rarity_scores = {
        0: 0,   # Sin rareza
        1: 5,   # Común
        2: 10,  # Poco común
        3: 15,  # Raro (~0.2% drop)
        4: 30,  # Mítico (~0.1% drop, 2x más difícil)
        5: 50,  # Legendario (~0.05% drop, 4x más difícil)
        6: 45,  # Reliquia (cyan)
        7: 40,  # Épico (red)
    }
    difficulty += rarity_scores.get(item.rarity, 5)
    
    # Extra penalty for epic/relic flags
    if item.is_epic:
        difficulty += 20  # Épicos son MUY raros
    if item.is_relic:
        difficulty += 25  # Reliquias son MUY raras
    
    # Source type (cómo se obtiene)
    if item.source_type == "harvest":
        difficulty += 3  # Farmeable
    elif item.source_type == "recipe":
        difficulty += 8  # Requiere crafteo
    elif item.source_type == "drop":
        difficulty += 15  # Drop de mob
    elif item.source_type == "special":
        difficulty += 5  # Quest o compra
    
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
                rarity_raw = item_def.get("baseParameters", {}).get("rarity", 0)
                
                # ✅ CRITICAL FIX: Rarity mapping for equipment
                # Wakfu's JSON rarity is offset from in-game display:
                # JSON 1 = Común (1)
                # JSON 2 = Raro (3)           ← Equipment skips "Poco común" (2)
                # JSON 3 = Mítico (4)
                # JSON 4 = Legendario (5)
                # JSON 5 = Reliquia (6)       ← TRUE Relic
                # JSON 6 = Recuerdo (6)       ← Renovated items (lvl 200), NOT true Relic
                # JSON 7 = Épico (7)
                rarity_map = {
                    1: 1,  # Común → Común
                    2: 3,  # Raro (equipment skips Poco común)
                    3: 4,  # Mítico
                    4: 5,  # Legendario
                    5: 6,  # Reliquia (true relic)
                    6: 6,  # Recuerdo → Same display rarity but different source
                    7: 7   # Épico
                }
                rarity = rarity_map.get(rarity_raw, rarity_raw)
                
                # Determine flags
                properties = item_def.get("baseParameters", {}).get("properties", [])
                is_epic = rarity == 7  # Épico
                # ✅ CRITICAL: Only JSON rarity 5 are TRUE Relics
                # JSON rarity 6 (Recuerdos) are NOT counted as Relics for constraints
                is_relic = (rarity_raw == 5)  # Only true Reliquias (JSON 5)
                has_gem_slot = False
                
                # ✅ IMPROVED: Detect 2H weapons using equipmentItemTypes.json
                # Check if weapon blocks SECOND_WEAPON slot (two-handed)
                blocks_second_weapon = False
                if slot == "FIRST_WEAPON" and equipment_def:
                    # Check for disabled positions in equipment type
                    disabled_positions = equipment_def.get("equipmentDisabledPositions", [])
                    if "SECOND_WEAPON" in disabled_positions:
                        blocks_second_weapon = True
                
                # Get item names in multiple languages
                title = item_data.get("title", {})
                name_en = title.get("en", f"Item {item_id}")
                name_es = title.get("es", name_en)  # Fallback to English if no Spanish
                name_fr = title.get("fr", name_en)  # Fallback to English if no French
                name = name_en  # Default to English
                
                # Extract stats (pass slot for contextual mapping)
                stats = extract_equipment_stats(item_data, slot)
                
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
                    name_en=name_en,
                    name_es=name_es,
                    name_fr=name_fr,
                    level=level,
                    rarity=rarity,
                    slot=slot,
                    is_epic=is_epic,
                    is_relic=is_relic,
                    has_gem_slot=has_gem_slot,
                    blocks_second_weapon=blocks_second_weapon,
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

