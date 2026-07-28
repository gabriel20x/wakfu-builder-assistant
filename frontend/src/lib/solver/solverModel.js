/**
 * Solver model builder.
 *
 * Faithful port of the model construction logic in api/app/services/solver.py
 * (item filtering, scoring/objective, constraints), targeting the HiGHS MILP
 * solver via CPLEX LP format text instead of PuLP/CBC.
 *
 * Items are plain objects loaded from the static items.json file (same fields
 * as the old DB columns), with `metadata` and `drop_sources` embedded.
 */

import { resolveElementStats } from './elementResolver.js';

// Equipment slots
export const SLOTS = [
  'HEAD', 'SHOULDERS', 'CHEST', 'BACK', 'BELT', 'LEGS',
  'FIRST_WEAPON', 'SECOND_WEAPON',
  'NECK', 'LEFT_HAND', 'RIGHT_HAND', // Amulet and rings
  'PET', 'MOUNT', 'ACCESSORY', // Pet, mount, emblem
];

// Solver tuning constants (copied from api/app/core/config.py Settings)
export const SETTINGS = {
  MAX_EPIC_ITEMS: 1,
  MAX_RELIC_ITEMS: 1,
  // Difficulty thresholds for build types
  EASY_DIFFICULTY_MAX: 48.0, // Raros (35) + algunos Míticos (no todos)
  MEDIUM_DIFFICULTY_MAX: 85.0, // Permite Legendarios (75) + 1 Épico/Reliquia
  HARD_DIFFICULTY_MAX: 100.0, // Sin límite
  // Lambda weights for solver (balancing stats vs difficulty)
  EASY_LAMBDA: 2.0, // Penaliza Míticos, prefiere Raros cuando sea posible
  MEDIUM_LAMBDA: 0.5, // Moderado: acepta Míticos/Legendarios si valen la pena
  HARD_LAMBDA: 0.0, // Sin penalización: puro stats + rarity bonus
};

// Normalization factors based on stat rarity/frequency on items
// (identical table used for both scoring and item power in solver.py)
export const NORMALIZATION_FACTORS = {
  // Muy raros
  AP: 100.0,
  MP: 80.0,
  Range: 60.0,
  // Raros
  Critical_Hit: 20.0,
  WP: 20.0,
  Control: 10.0,
  Block: 5.0,
  // Poco comunes
  Critical_Mastery: 2.0,
  Dodge: 1.0,
  Lock: 1.0,
  // Masteries (comunes)
  Fire_Mastery: 1.0,
  Water_Mastery: 1.0,
  Earth_Mastery: 1.0,
  Air_Mastery: 1.0,
  Melee_Mastery: 1.0,
  Distance_Mastery: 1.0,
  Rear_Mastery: 1.0,
  Healing_Mastery: 1.0,
  Berserk_Mastery: 1.0,
  // Resistencias (ajustadas según impacto)
  Fire_Resistance: 1.2,
  Water_Resistance: 1.2,
  Earth_Resistance: 1.2,
  Air_Resistance: 1.2,
  Elemental_Resistance: 1.5, // Vale por los 4 elementos pero valores más bajos
  Critical_Resistance: 1.0,
  Rear_Resistance: 1.0,
  // HP (extremadamente común)
  HP: 0.1,
  // Otros
  Initiative: 0.5,
  Prospecting: 0.5,
  Wisdom: 0.5,
  Armor_Given: 0.8,
  Armor_Received: 0.8,
};

const DEFAULT_ELEMENTS = ['Fire', 'Water', 'Earth', 'Air'];

function has(obj, key) {
  return obj != null && Object.prototype.hasOwnProperty.call(obj, key);
}

/**
 * Calculate item power based on its stats and user preferences.
 * Power = sum of (stat_value * user_weight * normalization_factor)
 * Used to rank items and find alternatives with lower power.
 */
