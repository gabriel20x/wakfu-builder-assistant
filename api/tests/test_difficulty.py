import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.database import Base
from app.db.models import Item, Recipe, HarvestResource
from app.services.difficulty import (
    calculate_item_difficulty,
    calculate_flag_score,
    calculate_rarity_score,
    calculate_level_score,
)

# Test database
TEST_DATABASE_URL = "sqlite:///./test_difficulty.db"

@pytest.fixture(scope="function")
def db_session():
    """Create a test database session"""
    engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSessionLocal()
    
    yield session
    
    session.close()
    Base.metadata.drop_all(bind=engine)

def test_flag_score_epic(db_session):
    """Test that epic items get +20 difficulty"""
    item = Item(
        item_id=1,
        name="Epic Item",
        level=100,
        rarity=7,
        slot="HEAD",
        is_epic=True,
        is_relic=False,
        has_gem_slot=False,
        source_type="drop",
        difficulty=0.0,
        stats={}
    )
    
    score = calculate_flag_score(item)
    assert score == 20.0

def test_flag_score_relic(db_session):
    """Test that relic items get +30 difficulty"""
    item = Item(
        item_id=1,
        name="Relic Item",
        level=100,
        rarity=5,
        slot="HEAD",
        is_epic=False,
        is_relic=True,
        has_gem_slot=False,
        source_type="drop",
        difficulty=0.0,
        stats={}
    )
    
    score = calculate_flag_score(item)
    assert score == 30.0

def test_flag_score_gem_slot(db_session):
    """Test that items with gem slots get +10 difficulty"""
    item = Item(
        item_id=1,
        name="Gem Item",
        level=100,
        rarity=2,
        slot="HEAD",
        is_epic=False,
        is_relic=False,
        has_gem_slot=True,
        source_type="drop",
        difficulty=0.0,
        stats={}
    )
    
    score = calculate_flag_score(item)
    assert score == 10.0

def test_rarity_score(db_session):
    """Test rarity scoring"""
    common_item = Item(item_id=1, name="Common", level=1, rarity=0, slot="HEAD", 
                      is_epic=False, is_relic=False, source_type="drop", stats={})
    legendary_item = Item(item_id=2, name="Legendary", level=1, rarity=4, slot="HEAD",
                         is_epic=False, is_relic=False, source_type="drop", stats={})
    
    common_score = calculate_rarity_score(common_item)
    legendary_score = calculate_rarity_score(legendary_item)
    
    assert legendary_score > common_score
    assert common_score == 10.0
    assert legendary_score == 40.0

def test_level_score(db_session):
    """Test level scoring"""
    low_level = Item(item_id=1, name="Low", level=50, rarity=0, slot="HEAD",
                    is_epic=False, is_relic=False, source_type="drop", stats={})
    high_level = Item(item_id=2, name="High", level=230, rarity=0, slot="HEAD",
                     is_epic=False, is_relic=False, source_type="drop", stats={})
    
    low_score = calculate_level_score(low_level)
    high_score = calculate_level_score(high_level)
    
    assert high_score > low_score
    assert high_score <= 100.0

def test_drop_item_difficulty(db_session):
    """Test difficulty calculation for drop items"""
    item = Item(
        item_id=1,
        name="Drop Item",
        level=100,
        rarity=2,
        slot="HEAD",
        is_epic=False,
        is_relic=False,
        source_type="drop",
        manual_drop_difficulty=50.0,
        stats={}
    )
    db_session.add(item)
    db_session.commit()
    
    difficulty = calculate_item_difficulty(item, db_session)
    
    # Should include manual drop difficulty
    assert difficulty > 0.0
    assert difficulty <= 100.0

def test_harvest_item_difficulty(db_session):
    """Test difficulty calculation for harvest items"""
    item = Item(
        item_id=1,
        name="Harvest Item",
        level=50,
        rarity=1,
        slot="HEAD",
        is_epic=False,
        is_relic=False,
        source_type="harvest",
        stats={}
    )
    db_session.add(item)
    
    harvest = HarvestResource(
        resource_id=1,
        item_id=1,
        collection_time=5.0,
        visibility=0.8,
        drop_rate=0.5,
        quantity=1
    )
    db_session.add(harvest)
    db_session.commit()
    
    difficulty = calculate_item_difficulty(item, db_session)
    
    # Should include harvest cost
    assert difficulty > 0.0
    assert difficulty <= 100.0

def test_recipe_item_difficulty(db_session):
    """Test difficulty calculation for recipe items"""
    # Create ingredient item
    ingredient = Item(
        item_id=1,
        name="Ingredient",
        level=20,
        rarity=0,
        slot="HEAD",
        is_epic=False,
        is_relic=False,
        source_type="harvest",
        difficulty=10.0,
        stats={}
    )
    db_session.add(ingredient)
    
    # Create result item
    result_item = Item(
        item_id=2,
        name="Crafted Item",
        level=50,
        rarity=2,
        slot="CHEST",
        is_epic=False,
        is_relic=False,
        source_type="recipe",
        stats={}
    )
    db_session.add(result_item)
    
    # Create recipe
    recipe = Recipe(
        recipe_id=1,
        result_item_id=2,
        ingredients=[{"item_id": 1, "quantity": 5}],
        craft_cost=2.0
    )
    db_session.add(recipe)
    db_session.commit()
    
    difficulty = calculate_item_difficulty(result_item, db_session)
    
    # Should include recipe cost
    assert difficulty > 0.0
    assert difficulty <= 100.0

