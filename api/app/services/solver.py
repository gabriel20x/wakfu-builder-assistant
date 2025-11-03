"""
Build solver using Linear Programming (PuLP)

Generates optimal equipment builds with constraints:
- 1 item per equipment slot
- Max 1 epic item
- Max 1 relic item
- Level range: [level_max - 25, level_max] (optimization)
  * Exception: PET slot (level 0) is always included
- Difficulty <= threshold (for easy/medium builds)

Objective: Maximize weighted stats - lambda * difficulty

Performance: Only considers items within 25 levels of target to reduce computation time
"""

from sqlalchemy.orm import Session
from app.db.models import Item
from app.core.config import settings
from pulp import LpProblem, LpMaximize, LpVariable, lpSum, LpStatus, value
import logging
from typing import Dict, List
from app.services.element_resolver import resolve_build_stats

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
    stat_weights: Dict[str, float],
    include_pet: bool = True,
    include_accessory: bool = True,
    damage_preferences: List[str] = None,
    resistance_preferences: List[str] = None
) -> Dict:
    """
    Solve for three builds: easy, medium, hard
    
    Returns dict with keys: easy, medium, hard
    Each containing: items, total_stats, total_difficulty, build_type
    """
    # Default element preferences
    if damage_preferences is None:
        damage_preferences = ['Fire', 'Water', 'Earth', 'Air']
    if resistance_preferences is None:
        resistance_preferences = ['Fire', 'Water', 'Earth', 'Air']
    
    # ✅ OPTIMIZATION: Only consider items within 25 levels of target
    # This significantly reduces computation time for high-level builds
    # EXCEPTION: PET slot (always level 0) is included without level restriction
    level_min = max(1, level_max - 25)
    
    # Fetch all eligible items
    # Include items in level range OR pets (which are always level 0)
    # Exclude Inusual (rarity 2) items EXCEPT for PET slot
    query = db.query(Item).filter(
        Item.slot.isnot(None)
    ).filter(
        (
            (Item.level <= level_max) & (Item.level >= level_min)  # Normal items in range
        ) | (
            Item.slot == "PET"  # OR pets (always level 0)
        )
    ).filter(
        # Exclude Inusual (rarity 2) unless it's a PET
        (Item.rarity != 2) | (Item.slot == "PET")
    )
    
    # Filter out PET and ACCESSORY if not included
    excluded_slots = []
    if not include_pet:
        excluded_slots.append("PET")
    if not include_accessory:
        excluded_slots.append("ACCESSORY")
    
    if excluded_slots:
        query = query.filter(~Item.slot.in_(excluded_slots))
    
    items = query.all()
    
    logger.info(f"Solving with {len(items)} items (level {level_min}-{level_max} + PET)")
    
    # Generate each build type
    easy_build = _solve_single_build(
        items, stat_weights, level_max,
        difficulty_max=settings.EASY_DIFFICULTY_MAX,
        lambda_weight=settings.EASY_LAMBDA,
        build_type="easy",
        db=db,
        damage_preferences=damage_preferences,
        resistance_preferences=resistance_preferences
    )
    
    medium_build = _solve_single_build(
        items, stat_weights, level_max,
        difficulty_max=settings.MEDIUM_DIFFICULTY_MAX,
        lambda_weight=settings.MEDIUM_LAMBDA,
        build_type="medium",
        db=db,
        damage_preferences=damage_preferences,
        resistance_preferences=resistance_preferences
    )
    
    hard_build = _solve_single_build(
        items, stat_weights, level_max,
        difficulty_max=settings.HARD_DIFFICULTY_MAX,
        lambda_weight=settings.HARD_LAMBDA,
        build_type="hard",
        db=db,
        damage_preferences=damage_preferences,
        resistance_preferences=resistance_preferences
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
    build_type: str,
    db: Session = None,
    damage_preferences: List[str] = None,
    resistance_preferences: List[str] = None
) -> Dict:
    """
    Solve for a single build using linear programming
    
    Build types:
    - EASY: Max rarity = Mítico (4). Excluye Legendarios/Épicos/Reliquias
    - MEDIUM: Requiere al menos 1 Épico O 1 Reliquia. Permite Legendarios
    - HARD: Sin restricciones, completamente optimizado
    """
    # Filter items by build type rarity restrictions
    if build_type == "easy":
        # EASY: Solo hasta Mítico (rarity <= 4), excluye Épicos y Reliquias
        # También excluye items individuales muy difíciles (difficulty > 48)
        items = [item for item in items 
                 if item.rarity <= 4 
                 and not item.is_epic 
                 and not item.is_relic
                 and item.difficulty <= 48.0]
        logger.info(f"Build EASY: Filtering to rarity <= Mítico, difficulty <= 48. Items: {len(items)}")
    
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
    
    # Constraint: MEDIUM build must have at least 1 Epic OR 1 Relic
    if build_type == "medium":
        if epic_vars or relic_vars:
            prob += lpSum(epic_vars + relic_vars) >= 1, "require_epic_or_relic"
            logger.info(f"Build MEDIUM: Requiring at least 1 Epic or Relic")
    
    # ✅ IMPROVED: Constraint - Two-handed weapons block SECOND_WEAPON slot
    # Use blocks_second_weapon field from database (detected during worker data load)
    two_handed_weapons = [item for item in items 
                          if item.slot == "FIRST_WEAPON" and item.blocks_second_weapon]
    second_weapons = [item for item in items if item.slot == "SECOND_WEAPON"]
    
    if two_handed_weapons and second_weapons:
        for two_hand in two_handed_weapons:
            for second_weapon in second_weapons:
                # Can't have 2H weapon and second weapon at same time
                prob += (item_vars[two_hand.item_id] + item_vars[second_weapon.item_id] <= 1), \
                        f"no_2h_with_second_{two_hand.item_id}_{second_weapon.item_id}"
    
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
    items_stats_list = []
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
            
            # Collect stats for resolution
            items_stats_list.append(item.stats)
            
            total_difficulty += item.difficulty
    
    # Resolve elemental stats based on user preferences
    if damage_preferences is None:
        damage_preferences = ['Fire', 'Water', 'Earth', 'Air']
    if resistance_preferences is None:
        resistance_preferences = ['Fire', 'Water', 'Earth', 'Air']
    
    total_stats = resolve_build_stats(
        items_stats_list,
        damage_preferences,
        resistance_preferences
    )
    
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

