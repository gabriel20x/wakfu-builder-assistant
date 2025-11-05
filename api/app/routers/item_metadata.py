"""
Item Metadata Management Router

Manages manual metadata for items (drop rates, recipe corrections, etc.)
that are not provided by Wakfu game data.
"""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import Item
from pydantic import BaseModel
from typing import Optional, Dict
import json
import os
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/item-metadata", tags=["item-metadata"])

# Get metadata file path from environment or use default
METADATA_PATH = os.getenv("METADATA_PATH", "/wakfu_data/item_metadata.json")

class DropMethodInfo(BaseModel):
    enabled: bool = False
    drop_rates: Optional[list] = []  # List of drop percentages

class RecipeMethodInfo(BaseModel):
    enabled: bool = False

class FragmentMethodInfo(BaseModel):
    enabled: bool = False
    fragment_rates: Optional[list] = []  # List of fragment drop percentages

class CrupierMethodInfo(BaseModel):
    enabled: bool = False

class ChallengeRewardMethodInfo(BaseModel):
    enabled: bool = False

class QuestMethodInfo(BaseModel):
    enabled: bool = False

class OtherMethodInfo(BaseModel):
    enabled: bool = False

class AcquisitionMethods(BaseModel):
    drop: Optional[DropMethodInfo] = DropMethodInfo()
    recipe: Optional[RecipeMethodInfo] = RecipeMethodInfo()
    fragments: Optional[FragmentMethodInfo] = FragmentMethodInfo()
    crupier: Optional[CrupierMethodInfo] = CrupierMethodInfo()
    challenge_reward: Optional[ChallengeRewardMethodInfo] = ChallengeRewardMethodInfo()
    quest: Optional[QuestMethodInfo] = QuestMethodInfo()
    other: Optional[OtherMethodInfo] = OtherMethodInfo()

class ItemMetadata(BaseModel):
    item_id: int
    name: Optional[str] = None
    acquisition_methods: Optional[AcquisitionMethods] = None

class ItemMetadataResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Dict] = None

