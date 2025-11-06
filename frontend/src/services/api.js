import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
})

export const builderAPI = {
  // Generate builds based on stat weights
  solveBuild(params) {
    return api.post('/build/solve', params)
  },

  // Get build history
  getBuildHistory(limit = 10) {
    return api.get(`/build/history?limit=${limit}`)
  },

  // Refresh items with latest data from database
  refreshItems(itemIds) {
    return api.post('/build/refresh-items', { item_ids: itemIds })
  },

  // Get items with filters
  getItems(filters = {}) {
    const params = new URLSearchParams()
    if (filters.level_min) params.append('level_min', filters.level_min)
    if (filters.level_max) params.append('level_max', filters.level_max)
    if (filters.slot) params.append('slot', filters.slot)
    if (filters.source_type) params.append('source_type', filters.source_type)
    if (filters.limit) params.append('limit', filters.limit)
    
    return api.get(`/items?${params.toString()}`)
  },

  // Get single item
  getItem(itemId) {
    return api.get(`/items/${itemId}`)
  },
}

export const presetsAPI = {
  // Get all available classes
  getClasses() {
    return api.get('/presets/classes')
  },

  // Get roles for a specific class
  getClassRoles(className) {
    return api.get(`/presets/classes/${className}/roles`)
  },

  // Get preset for a class and role
  getClassPreset(className, role = null) {
    const params = role ? `?role=${role}` : ''
    return api.get(`/presets/classes/${className}/preset${params}`)
  },

  // Get base role templates
  getRoleTemplates() {
    return api.get('/presets/roles')
  },

  // Get complete class details
  getClassDetails(className) {
    return api.get(`/presets/classes/${className}`)
  },
}

export const damageAPI = {
  // Estimate damage for a build at different resistance levels
  estimateDamage(buildStats, options = {}) {
    return api.post('/damage/estimate', {
      build_stats: buildStats,
      base_spell_damage: options.baseSpellDamage || 100.0,
      resistance_presets: options.resistancePresets || [0, 100, 200, 300, 400, 500],
      include_critical: options.includeCritical !== false,
      is_melee: options.isMelee !== false  // Default to melee
    })
  },

  // Calculate damage with custom enemy resistances
  calculateWithCustomResistances(buildStats, enemyResistances, baseSpellDamage = 100.0) {
    return api.post('/damage/custom-resistances', {
      build_stats: buildStats,
      enemy_resistances: enemyResistances,
      base_spell_damage: baseSpellDamage
    })
  },

  // Calculate damage with detailed parameters
  calculateDetailed(params) {
    return api.post('/damage/calculate', params)
  },
}

export const metadataAPI = {
  // Get all metadata
  getAllMetadata() {
    return api.get('/item-metadata/all')
  },

  // Get metadata statistics
  getMetadataStats() {
    return api.get('/item-metadata/stats')
  },

  // Search items for metadata editing
  searchItemsForMetadata(query) {
    return api.get(`/item-metadata/search?query=${encodeURIComponent(query)}`)
  },

  // Get metadata for a specific item
  getItemMetadata(itemId) {
    return api.get(`/item-metadata/item/${itemId}`)
  },

  // Update/create metadata for an item
  updateItemMetadata(itemId, metadata) {
    return api.post(`/item-metadata/item/${itemId}`, metadata)
  },

  // Delete metadata for an item
  deleteItemMetadata(itemId) {
    return api.delete(`/item-metadata/item/${itemId}`)
  },
}

export default {
  ...builderAPI,
  ...presetsAPI,
  ...damageAPI,
  ...metadataAPI,
  // Keep the axios instance for custom calls
  get: api.get.bind(api),
  post: api.post.bind(api),
  put: api.put.bind(api),
  delete: api.delete.bind(api),
}

