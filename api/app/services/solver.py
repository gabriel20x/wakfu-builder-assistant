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
from app.services.element_resolver import (
    resolve_build_stats, 
    resolve_element_stats,
    infer_element_preferences_from_weights
)

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
    Solve for five builds: easy, medium, hard_epic, hard_relic, full
    
    Returns dict with keys: easy, medium, hard_epic, hard_relic, full
    Each containing: items, total_stats, total_difficulty, build_type
    """
    # ✅ IMPROVED: Auto-detect element preferences from stat_weights
    if damage_preferences is None or len(damage_preferences) == 0:
        damage_preferences = infer_element_preferences_from_weights(stat_weights)
        logger.info(f"Auto-detected damage preferences from weights: {damage_preferences}")
    
    if resistance_preferences is None or len(resistance_preferences) == 0:
        resistance_preferences = ['Fire', 'Water', 'Earth', 'Air']
    
    # ✅ OPTIMIZATION: Optimized level range
    # Standard items: [level_max - 10, level_max]
    # High rarity (Legendario/Reliquia/Épico): [level_max - 10, level_max + 10]
    # Reason: Legendarios are often 5-6 levels ABOVE their Mítico versions
    # EXCEPTION: PET slot (always level 0) is included without level restriction
    level_min = max(1, level_max - 10)  # ✅ CHANGED: 25 → 10 (more focused)
    level_max_high_rarity = level_max + 10  # ✅ NEW: Allow +10 levels for rare items
    
    # Fetch all eligible items
    # Include items in level range OR high rarity extended range OR pets
    # Exclude Inusual (rarity 2) items EXCEPT for PET slot
    # ✅ Exclude Recuerdos (rarity 6 + is_relic = false) - PVP items
    query = db.query(Item).filter(
        Item.slot.isnot(None)
    ).filter(
        (
            (Item.level <= level_max) & (Item.level >= level_min)  # Normal items
        ) | (
            (Item.level <= level_max_high_rarity) & (Item.level >= level_min) & 
            (Item.rarity.in_([5, 6, 7]))  # Legendario/Reliquia/Épico: extended range
        ) | (
            Item.slot == "PET"  # OR pets (always level 0)
        )
    ).filter(
        # Exclude Inusual (rarity 2) unless it's a PET
        (Item.rarity != 2) | (Item.slot == "PET")
    ).filter(
        # ✅ Exclude Recuerdos (rarity 6 + is_relic = false) - PVP items
        ~((Item.rarity == 6) & (Item.is_relic == False))
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
    
    hard_epic_build = _solve_single_build(
        items, stat_weights, level_max,
        difficulty_max=settings.HARD_DIFFICULTY_MAX,
        lambda_weight=settings.HARD_LAMBDA,
        build_type="hard_epic",
        db=db,
        damage_preferences=damage_preferences,
        resistance_preferences=resistance_preferences
    )
    
    hard_relic_build = _solve_single_build(
        items, stat_weights, level_max,
        difficulty_max=settings.HARD_DIFFICULTY_MAX,
        lambda_weight=settings.HARD_LAMBDA,
        build_type="hard_relic",
        db=db,
        damage_preferences=damage_preferences,
        resistance_preferences=resistance_preferences
    )
    
    full_build = _solve_single_build(
        items, stat_weights, level_max,
        difficulty_max=settings.HARD_DIFFICULTY_MAX,
        lambda_weight=settings.HARD_LAMBDA,
        build_type="full",
        db=db,
        damage_preferences=damage_preferences,
        resistance_preferences=resistance_preferences
    )
    
    return {
        "easy": easy_build,
        "medium": medium_build,
        "hard_epic": hard_epic_build,
        "hard_relic": hard_relic_build,
        "full": full_build
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
    
    Build types (adaptive based on level):
    - EASY (level < 80): Común, Poco Común, Raro (≤3). Excluye Míticos, Legendarios, Épicos y Reliquias
    - EASY (level ≥ 80): Hasta Míticos (≤4). Excluye Legendarios, Épicos y Reliquias
    - MEDIUM (level < 80): Hasta Míticos (≤4). Excluye Legendarios, Épicos y Reliquias
    - MEDIUM (level ≥ 80): Míticos (4) + Legendarios (5). NO Épicos ni Reliquias. Max 1 Legendario
    - HARD_EPIC: Max Legendarios + REQUIRE 1 Épico (NO Reliquias)
    - HARD_RELIC: Max Legendarios + REQUIRE 1 Reliquia (NO Épicos)
    - FULL: Max Legendarios + REQUIRE 1 Épico + 1 Reliquia
    
    For low levels (< 80), EASY includes Common/Uncommon/Rare to ensure all slots have options
    (especially rings which are scarce at low levels).
    """
    # Filter items by build type rarity restrictions (adaptive to level)
    if build_type == "easy":
        # ✅ ADAPTIVE: For low levels (< 80), Mythical items are hard to farm
        # So EASY builds should only use Common/Uncommon/Rare (≤3) for levels < 80
        if level_max < 80:
            # Low level EASY: Común, Poco Común, Raro (rarity <= 3)
            # No difficulty filter to ensure all slots have options (especially rings)
            items = [item for item in items 
                     if item.rarity <= 3 
                     and not item.is_epic 
                     and not item.is_relic]
            logger.info(f"Build EASY (lvl<80): Filtering to rarity <= Raro (includes Común). Items: {len(items)}")
        else:
            # High level EASY: Hasta Míticos (rarity <= 4)
            items = [item for item in items 
                     if item.rarity <= 4 
                     and not item.is_epic 
                     and not item.is_relic
                     and item.difficulty <= 48.0]
            logger.info(f"Build EASY (lvl≥80): Filtering to rarity <= Mítico, difficulty <= 48. Items: {len(items)}")
    
    elif build_type == "medium":
        # ✅ ADAPTIVE: For low levels (< 80), Legendaries are too hard to get
        # MEDIUM should only allow Mythical (≤4) for levels < 80
        if level_max < 80:
            # Low level MEDIUM: Hasta Míticos (rarity <= 4), NO Legendarios
            items = [item for item in items 
                     if item.rarity <= 4 
                     and not item.is_epic 
                     and not item.is_relic]
            logger.info(f"Build MEDIUM (lvl<80): Filtering to rarity <= Mítico. Items: {len(items)}")
        else:
            # High level MEDIUM: Allows up to 1 Legendary (constraint added later)
            items = [item for item in items 
                     if not item.is_epic 
                     and not item.is_relic]
            logger.info(f"Build MEDIUM (lvl≥80): Allows Legendaries (max 1). Items: {len(items)}")
    
    # Create problem
    prob = LpProblem(f"WakfuBuild_{build_type}", LpMaximize)
    
    # Create binary variables for each item
    item_vars = {}
    for item in items:
        var_name = f"item_{item.item_id}"
        item_vars[item.item_id] = LpVariable(var_name, cat='Binary')
    
    # Objective function: maximize (weighted_stats - lambda * difficulty + rarity_bonus)
    objective = []
    
    for item in items:
        var = item_vars[item.item_id]
        
        # ✅ FIX: Resolve Multi_Element_Mastery stats BEFORE scoring
        # Items with Multi_Element_Mastery_X need to be resolved based on user preferences
        resolved_stats = resolve_element_stats(
            item.stats.copy(),
            damage_preferences or ['Fire', 'Water', 'Earth', 'Air'],
            resistance_preferences or ['Fire', 'Water', 'Earth', 'Air']
        )
        
        # ✅ SISTEMA DE SCORING REORGANIZADO
        # FACTORES DE NORMALIZACIÓN basados en rareza/frecuencia en items:
        # - Muy raros (1-2 por item): AP (100x), MP (80x), Range (60x)
        # - Raros (2-5 por item): Critical_Hit (20x), WP (20x), Control (10x), Block (5x)
        # - Poco comunes (10-50): Critical_Mastery (2x), Dodge (1x), Lock (1x)
        # - Comunes (20-100): Masteries elementales/secundarios (1x)
        # - Muy comunes (30-100): Resistencias (0.8x)
        # - Extremadamente común (100-500): HP (0.1x)
        
        normalization_factors = {
            # Muy raros
            "AP": 100.0,
            "MP": 80.0,
            "Range": 60.0,
            # Raros
            "Critical_Hit": 20.0,
            "WP": 20.0,
            "Control": 10.0,
            "Block": 5.0,
            # Poco comunes
            "Critical_Mastery": 2.0,
            "Dodge": 1.0,
            "Lock": 1.0,
            # Masteries (comunes)
            "Fire_Mastery": 1.0,
            "Water_Mastery": 1.0,
            "Earth_Mastery": 1.0,
            "Air_Mastery": 1.0,
            "Melee_Mastery": 1.0,
            "Distance_Mastery": 1.0,
            "Rear_Mastery": 1.0,
            "Healing_Mastery": 1.0,
            "Berserk_Mastery": 1.0,
            # Resistencias (ajustadas según impacto)
            "Fire_Resistance": 1.2,
            "Water_Resistance": 1.2,
            "Earth_Resistance": 1.2,
            "Air_Resistance": 1.2,
            "Elemental_Resistance": 1.5,  # Vale por los 4 elementos pero valores más bajos
            "Critical_Resistance": 1.0,
            "Rear_Resistance": 1.0,
            # HP (extremadamente común)
            "HP": 0.1,
            # Otros
            "Initiative": 0.5,
            "Prospecting": 0.5,
            "Wisdom": 0.5,
            "Armor_Given": 0.8,
            "Armor_Received": 0.8,
        }
        
        stat_score = 0.0
        bonus_score = 0.0
        negative_penalty = 0.0
        
        # Procesar cada stat del item
        for stat_name, stat_value in resolved_stats.items():
            # Saltar metadatos
            if stat_name in ["is_epic", "is_relic", "difficulty"]:
                continue
            
            # Obtener factor de normalización
            norm_factor = normalization_factors.get(stat_name, 1.0)
            
            # ========== STATS NEGATIVOS (PENALTIES) ==========
            if stat_value < 0:
                # Los stats negativos SIEMPRE aplican penalty, independiente de si el usuario los pidió
                abs_value = abs(stat_value)
                
                if stat_name in ["AP", "MP", "Range"]:
                    # Stats críticos negativos: penalty extrema (50x)
                    negative_penalty += abs_value * norm_factor * 50.0
                elif stat_name == "WP":
                    # WP negativo: penalty severa escalada por nivel (30x)
                    level_factor = min(level_max / 100.0, 2.0)
                    negative_penalty += abs_value * norm_factor * level_factor * 30.0
                elif stat_name in ["Critical_Hit", "Control", "Block"]:
                    # Stats importantes negativos: penalty alta (20x)
                    negative_penalty += abs_value * norm_factor * 20.0
                else:
                    # Otros stats negativos: penalty moderada (10x)
                    negative_penalty += abs_value * norm_factor * 10.0
                continue
            
            # ========== STATS POSITIVOS ==========
            if stat_value > 0:
                # Si el usuario PIDIÓ este stat: peso_usuario × valor × factor_normalización
                if stat_name in stat_weights:
                    user_weight = stat_weights[stat_name]
                    stat_score += stat_value * user_weight * norm_factor
                else:
                    # Si NO lo pidió: dar pequeño bonus (10% del valor normalizado)
                    # EXCEPTO: dominios elementales/secundarios (no contar si no se piden)
                    excluded_from_bonus = {"Fire_Mastery", "Water_Mastery", "Earth_Mastery", "Air_Mastery",
                                          "Melee_Mastery", "Distance_Mastery", "Rear_Mastery", 
                                          "Healing_Mastery", "Berserk_Mastery", "Critical_Mastery"}
                    
                    if stat_name not in excluded_from_bonus:
                        # Stats con valores moderados dan pequeño bonus
                        # HP incluido: 210 × 0.1 (norm) × 0.1 (bonus) = ~2 puntos OK
                        bonus_score += stat_value * norm_factor * 0.1
        
        # Bonus total por stats extra (no solicitados)
        power_bonus = bonus_score
        
        # ✅ PENALTIES POR STATS FALTANTES (basado en análisis de data JSON)
        # Slots que normalmente tienen AP: BACK, NECK, algunos FIRST_WEAPON
        # Slots que normalmente tienen MP: CHEST, LEGS, algunos FIRST_WEAPON
        missing_stat_penalty = 0.0
        
        # BACK (Capes) and NECK (Amulets) typically have AP
        # Compensación si tiene MP (alta) o Range (menor)
        if item.slot in ["BACK", "NECK"]:
            ap_value = resolved_stats.get("AP", 0)
            mp_value = resolved_stats.get("MP", 0)
            range_value = resolved_stats.get("Range", 0)
            
            if "AP" in stat_weights:
                if ap_value <= 0:
                    # Base penalty for missing AP (×200)
                    base_ap_penalty = stat_weights["AP"] * 200
                    total_compensation = 0.0
                    
                    # Compensación por MP (alta - 40% del base penalty max)
                    if mp_value > 0 and "MP" in stat_weights:
                        mp_compensation = min(mp_value * stat_weights["MP"] * 0.5, base_ap_penalty * 0.4)
                        total_compensation += mp_compensation
                    
                    # Compensación por Range (menor - 20% del base penalty max)
                    if range_value > 0 and "Range" in stat_weights:
                        range_compensation = min(range_value * stat_weights["Range"] * 0.3, base_ap_penalty * 0.2)
                        total_compensation += range_compensation
                    
                    # Aplicar penalty reducida por compensaciones
                    if total_compensation > 0:
                        missing_stat_penalty += base_ap_penalty - total_compensation
                    elif mp_value > 0 or range_value > 0:
                        # Tiene algo pero usuario no lo valora: penalty moderada (80%)
                        missing_stat_penalty += base_ap_penalty * 0.8
                    else:
                        # No tiene nada: penalty completa
                        missing_stat_penalty += base_ap_penalty
        
        # CHEST (Breastplates) and LEGS (Boots) typically have MP
        # Compensación si tiene AP (alta) o Range (menor)
        if item.slot in ["CHEST", "LEGS"]:
            mp_value = resolved_stats.get("MP", 0)
            ap_value = resolved_stats.get("AP", 0)
            range_value = resolved_stats.get("Range", 0)
            
            if "MP" in stat_weights:
                if mp_value <= 0:
                    # Base penalty for missing MP (×200)
                    base_mp_penalty = stat_weights["MP"] * 200
                    total_compensation = 0.0
                    
                    # Compensación por AP (alta - 40% del base penalty max)
                    if ap_value > 0 and "AP" in stat_weights:
                        ap_compensation = min(ap_value * stat_weights["AP"] * 0.5, base_mp_penalty * 0.4)
                        total_compensation += ap_compensation
                    
                    # Compensación por Range (menor - 20% del base penalty max)
                    if range_value > 0 and "Range" in stat_weights:
                        range_compensation = min(range_value * stat_weights["Range"] * 0.3, base_mp_penalty * 0.2)
                        total_compensation += range_compensation
                    
                    # Aplicar penalty reducida por compensaciones
                    if total_compensation > 0:
                        missing_stat_penalty += base_mp_penalty - total_compensation
                    elif ap_value > 0 or range_value > 0:
                        # Tiene algo pero usuario no lo valora: penalty moderada (80%)
                        missing_stat_penalty += base_mp_penalty * 0.8
                    else:
                        # No tiene nada: penalty completa
                        missing_stat_penalty += base_mp_penalty
        
        # ✅ NOTE: Stats negativos (including WP) ya se manejan arriba en la sección de negative_penalty
        
        # ✅ Add bonus for filling slots (better to have something than nothing)
        # This is especially important for EASY builds where low-stat items might be skipped
        # Rings (LEFT_HAND) get extra bonus since they're often skipped due to low stats
        slot_fill_bonus = 5.0 if item.slot == "LEFT_HAND" else 2.0
        
        # ✅ IMPROVED: Add rarity bonus for HARD builds
        # This makes HARD prefer higher rarity items (Legendario > Mítico)
        rarity_bonus = 0.0
        if build_type == "hard":
            # Exponential bonus to strongly prefer higher rarities:
            # Mítico (4): baseline (0)
            # Legendario (5): +50 (strongly prefer over Mítico)
            # Reliquia (6): +60
            # Épico (7): +70
            rarity_bonuses = {
                1: 0,   # Común
                2: 0,   # Poco común
                3: 0,   # Raro
                4: 0,   # Mítico (baseline)
                5: 50,  # Legendario (strong preference)
                6: 60,  # Reliquia
                7: 70   # Épico
            }
            rarity_bonus = rarity_bonuses.get(item.rarity, 0)
        
        # ✅ SCORE FINAL COMBINADO:
        # stat_score: Stats solicitados × peso_usuario × factor_normalización
        # power_bonus: Stats NO solicitados × 0.1 (bonus pequeño)
        # negative_penalty: Stats negativos con penalties proporcionales
        # missing_stat_penalty: Falta de AP/MP en slots que normalmente los tienen
        # difficulty_penalty: Penaliza dificultad de farmeo
        # rarity_bonus: Bonus por rareza en builds HARD
        # slot_fill_bonus: Incentivo para llenar slots
        item_score = stat_score + power_bonus - negative_penalty - missing_stat_penalty - lambda_weight * item.difficulty + rarity_bonus + slot_fill_bonus
        
        objective.append(item_score * var)
    
    prob += lpSum(objective)
    
    # Constraint: 1 item per slot (except rings which need special handling)
    slots_used = {}
    for item in items:
        if item.slot not in slots_used:
            slots_used[item.slot] = []
        slots_used[item.slot].append(item_vars[item.item_id])
    
    for slot, vars_in_slot in slots_used.items():
        if slot == "LEFT_HAND":
            # ✅ RINGS: Allow up to 2 rings in LEFT_HAND slot
            prob += lpSum(vars_in_slot) <= 2, f"max_two_rings"
        else:
            # All other slots: max 1 item
            prob += lpSum(vars_in_slot) <= 1, f"max_one_{slot}"
    
    # Constraint: Rings cannot be duplicated (same item_id OR same base name)
    # This prevents equipping the same ring twice, even with different rarities
    if "LEFT_HAND" in slots_used:
        ring_items = [item for item in items if item.slot == "LEFT_HAND"]
        
        # For each pair of rings, ensure they can't both be selected if they're the same
        for i, ring1 in enumerate(ring_items):
            for ring2 in ring_items[i+1:]:
                # Check if same item_id OR same base name (different rarities)
                # Use name_es as primary, fallback to name_en/name
                name1 = ring1.name_es or ring1.name_en or ring1.name
                name2 = ring2.name_es or ring2.name_en or ring2.name
                
                if ring1.item_id == ring2.item_id or name1 == name2:
                    # Can't equip both rings if they're the same (same item or same base name)
                    prob += (item_vars[ring1.item_id] + item_vars[ring2.item_id] <= 1), \
                            f"no_duplicate_ring_{ring1.item_id}_{ring2.item_id}"
    
    # Constraint: Epic and Relic management based on build type
    epic_items = [item for item in items if item.is_epic]
    relic_items = [item for item in items if item.is_relic]
    
    if build_type == "hard_epic":
        # HARD_EPIC: REQUIRE exactly 1 Epic, FORBID all Relics
        if epic_items:
            epic_vars = [item_vars[item.item_id] for item in epic_items]
            prob += lpSum(epic_vars) == 1, "require_one_epic"
        if relic_items:
            # Forbid each relic individually
            for relic_item in relic_items:
                prob += item_vars[relic_item.item_id] == 0, f"forbid_relic_{relic_item.item_id}"
    
    elif build_type == "hard_relic":
        # HARD_RELIC: REQUIRE exactly 1 Relic, FORBID all Epics
        if relic_items:
            relic_vars = [item_vars[item.item_id] for item in relic_items]
            prob += lpSum(relic_vars) == 1, "require_one_relic"
        if epic_items:
            # Forbid each epic individually
            for epic_item in epic_items:
                prob += item_vars[epic_item.item_id] == 0, f"forbid_epic_{epic_item.item_id}"
    
    elif build_type == "full":
        # FULL: REQUIRE exactly 1 Epic AND exactly 1 Relic
        if epic_items:
            epic_vars = [item_vars[item.item_id] for item in epic_items]
            prob += lpSum(epic_vars) == 1, "require_one_epic"
        if relic_items:
            relic_vars = [item_vars[item.item_id] for item in relic_items]
            prob += lpSum(relic_vars) == 1, "require_one_relic"
    
    elif build_type == "medium":
        # MEDIUM: NO Epics, NO Relics (only Raros, Míticos, Legendarios)
        if epic_items:
            for epic_item in epic_items:
                prob += item_vars[epic_item.item_id] == 0, f"forbid_epic_{epic_item.item_id}_medium"
        if relic_items:
            for relic_item in relic_items:
                prob += item_vars[relic_item.item_id] == 0, f"forbid_relic_{relic_item.item_id}_medium"
    
    else:
        # EASY: Already filtered by rarity in items list, no Epic/Relic constraints needed
        pass
    
    # ✅ Constraint for Legendarios (rarity 5)
    # MEDIUM: Max 1 Legendario to differentiate from HARD
    # HARD variants: No limit on Legendarios
    if build_type == "medium":
        legendary_vars = [item_vars[item.item_id] for item in items if item.rarity == 5]
        if legendary_vars:
            prob += lpSum(legendary_vars) <= 1, "max_one_legendary_medium"
    
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