def read_metadata_file() -> Dict:
    """Read the metadata JSON file"""
    try:
        if os.path.exists(METADATA_PATH):
            with open(METADATA_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # Return default structure if file doesn't exist
            return {
                "version": "1.0.0",
                "last_updated": datetime.now().isoformat(),
                "description": "Manual metadata for items not provided by Wakfu game data",
                "items": {}
            }
    except Exception as e:
        logger.error(f"Error reading metadata file: {e}")
        raise HTTPException(status_code=500, detail=f"Error reading metadata file: {str(e)}")

def write_metadata_file(data: Dict) -> None:
    """Write to the metadata JSON file"""
    try:
        # Update last_updated timestamp
        data["last_updated"] = datetime.now().isoformat()
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(METADATA_PATH), exist_ok=True)
        
        with open(METADATA_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        logger.error(f"Error writing metadata file: {e}")
        raise HTTPException(status_code=500, detail=f"Error writing metadata file: {str(e)}")

@router.get("/all")
async def get_all_metadata() -> ItemMetadataResponse:
    """Get all item metadata"""
    try:
        data = read_metadata_file()
        return ItemMetadataResponse(
            success=True,
            message="Metadata retrieved successfully",
            data=data
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/item/{item_id}")
async def get_item_metadata(item_id: int, db: Session = Depends(get_db)):
    """Get metadata for a specific item"""
    try:
        # Get item from database
        item = db.query(Item).filter(Item.item_id == item_id).first()
        if not item:
            raise HTTPException(status_code=404, detail="Item not found in database")
        
        # Get metadata
        metadata_file = read_metadata_file()
        item_metadata = metadata_file["items"].get(str(item_id), {})
        
        # Combine item info with metadata
        result = {
            "item_id": item.item_id,
            "name": item.name,
            "name_es": item.name_es,
            "name_en": item.name_en,
            "level": item.level,
            "rarity": item.rarity,
            "slot": item.slot,
            "source_type": item.source_type,
            "difficulty": item.difficulty,
            "metadata": item_metadata
        }
        
        return ItemMetadataResponse(
            success=True,
            message="Item metadata retrieved successfully",
            data=result
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting item metadata: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/item/{item_id}")
async def update_item_metadata(
    item_id: int, 
    metadata: ItemMetadata,
    db: Session = Depends(get_db)
):
    """Create or update metadata for an item"""
    try:
        # Verify item exists in database
        item = db.query(Item).filter(Item.item_id == item_id).first()
        if not item:
            raise HTTPException(status_code=404, detail="Item not found in database")
        
        # Read current metadata
        metadata_file = read_metadata_file()
        
        # Prepare metadata entry
        metadata_dict = metadata.dict(exclude_unset=True)
        metadata_dict["item_id"] = item_id
        metadata_dict["name"] = item.name  # Store name for reference
        
        if not metadata_dict.get("added_date"):
            metadata_dict["added_date"] = datetime.now().isoformat()
        
        # Update metadata
        metadata_file["items"][str(item_id)] = metadata_dict
        
        # Write to file
        write_metadata_file(metadata_file)
        
        return ItemMetadataResponse(
            success=True,
            message=f"Metadata updated for item {item_id}",
            data=metadata_dict
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating item metadata: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/item/{item_id}")
async def delete_item_metadata(item_id: int):
    """Delete metadata for an item"""
    try:
        metadata_file = read_metadata_file()
        
        if str(item_id) not in metadata_file["items"]:
            raise HTTPException(status_code=404, detail="Metadata not found for this item")
        
        del metadata_file["items"][str(item_id)]
        write_metadata_file(metadata_file)
        
        return ItemMetadataResponse(
            success=True,
            message=f"Metadata deleted for item {item_id}"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting item metadata: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/search")
async def search_items(
    query: str,
    db: Session = Depends(get_db)
):
    """Search items by name to add metadata"""
    try:
        items = db.query(Item).filter(
            (Item.name.ilike(f"%{query}%")) | 
            (Item.name_es.ilike(f"%{query}%")) |
            (Item.name_en.ilike(f"%{query}%"))
        ).limit(50).all()
        
        # Get metadata for these items
        metadata_file = read_metadata_file()
        
        results = []
        for item in items:
            has_metadata = str(item.item_id) in metadata_file["items"]
            results.append({
                "item_id": item.item_id,
                "name": item.name,
                "name_es": item.name_es,
                "name_en": item.name_en,
                "level": item.level,
                "rarity": item.rarity,
                "slot": item.slot,
                "source_type": item.source_type,
                "has_metadata": has_metadata,
                "metadata": metadata_file["items"].get(str(item.item_id), {})
            })
        
        return ItemMetadataResponse(
            success=True,
            message=f"Found {len(results)} items",
            data={"items": results}
        )
    except Exception as e:
        logger.error(f"Error searching items: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats")
async def get_metadata_stats(db: Session = Depends(get_db)):
    """Get statistics about metadata coverage"""
    try:
        metadata_file = read_metadata_file()
        items_with_metadata = len(metadata_file["items"])
        
        # Count total items in database
        total_items_in_game = db.query(Item).count()
        
        # Count by metadata type
        with_drop = sum(1 for item in metadata_file["items"].values() if item.get("acquisition_methods", {}).get("drop", {}).get("enabled"))
        with_recipe = sum(1 for item in metadata_file["items"].values() if item.get("acquisition_methods", {}).get("recipe", {}).get("enabled"))
        with_fragments = sum(1 for item in metadata_file["items"].values() if item.get("acquisition_methods", {}).get("fragments", {}).get("enabled"))
        with_crupier = sum(1 for item in metadata_file["items"].values() if item.get("acquisition_methods", {}).get("crupier", {}).get("enabled"))
        with_challenge = sum(1 for item in metadata_file["items"].values() if item.get("acquisition_methods", {}).get("challenge_reward", {}).get("enabled"))
        
        return ItemMetadataResponse(
            success=True,
            message="Statistics retrieved",
            data={
                "total_items_in_game": total_items_in_game,
                "total_items_with_metadata": items_with_metadata,
                "coverage_percent": round((items_with_metadata / total_items_in_game * 100), 2) if total_items_in_game > 0 else 0,
                "items_with_drop": with_drop,
                "items_with_recipe": with_recipe,
                "items_with_fragments": with_fragments,
                "items_with_crupier": with_crupier,
                "items_with_challenge": with_challenge,
                "last_updated": metadata_file.get("last_updated")
            }
        )
    except Exception as e:
        logger.error(f"Error getting metadata stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))

