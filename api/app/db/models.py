from sqlalchemy import Column, Integer, String, Float, Boolean, JSON, DateTime, Text
from sqlalchemy.sql import func
from app.db.database import Base

class Item(Base):
    __tablename__ = "items"
    
    item_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)  # Default name (English)
    name_es = Column(String)  # Spanish name
    name_en = Column(String)  # English name
    name_fr = Column(String)  # French name
    level = Column(Integer, nullable=False, index=True)
    rarity = Column(Integer, default=0)
    slot = Column(String, index=True)  # HEAD, CHEST, LEGS, etc.
    is_epic = Column(Boolean, default=False, index=True)
    is_relic = Column(Boolean, default=False, index=True)
    has_gem_slot = Column(Boolean, default=False)
    blocks_second_weapon = Column(Boolean, default=False)  # True para armas 2H
    source_type = Column(String, index=True)  # 'harvest', 'recipe', 'drop', 'special'
    difficulty = Column(Float, default=0.0, index=True)
    manual_drop_difficulty = Column(Float, nullable=True)
    stats = Column(JSON, default=dict)  # {"HP": 100, "AP": 1, ...}
    raw_data = Column(JSON, default=dict)  # Original item data
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Build(Base):
    __tablename__ = "builds"
    
    id = Column(Integer, primary_key=True, index=True)
    params = Column(JSON, nullable=False)  # Input parameters
    result = Column(JSON, nullable=False)  # Generated builds
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class GameDataVersion(Base):
    __tablename__ = "gamedata_versions"
    
    id = Column(Integer, primary_key=True, index=True)
    version_string = Column(String, nullable=False, unique=True)
    loaded_items = Column(Integer, default=0)
    status = Column(String, default="pending")  # pending, loading, completed, failed
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Recipe(Base):
    __tablename__ = "recipes"
    
    recipe_id = Column(Integer, primary_key=True, index=True)
    result_item_id = Column(Integer, index=True)
    ingredients = Column(JSON, nullable=False)  # [{"item_id": 123, "quantity": 5}, ...]
    craft_cost = Column(Float, default=1.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class HarvestResource(Base):
    __tablename__ = "harvest_resources"
    
    item_id = Column(Integer, primary_key=True, index=True)
    resource_id = Column(Integer, index=True)
    collection_time = Column(Float, default=1.0)
    visibility = Column(Float, default=1.0)
    drop_rate = Column(Float, default=1.0)
    quantity = Column(Integer, default=1)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

