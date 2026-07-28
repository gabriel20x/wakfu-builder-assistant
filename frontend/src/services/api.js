/**
 * Local (backend-less) implementation of the old REST API.
 *
 * Every function keeps the exact same name and axios-like `{ data }` response
 * shape the components already consume, but resolves everything locally:
 *  - static gamedata JSON (frontend/public/data/, built by scripts/build_static_data.py)
 *  - MILP solver running in a Web Worker (frontend/src/lib/solver/)
 *  - damage calculator and class presets ported to JS (frontend/src/lib/)
 *  - manual metadata edits persisted in localStorage (dataStore overlay)
 */

import {
  loadItems,
  loadMeta,
  getItemById,
  getItemsByIds,
  getEffectiveMetadata,
  getAllEffectiveMetadata,
  setMetadataOverride,
  deleteMetadataOverride,
  withEffectiveMetadata,
} from './dataStore'
import { solveBuildInWorker } from './localSolver'
import {
  estimateDamage,
  calculateWithCustomResistances,
  calculateDetailed,
} from '../lib/damage/damageCalculator'
import {
  listAllClasses,
  listRolesForClass,
  getClassPreset,
  getClassDetails,
  ROLE_TEMPLATES,
} from '../lib/presets/classPresets'

const ok = (data) => ({ data })

const BUILD_HISTORY_KEY = 'wakfu_build_history_v1'

function readBuildHistory() {
  try {
    return JSON.parse(localStorage.getItem(BUILD_HISTORY_KEY)) || []
  } catch {
    return []
  }
}

function pushBuildHistory(params, result) {
  const history = readBuildHistory()
  history.unshift({
    id: Date.now(),
    params,
    result,
    created_at: new Date().toISOString(),
  })
  localStorage.setItem(BUILD_HISTORY_KEY, JSON.stringify(history.slice(0, 20)))
}

export const builderAPI = {
  async solveBuild(params) {
    const result = await solveBuildInWorker(params)
    try {
      pushBuildHistory(
        { level_max: params.level_max, stat_weights: params.stat_weights },
        result
      )
    } catch {
      /* localStorage full — history is best-effort */
    }
    return ok(result)
  },

  async getBuildHistory(limit = 10) {
    return ok(readBuildHistory().slice(0, limit))
  },

  async refreshItems(itemIds) {
    const items = await getItemsByIds(itemIds)
    return ok({
      items: items.map((item) => ({
        item_id: item.item_id,
        name: item.name,
        name_es: item.name_es,
        name_en: item.name_en,
        name_fr: item.name_fr,
        level: item.level,
        slot: item.slot,
        rarity: item.rarity,
        is_epic: item.is_epic,
        is_relic: item.is_relic,
        difficulty: item.difficulty,
        gfx_id: item.gfx_id,
        stats: item.stats,
        source_type: item.source_type,
        has_gem_slot: item.has_gem_slot,
        drop_sources: item.drop_sources,
        metadata: getEffectiveMetadata(item),
      })),
    })
  },

  async getItems(filters = {}) {
    const all = await loadItems()
    let result = all
    if (filters.level_min != null) result = result.filter((i) => i.level >= filters.level_min)
    if (filters.level_max != null) result = result.filter((i) => i.level <= filters.level_max)
    if (filters.slot) result = result.filter((i) => i.slot === filters.slot)
    if (filters.source_type) result = result.filter((i) => i.source_type === filters.source_type)
    return ok(result.slice(0, filters.limit || 100))
  },

  async getItem(itemId) {
    const item = await getItemById(Number(itemId))
    if (!item) throw apiError(404, 'Item not found')
    return ok(item)
  },
}

export const presetsAPI = {
  async getClasses() {
    return ok(listAllClasses())
  },

  async getClassRoles(className) {
    return ok(listRolesForClass(className))
  },

  async getClassPreset(className, role = null) {
    // Returns the full `/preset` endpoint shape (incl. fallback for unknown class)
    return ok(getClassPreset(className, role))
  },

  async getRoleTemplates() {
    return ok(ROLE_TEMPLATES)
  },

  async getClassDetails(className) {
    return ok(getClassDetails(className))
  },
}

