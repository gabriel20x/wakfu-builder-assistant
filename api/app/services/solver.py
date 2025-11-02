"""
Build solver using Linear Programming (PuLP)

Generates optimal equipment builds with constraints:
- 1 item per equipment slot
- Max 1 epic item
- Max 1 relic item
- Level <= level_max
- Difficulty <= threshold (for easy/medium builds)

Objective: Maximize weighted stats - lambda * difficulty
"""

from sqlalchemy.orm import Session
from app.db.models import Item
from app.core.config import settings
from pulp import LpProblem, LpMaximize, LpVariable, lpSum, LpStatus, value
import logging
from typing import Dict, List

logger = logging.getLogger(__name__)

# Equipment slots
SLOTS = [
    "HEAD", "SHOULDERS", "CHEST", "BACK", "BELT", "LEGS",
    "FIRST_WEAPON", "SECOND_WEAPON",
    "NECK", "LEFT_HAND", "RIGHT_HAND",  # Amulet and rings
    "PET", "MOUNT", "ACCESSORY"  # Pet, mount, emblem
]

def solve_build(
    db: Session,
    level_max: int,
    stat_weights: Dict[str, float]
) -> Dict:
    """
    Solve for three builds: easy, medium, hard
    
    Returns dict with keys: easy, medium, hard
    Each containing: items, total_stats, total_difficulty, build_type
    """
    # Fetch all eligible items
    items = db.query(Item).filter(
        Item.level <= level_max,
        Item.slot.isnot(None)
    ).all()
    
    logger.info(f"Solving with {len(items)} items, max level {level_max}")
    
    # Generate each build type
    easy_build = _solve_single_build(
        items, stat_weights, level_max,
        difficulty_max=settings.EASY_DIFFICULTY_MAX,
        lambda_weight=settings.EASY_LAMBDA,
        build_type="easy"
    )
    
    medium_build = _solve_single_build(
        items, stat_weights, level_max,
        difficulty_max=settings.MEDIUM_DIFFICULTY_MAX,
        lambda_weight=settings.MEDIUM_LAMBDA,
        build_type="medium"
    )
    
    hard_build = _solve_single_build(
        items, stat_weights, level_max,
        difficulty_max=settings.HARD_DIFFICULTY_MAX,
        lambda_weight=settings.HARD_LAMBDA,
        build_type="hard"
    )
    
    return {
        "easy": easy_build,
        "medium": medium_build,
        "hard": hard_build
    }

def _solve_single_build(
    items: List[Item],
    stat_weights: Dict[str, float],
    level_max: int,
    difficulty_max: float,
    lambda_weight: float,
    build_type: str
) -> Dict:
    """
    Solve for a single build using linear programming
    """
    # Create problem
    prob = LpProblem(f"WakfuBuild_{build_type}", LpMaximize)
    
    # Create binary variables for each item
    item_vars = {}
    for item in items:
        var_name = f"item_{item.item_id}"
        item_vars[item.item_id] = LpVariable(var_name, cat='Binary')
    
    # Objective function: maximize (weighted_stats - lambda * difficulty)
    objective = []
    
    for item in items:
        var = item_vars[item.item_id]
        
        # Calculate item score from stats
        stat_score = 0.0
        for stat_name, weight in stat_weights.items():
            stat_value = item.stats.get(stat_name, 0)
            stat_score += stat_value * weight
        
        # Combine with difficulty penalty
        item_score = stat_score - lambda_weight * item.difficulty
        
        objective.append(item_score * var)
    
    prob += lpSum(objective)
    
    # Constraint: 1 item per slot (except rings which need special handling)
    slots_used = {}
    for item in items:
        if item.slot not in slots_used:
            slots_used[item.slot] = []
        slots_used[item.slot].append(item_vars[item.item_id])
    
    for slot, vars_in_slot in slots_used.items():
        if slot not in ["LEFT_HAND", "RIGHT_HAND"]:
            prob += lpSum(vars_in_slot) <= 1, f"max_one_{slot}"
        else:
            # Rings can have 1 per hand, but total 2
            prob += lpSum(vars_in_slot) <= 1, f"max_one_{slot}"
    
    # Constraint: Rings cannot be duplicated (same item_id in both hands)
    if "LEFT_HAND" in slots_used and "RIGHT_HAND" in slots_used:
        left_items = [item for item in items if item.slot == "LEFT_HAND"]
        right_items = [item for item in items if item.slot == "RIGHT_HAND"]
        
        for left_item in left_items:
            for right_item in right_items:
                if left_item.item_id == right_item.item_id:
                    # Can't equip same ring in both hands
                    prob += (item_vars[left_item.item_id] + item_vars[right_item.item_id] <= 1), \
                            f"no_duplicate_ring_{left_item.item_id}"
    
    # Constraint: Max 1 epic
    epic_vars = [item_vars[item.item_id] for item in items if item.is_epic]
    if epic_vars:
        prob += lpSum(epic_vars) <= settings.MAX_EPIC_ITEMS, "max_epic"
    
    # Constraint: Max 1 relic
    relic_vars = [item_vars[item.item_id] for item in items if item.is_relic]
    if relic_vars:
        prob += lpSum(relic_vars) <= settings.MAX_RELIC_ITEMS, "max_relic"
    
    # Constraint: Two-handed weapons block SECOND_WEAPON slot
    # Check raw_data for disabledSlots containing SECOND_WEAPON
    two_handed_weapons = []
    for item in items:
        if item.slot == "FIRST_WEAPON":
            # Check if it's a 2H weapon from raw_data
            raw_data = item.raw_data or {}
            definition = raw_data.get('definition', {})
            item_def = definition.get('item', {})
            base_params = item_def.get('baseParameters', {})
            
            # Look for equipment type definition
            # 2H weapons typically have properties or disabled slots
            if isinstance(item.raw_data, dict):
                # This is a simplified check - in production would need equipment type data
                # For now, we'll skip this constraint as we don't have equipment type info loaded
                pass
    
    # Constraint: Average difficulty <= threshold (for easy/medium)
    if difficulty_max < 100.0:
        total_difficulty = lpSum([
            item.difficulty * item_vars[item.item_id] for item in items
        ])
        num_items = lpSum([item_vars[item.item_id] for item in items])
        
        # Approximate: total_difficulty <= difficulty_max * num_items
        prob += total_difficulty <= difficulty_max * len(SLOTS), f"max_difficulty_{build_type}"
    
    # Solve
    prob.solve()
    
    status = LpStatus[prob.status]
    logger.info(f"Build {build_type} solver status: {status}")
    
    if status != "Optimal":
        logger.warning(f"Solver did not find optimal solution for {build_type}")
        return {
            "items": [],
            "total_stats": {},
            "total_difficulty": 0.0,
            "build_type": build_type,
            "status": status
        }
    
    # Extract solution
    selected_items = []
    total_stats = {}
    total_difficulty = 0.0
    
    for item in items:
        if value(item_vars[item.item_id]) == 1:
            selected_items.append({
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
                "stats": item.stats,
                "source_type": item.source_type,
                "has_gem_slot": item.has_gem_slot
            })
            
            # Accumulate stats
            for stat_name, stat_value in item.stats.items():
                total_stats[stat_name] = total_stats.get(stat_name, 0) + stat_value
            
            total_difficulty += item.difficulty
    
    # Calculate average difficulty
    avg_difficulty = total_difficulty / len(selected_items) if selected_items else 0.0
    
    return {
        "items": selected_items,
        "total_stats": total_stats,
        "total_difficulty": avg_difficulty,
        "build_type": build_type,
        "status": status,
        "num_items": len(selected_items)
    }