export function calculateItemPower(item, statWeights, damagePreferences = null, resistancePreferences = null) {
  if (damagePreferences == null) damagePreferences = DEFAULT_ELEMENTS;
  if (resistancePreferences == null) resistancePreferences = DEFAULT_ELEMENTS;

  const resolvedStats = resolveElementStats(
    { ...(item.stats || {}) },
    damagePreferences,
    resistancePreferences
  );

  let power = 0.0;
  for (const [statName, statValue] of Object.entries(resolvedStats)) {
    if (statValue > 0 && has(statWeights, statName)) {
      const normFactor = has(NORMALIZATION_FACTORS, statName) ? NORMALIZATION_FACTORS[statName] : 1.0;
      power += statValue * statWeights[statName] * normFactor;
    }
  }
  return power;
}

/**
 * Find alternative items for the same slot with lower item power.
 * Returns up to numAlternatives candidates {item, power, power_diff},
 * sorted by power (highest first).
 */
export function findItemAlternatives(
  item,
  allItems,
  statWeights,
  numAlternatives = 3,
  damagePreferences = null,
  resistancePreferences = null
) {
  if (damagePreferences == null) damagePreferences = DEFAULT_ELEMENTS;
  if (resistancePreferences == null) resistancePreferences = DEFAULT_ELEMENTS;

  const originalPower = calculateItemPower(item, statWeights, damagePreferences, resistancePreferences);

  const candidates = [];
  for (const candidate of allItems) {
    if (candidate.item_id === item.item_id) continue; // Skip self
    if (candidate.slot !== item.slot) continue; // Different slot

    const candidatePower = calculateItemPower(candidate, statWeights, damagePreferences, resistancePreferences);
    if (candidatePower < originalPower) {
      candidates.push({
        item: candidate,
        power: candidatePower,
        power_diff: originalPower - candidatePower,
      });
    }
  }

  // Sort by power (highest first). Array.prototype.sort is stable, matching
  // Python's stable sort for equal-power candidates.
  candidates.sort((a, b) => b.power - a.power);

  return candidates.slice(0, numAlternatives);
}

/**
 * Format a candidate item for the alternatives list.
 * Same structure as a main item but includes item_power / power_difference.
 * Uses the embedded item.metadata / item.drop_sources instead of DB queries.
 */
export function formatAlternativeItem(candidateDict) {
  const item = candidateDict.item;
  const itemMetadata = item.metadata && Object.keys(item.metadata).length > 0 ? item.metadata : {};

  return {
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
    metadata: itemMetadata,
    drop_sources: item.drop_sources || [],
    item_power: candidateDict.power,
    power_difference: candidateDict.power_diff,
  };
}

/**
 * Global eligibility filter — port of the SQLAlchemy query in solve_build().
 *
 * - slot must be set
 * - level in [level_max - 10, level_max], OR
 *   level in [level_max - 10, level_max + 10] for rarity 5/6/7, OR slot == PET
 * - exclude Inusual (rarity 2) unless PET
 * - exclude Recuerdos (rarity 6 + is_relic == false) — PVP items
 * - optional PET / ACCESSORY exclusion
 * - optional ignored item ids
 * - optional only_droppable / monster_types filtering via embedded drop_sources
 */
