-- Verification script to identify items affected by Dodge/Berserk misclassification
-- Run BEFORE applying the fix to see what will be changed
-- Run AFTER applying the fix to verify results

\echo '==================================================================='
\echo 'DODGE/BERSERK MISCLASSIFICATION VERIFICATION'
\echo '==================================================================='
\echo ''

-- 1. Items in weapon/head/shoulders slots with Berserk_Mastery < 250
\echo '1. Items in WEAPON/HEAD/SHOULDERS with Berserk_Mastery < 250'
\echo '   (These should likely be Dodge)'
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
    (stats::jsonb->>'Berserk_Mastery')::numeric as berserk_value
FROM items
WHERE slot IN ('HEAD', 'FIRST_WEAPON', 'SHOULDERS', 'SECOND_WEAPON')
    AND stats::jsonb ? 'Berserk_Mastery'
    AND (stats::jsonb->>'Berserk_Mastery')::numeric < 250
ORDER BY slot, level DESC, rarity DESC
LIMIT 20;

\echo ''
\echo '-------------------------------------------------------------------'
\echo ''

-- 2. Items in other slots with Berserk_Mastery < 100
\echo '2. Items in OTHER SLOTS with Berserk_Mastery < 100'
\echo '   (These might be Dodge)'
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
    (stats::jsonb->>'Berserk_Mastery')::numeric as berserk_value
FROM items
WHERE slot NOT IN ('HEAD', 'FIRST_WEAPON', 'SHOULDERS', 'SECOND_WEAPON')
    AND stats::jsonb ? 'Berserk_Mastery'
    AND (stats::jsonb->>'Berserk_Mastery')::numeric < 100
ORDER BY slot, level DESC, rarity DESC
LIMIT 20;

\echo ''
\echo '-------------------------------------------------------------------'
\echo ''

-- 3. Specific items mentioned in user report
\echo '3. SPECIFIC ITEMS MENTIONED IN USER REPORT'
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
    stats::jsonb->'Dodge' as dodge,
    stats::jsonb->'Berserk_Mastery' as berserk
FROM items
WHERE item_id IN (
    -- Screechcut / Peinado Ror
    21218, 21219, 21220, 21221, 21222,
    -- Pepepew Sword / Espada de Pym
    26638, 26639, 26640
)
OR name_es ILIKE '%peinado ror%'
OR name_es ILIKE '%espada de pym%'
OR name ILIKE '%screechcut%'
OR name ILIKE '%pepepew%'
ORDER BY name, rarity DESC;

\echo ''
\echo '-------------------------------------------------------------------'
\echo ''

-- 4. Summary statistics
\echo '4. SUMMARY STATISTICS'
\echo '-------------------------------------------------------------------'

WITH stats_summary AS (
    SELECT 
        'Total items' as category,
        COUNT(*) as count,
        NULL as avg_value
    FROM items
    
    UNION ALL
    
    SELECT 
        'Items with Dodge' as category,
        COUNT(*) as count,
        ROUND(AVG((stats::jsonb->>'Dodge')::numeric), 2) as avg_value
    FROM items
    WHERE stats::jsonb ? 'Dodge'
    
    UNION ALL
    
    SELECT 
        'Items with Berserk_Mastery' as category,
        COUNT(*) as count,
        ROUND(AVG((stats::jsonb->>'Berserk_Mastery')::numeric), 2) as avg_value
    FROM items
    WHERE stats::jsonb ? 'Berserk_Mastery'
    
    UNION ALL
    
    SELECT 
        'Items with Berserk < 250 (WEAPON/HEAD/SHOULDERS)' as category,
        COUNT(*) as count,
        ROUND(AVG((stats::jsonb->>'Berserk_Mastery')::numeric), 2) as avg_value
    FROM items
    WHERE slot IN ('HEAD', 'FIRST_WEAPON', 'SHOULDERS', 'SECOND_WEAPON')
        AND stats::jsonb ? 'Berserk_Mastery'
        AND (stats::jsonb->>'Berserk_Mastery')::numeric < 250
    
    UNION ALL
    
    SELECT 
        'Items with Berserk < 100 (OTHER SLOTS)' as category,
        COUNT(*) as count,
        ROUND(AVG((stats::jsonb->>'Berserk_Mastery')::numeric), 2) as avg_value
    FROM items
    WHERE slot NOT IN ('HEAD', 'FIRST_WEAPON', 'SHOULDERS', 'SECOND_WEAPON')
        AND stats::jsonb ? 'Berserk_Mastery'
        AND (stats::jsonb->>'Berserk_Mastery')::numeric < 100
)
SELECT * FROM stats_summary;

\echo ''
\echo '==================================================================='
\echo ''
\echo 'EXPECTED RESULTS AFTER FIX:'
\echo '  - Items with Berserk < 250/100: Should be 0 or very few'
\echo '  - Items with Dodge: Should increase significantly'
\echo '  - Specific items (21218, 26638): Should show Dodge, not Berserk'
\echo ''
\echo '==================================================================='

