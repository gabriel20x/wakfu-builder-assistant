from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Optional, List
from pydantic import BaseModel
from app.db.database import get_db
from app.db.models import Build, Item
from app.services.solver import solve_build
import json
import os
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

class SolveRequest(BaseModel):
    level_max: int = 230
    stat_weights: Dict[str, float] = {
        "HP": 1.0,
        "AP": 2.5,
        "MP": 2.0,
        "Critical_Hit": 1.5
    }
    include_pet: bool = True  # Incluir mascotas (pueden ser difíciles de conseguir)
    include_accessory: bool = True  # Incluir emblemas (pueden ser difíciles de conseguir)
    only_droppable: bool = False  # Solo items que se pueden obtener de drops de monstruos
    damage_preferences: list = ['Fire', 'Water', 'Earth', 'Air']  # Orden de preferencia para daños elementales
    resistance_preferences: list = ['Fire', 'Water', 'Earth', 'Air']  # Orden de preferencia para resistencias
    ignored_item_ids: List[int] = []  # Lista de IDs de items a ignorar/excluir
    monster_types: List[str] = []  # Filter items by monster types (empty = all types)

class BuildResponse(BaseModel):
    items: list
    total_stats: dict
    total_difficulty: float
    build_type: str

class SolveResponse(BaseModel):
    easy: BuildResponse
    medium: BuildResponse
    hard_epic: BuildResponse
    hard_relic: BuildResponse
    full: BuildResponse

@router.post("/solve", response_model=SolveResponse)
async def solve(request: SolveRequest, db: Session = Depends(get_db)):
    """
    Generate five builds (easy, medium, hard_epic, hard_relic, full) based on stat weights and level
    
    - easy: Only Rare items (accessible)
    - medium: Mix of Mythic + 1 Legendary + 1 Epic/Relic
    - hard_epic: Max Legendaries + 1 Epic (no Relic)
    - hard_relic: Max Legendaries + 1 Relic (no Epic)
    - full: Max Legendaries + 1 Epic + 1 Relic (best possible)
    """
    try:
        # Generate builds
        builds = solve_build(
            db=db,
            level_max=request.level_max,
            stat_weights=request.stat_weights,
            include_pet=request.include_pet,
            include_accessory=request.include_accessory,
            only_droppable=request.only_droppable,
            damage_preferences=request.damage_preferences,
            resistance_preferences=request.resistance_preferences,
            ignored_item_ids=request.ignored_item_ids,
            monster_types=request.monster_types
        )
        
        # Save to database
        build_record = Build(
            params={
                "level_max": request.level_max,
                "stat_weights": request.stat_weights
            },
            result=builds
        )
        db.add(build_record)
        db.commit()
        
        return builds
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history")
async def get_history(limit: int = 10, db: Session = Depends(get_db)):
    """Get recent build history"""
    builds = db.query(Build).order_by(
        Build.created_at.desc()
    ).limit(limit).all()
    
    return [
        {
            "id": b.id,
            "params": b.params,
            "result": b.result,
            "created_at": b.created_at
        }
        for b in builds
    ]

class RefreshItemsRequest(BaseModel):
    item_ids: List[int]

@router.post("/refresh-items")
async def refresh_items(request: RefreshItemsRequest, db: Session = Depends(get_db)):
    """
    Refresh items from database with updated metadata
    
    Takes a list of item IDs and returns the items with their current stats and metadata.
    Useful for updating stored builds with the latest metadata changes.
    """
    try:
        # Fetch items from database
        items = db.query(Item).filter(Item.item_id.in_(request.item_ids)).all()
        
        if not items:
            return {"items": []}
        
        # Load metadata once for all items
        metadata_map = {}
        metadata_path = os.getenv("METADATA_PATH", "/wakfu_data/item_metadata.json")
        try:
            if os.path.exists(metadata_path):
                with open(metadata_path, 'r', encoding='utf-8') as f:
                    metadata_file = json.load(f)
                    metadata_map = metadata_file.get("items", {})
        except Exception as e:
            logger.warning(f"Could not load metadata: {e}")
        
        # Format items with metadata
        refreshed_items = []
        for item in items:
            item_metadata = metadata_map.get(str(item.item_id), {})
            
            refreshed_items.append({
                "item_id": item.item_id,
                "name": item.name,
                "name_es": item.name_es,
                "name_en": item.name_en,
                "name_fr": item.name_fr,
                "level": item.level,
                "slot": item.slot,
                "rarity": item.rarity,
                "is_epic": item.is_epic,
                "is_relic": item.is_relic,
                "difficulty": item.difficulty,
                "gfx_id": item.gfx_id,
                "stats": item.stats,
                "source_type": item.source_type,
                "has_gem_slot": item.has_gem_slot,
                "metadata": item_metadata if item_metadata else {}
            })
        
        return {"items": refreshed_items}
    
    except Exception as e:
        logger.error(f"Error refreshing items: {e}")
        raise HTTPException(status_code=500, detail=str(e))