export const damageAPI = {
  async estimateDamage(buildStats, options = {}) {
    return ok(
      estimateDamage(buildStats, {
        baseSpellDamage: options.baseSpellDamage || 100.0,
        resistancePresets: options.resistancePresets || [0, 100, 200, 300, 400, 500],
        includeCritical: options.includeCritical !== false,
        isMelee: options.isMelee !== false,
      })
    )
  },

  async calculateWithCustomResistances(buildStats, enemyResistances, baseSpellDamage = 100.0) {
    return ok(calculateWithCustomResistances(buildStats, enemyResistances, baseSpellDamage))
  },

  async calculateDetailed(params) {
    return ok(calculateDetailed(params))
  },
}

export const metadataAPI = {
  async getAllMetadata() {
    const data = await getAllEffectiveMetadata()
    return ok({ success: true, message: 'Metadata retrieved successfully', data })
  },

  async getMetadataStats() {
    const [items, doc] = await Promise.all([loadItems(), getAllEffectiveMetadata()])
    const entries = Object.values(doc.items)
    const enabled = (entry, method) =>
      entry?.acquisition_methods?.[method]?.enabled ? 1 : 0
    const count = (method) => entries.reduce((acc, e) => acc + enabled(e, method), 0)
    const total = items.length
    return ok({
      success: true,
      message: 'Statistics retrieved',
      data: {
        total_items_in_game: total,
        total_items_with_metadata: entries.length,
        coverage_percent: total > 0 ? Math.round((entries.length / total) * 10000) / 100 : 0,
        items_with_drop: count('drop'),
        items_with_recipe: count('recipe'),
        items_with_fragments: count('fragments'),
        items_with_crupier: count('crupier'),
        items_with_challenge: count('challenge_reward'),
        last_updated: doc.last_updated,
      },
    })
  },

  async searchItemsForMetadata(query) {
    const items = await loadItems()
    const q = String(query).toLowerCase()
    const matches = items
      .filter(
        (i) =>
          (i.name && i.name.toLowerCase().includes(q)) ||
          (i.name_es && i.name_es.toLowerCase().includes(q)) ||
          (i.name_en && i.name_en.toLowerCase().includes(q))
      )
      .slice(0, 50)
    const results = matches.map((item) => {
      const metadata = getEffectiveMetadata(item)
      return {
        item_id: item.item_id,
        name: item.name,
        name_es: item.name_es,
        name_en: item.name_en,
        level: item.level,
        rarity: item.rarity,
        slot: item.slot,
        source_type: item.source_type,
        has_metadata: Object.keys(metadata).length > 0,
        metadata,
      }
    })
    return ok({
      success: true,
      message: `Found ${results.length} items`,
      data: { items: results },
    })
  },

  async getItemMetadata(itemId) {
    const item = await getItemById(Number(itemId))
    if (!item) throw apiError(404, 'Item not found in database')
    return ok({
      success: true,
      message: 'Item metadata retrieved successfully',
      data: {
        item_id: item.item_id,
        name: item.name,
        name_es: item.name_es,
        name_en: item.name_en,
        level: item.level,
        rarity: item.rarity,
        slot: item.slot,
        source_type: item.source_type,
        difficulty: item.difficulty,
        metadata: getEffectiveMetadata(item),
      },
    })
  },

  async updateItemMetadata(itemId, metadata) {
    const item = await getItemById(Number(itemId))
    if (!item) throw apiError(404, 'Item not found in database')
    const entry = {
      ...metadata,
      item_id: Number(itemId),
      name: item.name,
      added_date: metadata.added_date || new Date().toISOString(),
    }
    setMetadataOverride(itemId, entry)
    return ok({
      success: true,
      message: `Metadata updated for item ${itemId}`,
      data: entry,
    })
  },

  async deleteItemMetadata(itemId) {
    deleteMetadataOverride(itemId)
    return ok({
      success: true,
      message: `Metadata deleted for item ${itemId}`,
      data: null,
    })
  },
}

export const gamedataAPI = {
  async getMonsterTypes() {
    const meta = await loadMeta()
    return ok({
      types: meta.monster_types || [],
      counts: meta.monster_type_counts || {},
    })
  },

  async getGamedataStatus() {
    const meta = await loadMeta()
    return ok({
      version: meta.gamedata_version,
      status: meta.status || 'completed',
      loaded_items: meta.item_count,
      created_at: null,
    })
  },
}

/** Axios-compatible error so existing `err.response?.data?.detail` keeps working. */
function apiError(status, detail) {
  const err = new Error(detail)
  err.response = { status, data: { detail } }
  return err
}

export default {
  ...builderAPI,
  ...presetsAPI,
  ...damageAPI,
  ...metadataAPI,
  ...gamedataAPI,
}
