from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Optional
from pydantic import BaseModel
from app.db.database import get_db
from app.db.models import Build
from app.services.solver import solve_build

router = APIRouter()

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

class BuildResponse(BaseModel):
    items: list
    total_stats: dict
    total_difficulty: float
    build_type: str

class SolveResponse(BaseModel):
    easy: BuildResponse
    medium: BuildResponse
    hard: BuildResponse

@router.post("/solve", response_model=SolveResponse)
async def solve(request: SolveRequest, db: Session = Depends(get_db)):
    """
    Generate three builds (easy, medium, hard) based on stat weights and level
    """
    try:
        # Generate builds
        builds = solve_build(
            db=db,
            level_max=request.level_max,
            stat_weights=request.stat_weights,
            include_pet=request.include_pet,
            include_accessory=request.include_accessory
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

