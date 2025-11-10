-- Add monster_type column to monsters table
-- This will store the type from monsters_metadata.json (monster, boss, archmonster, ultimate_boss, dominant)

ALTER TABLE monsters ADD COLUMN IF NOT EXISTS monster_type VARCHAR(50);

-- Create index for filtering
CREATE INDEX IF NOT EXISTS idx_monsters_type ON monsters(monster_type);

-- Update existing records to have null type (will be populated by worker script)
COMMENT ON COLUMN monsters.monster_type IS 'Type of monster: monster, boss, archmonster, ultimate_boss, dominant';
