from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from app.db.database import get_db
from app.db.models import Item, MonsterDrop, Monster, MonsterFamily

router = APIRouter()

class MonsterFamilyResponse(BaseModel):
    id: Optional[int] = None
    names: Optional[Dict[str, str]] = None
    match: Optional[bool] = None
    candidate_ids: Optional[List[int]] = None

    class Config:
        from_attributes = True


class DropSourceResponse(BaseModel):
    monster_id: int
    monster_name: Optional[str] = None
    monster_names: Optional[Dict[str, str]] = None
    family: Optional[MonsterFamilyResponse] = None
    level_min: Optional[int] = None
    level_max: Optional[int] = None
    drop_rate: float
    drop_rate_percent: float
    image_url: str

class ItemResponse(BaseModel):
    item_id: int
    name: str
    name_es: Optional[str] = None
    name_en: Optional[str] = None
    name_fr: Optional[str] = None
    level: int
    rarity: int
    slot: Optional[str]
    is_epic: bool
    is_relic: bool
    has_gem_slot: bool
    source_type: Optional[str]
    difficulty: float
    manual_drop_difficulty: Optional[float]
    gfx_id: Optional[int] = None  # Graphics ID for item image
    stats: dict
    drop_sources: Optional[List[DropSourceResponse]] = None
    
    class Config:
        from_attributes = True

class UpdateDifficultyRequest(BaseModel):
    difficulty: float

class ItemFilter(BaseModel):
    level_min: Optional[int] = None
    level_max: Optional[int] = None
    slot: Optional[str] = None
    source_type: Optional[str] = None
    limit: int = 100

def _build_drop_source(drop: MonsterDrop, db: Session) -> DropSourceResponse:
    """Build drop source response with monster metadata"""
    # Get monster data from database
    monster = db.query(Monster).filter(Monster.monster_id == drop.monster_id).first()
    
    # Build monster names dict
    monster_names = {}
    if monster:
        if monster.name_fr:
            monster_names["fr"] = monster.name_fr
        if monster.name_en:
            monster_names["en"] = monster.name_en
        if monster.name_es:
            monster_names["es"] = monster.name_es
        if monster.name_pt:
            monster_names["pt"] = monster.name_pt
    
    # Get family info if available
    family_response = None
    if monster and monster.family_id:
        family = db.query(MonsterFamily).filter(
            MonsterFamily.family_id == monster.family_id
        ).first()
        
        if family:
            family_names = {}
            if family.name_fr:
                family_names["fr"] = family.name_fr
            if family.name_en:
                family_names["en"] = family.name_en
            if family.name_es:
                family_names["es"] = family.name_es
            if family.name_pt:
                family_names["pt"] = family.name_pt
            
            family_response = MonsterFamilyResponse(
                id=family.family_id,
                names=family_names if family_names else None,
                match=True,
                candidate_ids=None
            )
    
    # Build image URL
    gfx_id = monster.gfx_id if monster and monster.gfx_id else drop.monster_id
    image_url = f"https://static.ankama.com/wakfu/portal/game/monster/{gfx_id}/image"
    
    # Get preferred name (en > fr > es > pt)
    monster_name = None
    if monster:
        monster_name = (
            monster.name_en or 
            monster.name_fr or 
            monster.name_es or 
            monster.name_pt or 
            f"Monster {drop.monster_id}"
        )
    
    return DropSourceResponse(
        monster_id=drop.monster_id,
        monster_name=monster_name,
        monster_names=monster_names if monster_names else None,
        family=family_response,
        level_min=monster.level_min if monster else None,
        level_max=monster.level_max if monster else None,
        drop_rate=drop.drop_rate,
        drop_rate_percent=drop.drop_rate_percent,
        image_url=image_url
    )

@router.get("/{item_id}", response_model=ItemResponse)
async def get_item(item_id: int, db: Session = Depends(get_db)):
    """Get item details with calculated difficulty"""
    item = db.query(Item).filter(Item.item_id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    drop_rows = db.query(MonsterDrop).filter(MonsterDrop.item_id == item_id).all()
    drop_sources = [
        _build_drop_source(drop, db)
        for drop in drop_rows
    ]
    
    item_response = ItemResponse.from_orm(item)
    item_response.drop_sources = drop_sources
    return item_response

@router.post("/{item_id}/difficulty")
async def update_difficulty(
    item_id: int,
    request: UpdateDifficultyRequest,
    db: Session = Depends(get_db)
):
    """Update manual drop difficulty for an item"""
    item = db.query(Item).filter(Item.item_id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    if item.source_type != "drop":
        raise HTTPException(
            status_code=400,
            detail="Can only update difficulty for drop items"
        )
    
    item.manual_drop_difficulty = request.difficulty
    # Recalculate total difficulty with new manual value
    from app.services.difficulty import calculate_item_difficulty
    item.difficulty = calculate_item_difficulty(item, db)
    
    db.commit()
    db.refresh(item)
    
    return {
        "item_id": item.item_id,
        "name": item.name,
        "difficulty": item.difficulty,
        "manual_drop_difficulty": item.manual_drop_difficulty
    }

@router.get("/", response_model=List[ItemResponse])
async def list_items(
    level_min: Optional[int] = None,
    level_max: Optional[int] = None,
    slot: Optional[str] = None,
    source_type: Optional[str] = None,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List items with optional filters"""
    query = db.query(Item)
    
    if level_min is not None:
        query = query.filter(Item.level >= level_min)
    if level_max is not None:
        query = query.filter(Item.level <= level_max)
    if slot:
        query = query.filter(Item.slot == slot)
    if source_type:
        query = query.filter(Item.source_type == source_type)
    
    items = query.limit(limit).all()
    return items

