# Fix: Dodge vs Berserk_Mastery Incorrect Classification

## Issue Description

### Problem
Items with **Dodge** stats were incorrectly classified as **Berserk_Mastery** due to an improper threshold in the contextual stat mapping logic.

### Affected Items
- **Screechcut** (Peinado Ror) - HEAD slot
  - Rare version (item_id: 21218): Had Berserk_Mastery: 70, should be Dodge: 70
  - Legendary version: Has Dodge: 80 (correct in higher rarities)
  
- **Pepepew Sword** (Espada de Pym, el Pío) - FIRST_WEAPON slot
  - Rare version (item_id: 26638): Had Berserk_Mastery: 110, should be Dodge: 110
  - Legendary version: Has Dodge: 170 (correct in higher rarities)

- Other items in HEAD, FIRST_WEAPON, SHOULDERS, and SECOND_WEAPON slots with Dodge values > 50

### Root Cause
Action ID **175** in Wakfu game data is a **contextual stat** that can be either:
- **Dodge** (most common - values can range from 10 to 200+)
- **Berserk_Mastery** (rare - typically very high values 250+)

The worker script (`worker/fetch_and_load.py`) had an incorrect threshold:
- **OLD**: Dodge if value < 50, Berserk_Mastery if value >= 50
- **PROBLEM**: Dodge values frequently exceed 50 (especially on weapons which can reach 170+)

## Solution

### 1. Updated Threshold Logic (worker/fetch_and_load.py)

**NEW** slot-specific thresholds:
- **FIRST_WEAPON, HEAD, SHOULDERS, SECOND_WEAPON**: 
  - Dodge if value < 250
  - Berserk_Mastery if value >= 250
  
- **Other slots** (CHEST, BELT, LEGS, etc.):
  - Dodge if value < 100
  - Berserk_Mastery if value >= 100

**Rationale**: 
- Dodge values commonly reach 100-200 on weapons and certain armor pieces
- Berserk_Mastery is rare and typically has very high values (250+) when it appears
- Different equipment slots have different typical Dodge ranges

### 2. Database Migration

Created migration script: `migrations/fix_dodge_berserk_stats.sql`

This script:
1. Identifies all items with incorrectly classified Berserk_Mastery
2. Converts Berserk_Mastery back to Dodge for:
   - Items in HEAD/FIRST_WEAPON/SHOULDERS/SECOND_WEAPON with value < 250
   - Items in other slots with value < 100
3. Preserves legitimate Berserk_Mastery values (>= thresholds)

### 3. Python Fix Script

Created alternative script: `fix_dodge_stats.py`

Can be used to verify and fix items programmatically if needed.

## How to Apply the Fix

### Option 1: Using Docker (Recommended)

```bash
# Apply the SQL migration
docker-compose exec db psql -U wakfu -d wakfu_builder -f /migrations/fix_dodge_berserk_stats.sql

# Restart the worker to reload data with new logic
docker-compose restart worker
```

### Option 2: Reload All Game Data

```bash
# The worker script now has the correct logic
# Reloading game data will automatically use the new thresholds
docker-compose restart worker
```

### Option 3: Manual SQL Execution

Connect to your PostgreSQL database and run the migration file directly:
```bash
psql -U wakfu -d wakfu_builder < migrations/fix_dodge_berserk_stats.sql
```

## Verification

After applying the fix, verify with:

```sql
-- Check items that should have Dodge (Screechcut and Pepepew Sword)
SELECT item_id, name_es, name, slot, level, rarity, 
       stats::jsonb->'Dodge' as dodge,
       stats::jsonb->'Berserk_Mastery' as berserk
FROM items
WHERE item_id IN (21218, 26638)
   OR name_es LIKE '%Peinado Ror%'
   OR name_es LIKE '%Espada de Pym%';

-- Expected results:
-- Screechcut items: Should have Dodge, NOT Berserk_Mastery
-- Pepepew Sword items: Should have Dodge, NOT Berserk_Mastery
```

## Impact on Builds

### Before Fix
```json
{
  "easy": {
    "total_stats": {
      "Berserk_Mastery": 180,  // WRONG - includes Dodge misclassified
      "Dodge": 210              // INCOMPLETE - missing items
    }
  }
}
```

### After Fix
```json
{
  "easy": {
    "total_stats": {
      "Berserk_Mastery": 0,     // CORRECT - removed false positives
      "Dodge": 390              // CORRECT - includes all Dodge items
    }
  }
}
```

## Related Files Modified

1. **worker/fetch_and_load.py** (lines 276-297)
   - Updated `Dodge_or_Berserk` contextual mapping logic
   - Increased thresholds to more accurately reflect actual item stats

2. **migrations/fix_dodge_berserk_stats.sql** (new file)
   - SQL migration to fix existing database records

3. **fix_dodge_stats.py** (new file)
   - Python script for programmatic fixing (alternative method)

## Testing

Test with these specific builds:
- Level 165-170 builds with Screechcut helmet
- Level 165-170 builds with Pepepew Sword weapon
- Check that Dodge values are correctly summed in build stats
- Verify Berserk_Mastery only appears on items that legitimately have it

## Future Prevention

The updated worker script will automatically handle new data loads correctly. No further action needed for future updates.

## References

- User report: Issue identified through build comparison
- Game data analysis: Confirmed Dodge values can exceed 170 on weapons
- Action ID 175: Confirmed as contextual stat requiring threshold logic

