import { ref } from 'vue'

// Storage keys
// LAST_SEARCH_* are for builder generated results (type 1)
// SAVED_BUILDS are the user's saved builds (type 2)
const STORAGE_KEYS = {
  // New keys
  LAST_SEARCH_BUILD: 'wakfu_last_search_build',
  LAST_SEARCH_CONFIG: 'wakfu_last_search_config',
  SAVED_BUILDS: 'wakfu_saved_builds',
  // Backward-compatible legacy keys (read-only)
  LEGACY_CURRENT_BUILD: 'wakfu_current_build',
  LEGACY_CURRENT_CONFIG: 'wakfu_current_config'
}

const MAX_SAVED = 20

// Reactive state
const currentBuild = ref(null) // last generated (type 1)
const currentConfig = ref(null) // last generator config (type 1)
const savedBuilds = ref([])

// Initialize from localStorage
function initializePersistence() {
  try {
    // Load current/last search build (prefer new key, fallback to legacy)
    const storedBuild = localStorage.getItem(STORAGE_KEYS.LAST_SEARCH_BUILD)
      || localStorage.getItem(STORAGE_KEYS.LEGACY_CURRENT_BUILD)
    if (storedBuild) {
      currentBuild.value = JSON.parse(storedBuild)
    }

    // Load current/last search config (prefer new key, fallback to legacy)
    const storedConfig = localStorage.getItem(STORAGE_KEYS.LAST_SEARCH_CONFIG)
      || localStorage.getItem(STORAGE_KEYS.LEGACY_CURRENT_CONFIG)
    if (storedConfig) {
      currentConfig.value = JSON.parse(storedConfig)
    }

    // Load saved builds
    const storedSaved = localStorage.getItem(STORAGE_KEYS.SAVED_BUILDS)
    if (storedSaved) {
      savedBuilds.value = JSON.parse(storedSaved)
    }
  } catch (error) {
    console.error('Error loading persisted builds:', error)
  }
}

// Save last generated build (type 1). Do not use for previewing saved builds.
export function saveCurrentBuild(builds, config) {
  try {
    const buildData = {
      builds,
      config,
      timestamp: new Date().toISOString()
    }
    
    currentBuild.value = buildData
    localStorage.setItem(STORAGE_KEYS.LAST_SEARCH_BUILD, JSON.stringify(buildData))
  } catch (error) {
    console.error('Error saving current build:', error)
  }
}

// Save/merge last search config (when configuring or generating)
export function saveCurrentConfig(config) {
  try {
    const merged = {
      ...(currentConfig.value || {}),
      ...(config || {})
    }
    currentConfig.value = merged
    localStorage.setItem(STORAGE_KEYS.LAST_SEARCH_CONFIG, JSON.stringify(merged))
  } catch (error) {
    console.error('Error saving current config:', error)
  }
}

// Get current build
export function getCurrentBuild() {
  return currentBuild.value
}

// Get current config
export function getCurrentConfig() {
  return currentConfig.value
}

// Save a build with name (user saved builds)
export function saveBuildWithName(builds, config, name) {
  try {
    const buildData = {
      id: Date.now().toString(),
      name: name || `Build ${new Date().toLocaleString()}`,
      builds,
      config,
      saved_at: new Date().toISOString(),
      timestamp: new Date().toISOString()
    }
    
    savedBuilds.value.unshift(buildData)
    
    // Keep only MAX_SAVED
    if (savedBuilds.value.length > MAX_SAVED) {
      savedBuilds.value = savedBuilds.value.slice(0, MAX_SAVED)
    }
    
    localStorage.setItem(STORAGE_KEYS.SAVED_BUILDS, JSON.stringify(savedBuilds.value))
    
    return buildData
  } catch (error) {
    console.error('Error saving named build:', error)
    return null
  }
}

// Delete a saved build
export function deleteSavedBuild(buildId) {
  try {
    savedBuilds.value = savedBuilds.value.filter(b => b.id !== buildId)
    localStorage.setItem(STORAGE_KEYS.SAVED_BUILDS, JSON.stringify(savedBuilds.value))
  } catch (error) {
    console.error('Error deleting saved build:', error)
  }
}

// Rename a saved build
export function renameSavedBuild(buildId, newName) {
  try {
    const build = savedBuilds.value.find(b => b.id === buildId)
    if (build) {
      build.name = newName
      localStorage.setItem(STORAGE_KEYS.SAVED_BUILDS, JSON.stringify(savedBuilds.value))
    }
  } catch (error) {
    console.error('Error renaming saved build:', error)
  }
}

// Get saved builds
export function getSavedBuilds() {
  return savedBuilds.value
}

// Aliases for BuildViewer compatibility
export function getBuildHistory() {
  return getSavedBuilds()
}

export function deleteBuildFromHistory(buildId) {
  return deleteSavedBuild(buildId)
}

export function renameBuildInHistory(buildId, newName) {
  return renameSavedBuild(buildId, newName)
}

// Clear all persisted data
export function clearAllPersistence() {
  try {
    currentBuild.value = null
    currentConfig.value = null
    savedBuilds.value = []
    
    localStorage.removeItem(STORAGE_KEYS.LAST_SEARCH_BUILD)
    localStorage.removeItem(STORAGE_KEYS.LAST_SEARCH_CONFIG)
    localStorage.removeItem(STORAGE_KEYS.SAVED_BUILDS)
  } catch (error) {
    console.error('Error clearing persistence:', error)
  }
}

// Initialize on import
initializePersistence()

export function useBuildPersistence() {
  return {
    currentBuild,
    currentConfig,
    savedBuilds,
    saveCurrentBuild,
    saveCurrentConfig,
    getCurrentBuild,
    getCurrentConfig,
    saveBuildWithName,
    deleteSavedBuild,
    renameSavedBuild,
    getSavedBuilds,
    getBuildHistory,
    deleteBuildFromHistory,
    renameBuildInHistory,
    clearAllPersistence
  }
}

