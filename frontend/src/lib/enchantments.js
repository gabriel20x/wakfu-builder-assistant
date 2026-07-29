/**
 * Sistema de encantamientos (engarces) de Wakfu.
 *
 * Cada objeto equipable tiene hasta 4 engarces. Cada engarce tiene un color
 * (1=rojo/ofensivo, 2=verde/soporte, 3=azul/defensivo, 0=blanco/comodín) y puede
 * llevar una runa de nivel 1-11 que aporta una estadística.
 *
 * Las sublimaciones son pergaminos que se activan cuando su secuencia de 3 colores
 * aparece en orden dentro de los 4 engarces del objeto. Sus efectos son
 * mayormente condicionales, por lo que se muestran como texto y no se suman al
 * cálculo de estadísticas.
 *
 * Datos generados por scripts/build_static_data.py:
 *   - public/data/runes.json
 *   - public/data/sublimations.json
 */

export const RUNE_COLORS = {
  WHITE: 0,
  RED: 1,
  GREEN: 2,
  BLUE: 3,
}

export const COLOR_ORDER = [
  RUNE_COLORS.RED,
  RUNE_COLORS.GREEN,
  RUNE_COLORS.BLUE,
  RUNE_COLORS.WHITE,
]

export const COLOR_META = {
  [RUNE_COLORS.WHITE]: { key: 'white', hex: '#d8dee9' },
  [RUNE_COLORS.RED]: { key: 'red', hex: '#f4574f' },
  [RUNE_COLORS.GREEN]: { key: 'green', hex: '#4fc46a' },
  [RUNE_COLORS.BLUE]: { key: 'blue', hex: '#43b6f0' },
}

export const MAX_RUNE_SLOTS = 4
export const MAX_RUNE_LEVEL = 11

/**
 * Slots que nunca admiten engarces, según el gamedata: todos sus objetos
 * traen `maximumShardSlotNumber: 0`. Se usa como respaldo para builds
 * guardadas antes de que el pipeline emitiera `shard_slots`.
 */
export const NON_ENCHANTABLE_SLOTS = [
  'SECOND_WEAPON',
  'ACCESSORY',
  'PET',
  'MOUNT',
  'COSTUME',
]

/**
 * Nº de engarces de un objeto. El gamedata lo trae por objeto: dentro de un
 * mismo slot hay piezas con 4 y piezas con 0 (relatos, objetos de evento…),
 * así que manda el dato del objeto y no su slot.
 */
export function itemShardSlots(item) {
  if (!item) return 0
  if (typeof item.shard_slots === 'number') return item.shard_slots
  // Builds guardadas antes de que el pipeline emitiera shard_slots
  return NON_ENCHANTABLE_SLOTS.includes(item.slot) ? 0 : MAX_RUNE_SLOTS
}

export function isEnchantableItem(item) {
  return itemShardSlots(item) > 0
}

/**
 * Nivel máximo de runa permitido por el nivel del objeto.
 * `levelRequirements[i]` es el nivel de objeto mínimo para la runa de nivel i+1.
 */
export function maxRuneLevelForItem(rune, itemLevel) {
  const requirements = rune?.level_requirements || []
  if (!requirements.length) return MAX_RUNE_LEVEL
  let max = 1
  requirements.forEach((required, index) => {
    if (itemLevel >= required) max = index + 1
  })
  return max
}

/**
 * Valor de la runa en un objeto concreto. Ankama duplica el bonus cuando la runa
 * se engarza en uno de sus dos slots afines (`double_bonus_slots`).
 */
export function runeValue(rune, level, itemSlot) {
  if (!rune || !level) return 0
  const base = rune.values[level - 1] || 0
  const doubled = itemSlot && rune.double_bonus_slots?.includes(itemSlot)
  return doubled ? base * 2 : base
}

/** El engarce blanco actúa como comodín para cualquier color exigido. */
function patternMatchesAt(colors, pattern, offset) {
  return pattern.every((required, index) => {
    const actual = colors[offset + index]
    return actual === required || actual === RUNE_COLORS.WHITE
  })
}

/**
 * ¿Puede activarse esta sublimación con los colores de engarce dados?
 * La secuencia de 3 colores debe aparecer en los engarces 1-3 o 2-4.
 */
export function canSublimationFit(slotColors, sublimation) {
  const pattern = sublimation?.pattern || []
  if (!pattern.length) return false
  const colors = Array.from({ length: MAX_RUNE_SLOTS }, (_, i) => slotColors?.[i])
  return (
    patternMatchesAt(colors, pattern, 0) ||
    patternMatchesAt(colors, pattern, 1)
  )
}

/**
 * Marcadores de icono que Ankama incrusta en los textos de estado.
 * Se sustituyen por un símbolo legible ya que no cargamos esos sprites.
 */
const ICON_PLACEHOLDERS = {
  img_water: '💧',
  img_fire: '🔥',
  img_earth: '🌿',
  img_air: '💨',
  img_physical: '⚔️',
  img_ecnbi: '◆',
  img_ecnbr: '◆',
  img_ally: '🛡️',
}

/**
 * Renderiza el efecto de una sublimación sustituyendo los `{num_N}` de la
 * plantilla por el valor correspondiente al nivel del estado.
 * Devuelve `[{text, indented}]`.
 */
export function renderSublimationEffect(sublimation, lang = 'es') {
  const lines = sublimation?.effect?.lines || []
  const level = sublimation?.state_level || 1
  return lines
    .map((line) => {
      let text = line.text?.[lang] || line.text?.en || ''
      if (line.nums) {
        Object.entries(line.nums).forEach(([key, perLevel]) => {
          const value = perLevel[level - 1] ?? perLevel[perLevel.length - 1] ?? 0
          text = text.replaceAll(`{${key}}`, value)
        })
      }
      Object.entries(ICON_PLACEHOLDERS).forEach(([key, symbol]) => {
        text = text.replaceAll(`{${key}}`, symbol)
      })
      // Ankama escapa los literales entre comillas simples: {'|'} es un "|"
      text = text.replace(/\{'(.*?)'\}/g, '$1').trim()
      return { text, indented: line.indented }
    })
    .filter((line) => line.text)
}

/**
 * Suma las estadísticas que aportan todas las runas de una build.
 * `enchantments` es `{ [slot]: { runes: [{runeId, color, level}], subId } }`.
 * Devuelve claves del vocabulario de useStats, con `Elemental_Mastery`
 * expandido a los cuatro elementos (así lo hace el juego con esa runa).
 */
export function sumRuneStats(enchantments, runesById) {
  const totals = {}
  const add = (stat, value) => {
    if (!value) return
    totals[stat] = (totals[stat] || 0) + value
  }

  Object.entries(enchantments || {}).forEach(([slot, entry]) => {
    ;(entry?.runes || []).forEach((slotState) => {
      if (!slotState?.runeId) return
      const rune = runesById?.[slotState.runeId]
      if (!rune) return
      const value = runeValue(rune, slotState.level, slot)
      if (rune.stat === 'Elemental_Mastery') {
        add('Water_Mastery', value)
        add('Air_Mastery', value)
        add('Earth_Mastery', value)
        add('Fire_Mastery', value)
        return
      }
      add(rune.stat, value)
    })
  })

  return totals
}

/** Estado inicial de los engarces de un objeto: slots blancos vacíos. */
export function emptyItemEnchantment(slots = MAX_RUNE_SLOTS) {
  return {
    runes: Array.from({ length: slots }, () => ({
      color: RUNE_COLORS.WHITE,
      runeId: null,
      level: 1,
    })),
    subId: null,
  }
}
