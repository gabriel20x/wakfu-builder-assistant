"""
Tests for Damage Calculator Service
"""

import pytest
from app.services.damage_calculator import (
    DamageInput,
    calculate_damage,
    estimate_elemental_damage,
    calculate_average_damage_per_element
)


def test_basic_damage_calculation():
    """Test basic damage calculation without modifiers"""
    params = DamageInput(
        base_spell_damage=100.0,
        elemental_mastery=1000.0,
        resistances_target=0.0
    )
    
    result = calculate_damage(params)
    
    # With 1000 mastery, damage should be: 100 * (1 + 1000/100) = 100 * 11 = 1100
    assert result.total_mastery == 1000.0
    assert result.preliminary_damage == 1100.0
    assert result.final_damage == 1100.0


def test_damage_with_resistance():
    """Test damage calculation with enemy resistance"""
    params = DamageInput(
        base_spell_damage=100.0,
        elemental_mastery=1000.0,
        resistances_target=200.0  # 200% resistance
    )
    
    result = calculate_damage(params)
    
    # Preliminary: 1100
    # After 200% resistance: 1100 * (1 - 200/100) = 1100 * (-1) = -1100
    assert result.effective_damage == -1100.0


def test_critical_damage():
    """Test critical hit damage calculation"""
    params = DamageInput(
        base_spell_damage=100.0,
        elemental_mastery=1000.0,
        critical_hit=True,
        critical_mastery=400.0,
        resistances_target=0.0
    )
    
    result = calculate_damage(params)
    
    # Total mastery: 1000 + 400 = 1400
    # Preliminary: 100 * (1 + 1400/100) = 1500
    # Critical multiplier: 1500 * 1.25 = 1875
    assert result.total_mastery == 1400.0
    assert result.preliminary_damage == 1500.0
    assert result.final_damage == 1875.0


def test_damage_with_armor():
    """Test damage reduction from armor"""
    params = DamageInput(
        base_spell_damage=100.0,
        elemental_mastery=500.0,
        armor=200.0,
        resistances_target=0.0
    )
    
    result = calculate_damage(params)
    
    # Damage: 100 * (1 + 500/100) = 600
    # After armor: 600 - 200 = 400
    assert result.final_damage == 600.0
    assert result.damage_after_armor == 400.0


def test_estimate_elemental_damage():
    """Test elemental damage estimation"""
    build_stats = {
        'Fire_Mastery': 1200,
        'Water_Mastery': 800,
        'Earth_Mastery': 1000,
        'Air_Mastery': 600,
        'Elemental_Mastery': 400,
        'Critical_Mastery': 300
    }
    
    resistance_presets = [0, 100, 200]
    
    results = estimate_elemental_damage(
        build_stats=build_stats,
        base_spell_damage=100.0,
        resistance_presets=resistance_presets,
        include_critical=True
    )
    
    # Should return 4 elements
    assert len(results) == 4
    
    # Check Fire element
    fire_result = next(r for r in results if r.element == 'Fire')
    assert fire_result.base_mastery == 1600  # 1200 + 400
    assert len(fire_result.resistance_scenarios) == 3  # 0, 100, 200
    
    # Check that damage decreases with resistance
    fire_scenarios = fire_result.resistance_scenarios
    assert fire_scenarios[0]['normal_damage'] > fire_scenarios[1]['normal_damage']
    assert fire_scenarios[1]['normal_damage'] > fire_scenarios[2]['normal_damage']


def test_calculate_average_damage():
    """Test average damage calculation with custom resistances"""
    build_stats = {
        'Fire_Mastery': 1200,
        'Water_Mastery': 800,
        'Elemental_Mastery': 400,
        'Critical_Mastery': 300,
        'Melee_Mastery': 200
    }
    
    enemy_resistances = {
        'Fire': 200,
        'Water': 100,
        'Earth': 150,
        'Air': 50
    }
    
    results = calculate_average_damage_per_element(
        build_stats=build_stats,
        enemy_resistances=enemy_resistances,
        base_spell_damage=100.0
    )
    
    # Should return all 4 elements
    assert 'Fire' in results
    assert 'Water' in results
    assert 'Earth' in results
    assert 'Air' in results
    
    # Each element should have normal, critical, and average
    fire_damage = results['Fire']
    assert 'normal' in fire_damage
    assert 'critical' in fire_damage
    assert 'average' in fire_damage
    
    # Critical should be higher than normal
    assert fire_damage['critical'] > fire_damage['normal']


def test_position_modifiers():
    """Test damage with position modifiers"""
    params = DamageInput(
        base_spell_damage=100.0,
        elemental_mastery=1000.0,
        backstab_or_position_mod=0.25,  # 25% backstab bonus
        berserk_mod=0.15,  # 15% berserk bonus
        resistances_target=0.0
    )
    
    result = calculate_damage(params)
    
    # Base damage: 1100
    # Position total: 0.25 + 0.15 = 0.40 (40%)
    # With modifiers: 1100 * (1 + 0.40) = 1540
    assert result.final_damage == 1540.0


def test_final_damage_modifiers():
    """Test final damage bonus and resistance modifiers"""
    params = DamageInput(
        base_spell_damage=100.0,
        elemental_mastery=1000.0,
        final_damage_bonus=0.20,  # 20% damage bonus
        final_resistance_bonus=0.10,  # 10% resistance bonus
        resistances_target=0.0
    )
    
    result = calculate_damage(params)
    
    # Base damage: 1100
    # Final modifier: (1 + 0.20 - 0.10) = 1.10
    # Result: 1100 * 1.10 = 1210
    assert result.final_damage == 1210.0


def test_damage_reduction():
    """Test damage reduction (like Feca glyphs)"""
    params = DamageInput(
        base_spell_damage=100.0,
        elemental_mastery=1000.0,
        damage_reduction=25.0,  # 25% reduction
        resistances_target=0.0
    )
    
    result = calculate_damage(params)
    
    # Base damage: 1100
    # After reduction: 1100 * (1 - 25/100) = 825
    assert result.damage_after_armor == 825.0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