export function filterEligibleItems(allItems, {
  levelMax,
  includePet = true,
  includeAccessory = true,
  onlyDroppable = false,
  ignoredItemIds = null,
  monsterTypes = null,
} = {}) {
  const levelMin = Math.max(1, levelMax - 10);
  const levelMaxHighRarity = levelMax + 10;

  const excludedSlots = new Set();
  if (!includePet) excludedSlots.add('PET');
  if (!includeAccessory) excludedSlots.add('ACCESSORY');

  const ignoredSet = new Set(ignoredItemIds || []);
  const monsterTypeSet = new Set(monsterTypes || []);
  const useMonsterTypes = monsterTypeSet.size > 0;

  const dropSources = (item) => item.drop_sources || [];
  const isDroppable = (item) => dropSources(item).length > 0;
  const dropsFromSelectedTypes = (item) =>
    dropSources(item).some((d) => monsterTypeSet.has(d.monster_type));

  return allItems.filter((item) => {
    if (item.slot == null) return false;

    // Level range: normal, extended for high rarity, or PET
    const inNormalRange = item.level <= levelMax && item.level >= levelMin;
    const inHighRarityRange =
      item.level <= levelMaxHighRarity &&
      item.level >= levelMin &&
      [5, 6, 7].includes(item.rarity);
    if (!(inNormalRange || inHighRarityRange || item.slot === 'PET')) return false;

    // Exclude Inusual (rarity 2) unless it's a PET
    if (item.rarity === 2 && item.slot !== 'PET') return false;

    // Exclude Recuerdos (rarity 6 + is_relic = false) — PVP items
    if (item.rarity === 6 && !item.is_relic) return false;

    if (excludedSlots.has(item.slot)) return false;

    if (ignoredSet.size > 0 && ignoredSet.has(item.item_id)) return false;

    if (useMonsterTypes) {
      if (onlyDroppable) {
        // Only items that drop from monsters of the selected types
        if (!dropsFromSelectedTypes(item)) return false;
      } else {
        // Items from selected monster types OR non-drop items
        if (!(dropsFromSelectedTypes(item) || item.source_type !== 'drop')) return false;
      }
    } else if (onlyDroppable) {
      // Only items that have at least one drop source
      if (!isDroppable(item)) return false;
    }

    return true;
  });
}

/**
 * Build-type (tier) rarity filter — port of the head of _solve_single_build().
 * Returns the (possibly reduced) item list used for the tier's model.
 */
export function applyBuildTypeFilter(items, buildType, levelMax) {
  if (buildType === 'easy') {
    if (levelMax < 80) {
      // Low level EASY: Común, Poco Común, Raro (rarity <= 3), no difficulty filter
      return items.filter((item) => item.rarity <= 3 && !item.is_epic && !item.is_relic);
    }
    // High level EASY: rarity <= 3 and difficulty <= 48
    return items.filter(
      (item) => item.rarity <= 3 && !item.is_epic && !item.is_relic && item.difficulty <= 48.0
    );
  }

  if (buildType === 'medium') {
    if (levelMax < 80) {
      // Low level MEDIUM: rarity <= 3, NO Legendarios
      return items.filter((item) => item.rarity <= 3 && !item.is_epic && !item.is_relic);
    }
    // High level MEDIUM: allows Legendaries (max 1 via constraint)
    return items.filter((item) => !item.is_epic && !item.is_relic);
  }

  // hard_epic / hard_relic / full: no additional rarity filtering
  return items;
}

/**
 * Compute the objective coefficient (score) for one item.
 * Direct port of the scoring block inside _solve_single_build().
 */
