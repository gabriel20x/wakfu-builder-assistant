from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, List
from pydantic import BaseModel
from app.db.database import get_db
from app.db.models import Item

router = APIRouter()

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

@router.get("/{item_id}", response_model=ItemResponse)
async def get_item(item_id: int, db: Session = Depends(get_db)):
    """Get item details with calculated difficulty"""
    item = db.query(Item).filter(Item.item_id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

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

