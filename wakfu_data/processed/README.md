## Processed Data

This folder contains curated datasets derived from the raw community dumps.  
Currently the only artifact is `monsters_metadata.json`, which aggregates:

- Monster IDs that appear in `monsterDrops.json`
- Localised monster names (FR / EN / ES / PT) extracted from the old community scrap files
- Family metadata (using `monsterFamilies.json`)
- Minimum / maximum level ranges
- `gfx_id` placeholder (initially `null`)
- A note listing the item IDs that reference the monster in the scrap data

### Regenerating `monsters_metadata.json`

1. Restore the source dumps under `wakfu_data/gamedata_1.90.1.43/community-data/`:
   - `en_monsters_stats_data.json`
   - `monsterFamilies.json`
   - `ScrapData_items/*.json` (if you need to rebuild language mappings or item references)
2. From the project root run:

   ```bash
   python worker/create_monster_metadata.py
   ```

   The script writes the consolidated file to `wakfu_data/processed/monsters_metadata.json` and prints a summary of missing or ambiguous entries.

3. Once regenerated, the heavy community dumps can be removed again—the processed file is what the rest of the project uses.

If you later obtain the official `graphicParameters.gfxId` list, update `worker/create_monster_metadata.py` to fill the `gfx_id` field (currently `null`).*** End Patch

