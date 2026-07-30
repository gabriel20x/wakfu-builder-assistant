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

/** [from, from-1, ..., to] descending; empty-safe when from < to. */
function rangeDown(from, to) {
  const out = [];
  for (let v = from; v >= to; v--) out.push(v);
  return out.length > 0 ? out : [from];
}

/**
 * Solve a tier honoring AP/MP targets, relaxing them if infeasible.
 *
 * A hard target can be unreachable (level window too low, too many ignored
 * items, an over-ambitious number). Rather than returning an empty build, walk
 * the target down one point at a time and report what was actually achieved via
 * `target_shortfall`, so the UI can say "12 AP not reachable, best was 11".
 *
 * MP relaxes before AP: AP is almost always the bigger damage lever, so when
 * both can't be met the AP target is the one worth keeping.
 */
async function solveWithTargets(eligibleItems, opts) {
  const { apTarget, mpTarget, baseAp, baseMp } = opts;

  if (apTarget == null && mpTarget == null) {
    return solveSingleBuild(eligibleItems, opts);
  }

  // Candidate (ap, mp) pairs ordered by total shortfall, so the first feasible
  // one is the closest to what was asked. Within the same shortfall, prefer
  // giving up MP over AP (AP is the bigger damage lever).
  const apSteps = apTarget == null ? [null] : rangeDown(apTarget, baseAp);
  const mpSteps = mpTarget == null ? [null] : rangeDown(mpTarget, baseMp);

  const attempts = [];
  for (const ap of apSteps) {
    for (const mp of mpSteps) {
      attempts.push([ap, mp]);
    }
  }
  attempts.sort((a, b) => {
    const lossA = (apTarget == null ? 0 : apTarget - a[0]) + (mpTarget == null ? 0 : mpTarget - a[1]);
    const lossB = (apTarget == null ? 0 : apTarget - b[0]) + (mpTarget == null ? 0 : mpTarget - b[1]);
    if (lossA !== lossB) return lossA - lossB;
    // Tie-break: keep the higher AP.
    return (b[0] ?? 0) - (a[0] ?? 0);
  });

  for (const [ap, mp] of attempts) {
    const build = await solveSingleBuild(eligibleItems, {
      ...opts,
      apTarget: ap,
      mpTarget: mp,
    });
    if (build.items.length > 0) {
      const shortfall = {};
      if (apTarget != null && ap !== apTarget) shortfall.AP = { requested: apTarget, achieved: ap };
      if (mpTarget != null && mp !== mpTarget) shortfall.MP = { requested: mpTarget, achieved: mp };
      if (Object.keys(shortfall).length > 0) {
        build.target_shortfall = shortfall;
      }
      return build;
    }
  }

  // Nothing worked even fully relaxed — fall back to an unconstrained solve.
  return solveSingleBuild(eligibleItems, { ...opts, apTarget: null, mpTarget: null });
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
  apTarget = null,
  mpTarget = null,
  baseAp = 0,
  baseMp = 0,
}) {
  const { lpText, items } = buildLpModel(eligibleItems, {
    statWeights,
    levelMax,
    difficultyMax,
    lambdaWeight,
    buildType,
    damagePreferences,
    resistancePreferences,
    apTarget,
    mpTarget,
    baseAp,
    baseMp,
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
      shard_slots: item.shard_slots,
      epic_gem_slot: item.epic_gem_slot,
      relic_gem_slot: item.relic_gem_slot,
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
  const levelWindow = params.level_window != null ? params.level_window : 15;
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
    levelWindow,
    includePet,
    includeAccessory,
    onlyDroppable,
    ignoredItemIds,
    monsterTypes,
  });

  // AP/MP targets: total the finished character should reach. `base_ap`/`base_mp`
  // is what it already has without gear (innate + major aptitudes), so the
  // constraint only asks the items for the remainder. null = no target.
  const apTarget = params.ap_target != null ? params.ap_target : null;
  const mpTarget = params.mp_target != null ? params.mp_target : null;
  const baseAp = params.base_ap != null ? params.base_ap : 0;
  const baseMp = params.base_mp != null ? params.base_mp : 0;

  const common = {
    statWeights,
    levelMax,
    damagePreferences,
    resistancePreferences,
    apTarget,
    mpTarget,
    baseAp,
    baseMp,
  };

  const easy = await solveWithTargets(eligibleItems, {
    ...common,
    difficultyMax: SETTINGS.EASY_DIFFICULTY_MAX,
    lambdaWeight: SETTINGS.EASY_LAMBDA,
    buildType: 'easy',
  });

  const medium = await solveWithTargets(eligibleItems, {
    ...common,
    difficultyMax: SETTINGS.MEDIUM_DIFFICULTY_MAX,
    lambdaWeight: SETTINGS.MEDIUM_LAMBDA,
    buildType: 'medium',
  });

  const hardEpic = await solveWithTargets(eligibleItems, {
    ...common,
    difficultyMax: SETTINGS.HARD_DIFFICULTY_MAX,
    lambdaWeight: SETTINGS.HARD_LAMBDA,
    buildType: 'hard_epic',
  });

  const hardRelic = await solveWithTargets(eligibleItems, {
    ...common,
    difficultyMax: SETTINGS.HARD_DIFFICULTY_MAX,
    lambdaWeight: SETTINGS.HARD_LAMBDA,
    buildType: 'hard_relic',
  });

  const full = await solveWithTargets(eligibleItems, {
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
