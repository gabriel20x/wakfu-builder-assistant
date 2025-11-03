"""
Wakfu Damage Calculator Service

Calculates estimated damage output based on build stats and enemy resistances.
Implements the official Wakfu damage formulas from the wiki.

Formula:
Elemental Damage = Base Damage * (Backstab Bonus) * 
                   (1 + [Elemental Mastery + Secondary Mastery]/100) * 
                   (1 - [Elemental Resistance %])

Where:
- Elemental Resistance % = 1 - 0.8^(Flat Resist/100)
- Secondary Mastery = Critical + Berserk + Melee/Distance + Single Target/AoE
- Final Damage = Elemental Damage * (1 + Final Damage Bonus/100)
"""

from typing import Dict, List, Optional
from pydantic import BaseModel
import math


class DamageInput(BaseModel):
    """Input parameters for damage calculation"""
    base_spell_damage: float = 100.0
    elemental_mastery: float = 0.0
    
    # Secondary Masteries
    critical_mastery: float = 0.0
    berserk_mastery: float = 0.0
    melee_mastery: float = 0.0
    distance_mastery: float = 0.0
    rear_mastery: float = 0.0
    single_target_mastery: float = 0.0
    aoe_mastery: float = 0.0
    
    # Target resistance (FLAT value, not %)
    flat_resistance: float = 0.0
    
    # Combat conditions
    is_critical: bool = False
    is_berserk: bool = False  # Attacker below 50% HP
    is_backstab: bool = False  # Attacking from behind
    is_sidestab: bool = False  # Attacking from side
    is_melee: bool = True  # 2 cells or closer (default melee)
    is_single_target: bool = True  # Single target spell (default)
    
    # Final damage modifiers
    final_damage_bonus: float = 0.0
    
    # Legacy support
    armor: float = 0.0


class DamageOutput(BaseModel):
    """Output of damage calculation"""
    total_mastery: float
    preliminary_damage: float
    effective_damage: float
    final_damage: float
    damage_after_armor: float
    details: Dict


class ElementalDamageEstimate(BaseModel):
    """Damage estimate for a single element at different resistance levels"""
    element: str
    base_mastery: float
    resistance_scenarios: List[Dict]  # List of {resistance: value, damage: value}


def convert_flat_resistance_to_percent(flat_resistance: float) -> float:
    """
    Convert flat resistance to percentage using Wakfu formula
    
    Formula: Elemental Resistance % = 1 - 0.8^(Flat Resist/100)
    
    Examples:
    - 0 flat resist = 0% resist
    - 100 flat resist = 20% resist
    - 200 flat resist = 36% resist
    - 500 flat resist = 67.23% resist
    """
    if flat_resistance <= 0:
        return 0.0
    
    resistance_percent = (1 - math.pow(0.8, flat_resistance / 100)) * 100
    return resistance_percent


def calculate_damage(params: DamageInput) -> DamageOutput:
    """
    Calculate final damage using official Wakfu formulas from the wiki
    
    Official Formula:
    Elemental Damage = Base Damage * (Backstab Bonus) * 
                       (1 + [Elemental Mastery + Secondary Mastery]/100) * 
                       (1 - [Elemental Resistance %])
    
    Final Damage = Elemental Damage * (1 + Final Damage Bonus/100)
    
    Steps:
    1. Calculate backstab bonus (1.0, 1.10 for side, 1.25 for back)
    2. Calculate total mastery (elemental + all applicable secondary masteries)
    3. Convert flat resistance to resistance %
    4. Calculate elemental damage
    5. Apply final damage modifiers
    6. Apply armor (if any)
    """
    
    # Step 1: Calculate backstab bonus
    backstab_bonus = 1.0
    if params.is_backstab:
        backstab_bonus = 1.25
    elif params.is_sidestab:
        backstab_bonus = 1.10
    
    # Step 2: Calculate total secondary mastery (additive)
    secondary_mastery = 0.0
    
    # Critical mastery (only if critical hit)
    if params.is_critical:
        secondary_mastery += params.critical_mastery
    
    # Berserk mastery (only if below 50% HP)
    if params.is_berserk:
        secondary_mastery += params.berserk_mastery
    
    # Position mastery (melee vs distance)
    if params.is_melee:
        secondary_mastery += params.melee_mastery
    else:
        secondary_mastery += params.distance_mastery
    
    # Rear mastery (backstab/sidestab)
    if params.is_backstab or params.is_sidestab:
        secondary_mastery += params.rear_mastery
    
    # Target type mastery (single target vs AoE)
    if params.is_single_target:
        secondary_mastery += params.single_target_mastery
    else:
        secondary_mastery += params.aoe_mastery
    
    total_mastery = params.elemental_mastery + secondary_mastery
    
    # Step 3: Convert flat resistance to percentage
    resistance_percent = convert_flat_resistance_to_percent(params.flat_resistance)
    resistance_multiplier = 1 - (resistance_percent / 100)
    
    # Step 4: Calculate elemental damage (Official Formula)
    elemental_damage = (
        params.base_spell_damage * 
        backstab_bonus * 
        (1 + total_mastery / 100) * 
        resistance_multiplier
    )
    
    # Step 5: Apply final damage modifiers
    final_damage = elemental_damage * (1 + params.final_damage_bonus / 100)
    
    # Step 6: Apply armor (subtracts from final damage, cannot go below 0)
    damage_after_armor = max(0, final_damage - params.armor)
    
    # Note: Resistance cannot reduce damage below base damage in Wakfu
    # But for estimation purposes, we show the calculated value
    
    # Round to integers (Wakfu displays whole numbers)
    total_mastery = round(total_mastery)
    elemental_damage = round(elemental_damage)
    final_damage = round(final_damage)
    damage_after_armor = round(damage_after_armor)
    
    return DamageOutput(
        total_mastery=float(total_mastery),
        preliminary_damage=float(elemental_damage),
        effective_damage=float(elemental_damage),
        final_damage=float(final_damage),
        damage_after_armor=float(damage_after_armor),
        details={
            "flat_resistance": params.flat_resistance,
            "resistance_percent": round(resistance_percent, 2),
            "backstab_bonus": backstab_bonus,
            "secondary_mastery": round(secondary_mastery),
            "is_critical": params.is_critical,
            "is_berserk": params.is_berserk,
            "is_melee": params.is_melee,
            "is_single_target": params.is_single_target,
            "final_damage_bonus": params.final_damage_bonus
        }
    )


