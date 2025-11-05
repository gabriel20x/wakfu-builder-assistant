# Item Metadata Management Guide

## Overview

This system allows you to add extra information to items that is not provided by Wakfu's game data, such as:
- Drop rates (percentage)
- Corrected source type (if game data is wrong)
- Craftable flags
- Manual difficulty overrides
- Source notes and documentation

All metadata is stored in a separate JSON file (`wakfu_data/item_metadata.json`) and is automatically merged with item data when the worker loads items into the database.

## How It Works

### 1. Frontend Admin Interface

Access the metadata admin through the navigation tabs in the application:
- Click on "⚙️ Metadatos de Items" / "⚙️ Item Metadata"

**Features:**
- Search for items by name
- View current metadata statistics
- Add/edit metadata for any item
- Delete metadata when no longer needed
- See which items already have metadata

### 2. Metadata Fields

When editing an item, you can set:

| Field | Type | Description |
|-------|------|-------------|
| **Drop Rate (%)** | Number | Drop rate percentage (e.g., 2.5 for 2.5%) |
| **Is Craftable** | Boolean | Whether the item can be crafted |
| **Is Obtainable** | Boolean | Whether the item is still obtainable in-game |
| **Source Correction** | String | Override the detected source type (drop/recipe/harvest/special) |
| **Difficulty Override** | Number | Manual difficulty score override |
| **Source Notes** | Text | Free-form notes about how to obtain the item |
| **Added By** | String | Your name or identifier |

### 3. Example Use Cases

#### Example 1: Item with Drop Rate
**El Lumicetro** (shown in your screenshot):
- Drop Rate: 2%
- Source: Drop from Nox boss
- Rarity: 4 (Mythic)

To add this:
1. Search for "Lumicetro"
2. Click on the item
3. Fill in:
   - Drop Rate: 2
   - Source Notes: "Drops from Nox boss with 2% drop rate"
   - Added By: Your name
4. Click Save

#### Example 2: Craftable Item
**Amuleto de Zora** (shown in your screenshot):
- This should be marked as craftable if it's part of a recipe set

To verify/correct:
1. Search for "Amuleto de Zora"
2. Click on the item
3. Check current source type
4. If incorrect, set:
   - Source Correction: "recipe"
   - Is Craftable: Yes
   - Source Notes: "Part of Zora set, crafted at Jeweler"
5. Click Save

### 4. Data Format

The metadata is stored in `wakfu_data/item_metadata.json`:

```json
{
  "version": "1.0.0",
  "last_updated": "2025-11-05T...",
  "description": "Manual metadata for items...",
  "items": {
    "12345": {
      "item_id": 12345,
      "name": "Item Name",
      "drop_rate_percent": 2.0,
      "is_craftable": false,
      "is_obtainable": true,
      "source_notes": "Drops from Boss X",
      "corrected_source_type": "drop",
      "manual_difficulty_override": null,
      "added_by": "Your Name",
      "added_date": "2025-11-05T..."
    }
  }
}
```

### 5. How Metadata is Applied

When the worker loads items into the database:

1. **Source Type Correction**: If `corrected_source_type` is set, it overrides the automatically detected source type
2. **Difficulty Override**: If `manual_difficulty_override` is set, it replaces the calculated difficulty score

This happens automatically every time you reload the data using the worker.

## Workflow

### Adding Metadata Before Deployment

Since you're not deploying yet, you can build up your metadata file:

1. **Identify Items**: Use the game or community resources to identify items with known drop rates or special sources
2. **Add Metadata**: Use the admin interface to add metadata for these items
3. **Save File**: The metadata is automatically saved to `wakfu_data/item_metadata.json`
4. **Version Control**: Commit this file to your git repository
5. **Reload Data**: When you want to test, restart the worker container to reload with new metadata

### Reloading Data with Metadata

To reload the database with updated metadata:

```bash
# Stop and remove worker container
docker-compose stop worker
docker-compose rm -f worker

# Delete the version entry to force reload
docker-compose exec db psql -U wakfu -d wakfu_builder -c "DELETE FROM gamedata_versions;"

# Start worker again
docker-compose up -d worker

# Check logs
docker-compose logs -f worker
```

## API Endpoints

The system exposes these API endpoints:

- `GET /api/item-metadata/all` - Get all metadata
- `GET /api/item-metadata/stats` - Get statistics
- `GET /api/item-metadata/search?query=<name>` - Search items
- `GET /api/item-metadata/item/{item_id}` - Get specific item metadata
- `POST /api/item-metadata/item/{item_id}` - Create/update metadata
- `DELETE /api/item-metadata/item/{item_id}` - Delete metadata

## Checking Recipe Data

To verify if an item like "Amuleto de Zora" is correctly identified as craftable:

1. Search for the item in the admin interface
2. Check the "Current Source" field
3. If it says "drop" but should be "recipe", add a correction:
   - Set "Source Correction" to "recipe"
   - Set "Is Craftable" to "Yes"
4. Save and reload data

The worker will pick up the correction and update the item's source type.

## Tips

1. **Search is Smart**: Search works across all language names (English, Spanish, French)
2. **Visual Indicators**: Items with existing metadata show a green badge
3. **Statistics**: The stats panel shows how many items have metadata
4. **Incremental**: You can add metadata gradually - no need to do all items at once
5. **Backup**: The JSON file is plain text and easy to backup/share

## Future Enhancements

Possible improvements you might want to add:
- Bulk import from CSV
- Community contributions
- Drop rate verification system
- Integration with Wakfu wiki data
- Recipe chain visualization

## Troubleshooting

**Metadata not appearing in database?**
- Make sure you've reloaded the worker after adding metadata
- Check that `item_metadata.json` exists in `wakfu_data/`
- Check worker logs for any errors loading metadata

**Can't find an item?**
- Try searching with different language names
- Check if the item is an equipment item (system only handles equipment)
- Verify the item exists in the game data

**Metadata file not saving?**
- Check file permissions on `wakfu_data/` directory
- Check API logs for errors
- Verify the API container can write to the mounted volume

