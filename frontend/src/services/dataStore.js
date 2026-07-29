/**
 * Local data store for the 100% static version.
 *
 * Loads the pre-generated gamedata (frontend/public/data/*.json, built by
 * scripts/build_static_data.py) and exposes lookups previously served by the
 * FastAPI backend. Manual item-metadata edits are kept as a localStorage
 * overlay on top of the baked-in metadata.
 */

const METADATA_OVERLAY_KEY = 'wakfu_item_metadata_overrides_v1'

let itemsPromise = null
let metaPromise = null
let itemsById = null
let runesPromise = null
let sublimationsPromise = null

const baseUrl = import.meta.env.BASE_URL || '/'

async function fetchJson(path) {
  const res = await fetch(`${baseUrl}${path}`.replace('//', '/'))
  if (!res.ok) {
    throw new Error(`Failed to load ${path}: ${res.status}`)
  }
  return res.json()
}

export function loadItems() {
  if (!itemsPromise) {
    itemsPromise = fetchJson('data/items.json').then((items) => {
      itemsById = new Map(items.map((i) => [i.item_id, i]))
      return items
    })
  }
  return itemsPromise
}

export function loadMeta() {
  if (!metaPromise) {
    metaPromise = fetchJson('data/meta.json')
  }
  return metaPromise
}

/** Runas de encantamiento, indexadas por id además de la lista ordenada. */
export function loadRunes() {
  if (!runesPromise) {
    runesPromise = fetchJson('data/runes.json').then((doc) => {
      const runes = doc.runes || []
      return { runes, runesById: Object.fromEntries(runes.map((r) => [r.id, r])) }
    })
  }
  return runesPromise
}

/** Sublimaciones, separadas en normales (con patrón de colores) y épicas/relicarias. */
export function loadSublimations() {
  if (!sublimationsPromise) {
    sublimationsPromise = fetchJson('data/sublimations.json').then((doc) => {
      const all = doc.sublimations || []
      return {
        all,
        byId: Object.fromEntries(all.map((s) => [s.id, s])),
        normal: all.filter((s) => s.pattern.length > 0),
        epic: all.filter((s) => s.is_epic),
        relic: all.filter((s) => s.is_relic),
      }
    })
  }
  return sublimationsPromise
}

export async function getItemById(itemId) {
  await loadItems()
  return itemsById.get(itemId) || null
}

export async function getItemsByIds(itemIds) {
  await loadItems()
  return itemIds.map((id) => itemsById.get(id)).filter(Boolean)
}

// ---------------------------------------------------------------------------
// Metadata overlay (manual edits, persisted in localStorage)
// ---------------------------------------------------------------------------

function readOverlay() {
  try {
    return JSON.parse(localStorage.getItem(METADATA_OVERLAY_KEY)) || { items: {} }
  } catch {
    return { items: {} }
  }
}

function writeOverlay(overlay) {
  localStorage.setItem(METADATA_OVERLAY_KEY, JSON.stringify(overlay))
}

/** Effective metadata for an item: overlay wins; `null` marks a deletion. */
export function getEffectiveMetadata(item) {
  const overlay = readOverlay()
  const key = String(item.item_id)
  if (Object.prototype.hasOwnProperty.call(overlay.items, key)) {
    return overlay.items[key] === null ? {} : overlay.items[key]
  }
  return item.metadata || {}
}

export function setMetadataOverride(itemId, metadata) {
  const overlay = readOverlay()
  overlay.items[String(itemId)] = metadata
  overlay.last_updated = new Date().toISOString()
  writeOverlay(overlay)
  return metadata
}

export function deleteMetadataOverride(itemId) {
  const overlay = readOverlay()
  overlay.items[String(itemId)] = null
  overlay.last_updated = new Date().toISOString()
  writeOverlay(overlay)
}

export function hasMetadataOverride(itemId) {
  const overlay = readOverlay()
  return Object.prototype.hasOwnProperty.call(overlay.items, String(itemId))
}

/**
 * Full metadata document, mirroring the old item_metadata.json structure
 * ({version, last_updated, items: {id: {...}}}) with the overlay applied.
 */
export async function getAllEffectiveMetadata() {
  const items = await loadItems()
  const overlay = readOverlay()
  const result = {}
  for (const item of items) {
    const key = String(item.item_id)
    let meta
    if (Object.prototype.hasOwnProperty.call(overlay.items, key)) {
      meta = overlay.items[key]
      if (meta === null) continue
    } else {
      meta = item.metadata
    }
    if (meta && Object.keys(meta).length > 0) {
      result[key] = meta
    }
  }
  return {
    version: '1.0.0',
    last_updated: overlay.last_updated || null,
    description: 'Manual metadata for items not provided by Wakfu game data',
    items: result,
  }
}

/** Item with the metadata overlay applied (as the old API served it). */
export function withEffectiveMetadata(item) {
  const metadata = getEffectiveMetadata(item)
  return { ...item, metadata }
}

/** Export the effective metadata as a downloadable item_metadata.json. */
export async function exportMetadataFile() {
  const doc = await getAllEffectiveMetadata()
  const blob = new Blob([JSON.stringify(doc, null, 2)], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = 'item_metadata.json'
  a.click()
  URL.revokeObjectURL(url)
}