export function computeItemScore(item, statWeights, levelMax, lambdaWeight, buildType, damagePreferences, resistancePreferences) {
  const resolvedStats = resolveElementStats(
    { ...(item.stats || {}) },
    damagePreferences || DEFAULT_ELEMENTS,
    resistancePreferences || DEFAULT_ELEMENTS
  );

  let statScore = 0.0;
  let bonusScore = 0.0;
  let negativePenalty = 0.0;

  const elementalMasteries = new Set(['Fire_Mastery', 'Water_Mastery', 'Earth_Mastery', 'Air_Mastery']);
  const secondaryMasteries = new Set([
    'Melee_Mastery', 'Rear_Mastery', 'Healing_Mastery', 'Berserk_Mastery', 'Critical_Mastery',
  ]);

  for (const [statName, statValue] of Object.entries(resolvedStats)) {
    // Skip metadata pseudo-stats
    if (statName === 'is_epic' || statName === 'is_relic' || statName === 'difficulty') continue;

    const normFactor = has(NORMALIZATION_FACTORS, statName) ? NORMALIZATION_FACTORS[statName] : 1.0;

    // ========== NEGATIVE STATS (PENALTIES) ==========
    if (statValue < 0) {
      const absValue = Math.abs(statValue);

      if (statName === 'AP' || statName === 'MP' || statName === 'Range') {
        // Critical negative stats: extreme penalty (50x)
        negativePenalty += absValue * normFactor * 50.0;
      } else if (statName === 'WP') {
        // Negative WP: severe penalty scaled by level (30x)
        const levelFactor = Math.min(levelMax / 100.0, 2.0);
        negativePenalty += absValue * normFactor * levelFactor * 30.0;
      } else if (statName === 'Critical_Hit' || statName === 'Control' || statName === 'Block') {
        // Important negative stats: high penalty (20x)
        negativePenalty += absValue * normFactor * 20.0;
      } else {
        // Other negative stats: moderate penalty (10x)
        negativePenalty += absValue * normFactor * 10.0;
      }
      continue;
    }

    // ========== POSITIVE STATS ==========
    if (statValue > 0) {
      if (has(statWeights, statName)) {
        // Requested stat: user_weight * value * normalization factor
        statScore += statValue * statWeights[statName] * normFactor;
      } else if (elementalMasteries.has(statName)) {
        // Elemental masteries always matter for the damage multiplier:
        // bonus 30% of normalized value
        bonusScore += statValue * normFactor * 0.3;
      } else if (!secondaryMasteries.has(statName)) {
        // Other non-mastery stats: small bonus (10% of normalized value)
        bonusScore += statValue * normFactor * 0.1;
      }
      // Unrequested secondary masteries: no bonus
    }
  }

  const powerBonus = bonusScore;

  // ========== PENALTIES FOR MISSING SLOT-TYPICAL STATS ==========
  let missingStatPenalty = 0.0;

  // BACK (Capes) and NECK (Amulets) typically have AP
  if (item.slot === 'BACK' || item.slot === 'NECK') {
    const apValue = resolvedStats.AP || 0;
    const mpValue = resolvedStats.MP || 0;
    const rangeValue = resolvedStats.Range || 0;

    if (has(statWeights, 'AP')) {
      if (apValue <= 0) {
        const baseApPenalty = statWeights.AP * 200;
        let totalCompensation = 0.0;

        if (mpValue > 0 && has(statWeights, 'MP')) {
          totalCompensation += Math.min(mpValue * statWeights.MP * 0.5, baseApPenalty * 0.4);
        }
        if (rangeValue > 0 && has(statWeights, 'Range')) {
          totalCompensation += Math.min(rangeValue * statWeights.Range * 0.3, baseApPenalty * 0.2);
        }

        if (totalCompensation > 0) {
          missingStatPenalty += baseApPenalty - totalCompensation;
        } else if (mpValue > 0 || rangeValue > 0) {
          missingStatPenalty += baseApPenalty * 0.8;
        } else {
          missingStatPenalty += baseApPenalty;
        }
      }
    }
  }

  // CHEST (Breastplates) and LEGS (Boots) typically have MP
  if (item.slot === 'CHEST' || item.slot === 'LEGS') {
    const mpValue = resolvedStats.MP || 0;
    const apValue = resolvedStats.AP || 0;
    const rangeValue = resolvedStats.Range || 0;

    if (has(statWeights, 'MP')) {
      if (mpValue <= 0) {
        const baseMpPenalty = statWeights.MP * 200;
        let totalCompensation = 0.0;

        if (apValue > 0 && has(statWeights, 'AP')) {
          totalCompensation += Math.min(apValue * statWeights.AP * 0.5, baseMpPenalty * 0.4);
        }
        if (rangeValue > 0 && has(statWeights, 'Range')) {
          totalCompensation += Math.min(rangeValue * statWeights.Range * 0.3, baseMpPenalty * 0.2);
        }

        if (totalCompensation > 0) {
          missingStatPenalty += baseMpPenalty - totalCompensation;
        } else if (apValue > 0 || rangeValue > 0) {
          missingStatPenalty += baseMpPenalty * 0.8;
        } else {
          missingStatPenalty += baseMpPenalty;
        }
      }
    }
  }

  // Bonus for filling slots (rings get extra since they're often skipped)
  const slotFillBonus = item.slot === 'LEFT_HAND' ? 5.0 : 2.0;

  // Rarity bonus for HARD builds.
  // NOTE (fidelity): the Python code checks build_type == "hard", which never
  // matches the current tier names (hard_epic/hard_relic/full), so this bonus
  // is effectively dead code. Preserved as-is.
  let rarityBonus = 0.0;
  if (buildType === 'hard') {
    const rarityBonuses = { 1: 0, 2: 0, 3: 0, 4: 0, 5: 50, 6: 60, 7: 70 };
    rarityBonus = has(rarityBonuses, item.rarity) ? rarityBonuses[item.rarity] : 0;
  }

  return (
    statScore +
    powerBonus -
    negativePenalty -
    missingStatPenalty -
    lambdaWeight * item.difficulty +
    rarityBonus +
    slotFillBonus
  );
}

