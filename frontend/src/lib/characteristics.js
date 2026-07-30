// Sistema de características (aptitudes) de Wakfu — v1.92
//
// IDs verificados contra el "Código de características" que exporta el propio
// juego (formato `id:puntos-id:puntos-...`), cruzando wakfu.wiki.gg, wakfuli.com
// y mikeshardmind/wakfu-utils (solver de wakforge.org).

export const SECTIONS = ['intelligence', 'strength', 'agility', 'chance', 'major']

const SECTION_INDEX = { intelligence: 0, strength: 1, agility: 2, chance: 3 }

export const MAJOR_LEVELS = [25, 75, 125, 175, 225]

export const MAX_CHARACTER_LEVEL = 245

// PA/PM que todo personaje tiene antes de equipo y aptitudes.
export const BASE_AP = 6
export const BASE_MP = 3

/**
 * PA/PM base de un personaje: los puntos innatos más los que aportan las
 * aptitudes mayores (majorAp / majorMp). Es el punto de partida sobre el que
 * el solver debe alcanzar un objetivo de PA/PM: el equipo solo tiene que
 * cubrir la diferencia.
 *
 * @param {Object} bonusStats - salida de allocationToBonusStats()
 * @returns {{AP: number, MP: number}}
 */
export function baseApMp(bonusStats = null) {
  return {
    AP: BASE_AP + (bonusStats?.AP || 0),
    MP: BASE_MP + (bonusStats?.MP || 0),
  }
}

// statsPerPoint usa las claves internas de useStats.js. Claves especiales que
// no existen como stat de equipo: HP_Percent, Armor_Percent, Barrier.
export const APTITUDES = [
  // Inteligencia
  { id: 1,  key: 'percentHp',      section: 'intelligence', cap: null, statsPerPoint: { HP_Percent: 4 }, emoji: '❤️' },
  { id: 16, key: 'elementalRes',   section: 'intelligence', cap: 10,   statsPerPoint: { Elemental_Resistance: 10 }, emoji: '🔰' },
  { id: 17, key: 'barrier',        section: 'intelligence', cap: 10,   statsPerPoint: { Barrier: 1 }, emoji: '🚧' },
  { id: 27, key: 'healsReceived',  section: 'intelligence', cap: 5,    statsPerPoint: { Heals_Received: 6 }, emoji: '💚' },
  { id: 36, key: 'armorHp',        section: 'intelligence', cap: 10,   statsPerPoint: { Armor_Percent: 4 }, emoji: '🩹' },

  // Fuerza
  { id: 23, key: 'elementalMastery', section: 'strength', cap: null, statsPerPoint: { Elemental_Mastery: 5 }, emoji: '🌈' },
  { id: 26, key: 'meleeMastery',     section: 'strength', cap: 40,   statsPerPoint: { Melee_Mastery: 8 }, emoji: '⚔️' },
  { id: 30, key: 'distanceMastery',  section: 'strength', cap: 40,   statsPerPoint: { Distance_Mastery: 8 }, emoji: '🏹' },
  { id: 31, key: 'hp',               section: 'strength', cap: null, statsPerPoint: { HP: 20 }, emoji: '❤️' },

  // Agilidad
  { id: 18, key: 'lock',         section: 'agility', cap: null, statsPerPoint: { Lock: 6 }, emoji: '🤜' },
  { id: 19, key: 'dodge',        section: 'agility', cap: null, statsPerPoint: { Dodge: 6 }, emoji: '💨' },
  { id: 20, key: 'initiative',   section: 'agility', cap: 20,   statsPerPoint: { Initiative: 4 }, emoji: '⚡' },
  { id: 21, key: 'lockAndDodge', section: 'agility', cap: null, statsPerPoint: { Lock: 4, Dodge: 4 }, emoji: '🤜' },
  { id: 37, key: 'forceOfWill',  section: 'agility', cap: 20,   statsPerPoint: { Force_Of_Will: 1 }, emoji: '🧠' },

  // Suerte
  { id: 9,  key: 'criticalHit',        section: 'chance', cap: 20,   statsPerPoint: { Critical_Hit: 1 }, emoji: '💥' },
  { id: 10, key: 'block',              section: 'chance', cap: 20,   statsPerPoint: { Block: 1 }, emoji: '🛡️' },
  { id: 11, key: 'criticalMastery',    section: 'chance', cap: null, statsPerPoint: { Critical_Mastery: 4 }, emoji: '🎯' },
  { id: 12, key: 'rearMastery',        section: 'chance', cap: null, statsPerPoint: { Rear_Mastery: 6 }, emoji: '🗡️' },
  { id: 13, key: 'berserkMastery',     section: 'chance', cap: null, statsPerPoint: { Berserk_Mastery: 8 }, emoji: '😡' },
  { id: 14, key: 'healingMastery',     section: 'chance', cap: null, statsPerPoint: { Healing_Mastery: 6 }, emoji: '💉' },
  { id: 15, key: 'rearResistance',     section: 'chance', cap: 20,   statsPerPoint: { Rear_Resistance: 4 }, emoji: '🔙' },
  { id: 34, key: 'criticalResistance', section: 'chance', cap: 20,   statsPerPoint: { Critical_Resistance: 4 }, emoji: '🥊' },

  // Mayor (cada opción cuesta 1 punto Mayor, máximo 1 punto por opción)
  { id: 2,  key: 'majorAp',             section: 'major', cap: 1, statsPerPoint: { AP: 1 }, emoji: '⭐' },
  { id: 3,  key: 'majorMp',             section: 'major', cap: 1, statsPerPoint: { MP: 1, Elemental_Mastery: 20 }, emoji: '👟' },
  { id: 4,  key: 'majorRange',          section: 'major', cap: 1, statsPerPoint: { Range: 1, Elemental_Mastery: 40 }, emoji: '🔭' },
  { id: 5,  key: 'majorWp',             section: 'major', cap: 1, statsPerPoint: { WP: 2 }, emoji: '🌀' },
  { id: 6,  key: 'majorArmorGiven',     section: 'major', cap: 1, statsPerPoint: { Armor_Given: 20 }, emoji: '🤲' },
  { id: 8,  key: 'majorDamageInflicted', section: 'major', cap: 1, statsPerPoint: { Damage_Inflicted: 10 }, emoji: '💢' },
  { id: 35, key: 'majorRes',            section: 'major', cap: 1, statsPerPoint: { Elemental_Resistance: 50 }, emoji: '🔰' },
  { id: 38, key: 'majorHealsPerformed', section: 'major', cap: 1, statsPerPoint: { Heals_Performed: 10 }, emoji: '✨' },
  { id: 39, key: 'majorIndirectDamage', section: 'major', cap: 1, statsPerPoint: { Indirect_Damage: 10, Elemental_Mastery: 40 }, emoji: '☠️' },
]

