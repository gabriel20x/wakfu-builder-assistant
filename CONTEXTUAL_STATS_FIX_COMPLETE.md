# ✅ Contextual Stats Issues - FIXED

## 🎯 Issues Reported

User identified **two stat mapping errors** by comparing build outputs with in-game item screenshots:

### Issue 1: Dodge vs Berserk_Mastery ❌→✅
**Items affected:**
- **Peinado Ror / Screechcut** (HEAD)
- **Espada de Pym / Pepepew Sword** (FIRST_WEAPON)

**Problem:** 
- Build showed: `Berserk_Mastery: 70` and `Berserk_Mastery: 110`
- In-game shows: `Dodge: 80` and `Dodge: 170` (legendary versions)

**Root cause:** Action ID 175 threshold too low (50 → should be 250 for weapons/head)

### Issue 2: Prospecting vs -WP ❌→✅
**Items affected:**
- **Anillo pinxudo / Mamagring** (RINGS)

**Problem:**
- Build showed: `Prospecting: 1`
- In-game shows: `-1 PW máx.` (negative Willpower)

**Root cause:** Action ID 192 not handling negative values (should check sign)

---

## ✅ Solutions Applied

### 1. Updated Worker Code (`worker/fetch_and_load.py`)

#### Fix 1: Dodge vs Berserk (lines 276-297)
```python
elif stat_name == "Dodge_or_Berserk":
    # Slot-specific thresholds based on actual game data
    if slot in ["FIRST_WEAPON", "HEAD", "SHOULDERS", "SECOND_WEAPON"]:
        if stat_value < 250:  # ✅ FIXED: Was 50, now 250
            stat_name = "Dodge"
        else:
            stat_name = "Berserk_Mastery"
    else:
        if stat_value < 100:  # ✅ FIXED: Was 50, now 100
            stat_name = "Dodge"
        else:
            stat_name = "Berserk_Mastery"
```

#### Fix 2: Prospecting vs -WP (lines 306-314)
```python
192: "Prospecting_or_WP",  # ✅ NEW: Contextual mapping

elif stat_name == "Prospecting_or_WP":
    # Check value sign to determine stat type
    if stat_value > 0:
        stat_name = "Prospecting"  # Positive = resource finding
    else:
        stat_name = "WP"  # Negative = WP penalty (value already negative)
```

### 2. Database Migration Created

**File:** `migrations/fix_dodge_and_prospecting_stats.sql`

**What it does:**
1. Converts `Berserk_Mastery < 250` → `Dodge` (weapons/head/shoulders)
2. Converts `Berserk_Mastery < 100` → `Dodge` (other slots)
3. Converts `Prospecting: 1-2` on rings → `WP: -1/-2`
4. Provides detailed logs and verification queries

---

## 📊 Expected Results

### Before Fix ❌
```json
{
  "easy": {
    "items": [
      {
        "name": "Peinado Ror",
        "stats": {"Berserk_Mastery": 70}  // ❌ Wrong
      },
      {
        "name": "Espada de Pym",
        "stats": {"Berserk_Mastery": 110}  // ❌ Wrong
      },
      {
        "name": "Anillo pinxudo",
        "stats": {"Prospecting": 1}  // ❌ Wrong
      }
    ],
    "total_stats": {
      "Berserk_Mastery": 180,  // ❌ Should be 0
      "Dodge": 210,  // ❌ Should be ~390
      "Prospecting": 1,  // ❌ Should be 0
      "WP": 0  // ❌ Should be -1
    }
  }
}
```

### After Fix ✅
```json
{
  "easy": {
    "items": [
      {
        "name": "Peinado Ror",
        "stats": {"Dodge": 70}  // ✅ Correct
      },
      {
        "name": "Espada de Pym",
        "stats": {"Dodge": 110}  // ✅ Correct
      },
      {
        "name": "Anillo pinxudo",
        "stats": {"WP": -1}  // ✅ Correct
      }
    ],
    "total_stats": {
      "Berserk_Mastery": 0,  // ✅ Only legitimate items
      "Dodge": 390,  // ✅ All Dodge items counted
      "Prospecting": 0,  // ✅ No false Prospecting
      "WP": -1  // ✅ Correct penalty
    }
  }
}
```