/** Format a number for CPLEX LP text. */
function fmt(n) {
  if (!Number.isFinite(n)) throw new Error(`Non-finite coefficient in LP model: ${n}`);
  // Object.is distinguishes -0; plain toString of -0 is "0" anyway.
  return String(n);
}

/** LP variable name for an item. */
export function varName(item) {
  return `i${item.item_id}`;
}

/**
 * Build the full MILP model for a single build tier, as CPLEX LP format text.
 * Direct port of the variable/objective/constraint construction in
 * _solve_single_build().
 *
 * @returns {{ lpText: string, items: Array }} tier-filtered items and LP text
 */
export function buildLpModel(eligibleItems, {
  statWeights,
  levelMax,
  difficultyMax,
  lambdaWeight,
  buildType,
  damagePreferences = null,
  resistancePreferences = null,
}) {
  const items = applyBuildTypeFilter(eligibleItems, buildType, levelMax);

  // Objective coefficients
  const objTerms = [];
  for (const item of items) {
    const score = computeItemScore(
      item, statWeights, levelMax, lambdaWeight, buildType,
      damagePreferences, resistancePreferences
    );
    const sign = score < 0 ? '-' : '+';
    objTerms.push(`${sign} ${fmt(Math.abs(score))} ${varName(item)}`);
  }

  const constraints = [];
  let cIdx = 0;
  const addConstraint = (label, expr) => {
    cIdx += 1;
    constraints.push(` c${cIdx}_${label}: ${expr}`);
  };

  // Constraint: 1 item per slot (LEFT_HAND allows 2 rings)
  const slotsUsed = new Map();
  for (const item of items) {
    if (!slotsUsed.has(item.slot)) slotsUsed.set(item.slot, []);
    slotsUsed.get(item.slot).push(varName(item));
  }
  for (const [slot, varsInSlot] of slotsUsed.entries()) {
    if (slot === 'LEFT_HAND') {
      addConstraint('max_two_rings', `${varsInSlot.join(' + ')} <= 2`);
    } else {
      addConstraint(`max_one_${slot}`, `${varsInSlot.join(' + ')} <= 1`);
    }
  }

  // Constraint: rings cannot be duplicated (same item_id OR same base name)
  if (slotsUsed.has('LEFT_HAND')) {
    const ringItems = items.filter((item) => item.slot === 'LEFT_HAND');
    for (let i = 0; i < ringItems.length; i++) {
      const ring1 = ringItems[i];
      for (let j = i + 1; j < ringItems.length; j++) {
        const ring2 = ringItems[j];
        const name1 = ring1.name_es || ring1.name_en || ring1.name;
        const name2 = ring2.name_es || ring2.name_en || ring2.name;
        if (ring1.item_id === ring2.item_id || name1 === name2) {
          addConstraint(
            `no_dup_ring_${ring1.item_id}_${ring2.item_id}`,
            `${varName(ring1)} + ${varName(ring2)} <= 1`
          );
        }
      }
    }
  }

  // Constraint: Epic and Relic management based on build type
  const epicItems = items.filter((item) => item.is_epic);
  const relicItems = items.filter((item) => item.is_relic);

  if (buildType === 'hard_epic') {
    // REQUIRE exactly 1 Epic, FORBID all Relics
    if (epicItems.length > 0) {
      addConstraint('require_one_epic', `${epicItems.map(varName).join(' + ')} = 1`);
    }
    for (const relicItem of relicItems) {
      addConstraint(`forbid_relic_${relicItem.item_id}`, `${varName(relicItem)} = 0`);
    }
  } else if (buildType === 'hard_relic') {
    // REQUIRE exactly 1 Relic, FORBID all Epics
    if (relicItems.length > 0) {
      addConstraint('require_one_relic', `${relicItems.map(varName).join(' + ')} = 1`);
    }
    for (const epicItem of epicItems) {
      addConstraint(`forbid_epic_${epicItem.item_id}`, `${varName(epicItem)} = 0`);
    }
  } else if (buildType === 'full') {
    // REQUIRE exactly 1 Epic AND exactly 1 Relic
    if (epicItems.length > 0) {
      addConstraint('require_one_epic', `${epicItems.map(varName).join(' + ')} = 1`);
    }
    if (relicItems.length > 0) {
      addConstraint('require_one_relic', `${relicItems.map(varName).join(' + ')} = 1`);
    }
  } else if (buildType === 'medium') {
    // MEDIUM: NO Epics, NO Relics
    for (const epicItem of epicItems) {
      addConstraint(`forbid_epic_${epicItem.item_id}_medium`, `${varName(epicItem)} = 0`);
    }
    for (const relicItem of relicItems) {
      addConstraint(`forbid_relic_${relicItem.item_id}_medium`, `${varName(relicItem)} = 0`);
    }
  }
  // EASY: already filtered by rarity, no Epic/Relic constraints needed

  // MEDIUM: max 1 Legendario (rarity 5) to differentiate from HARD
  if (buildType === 'medium') {
    const legendaryVars = items.filter((item) => item.rarity === 5).map(varName);
    if (legendaryVars.length > 0) {
      addConstraint('max_one_legendary_medium', `${legendaryVars.join(' + ')} <= 1`);
    }
  }

  // Two-handed weapons block SECOND_WEAPON slot
  const twoHandedWeapons = items.filter(
    (item) => item.slot === 'FIRST_WEAPON' && item.blocks_second_weapon
  );
  const secondWeapons = items.filter((item) => item.slot === 'SECOND_WEAPON');
  if (twoHandedWeapons.length > 0 && secondWeapons.length > 0) {
    for (const twoHand of twoHandedWeapons) {
      for (const secondWeapon of secondWeapons) {
        addConstraint(
          `no_2h_${twoHand.item_id}_${secondWeapon.item_id}`,
          `${varName(twoHand)} + ${varName(secondWeapon)} <= 1`
        );
      }
    }
  }

  // Average difficulty <= threshold (for easy/medium):
  // total_difficulty <= difficulty_max * len(SLOTS)
  if (difficultyMax < 100.0) {
    const terms = items.map(
      (item) => `+ ${fmt(item.difficulty)} ${varName(item)}`
    );
    if (terms.length > 0) {
      addConstraint(
        `max_difficulty_${buildType}`,
        `${terms.join(' ')} <= ${fmt(difficultyMax * SLOTS.length)}`
      );
    }
  }

  // Assemble LP text. Chunk objective terms across lines to keep lines short.
  const lines = [];
  lines.push('Maximize');
  lines.push(' obj:');
  for (let i = 0; i < objTerms.length; i += 10) {
    lines.push('  ' + objTerms.slice(i, i + 10).join(' '));
  }
  lines.push('Subject To');
  for (const c of constraints) lines.push(c);
  lines.push('Binary');
  const binNames = items.map(varName);
  for (let i = 0; i < binNames.length; i += 20) {
    lines.push(' ' + binNames.slice(i, i + 20).join(' '));
  }
  lines.push('End');

  return { lpText: lines.join('\n'), items };
}
