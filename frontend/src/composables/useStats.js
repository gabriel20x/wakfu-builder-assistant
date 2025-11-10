import { useI18n } from './useI18n'

export const STAT_NAMES = {
  // Core stats
  HP: { key: 'HP', icon: 'health_points.png' },
  AP: { key: 'AP', icon: 'action_points.png' },
  MP: { key: 'MP', icon: 'movement_points.png' },
  WP: { key: 'WP', icon: 'wakfu_points.png' },
  
  // Elemental Masteries
  Water_Mastery: { key: 'Water_Mastery', icon: 'water_coin.png' },
  Air_Mastery: { key: 'Air_Mastery', icon: 'air_coin.png' },
  Earth_Mastery: { key: 'Earth_Mastery', icon: 'earth_coin.png' },
  Fire_Mastery: { key: 'Fire_Mastery', icon: 'fire_coin.png' },
  Elemental_Mastery: { key: 'Elemental_Mastery', icon: 'elemental_mastery.png' },
  
  // Multi-Element Mastery (✅ CORRECTED - updated from chest review)
  Multi_Element_Mastery_1: { key: 'Multi_Element_Mastery_1', icon: 'elemental_mastery.png' },
  Multi_Element_Mastery_2: { key: 'Multi_Element_Mastery_2', icon: 'elemental_mastery.png' },
  Multi_Element_Mastery_3: { key: 'Multi_Element_Mastery_3', icon: 'elemental_mastery.png' },
  Multi_Element_Mastery_4: { key: 'Multi_Element_Mastery_4', icon: 'elemental_mastery.png' },
  
  // Legacy naming (for backwards compatibility)
  Elemental_Mastery_1_elements: { key: 'Elemental_Mastery_1_elements', icon: 'elemental_mastery.png' },
  Elemental_Mastery_2_elements: { key: 'Elemental_Mastery_2_elements', icon: 'elemental_mastery.png' },
  Elemental_Mastery_3_elements: { key: 'Elemental_Mastery_3_elements', icon: 'elemental_mastery.png' },
  Elemental_Mastery_4_elements: { key: 'Elemental_Mastery_4_elements', icon: 'elemental_mastery.png' },
  Random_Elemental_Mastery: { key: 'Random_Elemental_Mastery', icon: 'elemental_mastery.png' },
  
  // Position Masteries
  Critical_Mastery: { key: 'Critical_Mastery', icon: 'critical_mastery.png' },
  Rear_Mastery: { key: 'Rear_Mastery', icon: 'rear_mastery.png' },
  Melee_Mastery: { key: 'Melee_Mastery', icon: 'melee_mastery.png' },
  Distance_Mastery: { key: 'Distance_Mastery', icon: 'distance_mastery.png' },
  Healing_Mastery: { key: 'Healing_Mastery', icon: 'healing_mastery.png' },
  Berserk_Mastery: { key: 'Berserk_Mastery', icon: 'berserk_mastery.png' },
  
  // Elemental Resistances
  Water_Resistance: { key: 'Water_Resistance', icon: 'water_coin.png' },
  Air_Resistance: { key: 'Air_Resistance', icon: 'air_coin.png' },
  Earth_Resistance: { key: 'Earth_Resistance', icon: 'earth_coin.png' },
  Fire_Resistance: { key: 'Fire_Resistance', icon: 'fire_coin.png' },
  Elemental_Resistance: { key: 'Elemental_Resistance', icon: 'elemental_resistance.png' },
  
  // Random Elemental Resistance (✅ CORRECTED - updated naming)
  Random_Elemental_Resistance_1: { key: 'Random_Elemental_Resistance_1', icon: 'elemental_resistance.png' },
  Random_Elemental_Resistance_2: { key: 'Random_Elemental_Resistance_2', icon: 'elemental_resistance.png' },
  Random_Elemental_Resistance_3: { key: 'Random_Elemental_Resistance_3', icon: 'elemental_resistance.png' },
  Random_Elemental_Resistance_4: { key: 'Random_Elemental_Resistance_4', icon: 'elemental_resistance.png' },
  
  // Legacy naming (for backwards compatibility)
  Elemental_Resistance_1_elements: { key: 'Elemental_Resistance_1_elements', icon: 'elemental_resistance.png' },
  Elemental_Resistance_2_elements: { key: 'Elemental_Resistance_2_elements', icon: 'elemental_resistance.png' },
  Elemental_Resistance_3_elements: { key: 'Elemental_Resistance_3_elements', icon: 'elemental_resistance.png' },
  Elemental_Resistance_4_elements: { key: 'Elemental_Resistance_4_elements', icon: 'elemental_resistance.png' },
  Random_Elemental_Resistance: { key: 'Random_Elemental_Resistance', icon: 'elemental_resistance.png' },
  
  // Other Resistances
  Critical_Resistance: { key: 'Critical_Resistance', icon: 'critical_resistance.png' },
  Rear_Resistance: { key: 'Rear_Resistance', icon: 'rear_resistance.png' },
  
  // Combat stats
  Critical_Hit: { key: 'Critical_Hit', icon: 'critical_hit.png', suffix: '%' },
  Block: { key: 'Block', icon: 'block.png', suffix: '%' },
  Initiative: { key: 'Initiative', icon: 'initiative.png' },
  Dodge: { key: 'Dodge', icon: 'dodge.png' },
  Lock: { key: 'Lock', icon: 'lock.png' },
  Wisdom: { key: 'Wisdom', icon: 'wisdom.png' },
  Prospecting: { key: 'Prospecting', icon: 'prospecting.png' },
  Range: { key: 'Range', icon: 'range.png' },
  Control: { key: 'Control', icon: 'control.png' },
  Force_Of_Will: { key: 'Force_Of_Will', icon: 'force_of_will.png' },
  
  // Percentages
  Damage_Inflicted: { key: 'Damage_Inflicted', icon: 'damage_inflicted.png', suffix: '%' },
  Heals_Performed: { key: 'Heals_Performed', icon: 'heals_performed.png', suffix: '%' },
  Heals_Received: { key: 'Heals_Received', icon: 'heals_received.png', suffix: '%' },
  Armor_Given: { key: 'Armor_Given', icon: 'armor_given.png', suffix: '%' },
  Armor_Received: { key: 'Armor_Received', icon: 'armor_received.png', suffix: '%' },
  Indirect_Damage: { key: 'Indirect_Damage', icon: 'indirect_damage.png', suffix: '%' },
  
  // Kit Skill
  Kit_Skill: { key: 'Kit_Skill', icon: 'kit_skill.png' },
  
  // Resistance (generic)
  Resistance: { key: 'Resistance', icon: 'resistance.png' },
}

