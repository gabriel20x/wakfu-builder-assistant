"""
Damage Calculator Router

Endpoints for calculating damage estimates based on build stats.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional

from app.services.damage_calculator import (
    DamageInput,
    estimate_elemental_damage,
    calculate_damage,
    calculate_average_damage_per_element
)

router = APIRouter()


class BuildDamageEstimateRequest(BaseModel):
    """Request to estimate damage for a build"""
    build_stats: Dict[str, float]
    base_spell_damage: float = 100.0
    resistance_presets: Optional[List[int]] = None
    include_critical: bool = True
    is_melee: bool = True  # True = Melee (≤2 cells), False = Distance (≥3 cells)


class CustomResistanceRequest(BaseModel):
    """Request to calculate damage with custom enemy resistances"""
    build_stats: Dict[str, float]
    enemy_resistances: Dict[str, float]  # e.g., {'Fire': 200, 'Water': 150}
    base_spell_damage: float = 100.0


@router.post("/estimate")
async def estimate_build_damage(request: BuildDamageEstimateRequest):
    """
    Estimate damage output for each element at different resistance levels
    
    Returns damage estimates showing how much damage each element would deal
    against targets with varying resistance levels.
    """
    try:
        results = estimate_elemental_damage(
            build_stats=request.build_stats,
            base_spell_damage=request.base_spell_damage,
            resistance_presets=request.resistance_presets,
            include_critical=request.include_critical,
            is_melee=request.is_melee
        )
        
        return {
            "estimates": [r.dict() for r in results],
            "base_spell_damage": request.base_spell_damage,
            "resistance_presets": request.resistance_presets or [0, 100, 200, 300, 400, 500],
            "is_melee": request.is_melee
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating damage: {str(e)}")


@router.post("/calculate")
async def calculate_specific_damage(params: DamageInput):
    """
    Calculate damage with specific parameters
    
    Allows detailed damage calculation with full control over all parameters.
    """
    try:
        result = calculate_damage(params)
        return result.dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating damage: {str(e)}")


@router.post("/custom-resistances")
async def calculate_with_custom_resistances(request: CustomResistanceRequest):
    """
    Calculate average damage per element against an enemy with specific resistances
    
    Useful for planning against specific bosses or enemy types.
    """
    try:
        results = calculate_average_damage_per_element(
            build_stats=request.build_stats,
            enemy_resistances=request.enemy_resistances,
            base_spell_damage=request.base_spell_damage
        )
        
        return {
            "damage_per_element": results,
            "enemy_resistances": request.enemy_resistances,
            "base_spell_damage": request.base_spell_damage
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating damage: {str(e)}")

