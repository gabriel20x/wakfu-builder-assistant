from fastapi import APIRouter
from typing import List, Dict, Optional
from pydantic import BaseModel
from app.data.class_presets import (
    list_all_classes,
    list_roles_for_class,
    get_class_preset,
    get_element_preferences_from_preset,
    CLASS_PRESETS,
    ROLE_TEMPLATES
)

router = APIRouter()


class ClassInfo(BaseModel):
    id: str
    name: str
    icon: str
    primary_role: str
    roles: List[str]


class RoleInfo(BaseModel):
    id: str
    name: str
    description: str
    elements: List[str]
    is_primary: bool


class PresetResponse(BaseModel):
    weights: Dict[str, float]
    damage_preferences: List[str]
    resistance_preferences: List[str]


@router.get("/classes", response_model=List[ClassInfo])
async def get_classes():
    """
    Get list of all available classes with their roles
    """
    return list_all_classes()


@router.get("/classes/{class_name}/roles", response_model=List[RoleInfo])
async def get_class_roles(class_name: str):
    """
    Get available roles for a specific class
    """
    return list_roles_for_class(class_name)


@router.get("/classes/{class_name}/preset", response_model=PresetResponse)
async def get_class_build_preset(
    class_name: str,
    role: Optional[str] = None
):
    """
    Get build preset (stat weights and element preferences) for a class and role
    
    Args:
        class_name: Class identifier (e.g. 'iop', 'cra', 'feca')
        role: Optional role identifier. If not provided, uses primary role
        
    Returns:
        Preset with stat weights and element preferences
    """
    weights = get_class_preset(class_name, role)
    
    if weights is None:
        return {
            "weights": {},
            "damage_preferences": ['Fire', 'Water', 'Earth', 'Air'],
            "resistance_preferences": ['Fire', 'Water', 'Earth', 'Air']
        }
    
    damage_prefs, resistance_prefs = get_element_preferences_from_preset(class_name, role)
    
    return {
        "weights": weights,
        "damage_preferences": damage_prefs,
        "resistance_preferences": resistance_prefs
    }


@router.get("/roles", response_model=Dict[str, dict])
async def get_role_templates():
    """
    Get base role templates (tank, dps_melee, dps_distance, healer, support, berserker)
    """
    return ROLE_TEMPLATES


@router.get("/classes/{class_name}")
async def get_class_details(class_name: str):
    """
    Get complete details for a specific class including all roles and presets
    """
    class_name = class_name.lower()
    
    if class_name not in CLASS_PRESETS:
        return {"error": "Class not found"}
    
    return CLASS_PRESETS[class_name]

