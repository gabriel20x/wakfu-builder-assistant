-- Check Mamagring / Anillo pinxudo stats across all rarities
-- To verify Prospecting vs -WP issue

\echo '==================================================================='
\echo 'MAMAGRING / ANILLO PINXUDO STATS VERIFICATION'
\echo '==================================================================='
\echo ''

-- 1. Find all Mamagring items
\echo '1. ALL MAMAGRING / ANILLO PINXUDO ITEMS'
\echo '-------------------------------------------------------------------'

SELECT 
    item_id,
    COALESCE(name_es, name) as name,
    slot,
    level,
    CASE rarity
        WHEN 1 THEN 'Blanco'
        WHEN 2 THEN 'Verde'
        WHEN 3 THEN 'Amarillo'
        WHEN 4 THEN 'Naranja'
        WHEN 5 THEN 'Rosa'
        WHEN 6 THEN 'Reliquia'
        WHEN 7 THEN 'Épico'
        WHEN 8 THEN 'Sonámbulo'
        ELSE CAST(rarity AS TEXT)
    END as rarity,
    stats::jsonb->'Prospecting' as prospecting,
    stats::jsonb->'WP' as wp,
    stats::jsonb->'HP' as hp,
    stats::jsonb->'Lock' as lock,
    stats::jsonb->'Dodge' as dodge
FROM items
WHERE (name_es ILIKE '%pinxudo%' 
    OR name_es ILIKE '%mamagring%'
    OR name ILIKE '%mamagring%'
    OR name ILIKE '%poutreux%')
    AND slot IN ('LEFT_HAND', 'RIGHT_HAND')
ORDER BY level, rarity;

\echo ''
\echo '-------------------------------------------------------------------'
\echo ''

-- 2. Check raw data for one of these items to see action IDs
\echo '2. RAW DATA FOR MAMAGRING (Level 165-170)'
\echo '-------------------------------------------------------------------'

SELECT 
    item_id,
    COALESCE(name_es, name) as name,
    level,
    CASE rarity
        WHEN 1 THEN 'Blanco'
        WHEN 2 THEN 'Verde'
        WHEN 3 THEN 'Amarillo'
        WHEN 4 THEN 'Naranja'
        WHEN 5 THEN 'Rosa'
        WHEN 6 THEN 'Reliquia'
        WHEN 7 THEN 'Épico'
        WHEN 8 THEN 'Sonámbulo'
        ELSE CAST(rarity AS TEXT)
    END as rarity,
    raw_data::jsonb->'definition'->'equipEffects' as equip_effects
FROM items
WHERE (name_es ILIKE '%pinxudo%' 
    OR name_es ILIKE '%mamagring%'
    OR name ILIKE '%mamagring%'
    OR name ILIKE '%poutreux%')
    AND slot IN ('LEFT_HAND', 'RIGHT_HAND')
    AND level BETWEEN 165 AND 170
ORDER BY level, rarity
LIMIT 3;

\echo ''
\echo '-------------------------------------------------------------------'
\echo ''

-- 3. Find all rings with Prospecting
\echo '3. ALL RINGS WITH PROSPECTING (Level 160-170)'
\echo '-------------------------------------------------------------------'

SELECT 
    item_id,
    COALESCE(name_es, name) as name,
    level,
    CASE rarity
        WHEN 1 THEN 'Blanco'
        WHEN 2 THEN 'Verde'
        WHEN 3 THEN 'Amarillo'
        WHEN 4 THEN 'Naranja'
        WHEN 5 THEN 'Rosa'
        WHEN 6 THEN 'Reliquia'
        WHEN 7 THEN 'Épico'
        WHEN 8 THEN 'Sonámbulo'
        ELSE CAST(rarity AS TEXT)
    END as rarity,
    stats::jsonb->'Prospecting' as prospecting,
    stats::jsonb->'WP' as wp
FROM items
WHERE slot IN ('LEFT_HAND', 'RIGHT_HAND')
    AND stats::jsonb ? 'Prospecting'
    AND level BETWEEN 160 AND 170
ORDER BY level DESC, rarity DESC;

\echo ''
\echo '-------------------------------------------------------------------'
\echo ''

-- 4. Find rings with negative WP (if any)
\echo '4. RINGS WITH NEGATIVE WP (if any exist in DB)'
\echo '-------------------------------------------------------------------'

SELECT 
    item_id,
    COALESCE(name_es, name) as name,
    level,
    CASE rarity
        WHEN 1 THEN 'Blanco'
        WHEN 2 THEN 'Verde'
        WHEN 3 THEN 'Amarillo'
        WHEN 4 THEN 'Naranja'
        WHEN 5 THEN 'Rosa'
        WHEN 6 THEN 'Reliquia'
        WHEN 7 THEN 'Épico'
        WHEN 8 THEN 'Sonámbulo'
        ELSE CAST(rarity AS TEXT)
    END as rarity,
    stats::jsonb->'WP' as wp
FROM items
WHERE slot IN ('LEFT_HAND', 'RIGHT_HAND')
    AND stats::jsonb ? 'WP'
    AND (stats::jsonb->>'WP')::numeric < 0
ORDER BY level DESC;

\echo ''
\echo '==================================================================='
\echo ''
\echo 'EXPECTED:'
\echo '  - Mamagring legendary: Should have -1 WP, NOT Prospecting'
\echo '  - If showing Prospecting instead, it's a mapping error'
\echo ''
\echo '==================================================================='

