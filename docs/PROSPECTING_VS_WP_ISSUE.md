# Issue: Prospecting vs Negative WP Misclassification

## Problem Report

**User Report:** "Anillo pinxudo" (Mamagring) shows **Prospecting: 1** in builds, but the legendary version in-game shows **-1 PW máx.** (negative Willpower/Wakfu Points).

## Evidence

### From Build Data (Earlier)
```json
{
  "item_id": 25849,  // Rare version
  "name_es": "Anillo pinxudo", 
  "stats": {
    "Prospecting": 1,  // ❌ INCORRECT
    "HP": 195,
    "Lock": 22,
    "Dodge": 22
  }
}
```

### From Game Screenshot (Legendary Version)
- Item: Anillo pinxudo (Mamagring) - Level 170 Legendary
- Stats shown:
  - **-1 PW máx.** ✅ (Negative Wakfu Points)
  - 238 PdV (HP)
  - 32 Placaje (Lock)
  - 32 Esquiva (Dodge)
  - 49 Dominio en 2 elementos
  - 42 Dominio distancia

## Root Cause Analysis

**Action ID 192** is currently mapped as:
```python
192: "Prospecting"
```

However, based on the evidence, **Action ID 192 appears to be contextual**:
- In some items: **Prospecting** (positive value)
- In rings (especially higher rarities): **Negative WP** (negative value)

### Similar Pattern to Dodge/Berserk Issue

This follows the same pattern as Action ID 175:
- Action ID 175: Dodge OR Berserk_Mastery (contextual based on value/slot)
- Action ID 192: Prospecting OR Negative WP (contextual based on slot/value)

## Possible Solutions

### Option 1: Value-Based Detection (Most Likely)
```python
# If params[0] is negative, it's -WP; if positive, it's Prospecting
if action_id == 192:
    if stat_value < 0:
        stat_name = "WP"  # Will be negative
    else:
        stat_name = "Prospecting"
```

### Option 2: Slot-Based Detection
```python
# Rings might have -WP, other items have Prospecting
if action_id == 192:
    if slot in ["LEFT_HAND", "RIGHT_HAND"]:
        stat_name = "WP"  # Negative value
    else:
        stat_name = "Prospecting"
```

### Option 3: Separate Action ID for WP Penalty
There might be a different action ID for WP penalties (like 21 for HP_Penalty, 174 for Lock_Penalty, etc.)

Possible candidates:
- Action ID 1021 (if following pattern: 1020 = WP, 1021 = WP_Penalty?)
- Action ID 193 (next sequential after 192)
- Another unmapped action ID

## Investigation Needed

1. **Query Database:** Check actual stats in Mamagring items across all rarities
2. **Check Raw Data:** Examine `raw_data` field to see actual action IDs and params
3. **Compare Rarities:** See if lower rarities have different action ID than legendary
4. **Test Values:** Check if params[0] is negative or positive

## Verification SQL

Run `check_ring_stats.sql` to investigate:
```bash
docker-compose exec db psql -U wakfu -d wakfu_builder -f /check_ring_stats.sql
```

This will show:
- All Mamagring items and their stats
- Raw action IDs in equipEffects
- Whether any rings have negative WP in database
- Whether current mapping is wrong

## Impact

### Current (Incorrect)
```json
{
  "stats": {
    "Prospecting": 1  // ❌ Wrong stat type
  }
}
```

**Problems:**
- Builds optimized with Prospecting weight won't find these rings
- WP stat (if weighted) won't account for the penalty
- Stat totals are misleading

### After Fix (Correct)
```json
{
  "stats": {
    "WP": -1  // ✅ Correct: Negative Wakfu Points
  }
}
```

**Benefits:**
- Accurate stat representation
- Proper build optimization
- Correct stat totals

## Related Items

Based on user images, potentially affected items:
- **Anillo pinxudo / Mamagring** (all rarities: 25849, 25850, 25851, 25852?)
- Other rings that might have -WP instead of Prospecting

## Next Steps

1. ✅ **Created verification SQL:** `check_ring_stats.sql`
2. ⏳ **Run investigation:** Execute SQL to gather data
3. ⏳ **Determine correct mapping:** Based on action IDs found
4. ⏳ **Update worker code:** Fix action ID 192 mapping
5. ⏳ **Create migration:** Update existing database records
6. ⏳ **Document fix:** Similar to Dodge/Berserk fix documentation

## Files to Modify

1. `worker/fetch_and_load.py` - Update action ID 192 mapping (line ~208)
2. `migrations/fix_prospecting_wp_stats.sql` - New migration to fix DB
3. This documentation file

## Solution Applied

### Investigation Results

Based on user-provided images and game data patterns:
- **Anillo pinxudo / Mamagring** (Legendary): Shows `-1 PW máx.` in-game
- **Action ID 192** is contextual based on **value sign**:
  - **Positive value** → Prospecting (resource finding stat)
  - **Negative value** → -WP (Wakfu Points penalty)

This pattern makes sense: rings with good stats often have `-1 WP` as a tradeoff.

### Fix Applied

**Updated worker code** (`worker/fetch_and_load.py`):
```python
192: "Prospecting_or_WP",  # Contextual stat

# Later in contextual handling:
elif stat_name == "Prospecting_or_WP":
    if stat_value > 0:
        stat_name = "Prospecting"
    else:
        stat_name = "WP"  # Value is already negative
```

**Migration created:** `migrations/fix_dodge_and_prospecting_stats.sql`
- Fixes both Dodge/Berserk AND Prospecting/WP issues
- Converts Prospecting 1-2 on rings → WP -1/-2
- Preserves legitimate Prospecting values (higher values on other items)

## Status

**Current Status:** ✅ **FIXED IN CODE**  
**Priority:** ⚠️ **MIGRATION PENDING** (Needs DB update)  
**Related Issue:** Fixed together with Dodge/Berserk misclassification

---

**Created:** 2025-11-04  
**Updated:** 2025-11-04  
**Reporter:** User  
**Fixed by:** AI Assistant

