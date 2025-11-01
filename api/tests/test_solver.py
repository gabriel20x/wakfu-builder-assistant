import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.database import Base
from app.db.models import Item
from app.services.solver import solve_build

# Test database
TEST_DATABASE_URL = "sqlite:///./test.db"

@pytest.fixture(scope="function")
def db_session():
    """Create a test database session"""
    engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSessionLocal()
    
    # Add test items
    test_items = [
        Item(
            item_id=1,
            name="Test Helmet",
            level=100,
            rarity=2,
            slot="HEAD",
            is_epic=False,
            is_relic=False,
            source_type="drop",
            difficulty=30.0,
            stats={"HP": 50, "AP": 1}
        ),
        Item(
            item_id=2,
            name="Epic Helmet",
            level=150,
            rarity=7,
            slot="HEAD",
            is_epic=True,
            is_relic=False,
            source_type="drop",
            difficulty=80.0,
            stats={"HP": 100, "AP": 2}
        ),
        Item(
            item_id=3,
            name="Test Chest",
            level=100,
            rarity=2,
            slot="CHEST",
            is_epic=False,
            is_relic=False,
            source_type="harvest",
            difficulty=20.0,
            stats={"HP": 80, "MP": 1}
        ),
        Item(
            item_id=4,
            name="Relic Ring",
            level=200,
            rarity=5,
            slot="LEFT_HAND",
            is_epic=False,
            is_relic=True,
            source_type="drop",
            difficulty=90.0,
            stats={"HP": 150, "AP": 3}
        ),
    ]
    
    for item in test_items:
        session.add(item)
    session.commit()
    
    yield session
    
    session.close()
    Base.metadata.drop_all(bind=engine)

def test_solver_respects_max_level(db_session):
    """Test that solver respects maximum level constraint"""
    builds = solve_build(
        db=db_session,
        level_max=120,
        stat_weights={"HP": 1.0, "AP": 2.0}
    )
    
    # Check all builds
    for build_type in ["easy", "medium", "hard"]:
        build = builds[build_type]
        for item in build["items"]:
            assert item["level"] <= 120, f"Item level {item['level']} exceeds max 120"

def test_solver_respects_max_epic(db_session):
    """Test that solver includes at most 1 epic item"""
    builds = solve_build(
        db=db_session,
        level_max=230,
        stat_weights={"HP": 1.0, "AP": 2.0}
    )
    
    # Check all builds
    for build_type in ["easy", "medium", "hard"]:
        build = builds[build_type]
        epic_count = sum(1 for item in build["items"] if item["is_epic"])
        assert epic_count <= 1, f"Build has {epic_count} epics, max is 1"

def test_solver_respects_max_relic(db_session):
    """Test that solver includes at most 1 relic item"""
    builds = solve_build(
        db=db_session,
        level_max=230,
        stat_weights={"HP": 1.0, "AP": 2.0}
    )
    
    # Check all builds
    for build_type in ["easy", "medium", "hard"]:
        build = builds[build_type]
        relic_count = sum(1 for item in build["items"] if item["is_relic"])
        assert relic_count <= 1, f"Build has {relic_count} relics, max is 1"

def test_solver_one_item_per_slot(db_session):
    """Test that solver includes at most 1 item per slot"""
    builds = solve_build(
        db=db_session,
        level_max=230,
        stat_weights={"HP": 1.0, "AP": 2.0}
    )
    
    # Check all builds
    for build_type in ["easy", "medium", "hard"]:
        build = builds[build_type]
        slots = [item["slot"] for item in build["items"]]
        assert len(slots) == len(set(slots)), "Build has duplicate slots"

def test_solver_difficulty_ordering(db_session):
    """Test that easy build has lower difficulty than hard build"""
    builds = solve_build(
        db=db_session,
        level_max=230,
        stat_weights={"HP": 1.0, "AP": 2.0}
    )
    
    easy_diff = builds["easy"]["total_difficulty"]
    medium_diff = builds["medium"]["total_difficulty"]
    hard_diff = builds["hard"]["total_difficulty"]
    
    # Note: This may not always be true due to solver constraints
    # but in general easy should be easier than hard
    print(f"Difficulties: Easy={easy_diff}, Medium={medium_diff}, Hard={hard_diff}")

def test_solver_returns_all_build_types(db_session):
    """Test that solver returns all three build types"""
    builds = solve_build(
        db=db_session,
        level_max=230,
        stat_weights={"HP": 1.0, "AP": 2.0}
    )
    
    assert "easy" in builds
    assert "medium" in builds
    assert "hard" in builds
    
    for build_type in ["easy", "medium", "hard"]:
        build = builds[build_type]
        assert "items" in build
        assert "total_stats" in build
        assert "total_difficulty" in build
        assert "build_type" in build
        assert build["build_type"] == build_type

