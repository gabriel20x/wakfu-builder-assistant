/**
 * Build solver — JavaScript port of api/app/services/solver.py (PuLP/CBC)
 * plus the API contract of api/app/routers/solver.py, running on HiGHS (WASM).
 *
 * Public API:
 *   solveBuild(items, params) -> Promise<SolveResponse>
 *
 * where `items` is the plain array loaded from frontend/public/data/items.json
 * and `params` mirrors the old POST /solve request body:
 *   { level_max, stat_weights, include_pet, include_accessory, only_droppable,
 *     damage_preferences, resistance_preferences, ignored_item_ids, monster_types }
 *
 * SolveResponse: { easy, medium, hard_epic, hard_relic, full }, each
 *   { items: [...], total_stats: {...}, total_difficulty: number, build_type: string }
 */

import {
  resolveBuildStats,
  inferElementPreferencesFromWeights,
} from './elementResolver.js';
import {
  SETTINGS,
  buildLpModel,
  filterEligibleItems,
  findItemAlternatives,
  formatAlternativeItem,
  varName,
} from './solverModel.js';
import { solveLp } from './engine.js';

const DEFAULT_ELEMENTS = ['Fire', 'Water', 'Earth', 'Air'];

// Defaults from SolveRequest in api/app/routers/solver.py
const DEFAULT_STAT_WEIGHTS = {
  HP: 1.0,
  AP: 2.5,
  MP: 2.0,
  Critical_Hit: 1.5,
};

function emptyBuild(buildType) {
  return {
    items: [],
    total_stats: {},
    total_difficulty: 0.0,
    build_type: buildType,
  };
}

/**
 * Solve a single build tier. Port of _solve_single_build().
 */
async function solveSingleBuild(eligibleItems, {
  statWeights,
  levelMax,
  difficultyMax,
  lambdaWeight,
  buildType,
  damagePreferences,
  resistancePreferences,
}) {
  const { lpText, items } = buildLpModel(eligibleItems, {
    statWeights,
    levelMax,
    difficultyMax,
    lambdaWeight,
    buildType,
    damagePreferences,
    resistancePreferences,
  });

  // PuLP happily "solves" an empty problem as Optimal with no items;
  // the LP text reader needs at least one variable, so short-circuit.
  if (items.length === 0) {
    return emptyBuild(buildType);
  }

  let solution;
  try {
    solution = await solveLp(lpText);
  } catch (err) {
    // Mirror Python's non-optimal fallback: empty build
    console.warn(`Solver error for ${buildType}: ${err && err.message}`);
    return emptyBuild(buildType);
  }

  if (!solution || solution.Status !== 'Optimal') {
    return emptyBuild(buildType);
  }

  // Extract solution (binary vars; use 0.5 threshold for FP robustness)
  const columns = solution.Columns || {};
  const selectedItems = items.filter((item) => {
    const col = columns[varName(item)];
    return col && col.Primal > 0.5;
  });

  const selectedSerialized = [];
  const itemsStatsList = [];
  let totalDifficulty = 0.0;

  for (const item of selectedItems) {
    // Metadata is embedded per item (was: METADATA_PATH json keyed by id)
    const itemMetadata =
      item.metadata && Object.keys(item.metadata).length > 0 ? item.metadata : {};

    const itemDict = {
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
      alternatives: [],
    };

    // Find and add alternatives (same tier-filtered candidate pool as Python)
    const alternatives = findItemAlternatives(
      item,
      items,
      statWeights,
      3,
      damagePreferences,
      resistancePreferences
    );
    for (const altCandidate of alternatives) {
      itemDict.alternatives.push(formatAlternativeItem(altCandidate));
    }

    selectedSerialized.push(itemDict);
    itemsStatsList.push(item.stats || {});
    totalDifficulty += item.difficulty;
  }

  const totalStats = resolveBuildStats(
    itemsStatsList,
    damagePreferences || DEFAULT_ELEMENTS,
    resistancePreferences || DEFAULT_ELEMENTS
  );

  const avgDifficulty =
    selectedSerialized.length > 0 ? totalDifficulty / selectedSerialized.length : 0.0;

  return {
    items: selectedSerialized,
    total_stats: totalStats,
    total_difficulty: avgDifficulty,
    build_type: buildType,
  };
}

/**
 * Solve for five builds: easy, medium, hard_epic, hard_relic, full.
 * Port of solve_build() + the router serialization (response contains exactly
 * items / total_stats / total_difficulty / build_type per tier).
 *
 * @param {Array<Object>} allItems - full item array from items.json
 * @param {Object} params - request params (snake_case, same as the old API)
 * @returns {Promise<Object>} SolveResponse
 */
export async function solveBuild(allItems, params = {}) {
  const levelMax = params.level_max != null ? params.level_max : 230;
  const statWeights =
    params.stat_weights != null ? params.stat_weights : { ...DEFAULT_STAT_WEIGHTS };
  const includePet = params.include_pet != null ? params.include_pet : true;
  const includeAccessory =
    params.include_accessory != null ? params.include_accessory : true;
  const onlyDroppable = params.only_droppable != null ? params.only_droppable : false;
  const ignoredItemIds = params.ignored_item_ids || null;
  const monsterTypes = params.monster_types || null;

  // Auto-detect element preferences from stat_weights if not provided
  let damagePreferences = params.damage_preferences;
  if (damagePreferences == null || damagePreferences.length === 0) {
    damagePreferences = inferElementPreferencesFromWeights(statWeights);
  }
  let resistancePreferences = params.resistance_preferences;
  if (resistancePreferences == null || resistancePreferences.length === 0) {
    resistancePreferences = DEFAULT_ELEMENTS;
  }

  const eligibleItems = filterEligibleItems(allItems, {
    levelMax,
    includePet,
    includeAccessory,
    onlyDroppable,
    ignoredItemIds,
    monsterTypes,
  });

  const common = {
    statWeights,
    levelMax,
    damagePreferences,
    resistancePreferences,
  };

  const easy = await solveSingleBuild(eligibleItems, {
    ...common,
    difficultyMax: SETTINGS.EASY_DIFFICULTY_MAX,
    lambdaWeight: SETTINGS.EASY_LAMBDA,
    buildType: 'easy',
  });

  const medium = await solveSingleBuild(eligibleItems, {
    ...common,
    difficultyMax: SETTINGS.MEDIUM_DIFFICULTY_MAX,
    lambdaWeight: SETTINGS.MEDIUM_LAMBDA,
    buildType: 'medium',
  });

  const hardEpic = await solveSingleBuild(eligibleItems, {
    ...common,
    difficultyMax: SETTINGS.HARD_DIFFICULTY_MAX,
    lambdaWeight: SETTINGS.HARD_LAMBDA,
    buildType: 'hard_epic',
  });

  const hardRelic = await solveSingleBuild(eligibleItems, {
    ...common,
    difficultyMax: SETTINGS.HARD_DIFFICULTY_MAX,
    lambdaWeight: SETTINGS.HARD_LAMBDA,
    buildType: 'hard_relic',
  });

  const full = await solveSingleBuild(eligibleItems, {
    ...common,
    difficultyMax: SETTINGS.HARD_DIFFICULTY_MAX,
    lambdaWeight: SETTINGS.HARD_LAMBDA,
    buildType: 'full',
  });

  return {
    easy,
    medium,
    hard_epic: hardEpic,
    hard_relic: hardRelic,
    full,
  };
}
