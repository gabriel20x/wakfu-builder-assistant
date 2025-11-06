-- Add gfx_id column to items table
-- This column stores the graphics ID from graphicParameters.gfxId
-- Used to display the correct item image

ALTER TABLE items
ADD COLUMN IF NOT EXISTS gfx_id INTEGER;

-- No index needed as this is only used for display, not for queries

-- Existing items will be updated with gfx_id on next data load
-- The worker will extract gfx_id from raw_data if needed