export const APTITUDES_BY_ID = Object.fromEntries(APTITUDES.map(a => [a.id, a]))

export function getAptitudesBySection(section) {
  return APTITUDES.filter(a => a.section === section)
}

// Puntos disponibles por sección según nivel.
// 1 punto por nivel desde el 2, rotando Int→Fuerza→Agi→Suerte.
// Mayor: 1 punto en los niveles 25/75/125/175/225.
// Bonus post-215: +3 puntos al llegar a 230 y +1 más al 245 (modelo de wakfuli.com,
// deja las 4 secciones parejas: 58 c/u al 230, 62 c/u al 245).
export function getPointsForSection(level, section) {
  if (section === 'major') {
    return MAJOR_LEVELS.filter(l => level >= l).length
  }
  let points = level - 1
  if (level >= 230) points += 3
  if (level >= 245) points += 1
  const remainder = points % 4
  return (points - remainder) / 4 + (remainder > SECTION_INDEX[section] ? 1 : 0)
}

export function getTotalPointsForLevel(level) {
  return SECTIONS.reduce((sum, s) => sum + getPointsForSection(level, s), 0)
}

const CODE_REGEX = /^\d{1,2}:\d{1,3}(-\d{1,2}:\d{1,3})*$/

// Parsea el "Código de características" del juego.
// Devuelve { allocation, errors } — allocation es { [aptitudeId]: puntos }.
export function parseCharacteristicsCode(code) {
  const errors = []
  const allocation = {}
  const trimmed = (code || '').trim()

  if (!trimmed) {
    return { allocation, errors: ['empty'] }
  }
  if (!CODE_REGEX.test(trimmed)) {
    return { allocation, errors: ['format'] }
  }

  for (const pair of trimmed.split('-')) {
    const [idStr, pointsStr] = pair.split(':')
    const id = parseInt(idStr, 10)
    const points = parseInt(pointsStr, 10)
    const aptitude = APTITUDES_BY_ID[id]

    if (!aptitude) {
      errors.push(`unknownId:${id}`)
      continue
    }
    if (points < 0 || (aptitude.cap !== null && points > aptitude.cap)) {
      errors.push(`overCap:${id}`)
    }
    if (points > 0) {
      allocation[id] = (allocation[id] || 0) + points
    }
  }

  return { allocation, errors }
}

// Serializa una asignación al mismo formato que exporta el juego (solo valores > 0).
export function serializeCharacteristicsCode(allocation) {
  return APTITUDES
    .filter(a => (allocation[a.id] || 0) > 0)
    .map(a => `${a.id}:${allocation[a.id]}`)
    .join('-')
}

// Valida una asignación contra el nivel: gasto por sección y topes por aptitud.
export function validateAllocation(allocation, level) {
  const sections = {}
  for (const section of SECTIONS) {
    const available = getPointsForSection(level, section)
    const spent = getAptitudesBySection(section)
      .reduce((sum, a) => sum + (allocation[a.id] || 0), 0)
    sections[section] = {
      available,
      spent,
      remaining: available - spent,
      overspent: spent > available
    }
  }

  const overCap = APTITUDES
    .filter(a => a.cap !== null && (allocation[a.id] || 0) > a.cap)
    .map(a => a.id)

  return {
    sections,
    overCap,
    valid: overCap.length === 0 && !Object.values(sections).some(s => s.overspent)
  }
}

// Convierte la asignación en bonos de stats (claves internas de useStats.js).
// HP_Percent / Armor_Percent / Barrier son claves especiales que la UI trata aparte.
export function allocationToBonusStats(allocation) {
  const bonus = {}
  for (const aptitude of APTITUDES) {
    const points = allocation[aptitude.id] || 0
    if (points <= 0) continue
    const effective = aptitude.cap !== null ? Math.min(points, aptitude.cap) : points
    for (const [statKey, perPoint] of Object.entries(aptitude.statsPerPoint)) {
      bonus[statKey] = (bonus[statKey] || 0) + perPoint * effective
    }
  }
  return bonus
}
