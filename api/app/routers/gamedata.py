from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import GameDataVersion
from app.services.normalizer import load_gamedata

router = APIRouter()

@router.post("/update")
async def update_gamedata(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Trigger gamedata update from JSON files"""
    # Create new version entry
    version = GameDataVersion(
        version_string="1.90.1.43",
        status="loading"
    )
    db.add(version)
    db.commit()
    
    # Run data loading in background
    background_tasks.add_task(load_gamedata, version.id)
    
    return {
        "message": "Gamedata update started",
        "version_id": version.id,
        "status": "loading"
    }

@router.get("/status")
async def get_status(db: Session = Depends(get_db)):
    """Get current gamedata status"""
    latest = db.query(GameDataVersion).order_by(
        GameDataVersion.created_at.desc()
    ).first()
    
    if not latest:
        return {"status": "no_data", "message": "No gamedata loaded yet"}
    
    return {
        "version": latest.version_string,
        "status": latest.status,
        "loaded_items": latest.loaded_items,
        "created_at": latest.created_at
    }

