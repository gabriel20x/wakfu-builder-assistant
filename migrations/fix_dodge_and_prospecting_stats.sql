-- Fix two contextual stat mapping issues:
-- 1. Dodge vs Berserk_Mastery (Action ID 175)
-- 2. Prospecting vs -WP (Action ID 192)
--
-- Issue 1: Items with Berserk_Mastery that should be Dodge
-- - Screechcut/Peinado Ror (HEAD): 70 Berserk → 70 Dodge
-- - Pepepew Sword/Espada de Pym (FIRST_WEAPON): 110 Berserk → 110 Dodge
-- - Other items in weapon/head/shoulders slots with Berserk < 250
--
-- Issue 2: Items with Prospecting that should be -WP
-- - Mamagring/Anillo pinxudo (RINGS): Prospecting: 1 → WP: -1
-- - Other rings with low Prospecting values that are actually -WP
--
-- Date: 2025-11-04

\echo '==================================================================='
\echo 'FIXING DODGE/BERSERK AND PROSPECTING/WP ISSUES'
\echo '==================================================================='
\echo ''

-- Create a temporary function to fix both issues
CREATE OR REPLACE FUNCTION fix_contextual_stats() RETURNS void AS $$
DECLARE
    item_record RECORD;
    new_stats jsonb;
    old_value numeric;
    new_value numeric;
    fixes_count integer := 0;
BEGIN
    \echo '-------------------------------------------------------------------'
    \echo 'PART 1: FIXING DODGE vs BERSERK_MASTERY'
    \echo '-------------------------------------------------------------------'
    
    -- Fix items with Berserk_Mastery < 250 in weapon/head/shoulders slots
    FOR item_record IN 
        SELECT item_id, name, name_es, slot, level, rarity, stats
        FROM items
        WHERE slot IN ('HEAD', 'FIRST_WEAPON', 'SHOULDERS', 'SECOND_WEAPON')
        AND stats::jsonb ? 'Berserk_Mastery'
        AND (stats::jsonb->>'Berserk_Mastery')::numeric < 250
    LOOP
        old_value := (item_record.stats::jsonb->>'Berserk_Mastery')::numeric;
        
        -- Get current Dodge value (if exists)
        IF item_record.stats::jsonb ? 'Dodge' THEN
            new_value := (item_record.stats::jsonb->>'Dodge')::numeric + old_value;
        ELSE
            new_value := old_value;
        END IF;
        
        -- Create new stats with Berserk_Mastery removed and Dodge added/updated
        new_stats := item_record.stats::jsonb;
        new_stats := new_stats - 'Berserk_Mastery';
        new_stats := jsonb_set(new_stats, '{Dodge}', to_jsonb(new_value));
        
        -- Update the item
        UPDATE items
        SET stats = new_stats::json
        WHERE item_id = item_record.item_id;
        
        fixes_count := fixes_count + 1;
        
        RAISE NOTICE 'Fixed item % (%, %, Lvl %, Rarity %): Berserk % → Dodge %',
            item_record.item_id,
            COALESCE(item_record.name_es, item_record.name),
            item_record.slot,
            item_record.level,
            item_record.rarity,
            old_value,
            new_value;
    END LOOP;
    
    -- Fix items with Berserk_Mastery < 100 in other slots
    FOR item_record IN 
        SELECT item_id, name, name_es, slot, level, rarity, stats
        FROM items
        WHERE slot NOT IN ('HEAD', 'FIRST_WEAPON', 'SHOULDERS', 'SECOND_WEAPON')
        AND stats::jsonb ? 'Berserk_Mastery'
        AND (stats::jsonb->>'Berserk_Mastery')::numeric < 100
    LOOP
        old_value := (item_record.stats::jsonb->>'Berserk_Mastery')::numeric;
        
        IF item_record.stats::jsonb ? 'Dodge' THEN
            new_value := (item_record.stats::jsonb->>'Dodge')::numeric + old_value;
        ELSE
            new_value := old_value;
        END IF;
        
        new_stats := item_record.stats::jsonb;
        new_stats := new_stats - 'Berserk_Mastery';
        new_stats := jsonb_set(new_stats, '{Dodge}', to_jsonb(new_value));
        
        UPDATE items
        SET stats = new_stats::json
        WHERE item_id = item_record.item_id;
        
        fixes_count := fixes_count + 1;
        
        RAISE NOTICE 'Fixed item % (%, %, Lvl %, Rarity %): Berserk % → Dodge %',
            item_record.item_id,
            COALESCE(item_record.name_es, item_record.name),
            item_record.slot,
            item_record.level,
            item_record.rarity,
            old_value,
            new_value;
    END LOOP;
    
    RAISE NOTICE 'Part 1 complete: Fixed % items (Dodge/Berserk)', fixes_count;
    fixes_count := 0;
    
    \echo ''
    \echo '-------------------------------------------------------------------'
    \echo 'PART 2: FIXING PROSPECTING vs -WP'
    \echo '-------------------------------------------------------------------'
    
    -- Fix items with Prospecting that should be -WP
    -- Heuristic: Prospecting value of 1-2 on rings is likely -WP
    -- (Legitimate Prospecting is usually higher, like 5-10+)
    FOR item_record IN 
        SELECT item_id, name, name_es, slot, level, rarity, stats
        FROM items
        WHERE slot IN ('LEFT_HAND', 'RIGHT_HAND')
        AND stats::jsonb ? 'Prospecting'
        AND (stats::jsonb->>'Prospecting')::numeric <= 2
        AND (stats::jsonb->>'Prospecting')::numeric > 0
    LOOP
        old_value := (item_record.stats::jsonb->>'Prospecting')::numeric;
        new_value := -old_value;  -- Convert to negative WP
        
        -- Get current WP value (if exists)
        IF item_record.stats::jsonb ? 'WP' THEN
            new_value := (item_record.stats::jsonb->>'WP')::numeric + new_value;
        END IF;
        
        -- Create new stats with Prospecting removed and WP added/updated
        new_stats := item_record.stats::jsonb;
        new_stats := new_stats - 'Prospecting';
        new_stats := jsonb_set(new_stats, '{WP}', to_jsonb(new_value));
        
        -- Update the item
        UPDATE items
        SET stats = new_stats::json
        WHERE item_id = item_record.item_id;
        
        fixes_count := fixes_count + 1;
        
        RAISE NOTICE 'Fixed item % (%, %, Lvl %, Rarity %): Prospecting % → WP %',
            item_record.item_id,
            COALESCE(item_record.name_es, item_record.name),
            item_record.slot,
            item_record.level,
            item_record.rarity,
            old_value,
            new_value;
    END LOOP;
    
    RAISE NOTICE 'Part 2 complete: Fixed % items (Prospecting/WP)', fixes_count;
