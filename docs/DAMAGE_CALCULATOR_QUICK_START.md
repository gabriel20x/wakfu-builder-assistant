# 🚀 Damage Calculator - Quick Start Guide

## For Users

### Accessing the Damage Calculator

1. **Open the Wakfu Builder Assistant**
2. **Configure Your Build**:
   - Set your character level
   - Select stats to prioritize
   - Choose element preferences
3. **Generate Builds**: Click "Generar Builds"
4. **View Results**: Select a build difficulty tab (Fácil, Medio, Difícil, etc.)
5. **Scroll Down**: In the "Stats Totales" panel, scroll to see the Damage Estimator

### Using the Damage Calculator

**Controls**:
- **Resistance Toggles**: Click the percentage buttons (0%, 100%, 200%, etc.) to show/hide those resistance levels
- **Critical Checkbox**: Toggle to show/hide critical damage calculations

**Reading the Results**:
- Each element shows its total mastery (base element + elemental mastery)
- Horizontal bars represent damage output
- Longer bars = more damage
- Values are shown at the end of each bar
- Blue bars = normal damage
- Red bars = critical damage

**Recommendation**:
- At the bottom, see which element offers the best average damage
- Use this to guide your spell choices in combat

## For Developers

### Quick API Test

Test the damage calculator endpoint:

```bash
# Start the API server
cd api
uvicorn app.main:app --reload

# Test the estimate endpoint
curl -X POST "http://localhost:8000/api/damage/estimate" \
  -H "Content-Type: application/json" \
  -d '{
    "build_stats": {
      "Fire_Mastery": 1200,
      "Water_Mastery": 800,
      "Elemental_Mastery": 500,
      "Critical_Mastery": 400
    },
    "base_spell_damage": 100.0,
    "resistance_presets": [0, 100, 200],
    "include_critical": true
  }'
```

### Running Tests

```bash
cd api
pytest tests/test_damage_calculator.py -v
```

### Frontend Development

```bash
# Start the frontend dev server
cd frontend
npm run dev

# The DamageEstimator component will auto-update when builds are generated
```

### Adding Custom Calculations

**Backend** (`api/app/services/damage_calculator.py`):

```python
from app.services.damage_calculator import DamageInput, calculate_damage

# Create custom calculation
params = DamageInput(
    base_spell_damage=150.0,
    elemental_mastery=2000.0,
    critical_hit=True,
    critical_mastery=500.0,
    resistances_target=150.0
)

result = calculate_damage(params)
print(f"Damage: {result.final_damage}")
```

**Frontend** (`YourComponent.vue`):

```vue
<script setup>
import { damageAPI } from '@/services/api'

const calculateDamage = async () => {
  const response = await damageAPI.estimateDamage({
    Fire_Mastery: 1500,
    Elemental_Mastery: 600,
    Critical_Mastery: 400
  }, {
    baseSpellDamage: 120,
    resistancePresets: [0, 50, 100, 150, 200]
  })
  
  console.log(response.data.estimates)
}
</script>
```

## Configuration

### Resistance Presets

Default resistance levels tested: `[0, 100, 200, 300, 400, 500]`

To customize:

**In Component**:
```javascript
const availablePresets = [0, 50, 100, 150, 200, 250, 300]
```

**In API Call**:
```javascript
damageAPI.estimateDamage(buildStats, {
  resistancePresets: [0, 50, 100, 150]
})
```

### Base Spell Damage

Default: 100

To customize:
```javascript
damageAPI.estimateDamage(buildStats, {
  baseSpellDamage: 150  // For stronger spells
})
```

## Troubleshooting

### Component Not Showing
- **Check**: Have you generated a build?
- **Check**: Is the stats panel visible?
- **Fix**: Generate at least one build to see the damage calculator

### API Errors
- **Check**: Is the API server running?
- **Check**: Are CORS settings configured?
- **Fix**: Restart API server with `uvicorn app.main:app --reload`

### Incorrect Calculations
- **Check**: Are masteries correctly summed? (Element + Elemental)
- **Check**: Is resistance above 100% showing negative damage? (This is correct!)
- **Fix**: Verify build_stats contains all mastery values

### Loading State Stuck
- **Check**: Browser console for API errors
- **Check**: Network tab for failed requests
- **Fix**: Verify API endpoint is accessible at `/api/damage/estimate`

## Advanced Usage

### Custom Enemy Profiles

Create preset enemy resistance profiles:

```javascript
const bossProfiles = {
  flameGolem: {
    Fire: 400,
    Water: -50,
    Earth: 200,
    Air: 150
  },
  frostDragon: {
    Fire: -30,
    Water: 350,
    Earth: 100,
    Air: 100
  }
}

// Calculate damage vs specific boss
const response = await damageAPI.calculateWithCustomResistances(
  buildStats,
  bossProfiles.flameGolem,
  100
)
```

### Position Mastery Integration

For future enhancement, add position masteries:

```javascript
const params = {
  base_spell_damage: 100,
  elemental_mastery: totalFireMastery,
  secondary_mastery: meleeMastery + rearMastery,
  backstab_or_position_mod: isBackstab ? 0.25 : 0,
  resistances_target: resistance
}
```

### DPS Calculator

Extend with DPS calculations:

```javascript
const calculateDPS = (damage, apCost, cooldown, totalAP) => {
  const castsPerTurn = Math.floor(totalAP / apCost)
  const damagePerTurn = damage * castsPerTurn
  const turnsForCooldown = Math.ceil(cooldown / castsPerTurn)
  const averageDPS = damagePerTurn / turnsForCooldown
  return averageDPS
}
```

## API Documentation

Full API documentation available at:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

Navigate to the "damage" tag to see all damage calculator endpoints.

## File Locations

```
Project Structure:
├── api/
│   ├── app/
│   │   ├── services/
│   │   │   └── damage_calculator.py      ← Core logic
│   │   └── routers/
│   │       └── damage_calculator.py      ← API endpoints
│   └── tests/
│       └── test_damage_calculator.py     ← Unit tests
├── frontend/
│   └── src/
│       ├── components/
│       │   ├── DamageEstimator.vue       ← Main component
│       │   └── BuildGenerator.vue        ← Integration
│       └── services/
│           └── api.js                    ← API client
└── docs/
    ├── DAMAGE_CALCULATOR.md              ← Full documentation
    ├── DAMAGE_CALCULATOR_EXAMPLE.md      ← Usage examples
    └── DAMAGE_CALCULATOR_QUICK_START.md  ← This file
```

## Support

For issues or questions:
1. Check documentation in `docs/DAMAGE_CALCULATOR.md`
2. Review examples in `docs/DAMAGE_CALCULATOR_EXAMPLE.md`
3. Inspect browser console for errors
4. Check API logs for backend errors

## Next Steps

Explore advanced features:
1. **Custom Resistances**: Test against specific bosses
2. **Position Modifiers**: Add rear/melee/distance calculations
3. **Buff Simulation**: Factor in team buffs
4. **Export Results**: Save damage comparisons

Happy calculating! 🎯

