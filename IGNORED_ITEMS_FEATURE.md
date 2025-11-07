# Ignored Items Feature

## Overview
The Ignored Items feature allows users to exclude specific items from future build searches. This is useful for managing user preferences and filtering out items they don't want to use.

## Features

### 1. **Ignore/Unignore Items**
- Users can click a ban button (🚫) on any item card to add it to the ignored list
- Ignored items turn green (✓) and can be restored by clicking again
- Ignored items are stored in browser localStorage for persistence

### 2. **Ignored Items Manager**
- Visual component showing all ignored items
- Displays item name, level, slot, rarity, and when it was ignored
- Allows restoring individual items or clearing the entire list
- Export/Import functionality for backing up preferences

### 3. **API Integration**
- Ignored item IDs are sent with each build request
- Server-side filtering removes ignored items from the search pool
- Logged in server output for debugging

## Technical Implementation

### Frontend Components

#### 1. `useIgnoredItems.js` (Composable)
Located: `frontend/src/composables/useIgnoredItems.js`

**Exports:**
- `ignoredItems` - Array of ignored item objects
- `ignoredItemIds` - Array of item IDs (for API)
- `ignoredItemsCount` - Number of ignored items
- `ignoreItem(item)` - Add item to ignored list
- `unignoreItem(itemId)` - Remove item from ignored list
- `isItemIgnored(itemId)` - Check if item is ignored
- `toggleItemIgnored(item)` - Toggle ignore state
- `clearAllIgnoredItems()` - Remove all ignored items
- `exportIgnoredItems()` - Export as JSON
- `importIgnoredItems(data)` - Import from JSON

**Storage:**
- Uses localStorage key: `wakfu_builder_ignored_items`
- Data persists across browser sessions

#### 2. `IgnoredItemsManager.vue` (Component)
Located: `frontend/src/components/IgnoredItemsManager.vue`

**Features:**
- Lists all ignored items with metadata
- Individual restore buttons
- Clear all button (with confirmation)
- Export to JSON file
- Import from JSON file
- Empty state with helpful instructions

#### 3. `ItemCard.vue` (Modified)
Located: `frontend/src/components/ItemCard.vue`

**Added:**
- Ban/Unban button (top-right, next to edit button)
- Red (🚫) when not ignored, Green (✓) when ignored
- Emits `item-ignored` and `item-restored` events
- New prop: `showIgnoreButton` (default: true)

#### 4. `BuildGenerator.vue` (Modified)
Located: `frontend/src/components/BuildGenerator.vue`

**Changes:**
- Imports `useIgnoredItems` composable
- Imports `IgnoredItemsManager` component
- Passes `ignored_item_ids` to API call
- Displays IgnoredItemsManager in config panel

### Backend Changes

#### 1. `solver.py` (Router)
Located: `api/app/routers/solver.py`

**Modified:**
- `SolveRequest` model now accepts `ignored_item_ids: List[int] = []`
- Passes ignored_item_ids to `solve_build()` service

#### 2. `solver.py` (Service)
Located: `api/app/services/solver.py`

**Modified:**
- `solve_build()` function accepts `ignored_item_ids` parameter
- Filters out ignored items from database query:
  ```python
  if ignored_item_ids and len(ignored_item_ids) > 0:
      query = query.filter(~Item.item_id.in_(ignored_item_ids))
  ```
- Logs ignored item count in filter info

### Translations

#### Added to `useI18n.js`
Located: `frontend/src/composables/useI18n.js`

All Spanish translations for:
- `ignoredItems.title` - "Items Ignorados"
- `ignoredItems.description` - Component description
- `ignoredItems.ignore` - "Ignorar item"
- `ignoredItems.unignore` - "Permitir item"
- `ignoredItems.restore` - "Restaurar"
- `ignoredItems.clearAll` - "Limpiar Todo"
- And 10+ more translation keys

## Usage Examples

### For Users

#### Ignoring an Item
1. Generate a build
2. Find an item you don't want to use
3. Click the red ban button (🚫) on the item card
4. Item is now ignored and won't appear in future searches

#### Restoring an Item
1. Scroll to "Items Ignorados" section in config panel
2. Find the item you want to restore
3. Click the green "Restaurar" button
4. Item will now appear in future searches

#### Export/Import
1. **Export**: Click "Exportar" to download JSON file with ignored items
2. **Import**: Click "Importar" and select a previously exported JSON file
3. Useful for backing up preferences or sharing with other devices

### For Developers

