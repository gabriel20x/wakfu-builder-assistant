import { ref, computed } from 'vue'
import { loadRunes, loadSublimations } from '../services/dataStore'
import {
  emptyItemEnchantment,
  sumRuneStats,
  MAX_RUNE_SLOTS,
  RUNE_COLORS,
} from '../lib/enchantments'

/**
 * Estado de encantamientos (engarces) por build.
 *
 * Cada build tiene su propio conjunto de engarces, indexado por la clave de
 * build (`buildKey`), que combina el id de la build guardada con el tier
 * mostrado (easy/medium/full/...), ya que cada tier equipa objetos distintos.
 *
 * Forma persistida:
 *   { [buildKey]: {
 *       slots: { [slot]: { runes: [{color, runeId, level}], subId } },
 *       epicSubId, relicSubId
 *   } }
 */

const STORAGE_KEY = 'wakfu_enchantments_v1'

const enchantments = ref({})
const runeCatalog = ref({ runes: [], runesById: {} })
const sublimationCatalog = ref({ all: [], byId: {}, normal: [], epic: [], relic: [] })
const catalogsLoaded = ref(false)
let catalogPromise = null

function load() {
  try {
    const stored = localStorage.getItem(STORAGE_KEY)
    if (stored) enchantments.value = JSON.parse(stored)
  } catch (error) {
    console.error('Error loading enchantments:', error)
    enchantments.value = {}
  }
}

function persist() {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(enchantments.value))
  } catch (error) {
    console.error('Error saving enchantments:', error)
  }
}

load()

/** Clave estable para un (build, tier). Las builds sin guardar usan 'current'. */
export function buildKeyFor(buildId, tier) {
  return `${buildId || 'current'}::${tier || 'full'}`
}

function ensureBuild(key) {
  if (!enchantments.value[key]) {
    enchantments.value[key] = { slots: {}, epicSubId: null, relicSubId: null }
  }
  return enchantments.value[key]
}

function ensureSlot(key, slot, slotCount = MAX_RUNE_SLOTS) {
  const build = ensureBuild(key)
  if (!build.slots[slot]) {
    build.slots[slot] = emptyItemEnchantment(slotCount)
  }
  return build.slots[slot]
}

export function useEnchantments() {
  /** Carga los catálogos estáticos de runas y sublimaciones (una sola vez). */
  const loadCatalogs = () => {
    if (!catalogPromise) {
      catalogPromise = Promise.all([loadRunes(), loadSublimations()])
        .then(([runes, subs]) => {
          runeCatalog.value = runes
          sublimationCatalog.value = subs
          catalogsLoaded.value = true
        })
        .catch((error) => {
          console.error('Error loading enchantment catalogs:', error)
          catalogPromise = null
        })
    }
    return catalogPromise
  }

  const getBuildEnchantments = (key) => enchantments.value[key] || null

  const getSlotEnchantment = (key, slot) =>
    enchantments.value[key]?.slots?.[slot] || emptyItemEnchantment()

  /** Colores actuales de los 4 engarces de un objeto. */
  const getSlotColors = (key, slot) =>
    getSlotEnchantment(key, slot).runes.map((r) => r.color)

  const setRuneColor = (key, slot, index, color) => {
    if (index < 0 || index >= MAX_RUNE_SLOTS) return
    const entry = ensureSlot(key, slot)
    entry.runes[index].color = color
    persist()
  }

  const setRune = (key, slot, index, runeId, level = 1) => {
    if (index < 0 || index >= MAX_RUNE_SLOTS) return
    const entry = ensureSlot(key, slot)
    const rune = runeCatalog.value.runesById[runeId]
    entry.runes[index].runeId = runeId
    entry.runes[index].level = level
    // La runa fija el color del engarce (en el juego el color debe coincidir)
    if (rune) entry.runes[index].color = rune.color
    persist()
  }

  const setRuneLevel = (key, slot, index, level) => {
    if (index < 0 || index >= MAX_RUNE_SLOTS) return
    const entry = ensureSlot(key, slot)
    entry.runes[index].level = level
    persist()
  }

  const clearRune = (key, slot, index) => {
    if (index < 0 || index >= MAX_RUNE_SLOTS) return
    const entry = ensureSlot(key, slot)
    entry.runes[index] = { color: RUNE_COLORS.WHITE, runeId: null, level: 1 }
    persist()
  }

  const setSublimation = (key, slot, subId) => {
    const entry = ensureSlot(key, slot)
    entry.subId = subId
    persist()
  }

  const setSpecialSublimation = (key, kind, subId) => {
    const build = ensureBuild(key)
    if (kind === 'epic') build.epicSubId = subId
    else build.relicSubId = subId
    persist()
  }

  const clearBuildEnchantments = (key) => {
    delete enchantments.value[key]
    persist()
  }

  /** Estadísticas aportadas por todas las runas de la build. */
  const getRuneStats = (key) => {
    const build = enchantments.value[key]
    if (!build) return {}
    return sumRuneStats(build.slots, runeCatalog.value.runesById)
  }

  /**
   * Sublimaciones activas de la build: las de objeto cuya secuencia de colores
   * encaja, más la épica y la relicaria.
   */
  const getActiveSublimations = (key) => {
    const build = enchantments.value[key]
    if (!build) return []
    const byId = sublimationCatalog.value.byId
    const active = []

    Object.entries(build.slots).forEach(([slot, entry]) => {
      const sub = entry.subId ? byId[entry.subId] : null
      if (sub) active.push({ ...sub, slot })
    })
    if (build.epicSubId && byId[build.epicSubId]) {
      active.push({ ...byId[build.epicSubId], slot: 'EPIC' })
    }
    if (build.relicSubId && byId[build.relicSubId]) {
      active.push({ ...byId[build.relicSubId], slot: 'RELIC' })
    }
    return active
  }

  /** Cuenta cuántas veces se repite cada sublimación (para el límite de stacks). */
  const getSublimationStacks = (key) => {
    const stacks = {}
    getActiveSublimations(key).forEach((sub) => {
      stacks[sub.id] = (stacks[sub.id] || 0) + (sub.state_level || 1)
    })
    return stacks
  }

  /** ¿Hay algún engarce configurado en esta build? */
  const hasEnchantments = (key) => {
    const build = enchantments.value[key]
    if (!build) return false
    if (build.epicSubId || build.relicSubId) return true
    return Object.values(build.slots).some(
      (entry) => entry.subId || entry.runes.some((r) => r.runeId)
    )
  }

  /** Copia los engarces de una clave a otra (al guardar una build sin nombre). */
  const copyEnchantments = (fromKey, toKey) => {
    const source = enchantments.value[fromKey]
    if (!source) return
    enchantments.value[toKey] = JSON.parse(JSON.stringify(source))
    persist()
  }

  return {
    // Estado
    enchantments,
    runes: computed(() => runeCatalog.value.runes),
    runesById: computed(() => runeCatalog.value.runesById),
    sublimations: computed(() => sublimationCatalog.value),
    catalogsLoaded,

    // Carga
    loadCatalogs,

    // Lectura
    getBuildEnchantments,
    getSlotEnchantment,
    getSlotColors,
    getRuneStats,
    getActiveSublimations,
    getSublimationStacks,
    hasEnchantments,

    // Escritura
    setRuneColor,
    setRune,
    setRuneLevel,
    clearRune,
    setSublimation,
    setSpecialSublimation,
    clearBuildEnchantments,
    copyEnchantments,
  }
}
