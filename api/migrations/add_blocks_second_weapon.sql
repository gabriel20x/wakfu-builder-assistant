-- Add blocks_second_weapon column to items table
-- This column tracks if a weapon is 2H and blocks SECOND_WEAPON slot

ALTER TABLE items
ADD COLUMN IF NOT EXISTS blocks_second_weapon BOOLEAN DEFAULT FALSE;

-- Create index for faster queries
CREATE INDEX IF NOT EXISTS idx_items_blocks_second_weapon 
ON items(blocks_second_weapon);

-- Update existing 2H weapons if any data is already loaded
-- This will be handled by the worker on next data load

