-- Migration: Add blocks_second_weapon field to items table
-- Date: 2025-11-02
-- Purpose: Improve 2H weapon detection using equipmentItemTypes.json data

-- Add column if it doesn't exist
ALTER TABLE items 
ADD COLUMN IF NOT EXISTS blocks_second_weapon BOOLEAN DEFAULT FALSE;

-- Create index for better query performance
CREATE INDEX IF NOT EXISTS idx_items_blocks_second_weapon 
ON items(blocks_second_weapon);

-- Set blocks_second_weapon = true for existing 2H weapons (based on old heuristic)
-- This will be properly updated when worker runs again with new detection logic
UPDATE items 
SET blocks_second_weapon = TRUE
WHERE slot = 'FIRST_WEAPON' 
  AND raw_data::jsonb->'definition'->'item'->'useParameters'->>'useCostAp'::text::int >= 4;

-- Verify migration
SELECT COUNT(*) as two_handed_weapons 
FROM items 
WHERE blocks_second_weapon = TRUE;