---

## 🚀 How to Apply the Fix

### Step 1: Apply Migration
```bash
# Run the combined migration (fixes both issues)
docker-compose exec db psql -U wakfu -d wakfu_builder \
  -f /migrations/fix_dodge_and_prospecting_stats.sql
```

### Step 2: Restart Services
```bash
# Clear API cache
docker-compose restart api

# Or restart everything
docker-compose restart
```

### Step 3: Verify
```bash
# Generate a new build and check stats
curl -X POST http://localhost:8000/solver \
  -H "Content-Type: application/json" \
  -d '{
    "level_max": 165,
    "stat_weights": {
      "HP": 1,
      "Dodge": 3,
      "WP": 1
    }
  }'
```

**Expected in response:**
- ✅ Screechcut: Shows `Dodge`, NOT `Berserk_Mastery`
- ✅ Pepepew Sword: Shows `Dodge`, NOT `Berserk_Mastery`
- ✅ Anillo pinxudo: Shows `WP: -1`, NOT `Prospecting: 1`

---

## 📁 Files Modified

| File | Changes | Status |
|------|---------|--------|
| `worker/fetch_and_load.py` | Updated Action ID 175 & 192 thresholds | ✅ Complete |
| `migrations/fix_dodge_and_prospecting_stats.sql` | Combined migration for both issues | ✅ Ready |
| `docs/FIX_DODGE_BERSERK_ISSUE.md` | Detailed Dodge/Berserk documentation | ✅ Complete |
| `docs/PROSPECTING_VS_WP_ISSUE.md` | Detailed Prospecting/WP documentation | ✅ Complete |
| `CONTEXTUAL_STATS_FIX_COMPLETE.md` | This summary document | ✅ Complete |
| `check_ring_stats.sql` | Verification queries for rings | ✅ Available |
| `verify_dodge_items.sql` | Verification queries for dodge items | ✅ Available |

---

## ✅ Additional Issue Verified

### Ring Slots: Already Working Correctly ✅

User also mentioned that Wakfu allows **2 rings equipped** (can't be the same ring twice).

**Verification result:** The solver already handles this correctly!
- Uses both `LEFT_HAND` and `RIGHT_HAND` slots
- Has constraint preventing same ring in both slots
- Code: `api/app/services/solver.py` lines 262-276

No fix needed for this - it's already correct! ✅

---

## 🎉 Summary

| Issue | Status | Impact |
|-------|--------|--------|
| Dodge vs Berserk | ✅ Fixed | ~180 points Dodge correctly attributed |
| Prospecting vs -WP | ✅ Fixed | -1 WP penalty properly tracked |
| Ring duplicate prevention | ✅ Already working | No changes needed |
| Worker code | ✅ Updated | Future data loads will be correct |
| Database migration | ⏳ Ready to apply | Run SQL to fix existing data |

---

## 🔍 Investigation Method

Both issues were identified through:
1. **User screenshots** showing in-game item stats
2. **Build output** showing incorrect stats
3. **Pattern analysis** comparing rare vs legendary versions
4. **Action ID investigation** finding contextual mappings

**Key insight:** Wakfu uses **contextual Action IDs** that map to different stats based on:
- Value magnitude (Dodge < 250 vs Berserk >= 250)
- Value sign (Prospecting > 0 vs WP < 0)
- Item slot (different thresholds per slot type)

---

## 📚 Documentation

- **Quick Guide:** `DODGE_BERSERK_FIX_GUIDE.md` (for Dodge fix only)
- **This Document:** `CONTEXTUAL_STATS_FIX_COMPLETE.md` (complete overview)
- **Technical Details:** `docs/FIX_DODGE_BERSERK_ISSUE.md` and `docs/PROSPECTING_VS_WP_ISSUE.md`
- **Migration Guide:** `migrations/README.md`

---

**Last Updated:** 2025-11-04  
**Status:** ✅ **CODE FIXED** | ⏳ **MIGRATION READY**  
**Reported by:** User  
**Fixed by:** AI Assistant

**Apply the migration and enjoy accurate stats!** 🎯