export const STAT_CATEGORIES = {
  main: ['HP', 'AP', 'MP', 'WP'],
  elementalMasteries: ['Water_Mastery', 'Air_Mastery', 'Earth_Mastery', 'Fire_Mastery'],
  elementalResistances: ['Water_Resistance', 'Air_Resistance', 'Earth_Resistance', 'Fire_Resistance'],
  combat: ['Damage_Inflicted', 'Critical_Hit', 'Initiative', 'Dodge', 'Wisdom', 'Control', 'Heals_Performed', 'Block', 'Range', 'Lock', 'Prospecting', 'Force_Of_Will'],
  secondary: ['Critical_Mastery', 'Rear_Mastery', 'Melee_Mastery', 'Distance_Mastery', 'Healing_Mastery', 'Berserk_Mastery', 'Critical_Resistance', 'Rear_Resistance', 'Armor_Given', 'Armor_Received', 'Indirect_Damage']
}

export const DEFAULT_STAT_WEIGHTS = {
  HP: 1.0,
  AP: 2.5,
  MP: 2.0,
  WP: 1.5,
  Critical_Hit: 1.5,
  Critical_Mastery: 2.0,
  Distance_Mastery: 2.0,
  Melee_Mastery: 2.0,
  Water_Mastery: 1.8,
  Fire_Mastery: 1.8,
  Earth_Mastery: 1.8,
  Air_Mastery: 1.8,
}

export const RARITY_COLORS = {
  0: '#808080',     // Sin rareza - Gris
  1: '#808080',     // Común - Gris
  // 2: No existe en equipment (skip "Poco común")
  3: '#4CAF50',     // Raro - Verde
  4: '#FF9800',     // Mítico - Naranja
  5: '#FFD700',     // ✅ Legendario - Dorado (backend v1.7 mapping)
  6: '#87CEFA',     // ✅ Recuerdo - Celeste/Azul claro (PVP items, lvl 200+)
  7: '#D946EF',     // ✅ Épico - Púrpura (backend v1.7 mapping)
  // Épicos siempre tienen is_epic = true
  // Reliquias (rarity 6 + is_relic = true) usan #E91E63 (Fucsia) overridden en ItemCard.vue
  // Recuerdos (rarity 6 + is_relic = false) usan #87CEFA (Celeste)
}

export const RARITY_NAMES = {
  0: 'Común',
  1: 'Común',
  // 2: No existe en equipment
  3: 'Raro',
  4: 'Mítico',
  5: 'Legendario',  // ✅ FIXED - Backend v1.7 mapping
  6: 'Recuerdo',    // ✅ FIXED - Default for rarity 6 (Souvenir items lvl 200+)
  7: 'Épico',       // ✅ FIXED - Backend v1.7 mapping
  // ItemCard.vue usa is_epic e is_relic para sobrescribir nombres
  // Rarity 6 + is_relic = true → "Reliquia" (overridden in ItemCard.vue)
}

export function getStatLabel(statKey) {
  const { t } = useI18n()
  const statInfo = STAT_NAMES[statKey]
  if (statInfo?.key) {
    return t(`stat.${statInfo.key}`)
  }
  return statKey
}

export function getStatIcon(statKey) {
  return STAT_NAMES[statKey]?.icon || 'default.png'
}

export function getStatSuffix(statKey) {
  return STAT_NAMES[statKey]?.suffix || ''
}

export function getRarityColor(rarity) {
  return RARITY_COLORS[rarity] || '#808080'
}

export function getRarityName(rarity) {
  const { t } = useI18n()
  const rarityMap = {
    0: 'common',
    1: 'common',
    3: 'rare',
    4: 'mythic',
    5: 'legendary',
    6: 'relic',
    7: 'epic'
  }
  const rarityKey = rarityMap[rarity]
  return rarityKey ? t(`rarity.${rarityKey}`) : 'Unknown'
}

