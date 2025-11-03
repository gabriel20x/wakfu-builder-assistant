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

export default api