def estimate_elemental_damage(
    build_stats: Dict[str, float],
    base_spell_damage: float = 100.0,
    resistance_presets: Optional[List[int]] = None,
    include_critical: bool = True,
    is_melee: bool = True
) -> List[ElementalDamageEstimate]:
    """
    Estimate damage for each element at different resistance levels
    
    Uses official Wakfu formulas with proper resistance conversion and secondary masteries.
    Only shows positive damage values (per user request).
    
    Args:
        build_stats: Dictionary of build statistics
        base_spell_damage: Base damage of spell (default 100)
        resistance_presets: List of FLAT resistance values to test (default [0, 100, 200, 300, 400, 500])
        include_critical: Whether to include critical hit in calculations
        is_melee: True for melee (≤2 cells), False for distance (≥3 cells)
    
    Returns:
        List of damage estimates per element
    """
    
    if resistance_presets is None:
        resistance_presets = [0, 100, 200, 300, 400, 500]
    
    elements = [
        ('Fire', 'Fire_Mastery'),
        ('Water', 'Water_Mastery'),
        ('Earth', 'Earth_Mastery'),
        ('Air', 'Air_Mastery')
    ]
    
    results = []
    
    # Get all secondary masteries from build
    critical_mastery = build_stats.get('Critical_Mastery', 0)
    berserk_mastery = build_stats.get('Berserk_Mastery', 0)
    melee_mastery = build_stats.get('Melee_Mastery', 0)
    distance_mastery = build_stats.get('Distance_Mastery', 0)
    rear_mastery = build_stats.get('Rear_Mastery', 0)
    elemental_mastery = build_stats.get('Elemental_Mastery', 0)
    
    for element_name, mastery_key in elements:
        element_mastery = build_stats.get(mastery_key, 0)
        total_element_mastery = element_mastery + elemental_mastery
        
        resistance_scenarios = []
        
        for flat_resistance in resistance_presets:
            # Calculate with normal hit (single target)
            normal_params = DamageInput(
                base_spell_damage=base_spell_damage,
                elemental_mastery=total_element_mastery,
                melee_mastery=melee_mastery if is_melee else 0,
                distance_mastery=distance_mastery if not is_melee else 0,
                flat_resistance=flat_resistance,
                is_critical=False,
                is_melee=is_melee,
                is_single_target=True
            )
            normal_result = calculate_damage(normal_params)
            
            # Calculate with critical hit (single target)
            crit_params = DamageInput(
                base_spell_damage=base_spell_damage,
                elemental_mastery=total_element_mastery,
                critical_mastery=critical_mastery,
                melee_mastery=melee_mastery if is_melee else 0,
                distance_mastery=distance_mastery if not is_melee else 0,
                flat_resistance=flat_resistance,
                is_critical=True,
                is_melee=is_melee,
                is_single_target=True
            )
            crit_result = calculate_damage(crit_params)
            
            # Calculate backstab damage (1.25x backstab bonus)
            backstab_params = DamageInput(
                base_spell_damage=base_spell_damage,
                elemental_mastery=total_element_mastery,
                melee_mastery=melee_mastery if is_melee else 0,
                distance_mastery=distance_mastery if not is_melee else 0,
                rear_mastery=rear_mastery,
                flat_resistance=flat_resistance,
                is_critical=False,
                is_melee=is_melee,
                is_backstab=True,
                is_single_target=True
            )
            backstab_result = calculate_damage(backstab_params)
            
            # Calculate backstab + critical damage
            backstab_crit_params = DamageInput(
                base_spell_damage=base_spell_damage,
                elemental_mastery=total_element_mastery,
                critical_mastery=critical_mastery,
                melee_mastery=melee_mastery if is_melee else 0,
                distance_mastery=distance_mastery if not is_melee else 0,
                rear_mastery=rear_mastery,
                flat_resistance=flat_resistance,
                is_critical=True,
                is_melee=is_melee,
                is_backstab=True,
                is_single_target=True
            )
            backstab_crit_result = calculate_damage(backstab_crit_params)
            
            # Only show positive damage (no healing enemy)
            normal_damage = max(0, normal_result.final_damage)
            critical_damage = max(0, crit_result.final_damage) if include_critical else None
            backstab_damage = max(0, backstab_result.final_damage)
            backstab_critical_damage = max(0, backstab_crit_result.final_damage) if include_critical else None
            
            # Get resistance percentage for display
            resistance_percent = convert_flat_resistance_to_percent(flat_resistance)
            
            resistance_scenarios.append({
                'flat_resistance': flat_resistance,
                'resistance_percent': round(resistance_percent, 1),
                'normal_damage': normal_damage,
                'critical_damage': critical_damage,
                'backstab_damage': backstab_damage,
                'backstab_critical_damage': backstab_critical_damage
            })
        
        results.append(ElementalDamageEstimate(
            element=element_name,
            base_mastery=total_element_mastery,
            resistance_scenarios=resistance_scenarios
        ))
    
    return results