END;
$$ LANGUAGE plpgsql;

-- Execute the fix
SELECT fix_contextual_stats();

-- Drop the temporary function
DROP FUNCTION fix_contextual_stats();

\echo ''
\echo '==================================================================='
\echo 'SUMMARY: VERIFICATION QUERIES'
\echo '==================================================================='
\echo ''

-- Show specific items mentioned in user reports
\echo 'Specific items from user report:'
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
        ELSE CAST(rarity AS TEXT)
    END as rarity,
    stats::jsonb->'Dodge' as dodge,
    stats::jsonb->'Berserk_Mastery' as berserk,
    stats::jsonb->'WP' as wp,
    stats::jsonb->'Prospecting' as prospecting
FROM items
WHERE item_id IN (
    21218, 26638,  -- Screechcut, Pepepew Sword (Rare)
    25849, 25850, 25851  -- Mamagring (various rarities)
)
OR name_es ILIKE '%peinado ror%'
OR name_es ILIKE '%espada de pym%'
OR name_es ILIKE '%pinxudo%'
OR name ILIKE '%mamagring%'
ORDER BY name, level, rarity;

\echo ''
\echo '-------------------------------------------------------------------'
\echo ''

-- Summary statistics
SELECT 
    'Items with Dodge' as stat_type,
    COUNT(*) as count,
    ROUND(AVG((stats::jsonb->>'Dodge')::numeric), 2) as avg_value
FROM items
WHERE stats::jsonb ? 'Dodge'

UNION ALL

SELECT 
    'Items with Berserk_Mastery (legitimate)' as stat_type,
    COUNT(*) as count,
    ROUND(AVG((stats::jsonb->>'Berserk_Mastery')::numeric), 2) as avg_value
FROM items
WHERE stats::jsonb ? 'Berserk_Mastery'

UNION ALL

SELECT 
    'Items with negative WP' as stat_type,
    COUNT(*) as count,
    ROUND(AVG((stats::jsonb->>'WP')::numeric), 2) as avg_value
FROM items
WHERE stats::jsonb ? 'WP' AND (stats::jsonb->>'WP')::numeric < 0

UNION ALL

SELECT 
    'Items with Prospecting' as stat_type,
    COUNT(*) as count,
    ROUND(AVG((stats::jsonb->>'Prospecting')::numeric), 2) as avg_value
FROM items
WHERE stats::jsonb ? 'Prospecting';

\echo ''
\echo '==================================================================='
\echo 'EXPECTED RESULTS:'
\echo '  - Screechcut (21218): Dodge ✓, NO Berserk'
\echo '  - Pepepew Sword (26638): Dodge ✓, NO Berserk'
\echo '  - Mamagring rings: WP: -1 ✓, NO Prospecting'
\echo '  - Berserk_Mastery count: Should be very low (only legitimate items)'
\echo '==================================================================='

