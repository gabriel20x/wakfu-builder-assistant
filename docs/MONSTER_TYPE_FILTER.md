# Monster Type Filter Feature

## Overview
This feature allows users to filter items in build generation based on the types of monsters that drop them. Users can select which monster types (monster, boss, archmonster, ultimate_boss, dominant) to consider when generating builds.

## Changes Made

### 1. Database Schema
**File:** `migrations/add_monster_type.sql`
- Added `monster_type` column to `monsters` table
- Created index for efficient filtering
- Supports types: monster, boss, archmonster, ultimate_boss, dominant

### 2. Backend Models
**Files:** 
- `api/app/db/models.py`
- `worker/fetch_and_load.py`

Updated `Monster` model to include `monster_type` field:
```python
monster_type = Column(String, index=True, nullable=True)
```

### 3. Worker Script
**File:** `worker/fetch_and_load.py`

Modified monster loading logic to extract and store monster type from `monsters_metadata.json`:
```python
monster_type = monster_entry.get("type")
```

### 4. Backend API

#### New Endpoint
**File:** `api/app/routers/gamedata.py`

```python
@router.get("/monster-types")
async def get_monster_types(db: Session = Depends(get_db)):
    """Get available monster types from database"""
```

Returns:
```json
{
  "types": ["archmonster", "boss", "dominant", "monster", "ultimate_boss"],
  "counts": {
    "archmonster": 45,
    "boss": 89,
    "dominant": 12,
    "monster": 520,
    "ultimate_boss": 8
  }
}
```

#### Updated Solver
**Files:**
- `api/app/routers/solver.py`
- `api/app/services/solver.py`

Added `monster_types` parameter to `SolveRequest` and `solve_build`:
```python
monster_types: List[str] = []  # Filter items by monster types
```

The solver now filters items based on:
- Items that drop from selected monster types
- Non-drop items (craft, harvest) are still included unless `only_droppable` is True

### 5. Frontend

#### API Service
**File:** `frontend/src/services/api.js`

Added new `gamedataAPI` namespace:
```javascript
export const gamedataAPI = {
  getMonsterTypes() {
    return api.get('/gamedata/monster-types')
  }
}
```

#### New Component
**File:** `frontend/src/components/MonsterTypeFilter.vue`

Features:
- Displays all available monster types with counts
- Multi-select checkboxes with visual icons
- Select All / Deselect All quick actions
- Localized type names and icons
- Auto-selects all types by default

Type Icons:
- 👹 Monster
- 👑 Boss
- 💀 Archmonster
- 🔥 Ultimate Boss
- ⚔️ Dominant

#### Integration
**File:** `frontend/src/components/BuildGenerator.vue`

- Added `MonsterTypeFilter` component to config panel
- Added `selectedMonsterTypes` reactive ref
- Passes selected types to solver API

#### Translations
**File:** `frontend/src/composables/useI18n.js`

Added translations for:
- `monsterTypeFilter.title`
- `monsterTypeFilter.description`
- `monsterTypeFilter.selectAll`
- `monsterTypeFilter.deselectAll`
- `monsterTypeFilter.error`

Available in Spanish, English, and French.

## Usage

1. **Database Migration**
   ```bash
   # Run migration to add monster_type column
   psql -d wakfu_builder -f migrations/add_monster_type.sql
   ```

2. **Reload Monster Data**
   ```bash
   # Worker will automatically populate monster_type field
   cd worker
   python fetch_and_load.py
   ```

3. **Frontend Usage**
   - Navigate to Build Generator
   - Find "Filtro por Tipo de Monstruo" section
   - Select desired monster types
   - Generate builds - only items from selected monster types will be considered

## Technical Details

### Filter Logic
When monster types are selected:
1. Query all items that drop from monsters of selected types
2. If `only_droppable` is False: Also include non-drop items (craft, harvest, quest)
3. If `only_droppable` is True: Only include items from selected monster types

### Performance Considerations
- Monster type query uses indexed joins for efficiency
- Distinct item IDs are cached per request
- Filter is applied before solver algorithm runs

### Default Behavior
- If no monster types are selected, ALL types are considered (no filtering)
- Component auto-selects all types on mount for user convenience
- Empty selection = no filter applied

## Future Enhancements

Possible improvements:
1. Add monster family filter (e.g., only Gobballs, only Dragons)
2. Add level range filter for monsters
3. Show monster names that drop each item
4. Add preset filters (e.g., "Only Dungeon Bosses", "Only World Bosses")
5. Save monster type preferences per build preset

## Testing

To test the feature:
1. Ensure database has monster types populated
2. Select only "boss" monster type
3. Generate build - verify items are mostly boss drops
4. Compare with "Select All" to see difference in available items