def calculate_average_damage_per_element(
    build_stats: Dict[str, float],
    enemy_resistances: Dict[str, float],
    base_spell_damage: float = 100.0
) -> Dict[str, float]:
    """
    Calculate average damage for each element given specific enemy resistances (FLAT values)
    
    Args:
        build_stats: Dictionary of build statistics
        enemy_resistances: Dictionary of enemy FLAT resistances per element (e.g., {'Fire': 200, 'Water': 150})
        base_spell_damage: Base damage of spell
    
    Returns:
        Dictionary with average damage per element (only positive values)
    """
    
    elements = {
        'Fire': 'Fire_Mastery',
        'Water': 'Water_Mastery',
        'Earth': 'Earth_Mastery',
        'Air': 'Air_Mastery'
    }
    
    elemental_mastery = build_stats.get('Elemental_Mastery', 0)
    critical_mastery = build_stats.get('Critical_Mastery', 0)
    melee_mastery = build_stats.get('Melee_Mastery', 0)
    
    results = {}
    
    for element_name, mastery_key in elements.items():
        element_mastery = build_stats.get(mastery_key, 0)
        total_element_mastery = element_mastery + elemental_mastery
        flat_resistance = enemy_resistances.get(element_name, 0)
        
        # Calculate normal damage (melee, single target)
        normal_params = DamageInput(
            base_spell_damage=base_spell_damage,
            elemental_mastery=total_element_mastery,
            melee_mastery=melee_mastery,
            flat_resistance=flat_resistance,
            is_critical=False,
            is_melee=True,
            is_single_target=True
        )
        normal_damage = max(0, calculate_damage(normal_params).final_damage)
        
        # Calculate critical damage (melee, single target)
        crit_params = DamageInput(
            base_spell_damage=base_spell_damage,
            elemental_mastery=total_element_mastery,
            critical_mastery=critical_mastery,
            melee_mastery=melee_mastery,
            flat_resistance=flat_resistance,
            is_critical=True,
            is_melee=True,
            is_single_target=True
        )
        crit_damage = max(0, calculate_damage(crit_params).final_damage)
        
        # Convert resistance for display
        resistance_percent = convert_flat_resistance_to_percent(flat_resistance)
        
        # Average (simple average, can be weighted by crit chance)
        results[element_name] = {
            'normal': normal_damage,
            'critical': crit_damage,
            'average': (normal_damage + crit_damage) / 2,
            'flat_resistance': flat_resistance,
            'resistance_percent': round(resistance_percent, 1)
        }
    
    return results

