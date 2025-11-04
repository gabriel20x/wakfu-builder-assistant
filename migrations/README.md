# Database Migrations

This folder contains SQL migration scripts for the Wakfu Builder database.

## Available Migrations

### 1. `add_blocks_second_weapon.sql`
Adds the `blocks_second_weapon` column to track two-handed weapons.

**Status:** ✅ Applied

### 2. `fix_dodge_and_prospecting_stats.sql` 
Fixes TWO contextual stat issues:
1. **Dodge vs Berserk_Mastery** (Action ID 175)
2. **Prospecting vs -WP** (Action ID 192)

**Status:** ⚠️ **PENDING - REQUIRES APPLICATION**

**Issue 1 - Dodge/Berserk:** Action ID 175 was using too low threshold (50), causing items with Dodge > 50 to be incorrectly classified as Berserk_Mastery.

**Issue 2 - Prospecting/WP:** Action ID 192 wasn't checking value sign, causing negative WP values to be stored as Prospecting.

**Affected items:**
- Screechcut/Peinado Ror (HEAD) - Berserk → Dodge
- Pepepew Sword/Espada de Pym (FIRST_WEAPON) - Berserk → Dodge
- Mamagring/Anillo pinxudo (RINGS) - Prospecting → -WP
- Other items with similar misclassifications

## How to Apply Migrations

### Using Docker (Recommended)

#### Option 1: Run SQL migration directly
```bash
# Copy migration to database container
docker cp migrations/fix_dodge_and_prospecting_stats.sql wakfu-builder-assistant-db-1:/tmp/

# Execute migration
docker-compose exec db psql -U wakfu -d wakfu_builder -f /tmp/fix_dodge_and_prospecting_stats.sql

# Restart API to clear cache
docker-compose restart api
```

#### Option 2: Use psql from host (if port is exposed)
```bash
psql -h localhost -p 5432 -U wakfu -d wakfu_builder -f migrations/fix_dodge_and_prospecting_stats.sql
```

#### Option 3: Interactive psql session
```bash
# Connect to database
docker-compose exec db psql -U wakfu -d wakfu_builder

# Copy and paste the migration SQL
\i /migrations/fix_dodge_and_prospecting_stats.sql
```

### Local Development

If running PostgreSQL locally:
```bash
psql -U wakfu -d wakfu_builder < migrations/fix_dodge_berserk_stats.sql
```

## Verification

After applying `fix_dodge_and_prospecting_stats.sql`, verify the changes:

```sql
-- Check specific items mentioned in the user report
SELECT item_id, name_es, name, slot, level, rarity, 
       stats::jsonb->'Dodge' as dodge,
       stats::jsonb->'Berserk_Mastery' as berserk,
       stats::jsonb->'WP' as wp,
       stats::jsonb->'Prospecting' as prospecting
FROM items
WHERE item_id IN (21218, 26638, 25849, 25850, 25851)
   OR name_es ILIKE '%peinado ror%'
   OR name_es ILIKE '%espada de pym%'
   OR name_es ILIKE '%pinxudo%'
   OR name ILIKE '%mamagring%';

-- Expected: 
-- - Screechcut/Pepepew: Should have Dodge, NOT Berserk_Mastery
-- - Mamagring: Should have WP: -1, NOT Prospecting
```

### Count items fixed
```sql
-- Count items with Dodge (should increase after fix)
SELECT 
    'Items with Dodge' as category,
    COUNT(*) as count
FROM items
WHERE stats::jsonb ? 'Dodge'
UNION ALL
-- Count items with Berserk_Mastery (should decrease, only legitimate ones remain)
SELECT 
    'Items with Berserk_Mastery' as category,
    COUNT(*) as count
FROM items
WHERE stats::jsonb ? 'Berserk_Mastery';
```

## Testing Builds After Migration

Generate a build with the affected items to verify:

```bash
# API Request
curl -X POST http://localhost:8000/solver \
  -H "Content-Type: application/json" \
  -d '{
    "level_max": 165,
    "stat_weights": {
      "HP": 1,
      "Dodge": 5
    }
  }'

# Check response for items with Dodge
```

## Rollback (if needed)

If you need to rollback the fix:

```sql
-- WARNING: This will revert the fixes, restoring incorrect classifications
-- Only use if you encounter issues and need to investigate

-- Better option: Reload all data from worker
-- The worker code has been fixed, so reloading will apply correct mappings
docker-compose restart worker
```

## Migration History

| Migration | Date | Status | Notes |
|-----------|------|--------|-------|
| `add_blocks_second_weapon.sql` | 2025-11-02 | ✅ Applied | Two-handed weapon support |
| `fix_dodge_and_prospecting_stats.sql` | 2025-11-04 | ⚠️ Pending | Fix Dodge/Berserk + Prospecting/WP |

## Creating New Migrations

When creating a new migration:

1. **Name format:** `description_of_change.sql`
2. **Include comments:** Explain what, why, and how
3. **Add verification queries:** Help users confirm the migration worked
4. **Update this README:** Add to migration history table
5. **Test locally first:** Always test before applying to production

### Migration Template

```sql
-- Description: What does this migration do?
-- Issue: Link to issue or explain the problem
-- Date: YYYY-MM-DD

-- Migration code here
...

-- Verification query
SELECT ...;
```

## Troubleshooting

### Migration fails with "permission denied"
```bash
# Ensure the file has correct permissions
chmod 644 migrations/fix_dodge_and_prospecting_stats.sql

# Or run as postgres superuser
docker-compose exec db psql -U postgres -d wakfu_builder -f /migrations/fix_dodge_and_prospecting_stats.sql
```

### "No such file or directory"
```bash
# Make sure you're in the project root
cd /path/to/wakfu-builder-assistant

# Verify file exists
ls -la migrations/

# Use absolute path
docker-compose exec db psql -U wakfu -d wakfu_builder -f /migrations/fix_dodge_and_prospecting_stats.sql
```

### Changes not reflected in API
```bash
# Restart API to clear any caching
docker-compose restart api

# Or restart all services
docker-compose restart
```

## Related Documentation

- **Complete Fix Guide:** `CONTEXTUAL_STATS_FIX_COMPLETE.md` (comprehensive overview)
- **Dodge/Berserk Details:** `docs/FIX_DODGE_BERSERK_ISSUE.md`
- **Prospecting/WP Details:** `docs/PROSPECTING_VS_WP_ISSUE.md`
- **Worker Script:** `worker/fetch_and_load.py` (lines 276-314)
- **Summary:** `docs/rarity_analysis/SUMMARY.md`

## Support

If you encounter issues:
1. Check the migration output for errors
2. Verify database connection: `docker-compose exec db psql -U wakfu -d wakfu_builder -c "\dt"`
3. Check logs: `docker-compose logs db`
4. See full documentation in `docs/FIX_DODGE_BERSERK_ISSUE.md`

