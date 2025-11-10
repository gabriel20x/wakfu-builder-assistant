import { ref, computed, watch } from 'vue'

const STORAGE_KEY = 'wakfu_builder_ignored_items'

// Global state
const ignoredItems = ref(new Map())

// Load from localStorage on init
const loadIgnoredItems = () => {
  try {
    const stored = localStorage.getItem(STORAGE_KEY)
    if (stored) {
      const parsed = JSON.parse(stored)
      ignoredItems.value = new Map(Object.entries(parsed))
    }
  } catch (error) {
    console.error('Error loading ignored items:', error)
    ignoredItems.value = new Map()
  }
}

// Save to localStorage
const saveIgnoredItems = () => {
  try {
    const obj = Object.fromEntries(ignoredItems.value)
    localStorage.setItem(STORAGE_KEY, JSON.stringify(obj))
  } catch (error) {
    console.error('Error saving ignored items:', error)
  }
}

// Initialize on first import
loadIgnoredItems()

/**
 * Composable for managing ignored items
 */
export function useIgnoredItems() {
  // Add item to ignored list
  const ignoreItem = (item) => {
    if (!item || !item.item_id) return false
    
    const itemData = {
      item_id: item.item_id,
      name: item.name || item.name_es || item.name_en || 'Unknown',
      level: item.level,
      slot: item.slot,
      rarity: item.rarity,
      ignored_at: new Date().toISOString()
    }
    
    ignoredItems.value.set(item.item_id.toString(), itemData)
    saveIgnoredItems()
    return true
  }
  
  // Remove item from ignored list
  const unignoreItem = (itemId) => {
    const id = itemId.toString()
    const existed = ignoredItems.value.has(id)
    ignoredItems.value.delete(id)
    if (existed) {
      saveIgnoredItems()
    }
    return existed
  }
  
  // Check if item is ignored
  const isItemIgnored = (itemId) => {
    return ignoredItems.value.has(itemId.toString())
  }
  
  // Get ignored item data
  const getIgnoredItem = (itemId) => {
    return ignoredItems.value.get(itemId.toString()) || null
  }
  
  // Get all ignored items as array
  const getAllIgnoredItems = computed(() => {
    return Array.from(ignoredItems.value.values())
      .sort((a, b) => {
        // Sort by ignored_at (most recent first)
        return new Date(b.ignored_at) - new Date(a.ignored_at)
      })
  })
  
  // Get ignored item IDs as array (for API)
  const getIgnoredItemIds = computed(() => {
    return Array.from(ignoredItems.value.keys()).map(id => parseInt(id))
  })
  
  // Get count of ignored items
  const ignoredItemsCount = computed(() => {
    return ignoredItems.value.size
  })
  
  // Clear all ignored items
  const clearAllIgnoredItems = () => {
    ignoredItems.value.clear()
    saveIgnoredItems()
  }
  
  // Toggle item ignored state
  const toggleItemIgnored = (item) => {
    if (isItemIgnored(item.item_id)) {
      unignoreItem(item.item_id)
      return false
    } else {
      ignoreItem(item)
      return true
    }
  }
  
  // Import ignored items from JSON
  const importIgnoredItems = (data) => {
    try {
      if (Array.isArray(data)) {
        // Array format: [{item_id, name, ...}, ...]
        data.forEach(item => {
          if (item.item_id) {
            ignoredItems.value.set(item.item_id.toString(), item)
          }
        })
      } else if (typeof data === 'object') {
        // Object format: {item_id: {data}, ...}
        Object.entries(data).forEach(([id, item]) => {
          ignoredItems.value.set(id.toString(), item)
        })
      }
      saveIgnoredItems()
      return true
    } catch (error) {
      console.error('Error importing ignored items:', error)
      return false
    }
  }
  
  // Export ignored items as JSON
  const exportIgnoredItems = () => {
    return getAllIgnoredItems.value
  }
  
  return {
    // State
    ignoredItems: getAllIgnoredItems,
    ignoredItemIds: getIgnoredItemIds,
    ignoredItemsCount,
    
    // Methods
    ignoreItem,
    unignoreItem,
    isItemIgnored,
    getIgnoredItem,
    toggleItemIgnored,
    clearAllIgnoredItems,
    importIgnoredItems,
    exportIgnoredItems
  }
}