#### Using the Composable
```javascript
import { useIgnoredItems } from '@/composables/useIgnoredItems'

const { 
  ignoredItems,           // ref<Array>
  ignoredItemIds,         // computed<number[]>
  ignoredItemsCount,      // computed<number>
  ignoreItem,             // (item: Object) => boolean
  unignoreItem,           // (itemId: number) => boolean
  isItemIgnored,          // (itemId: number) => boolean
  toggleItemIgnored       // (item: Object) => boolean
} = useIgnoredItems()

// Check if item is ignored
if (isItemIgnored(12345)) {
  console.log('Item is ignored')
}

// Toggle ignore state
const nowIgnored = toggleItemIgnored(item)
console.log(nowIgnored ? 'Now ignored' : 'Now allowed')
```

#### API Request Format
```javascript
const response = await builderAPI.solveBuild({
  level_max: 230,
  stat_weights: { HP: 1.0, AP: 2.5 },
  include_pet: true,
  include_accessory: true,
  only_droppable: false,
  damage_preferences: ['Fire', 'Water', 'Earth', 'Air'],
  resistance_preferences: ['Fire', 'Water', 'Earth', 'Air'],
  ignored_item_ids: [12345, 67890, 11111]  // <-- New parameter
})
```

## Data Structure

### Ignored Item Object
```javascript
{
  item_id: 12345,                          // number
  name: "Corona del Ogro",                 // string
  level: 215,                              // number
  slot: "HEAD",                            // string
  rarity: 7,                               // number
  ignored_at: "2024-11-07T12:34:56.789Z"  // ISO timestamp
}
```

### LocalStorage Format
```json
{
  "12345": {
    "item_id": 12345,
    "name": "Corona del Ogro",
    "level": 215,
    "slot": "HEAD",
    "rarity": 7,
    "ignored_at": "2024-11-07T12:34:56.789Z"
  },
  "67890": {
    "item_id": 67890,
    "name": "Anillo de Otomai",
    "level": 200,
    "slot": "LEFT_HAND",
    "rarity": 5,
    "ignored_at": "2024-11-07T12:35:12.345Z"
  }
}
```

## Files Modified

### Frontend
- ✅ `frontend/src/composables/useIgnoredItems.js` (NEW)
- ✅ `frontend/src/components/IgnoredItemsManager.vue` (NEW)
- ✅ `frontend/src/components/ItemCard.vue` (MODIFIED)
- ✅ `frontend/src/components/BuildGenerator.vue` (MODIFIED)
- ✅ `frontend/src/composables/useI18n.js` (MODIFIED)

### Backend
- ✅ `api/app/routers/solver.py` (MODIFIED)
- ✅ `api/app/services/solver.py` (MODIFIED)

## Testing Checklist

### Frontend
- [ ] Can ignore an item from ItemCard
- [ ] Ignored item shows green checkmark
- [ ] Can restore item from ItemCard
- [ ] IgnoredItemsManager displays all ignored items
- [ ] Can restore individual items from manager
- [ ] Clear all button works with confirmation
- [ ] Export downloads JSON file
- [ ] Import loads JSON file
- [ ] Data persists after page reload
- [ ] Translations display correctly

### Backend
- [ ] API accepts ignored_item_ids parameter
- [ ] Ignored items are excluded from results
- [ ] Server logs show ignored count
- [ ] Builds generate correctly with ignored items
- [ ] Empty ignored list works (no errors)

### Integration
- [ ] Ignored items don't appear in Easy build
- [ ] Ignored items don't appear in Medium build
- [ ] Ignored items don't appear in Hard builds
- [ ] Ignored items don't appear in Full build
- [ ] Restoring items makes them appear again
- [ ] Multiple builds with different ignore lists work

## Future Enhancements

### Possible Improvements
1. **Ignore by Category**: Ignore all items of a certain rarity or slot
2. **Temporary Ignore**: Set expiration time for ignored items
3. **Cloud Sync**: Sync ignored items across devices (requires backend)
4. **Ignore Reasons**: Add notes explaining why items are ignored
5. **Search/Filter**: Search within ignored items list
6. **Bulk Operations**: Select multiple items to ignore/restore at once
7. **Undo/Redo**: Undo recent ignore actions
8. **Statistics**: Show how many times builds were affected by ignores

## Known Limitations

1. **Browser-Only Storage**: Ignored items are stored in localStorage, not synced across devices
2. **No Server Persistence**: If localStorage is cleared, ignored items are lost
3. **Item Updates**: If an item's name changes in game data, ignored list shows old name
4. **No Search**: Large ignore lists may be hard to navigate
5. **Performance**: Very large ignore lists (1000+ items) may slow down UI slightly

## Support

For issues or feature requests, please contact the development team or create an issue in the project repository.

