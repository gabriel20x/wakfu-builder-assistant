export const STAT_NAMES = {
  // Core stats
  HP: { label: 'PdV', icon: 'health_points.png' },
  AP: { label: 'PA', icon: 'action_points.png' },
  MP: { label: 'PM', icon: 'movement_points.png' },
  WP: { label: 'PW', icon: 'wakfu_points.png' },
  
  // Elemental Masteries
  Water_Mastery: { label: 'Maestría Agua', icon: 'water_coin.png' },
  Air_Mastery: { label: 'Maestría Aire', icon: 'air_coin.png' },
  Earth_Mastery: { label: 'Maestría Tierra', icon: 'earth_coin.png' },
  Fire_Mastery: { label: 'Maestría Fuego', icon: 'fire_coin.png' },
  Elemental_Mastery: { label: 'Maestría Elemental', icon: 'elemental_mastery.png' },
  
  // Multi-Element Mastery (✅ CORRECTED - updated from chest review)
  Multi_Element_Mastery_1: { label: 'Dominio (1 elemento)', icon: 'elemental_mastery.png' },
  Multi_Element_Mastery_2: { label: 'Dominio (2 elementos)', icon: 'elemental_mastery.png' },
  Multi_Element_Mastery_3: { label: 'Dominio (3 elementos)', icon: 'elemental_mastery.png' },
  Multi_Element_Mastery_4: { label: 'Dominio (4 elementos)', icon: 'elemental_mastery.png' },
  
  // Legacy naming (for backwards compatibility)
  Elemental_Mastery_1_elements: { label: 'Maestría (1 elemento)', icon: 'elemental_mastery.png' },
  Elemental_Mastery_2_elements: { label: 'Maestría (2 elementos)', icon: 'elemental_mastery.png' },
  Elemental_Mastery_3_elements: { label: 'Maestría (3 elementos)', icon: 'elemental_mastery.png' },
  Elemental_Mastery_4_elements: { label: 'Maestría (4 elementos)', icon: 'elemental_mastery.png' },
  Random_Elemental_Mastery: { label: 'Maestría Elemental Aleatoria', icon: 'elemental_mastery.png' },
  
  // Position Masteries
  Critical_Mastery: { label: 'Dominio Crítico', icon: 'critical_mastery.png' },
  Rear_Mastery: { label: 'Dominio Espalda', icon: 'rear_mastery.png' },
  Melee_Mastery: { label: 'Dominio de Melé', icon: 'melee_mastery.png' },
  Distance_Mastery: { label: 'Dominio Distancia', icon: 'distance_mastery.png' },
  Healing_Mastery: { label: 'Dominio Cura', icon: 'healing_mastery.png' },
  Berserk_Mastery: { label: 'Dominio Berserker', icon: 'berserk_mastery.png' },
  
  // Elemental Resistances
  Water_Resistance: { label: 'Resistencia Agua', icon: 'water_coin.png' },
  Air_Resistance: { label: 'Resistencia Aire', icon: 'air_coin.png' },
  Earth_Resistance: { label: 'Resistencia Tierra', icon: 'earth_coin.png' },
  Fire_Resistance: { label: 'Resistencia Fuego', icon: 'fire_coin.png' },
  Elemental_Resistance: { label: 'Resistencia Elemental', icon: 'elemental_resistance.png' },
  
  // Random Elemental Resistance (✅ CORRECTED - updated naming)
  Random_Elemental_Resistance_1: { label: 'Resistencia (1 elemento)', icon: 'elemental_resistance.png' },
  Random_Elemental_Resistance_2: { label: 'Resistencia (2 elementos)', icon: 'elemental_resistance.png' },
  Random_Elemental_Resistance_3: { label: 'Resistencia (3 elementos)', icon: 'elemental_resistance.png' },
  Random_Elemental_Resistance_4: { label: 'Resistencia (4 elementos)', icon: 'elemental_resistance.png' },
  
  // Legacy naming (for backwards compatibility)
  Elemental_Resistance_1_elements: { label: 'Resistencia (1 elemento)', icon: 'elemental_resistance.png' },
  Elemental_Resistance_2_elements: { label: 'Resistencia (2 elementos)', icon: 'elemental_resistance.png' },
  Elemental_Resistance_3_elements: { label: 'Resistencia (3 elementos)', icon: 'elemental_resistance.png' },
  Elemental_Resistance_4_elements: { label: 'Resistencia (4 elementos)', icon: 'elemental_resistance.png' },
  Random_Elemental_Resistance: { label: 'Resistencia Elemental Aleatoria', icon: 'elemental_resistance.png' },
  
  // Other Resistances
  Critical_Resistance: { label: 'Resistencia Crítica', icon: 'critical_resistance.png' },
  Rear_Resistance: { label: 'Resistencia Espalda', icon: 'rear_resistance.png' },
  
  // Combat stats
  Critical_Hit: { label: 'Golpe Crítico', icon: 'critical_hit.png', suffix: '%' },
  Block: { label: 'Anticipación', icon: 'block.png', suffix: '%' },
  Initiative: { label: 'Iniciativa', icon: 'initiative.png' },
  Dodge: { label: 'Esquiva', icon: 'dodge.png' },
  Lock: { label: 'Placaje', icon: 'lock.png' },
  Wisdom: { label: 'Sabiduría', icon: 'wisdom.png' },
  Prospecting: { label: 'Prospección', icon: 'prospecting.png' },
  Range: { label: 'Alcance', icon: 'range.png' },
  Control: { label: 'Control', icon: 'control.png' },
  Force_Of_Will: { label: 'Voluntad', icon: 'force_of_will.png' },
  
  // Percentages
  Damage_Inflicted: { label: 'Daños Finales', icon: 'damage_inflicted.png', suffix: '%' },
  Heals_Performed: { label: 'Curas Finales', icon: 'heals_performed.png', suffix: '%' },
  Heals_Received: { label: 'Curas Recibidas', icon: 'heals_received.png', suffix: '%' },
  Armor_Given: { label: 'Armadura Dada', icon: 'armor_given.png', suffix: '%' },
  Armor_Received: { label: 'Armadura Recibida', icon: 'armor_received.png', suffix: '%' },
  Indirect_Damage: { label: 'Daños Indirectos', icon: 'indirect_damage.png', suffix: '%' },
  
  // Kit Skill
  Kit_Skill: { label: 'Nivel de Kit', icon: 'kit_skill.png' },
  
  // Resistance (generic)
  Resistance: { label: 'Resistencia', icon: 'resistance.png' },
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
  6: '#E91E63',     // Reliquia/Recuerdo - Fucsia (ver flags is_relic)
  7: '#D946EF',     // ✅ Épico - Púrpura (backend v1.7 mapping)
  // Épicos siempre tienen is_epic = true
  // Reliquias (rarity 6 + is_relic = true) vs Recuerdos (rarity 6 + is_relic = false)
}

export const RARITY_NAMES = {
  0: 'Común',
  1: 'Común',
  // 2: No existe en equipment
  3: 'Raro',
  4: 'Mítico',
  5: 'Legendario',  // ✅ FIXED - Backend v1.7 mapping (era "Reliquia")
  6: 'Reliquia',    // Default para rarity 6, sobrescrito por flags
  7: 'Épico',       // ✅ FIXED - Backend v1.7 mapping (era "Legendario")
  // ItemCard.vue usa is_epic e is_relic para sobrescribir nombres
}

export function getStatLabel(statKey) {
  return STAT_NAMES[statKey]?.label || statKey
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
  return RARITY_NAMES[rarity] || 'Unknown'
}

