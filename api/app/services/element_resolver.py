"""
Element Resolver Service

Resolves random elemental stats (damages and resistances) based on user preferences.
When an item has stats like "Multi_Element_Mastery_3" (3 random elemental masteries),
this service applies them to the user's preferred elements in order.
"""

from typing import Dict, List
import logging

logger = logging.getLogger(__name__)

# Mapping of random stat keys to their base stat type
RANDOM_MASTERY_STATS = {
    'Multi_Element_Mastery_1': 1,
    'Multi_Element_Mastery_2': 2,
    'Multi_Element_Mastery_3': 3,
    'Multi_Element_Mastery_4': 4,
    'Elemental_Mastery_1_elements': 1,
    'Elemental_Mastery_2_elements': 2,
    'Elemental_Mastery_3_elements': 3,
    'Elemental_Mastery_4_elements': 4,
    'Random_Elemental_Mastery': 1,
}

RANDOM_RESISTANCE_STATS = {
    'Random_Elemental_Resistance_1': 1,
    'Random_Elemental_Resistance_2': 2,
    'Random_Elemental_Resistance_3': 3,
    'Random_Elemental_Resistance_4': 4,
    'Elemental_Resistance_1_elements': 1,
    'Elemental_Resistance_2_elements': 2,
    'Elemental_Resistance_3_elements': 3,
    'Elemental_Resistance_4_elements': 4,
    'Random_Elemental_Resistance': 1,
}

# Global elemental stats
GLOBAL_MASTERY_STATS = ['Elemental_Mastery']
GLOBAL_RESISTANCE_STATS = ['Elemental_Resistance']


def resolve_element_stats(
    stats: Dict[str, float],
    damage_preferences: List[str],
    resistance_preferences: List[str]
) -> Dict[str, float]:
    """
    Resolve random elemental stats based on user preferences.
    
    Args:
        stats: Dictionary of item stats (may contain random elemental stats)
        damage_preferences: Ordered list of element preferences for damage ['Fire', 'Water', 'Earth', 'Air']
        resistance_preferences: Ordered list of element preferences for resistances
        
    Returns:
        Dictionary with resolved stats (random stats converted to specific elements)
    """
    resolved_stats = stats.copy()
    
    # Process random mastery stats
    for random_stat, num_elements in RANDOM_MASTERY_STATS.items():
        if random_stat in resolved_stats:
            value = resolved_stats.pop(random_stat)
            
            # Apply to the first N preferred elements
            for i in range(min(num_elements, len(damage_preferences))):
                element = damage_preferences[i]
                stat_key = f"{element}_Mastery"
                resolved_stats[stat_key] = resolved_stats.get(stat_key, 0) + value
                
            logger.debug(f"Resolved {random_stat} ({value}) to first {num_elements} damage elements")
    
    # Process random resistance stats
    for random_stat, num_elements in RANDOM_RESISTANCE_STATS.items():
        if random_stat in resolved_stats:
            value = resolved_stats.pop(random_stat)
            
            # Apply to the first N preferred elements
            for i in range(min(num_elements, len(resistance_preferences))):
                element = resistance_preferences[i]
                stat_key = f"{element}_Resistance"
                resolved_stats[stat_key] = resolved_stats.get(stat_key, 0) + value
                
            logger.debug(f"Resolved {random_stat} ({value}) to first {num_elements} resistance elements")
    
    # Process global mastery stats (apply to all elements)
    for global_stat in GLOBAL_MASTERY_STATS:
        if global_stat in resolved_stats:
            value = resolved_stats[global_stat]
            
            # Apply to all elements in preference order
            for element in damage_preferences:
                stat_key = f"{element}_Mastery"
                resolved_stats[stat_key] = resolved_stats.get(stat_key, 0) + value
                
            logger.debug(f"Resolved {global_stat} ({value}) to all damage elements")
    
    # Process global resistance stats (apply to all elements)
    for global_stat in GLOBAL_RESISTANCE_STATS:
        if global_stat in resolved_stats:
            value = resolved_stats[global_stat]
            
            # Apply to all elements in preference order
            for element in resistance_preferences:
                stat_key = f"{element}_Resistance"
                resolved_stats[stat_key] = resolved_stats.get(stat_key, 0) + value
                
            logger.debug(f"Resolved {global_stat} ({value}) to all resistance elements")
    
    return resolved_stats


def resolve_build_stats(
    items_stats_list: List[Dict[str, float]],
    damage_preferences: List[str],
    resistance_preferences: List[str]
) -> Dict[str, float]:
    """
    Resolve stats for an entire build (all items combined).
    
    Args:
        items_stats_list: List of stat dictionaries from each item in the build
        damage_preferences: Ordered list of element preferences for damage
        resistance_preferences: Ordered list of element preferences for resistances
        
    Returns:
        Dictionary with total resolved stats for the build
    """
    total_stats = {}
    
    # First, accumulate all stats
    for item_stats in items_stats_list:
        for stat_key, stat_value in item_stats.items():
            total_stats[stat_key] = total_stats.get(stat_key, 0) + stat_value
    
    # Then resolve random elemental stats
    resolved_stats = resolve_element_stats(
        total_stats,
        damage_preferences,
        resistance_preferences
    )
    
    return resolved_stats

