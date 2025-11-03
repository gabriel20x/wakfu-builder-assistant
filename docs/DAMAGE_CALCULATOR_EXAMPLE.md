# 📊 Damage Calculator - Visual Example

## Example Scenario

Let's see how the damage calculator works with a real build example.

### Build Stats
```
Fire Mastery: 1200
Water Mastery: 800
Earth Mastery: 1000
Air Mastery: 600
Elemental Mastery: 400
Critical Mastery: 300
Melee Mastery: 200
```

## Damage Comparison (Base Spell: 100 damage)

### 🔥 Fire Element
**Total Mastery**: 1200 + 400 = 1600

| Resistance | Normal Damage | Critical Damage |
|------------|--------------|-----------------|
| 0%         | 1,800        | 2,475          |
| 100%       | 0            | 0              |
| 200%       | -1,800       | -2,475         |
| 300%       | -3,600       | -4,950         |

### 💧 Water Element
**Total Mastery**: 800 + 400 = 1200

| Resistance | Normal Damage | Critical Damage |
|------------|--------------|-----------------|
| 0%         | 1,400        | 1,925          |
| 100%       | 0            | 0              |
| 200%       | -1,400       | -1,925         |
| 300%       | -2,800       | -3,850         |

### 🌍 Earth Element
**Total Mastery**: 1000 + 400 = 1400

| Resistance | Normal Damage | Critical Damage |
|------------|--------------|-----------------|
| 0%         | 1,600        | 2,200          |
| 100%       | 0            | 0              |
| 200%       | -1,600       | -2,200         |
| 300%       | -3,200       | -4,400         |

### 💨 Air Element
**Total Mastery**: 600 + 400 = 1000

| Resistance | Normal Damage | Critical Damage |
|------------|--------------|-----------------|
| 0%         | 1,200        | 1,650          |
| 100%       | 0            | 0              |
| 200%       | -1,200       | -1,650         |
| 300%       | -2,400       | -3,300         |

## Visual Representation

The component displays this as horizontal bar charts:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔥 Fire                        1600 dominio
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
0% res   ████████████████████ 1800
100% res █ 0
200% res (negative) -1800

💧 Water                       1200 dominio
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
0% res   ███████████████ 1400
100% res █ 0
200% res (negative) -1400

🌍 Earth                       1400 dominio
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
0% res   ████████████████ 1600
100% res █ 0
200% res (negative) -1600

💨 Air                         1000 dominio
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
0% res   ████████████ 1200
100% res █ 0
200% res (negative) -1200
```

## Recommendation

```
ℹ️ Recomendación:
🔥 Fire ofrece el mejor daño promedio (600 por hechizo)
```

## Use Cases

### Case 1: Low Resistance Enemy (0-50%)
**Best Choice**: Fire (highest mastery = highest damage)
- Fire deals 1,800+ damage
- Water deals 1,400 damage
- Earth deals 1,600 damage
- Difference: Fire is 12.5% better than Earth

### Case 2: Moderate Resistance Enemy (100-150%)
**Analysis**: All elements perform similarly poorly
- Consider element with highest mastery still
- Fire still has slight edge due to mastery

### Case 3: High Resistance Enemy (200%+)
**Warning**: Damage becomes negative (heals enemy!)
- Fire at 200% res: -1,800 (heals enemy)
- Switch elements or avoid this enemy
- Consider using elemental reduction spells first

### Case 4: Mixed Resistance Enemy
**Example Enemy Resistances**:
- Fire: 300%
- Water: 100%
- Earth: 150%
- Air: 50%

**Best Strategy**: Use Air element
- Air at 50% res: ~600 damage (still positive)
- Fire would heal enemy
- Water would do 0 damage
- Earth would do negative damage

## Real Boss Example: Imaginary Boss "Flame Golem"

### Boss Stats
```
Level: 230
Fire Resistance: 400%
Water Resistance: -50% (weak to water!)
Earth Resistance: 200%
Air Resistance: 150%
```

### Your Build Damage
Using the example build stats:

| Element | Base Mastery | Damage vs Boss |
|---------|-------------|----------------|
| 🔥 Fire | 1,600       | -5,400 (heals!)  |
| 💧 Water| 1,200       | 2,100 ⭐        |
| 🌍 Earth| 1,400       | -1,600 (heals!)  |
| 💨 Air  | 1,000       | -600 (heals!)    |

**Clear Choice**: Water element is the only viable option!

### Insight
Even though your Fire mastery is 400 points higher than Water:
- Fire would heal the boss by 5,400 HP per spell
- Water with lower mastery deals 2,100 damage
- This is a **7,500 damage swing** by choosing correctly!

## API Response Example

```json
{
  "estimates": [
    {
      "element": "Fire",
      "base_mastery": 1600.0,
      "resistance_scenarios": [
        {
          "resistance": 0,
          "normal_damage": 1800.0,
          "critical_damage": 2475.0
        },
        {
          "resistance": 100,
          "normal_damage": 0.0,
          "critical_damage": 0.0
        },
        {
          "resistance": 200,
          "normal_damage": -1800.0,
          "critical_damage": -2475.0
        }
      ]
    }
    // ... other elements
  ],
  "base_spell_damage": 100.0,
  "resistance_presets": [0, 100, 200, 300, 400, 500]
}
```

## Formula Breakdown

Let's calculate Fire damage at 0% resistance step by step:

```
Given:
- Base Spell Damage: 100
- Fire Mastery: 1200
- Elemental Mastery: 400
- Total Fire Mastery: 1600
- Melee Mastery: 200
- Target Resistance: 0%

Step 1: Total Mastery
= Elemental Mastery (1600) + Secondary Mastery (200)
= 1800

Step 2: Preliminary Damage
= Base Damage × (1 + Total Mastery / 100)
= 100 × (1 + 1800 / 100)
= 100 × 19
= 1900

Step 3: Apply Resistance
= Preliminary Damage × (1 - Resistance / 100)
= 1900 × (1 - 0 / 100)
= 1900 × 1
= 1900

Step 4: No Critical (normal damage)
= 1900

Final Damage: 1,900
```

With Critical Hit:
```
Step 4: Critical Multiplier
= 1900 × 1.25
= 2375

Plus Critical Mastery (300):
Total Mastery = 1800 + 300 = 2100
Preliminary = 100 × (1 + 2100/100) = 2200
After Resistance = 2200 × 1 = 2200
Critical = 2200 × 1.25 = 2750

Final Critical Damage: 2,750
```

## Tips for Using the Calculator

1. **Always Check All Elements**: Your highest mastery might not be best against certain enemies
2. **Watch for Negative Damage**: Anything below 0 heals the enemy!
3. **Consider Resistance Thresholds**: 
   - 0-100%: Normal damage scaling
   - 100%+: Damage becomes negative
4. **Balance Your Build**: Consider adding elemental variety if you face varied enemies
5. **Use Custom Resistance**: Test against specific boss profiles
6. **Factor in Critical Chance**: If you have high crit chance, weight critical damage more heavily

## Conclusion

The Damage Calculator provides instant visual feedback on element effectiveness, helping you:
- Choose the right element for each fight
- Understand resistance impacts
- Optimize your build for specific content
- Avoid accidentally healing enemies!

