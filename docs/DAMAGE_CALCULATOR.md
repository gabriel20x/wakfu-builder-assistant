# 🧮 Wakfu Damage Calculator

## Overview

The Damage Calculator is a new feature that estimates damage output for each element based on build statistics and enemy resistances. This helps players understand which element will perform best against different enemy types.

## Features

### 🎯 Damage Estimation
- **Element Comparison**: See damage estimates for all four elements (Fire, Water, Earth, Air)
- **Resistance Scenarios**: View damage at multiple resistance levels (0%, 100%, 200%, 300%, 400%, 500%)
- **Critical Hits**: Toggle between normal and critical damage calculations
- **Mastery Display**: Shows total mastery for each element

### 📊 Visual Representation
- **Horizontal Bar Charts**: Easy-to-read visual comparison of damage output
- **Color-Coded Elements**: Each element has its distinctive color
- **Best Element Recommendation**: Automatic recommendation based on average damage

### ⚙️ Customization
- **Resistance Presets**: Select which resistance levels to display
- **Base Spell Damage**: Calculations based on 100 base damage spell
- **Critical Toggle**: Show or hide critical damage bars

## API Endpoints

### `/damage/estimate` (POST)
Estimate damage for a build at different resistance levels.

**Request Body:**
```json
{
  "build_stats": {
    "Fire_Mastery": 1200,
    "Water_Mastery": 800,
    "Elemental_Mastery": 500,
    "Critical_Mastery": 400
  },
  "base_spell_damage": 100.0,
  "resistance_presets": [0, 100, 200, 300, 400, 500],
  "include_critical": true
}
```

**Response:**
```json
{
  "estimates": [
    {
      "element": "Fire",
      "base_mastery": 1700.0,
      "resistance_scenarios": [
        {
          "resistance": 0,
          "normal_damage": 1800.0,
          "critical_damage": 2475.0
        },
        ...
      ]
    },
    ...
  ],
  "base_spell_damage": 100.0,
  "resistance_presets": [0, 100, 200, 300, 400, 500]
}
```

### `/damage/custom-resistances` (POST)
Calculate damage with specific enemy resistances.

**Request Body:**
```json
{
  "build_stats": {
    "Fire_Mastery": 1200,
    "Water_Mastery": 800
  },
  "enemy_resistances": {
    "Fire": 200,
    "Water": 150,
    "Earth": 250,
    "Air": 180
  },
  "base_spell_damage": 100.0
}
```

### `/damage/calculate` (POST)
Detailed damage calculation with full parameter control.

**Request Body:**
```json
{
  "attacker_level": 230,
  "target_level": 230,
  "base_spell_damage": 100.0,
  "elemental_mastery": 1200.0,
  "secondary_mastery": 800.0,
  "resistances_target": 200.0,
  "critical_hit": true,
  "critical_mastery": 400.0,
  "final_damage_bonus": 0.15,
  "backstab_or_position_mod": 0.0,
  "armor": 0.0
}
```

## Damage Formula

The calculator implements the official Wakfu damage formulas:

1. **Total Mastery** = Elemental Mastery + Secondary Mastery + Critical Mastery (if crit)
2. **Preliminary Damage** = Base Spell Damage × (1 + Total Mastery / 100)
3. **Apply Resistances**: Effective Damage = Preliminary Damage × (1 - Resistance / 100)
4. **Critical Multiplier**: If critical, multiply by 1.25
5. **Position Modifiers**: Apply backstab, berserk, distance modifiers
6. **Final Damage Modifiers**: Apply buffs and debuffs
7. **Armor Reduction**: Subtract armor value
8. **Damage Reduction**: Apply percentage reductions (e.g., Feca glyphs)

## Usage in Frontend

The damage estimator is automatically displayed in the **Stats Panel** after generating a build:

1. **Generate a Build**: Configure your stat weights and generate builds
2. **View Stats**: Switch between different build difficulties
3. **Check Damage**: Scroll down in the Stats Panel to see the Damage Estimator
4. **Customize View**: 
   - Toggle resistance levels to display
   - Enable/disable critical damage
   - Read the recommendation for best element

## Example Scenarios

### Scenario 1: Mono-Element Build
```
Fire Mastery: 2000
Elemental Mastery: 400
Total Fire Mastery: 2400

Against 0% resistance: ~2500 damage
Against 200% resistance: ~-100 damage (heals enemy!)
Against 300% resistance: ~-200 damage
```

### Scenario 2: Multi-Element Build
```
Fire Mastery: 1200
Water Mastery: 1000
Earth Mastery: 800
Elemental Mastery: 500

Best against 200% Fire resistance: Use Water or Earth
Best against balanced resistances: Use Fire (highest mastery)
```

## Technical Implementation

### Backend (Python/FastAPI)
- **Service**: `api/app/services/damage_calculator.py`
  - `calculate_damage()`: Core damage calculation function
  - `estimate_elemental_damage()`: Generate estimates for all elements
  - `calculate_average_damage_per_element()`: Custom resistance calculations

- **Router**: `api/app/routers/damage_calculator.py`
  - Three endpoints for different calculation needs
  - Pydantic models for request/response validation

### Frontend (Vue 3)
- **Component**: `frontend/src/components/DamageEstimator.vue`
  - Reactive damage calculations
  - Interactive resistance preset selection
  - Visual bar charts with smooth animations
  - Element-specific color coding

- **API Client**: `frontend/src/services/api.js`
  - `damageAPI.estimateDamage()`: Fetch damage estimates
  - `damageAPI.calculateWithCustomResistances()`: Custom calculations
  - `damageAPI.calculateDetailed()`: Full parameter control

## Future Enhancements

Potential improvements for the damage calculator:

1. **Critical Hit Chance**: Weight normal vs critical damage by actual crit chance
2. **Position Mastery**: Add rear/melee/distance mastery to calculations
3. **Spell Database**: Select actual spells with their base damage values
4. **Enemy Database**: Pre-configured enemy resistance profiles
5. **DPS Calculator**: Factor in AP costs and spell cooldowns
6. **Buff Simulation**: Add common buffs/debuffs to calculations
7. **Export Results**: Download damage comparison charts

## Credits

Based on the official Wakfu damage formulas and the Wakfu Damage Calculator spreadsheet.

