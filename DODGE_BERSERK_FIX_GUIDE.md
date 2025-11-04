# 🔧 Quick Fix Guide: Dodge vs Berserk_Mastery Issue

## ⚡ Quick Summary

**Problem:** Items showing **Berserk_Mastery** instead of **Dodge**  
**Cause:** Incorrect threshold in stat mapping logic  
**Status:** ✅ **FIX READY** - Waiting for application  

---

## 🎯 Affected Items Examples

### User Report (Level 165 Easy Build)
- **Peinado Ror / Screechcut** (HEAD)
  - ❌ Shows: Berserk_Mastery: 70
  - ✅ Should be: Dodge: 70

- **Espada de Pym / Pepepew Sword** (FIRST_WEAPON)
  - ❌ Shows: Berserk_Mastery: 110
  - ✅ Should be: Dodge: 110

**Note:** The legendary versions (shown in images) correctly display Dodge: 80 and Dodge: 170 respectively.

---

## 🚀 How to Apply the Fix (Choose ONE method)

### Method 1: SQL Migration (Recommended - Fast & Precise)

```bash
# Step 1: Run verification (optional - see what will change)
docker-compose exec db psql -U wakfu -d wakfu_builder -f /verify_dodge_items.sql

# Step 2: Apply the fix
docker-compose exec db psql -U wakfu -d wakfu_builder -f /migrations/fix_dodge_berserk_stats.sql

# Step 3: Restart API
docker-compose restart api

# Step 4: Verify fix worked
docker-compose exec db psql -U wakfu -d wakfu_builder -f /verify_dodge_items.sql
```

### Method 2: Reload Game Data (Slower but Complete)

```bash
# This will reload all items with the new threshold logic
docker-compose restart worker

# Wait for worker to finish loading (check logs)
docker-compose logs -f worker
```

---

## ✅ Verification

After applying the fix, verify it worked:

```bash
# Check specific items
docker-compose exec db psql -U wakfu -d wakfu_builder -c \
  "SELECT item_id, name_es, slot, rarity, 
          stats::jsonb->'Dodge' as dodge,
          stats::jsonb->'Berserk_Mastery' as berserk
   FROM items
   WHERE item_id IN (21218, 26638);"
```

**Expected output:**
```
 item_id |        name_es         | slot | rarity | dodge | berserk
---------+------------------------+------+--------+-------+---------
  21218  | Peinado Ror           | HEAD |   3    |  70   | null
  26638  | Espada de Pym, el Pío | FIRST_WEAPON | 3 | 110 | null
```

---

## 📊 Impact on Builds

### Before Fix
```json
{
  "total_stats": {
    "Berserk_Mastery": 180,  // ❌ Incorrectly includes Dodge items
    "Dodge": 210              // ❌ Missing Dodge from misclassified items
  }
}
```

### After Fix
```json
{
  "total_stats": {
    "Berserk_Mastery": 0,     // ✅ Only legitimate Berserk items (none in easy build)
    "Dodge": 390              // ✅ All Dodge items correctly counted
  }
}
```

---

## 📁 Files Modified

| File | Purpose | Status |
|------|---------|--------|
| `worker/fetch_and_load.py` | Fixed threshold logic (lines 276-297) | ✅ Updated |
| `migrations/fix_dodge_berserk_stats.sql` | SQL migration to fix DB | ✅ Ready |
| `verify_dodge_items.sql` | Verification queries | ✅ Ready |
| `docs/FIX_DODGE_BERSERK_ISSUE.md` | Detailed documentation | ✅ Complete |
| `docs/rarity_analysis/SUMMARY.md` | Updated with fix info | ✅ Updated |
| `migrations/README.md` | Migration guide | ✅ Complete |

---

## 🔍 Technical Details

### What Changed in Code

**OLD** threshold (incorrect):
```python
if stat_value < 50:
    stat_name = "Dodge"
else:
    stat_name = "Berserk_Mastery"
```

**NEW** threshold (correct):
```python
# Slot-specific thresholds
if slot in ["FIRST_WEAPON", "HEAD", "SHOULDERS", "SECOND_WEAPON"]:
    if stat_value < 250:
        stat_name = "Dodge"
    else:
        stat_name = "Berserk_Mastery"
else:
    if stat_value < 100:
        stat_name = "Dodge"
    else:
        stat_name = "Berserk_Mastery"
```

### Why These Thresholds?

Based on analysis of item stats in images:
- **Dodge** values range: 10 to 200+ (weapons can have 170+)
- **Berserk_Mastery** values: Typically 250+ when it appears
- **Different slots** have different typical ranges

---

## 🎮 Test the Fix

Generate a new build and check stats:

```bash
# Example API request
curl -X POST http://localhost:8000/solver \
  -H "Content-Type: application/json" \
  -d '{
    "level_max": 165,
    "stat_weights": {
      "HP": 1,
      "Dodge": 3,
      "Distance_Mastery": 2
    }
  }'
```

Check the response for:
- ✅ Items should show **Dodge**, not Berserk_Mastery
- ✅ Total Dodge stat should be higher
- ✅ Berserk_Mastery should be 0 or only appear on legitimate items

---

## ❓ Troubleshooting

### "psql: command not found"
The database isn't running or you're not using Docker.

**Solution:**
```bash
# Start the database
docker-compose up -d db

# Verify it's running
docker-compose ps
```

### "No such file or directory"
Path to migration file is incorrect.

**Solution:**
```bash
# Use absolute path in container
docker cp migrations/fix_dodge_berserk_stats.sql wakfu-builder-assistant-db-1:/tmp/
docker-compose exec db psql -U wakfu -d wakfu_builder -f /tmp/fix_dodge_berserk_stats.sql
```

### Changes not visible in frontend
API cache needs to be cleared.

**Solution:**
```bash
# Restart API
docker-compose restart api

# Or restart everything
docker-compose restart
```

---

## 📚 Additional Documentation

- **Full technical details:** `docs/FIX_DODGE_BERSERK_ISSUE.md`
- **Migration instructions:** `migrations/README.md`
- **Project summary:** `docs/rarity_analysis/SUMMARY.md`

---

## ✨ Summary

| Aspect | Details |
|--------|---------|
| **Problem** | Dodge > 50 incorrectly classified as Berserk_Mastery |
| **Solution** | Updated thresholds: 250 for weapons/head, 100 for others |
| **Fix Type** | Code update + SQL migration |
| **Downtime** | None (migration runs in < 1 second) |
| **Risk** | Very low (only fixes incorrect data) |
| **Reversible** | Yes (reload game data if needed) |

---

**Last Updated:** 2025-11-04  
**Status:** ✅ **READY TO APPLY**

Apply the fix and enjoy accurate Dodge stats! 🎯

