/**
 * Solver port tests — run with: node frontend/tests/solver.test.mjs
 * No test framework required.
 *
 * Ports the meaningful cases from api/tests/test_solver.py (adapted to the
 * five-tier response: easy/medium/hard_epic/hard_relic/full) and adds an
 * integration test against the real frontend/public/data/items.json.
 */

import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

import { solveBuild } from '../src/lib/solver/solver.js';
import {
  inferElementPreferencesFromWeights,
  resolveElementStats,
  resolveBuildStats,
} from '../src/lib/solver/elementResolver.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const TIERS = ['easy', 'medium', 'hard_epic', 'hard_relic', 'full'];

// ---------------------------------------------------------------------------
// Tiny test harness
// ---------------------------------------------------------------------------
let passed = 0;
let failed = 0;
const failures = [];

function assert(cond, msg) {
  if (cond) {
    passed++;
  } else {
    failed++;
    failures.push(msg);
    console.error(`  FAIL: ${msg}`);
  }
}

function assertEqual(actual, expected, msg) {
  const ok = JSON.stringify(actual) === JSON.stringify(expected);
  assert(ok, `${msg} (expected ${JSON.stringify(expected)}, got ${JSON.stringify(actual)})`);
}

function assertClose(actual, expected, msg, tol = 1e-6) {
  assert(
    Math.abs(actual - expected) <= tol,
    `${msg} (expected ~${expected}, got ${actual})`
  );
}

function section(name) {
  console.log(`\n=== ${name} ===`);
}

// ---------------------------------------------------------------------------
// Fixture helpers
// ---------------------------------------------------------------------------
let nextId = 1;
function makeItem(overrides = {}) {
  const id = overrides.item_id != null ? overrides.item_id : nextId++;
  return {
    item_id: id,
    name: overrides.name || `Item ${id}`,
    name_en: overrides.name_en || overrides.name || `Item ${id}`,
    name_es: overrides.name_es || overrides.name || `Item ${id}`,
    name_fr: overrides.name_fr || overrides.name || `Item ${id}`,
    level: overrides.level != null ? overrides.level : 225,
    rarity: overrides.rarity != null ? overrides.rarity : 3,
    slot: overrides.slot !== undefined ? overrides.slot : 'HEAD',
    is_epic: overrides.is_epic || false,
    is_relic: overrides.is_relic || false,
    has_gem_slot: overrides.has_gem_slot || false,
    blocks_second_weapon: overrides.blocks_second_weapon || false,
    source_type: overrides.source_type || 'drop',
    difficulty: overrides.difficulty != null ? overrides.difficulty : 30.0,
    manual_drop_difficulty: null,
    gfx_id: overrides.gfx_id != null ? overrides.gfx_id : id,
    stats: overrides.stats || { HP: 50 },
    drop_sources:
      overrides.drop_sources !== undefined
        ? overrides.drop_sources
        : [
            {
              monster_id: 1,
              monster_name: 'Test Monster',
              monster_names: { en: 'Test Monster' },
              monster_type: 'monster',
              family: null,
              level_min: 1,
              level_max: 230,
              drop_rate: 0.1,
              drop_rate_percent: 10,
              image_url: 'https://example.invalid/1.png',
            },
          ],
    metadata: overrides.metadata !== undefined ? overrides.metadata : null,
  };
}

/** Validate slot occupancy: max 1 per slot, except LEFT_HAND (max 2). */
function checkSlots(build, label) {
  const counts = {};
  for (const item of build.items) {
    counts[item.slot] = (counts[item.slot] || 0) + 1;
  }
  for (const [slot, count] of Object.entries(counts)) {
    const max = slot === 'LEFT_HAND' ? 2 : 1;
    assert(count <= max, `${label}: slot ${slot} has ${count} items (max ${max})`);
  }
}

function countEpics(build) {
  return build.items.filter((i) => i.is_epic).length;
}
function countRelics(build) {
  return build.items.filter((i) => i.is_relic).length;
}

function checkResponseShape(builds, label) {
  for (const tier of TIERS) {
    assert(tier in builds, `${label}: response has '${tier}'`);
    const build = builds[tier];
    for (const key of ['items', 'total_stats', 'total_difficulty', 'build_type']) {
      assert(key in build, `${label}: ${tier} has '${key}'`);
    }
    assertEqual(build.build_type, tier, `${label}: ${tier} build_type`);
    assert(Array.isArray(build.items), `${label}: ${tier} items is array`);
    assert(typeof build.total_stats === 'object', `${label}: ${tier} total_stats is object`);
    assert(typeof build.total_difficulty === 'number', `${label}: ${tier} total_difficulty is number`);
    // Response contract: exactly the 4 BuildResponse keys (router strips extras)
    assertEqual(
      Object.keys(build).sort(),
      ['build_type', 'items', 'total_difficulty', 'total_stats'],
      `${label}: ${tier} has exactly the BuildResponse keys`
    );
  }
}

/** total_stats must equal resolveBuildStats over the chosen items' raw stats. */
function checkTotalStats(build, damagePrefs, resistancePrefs, label) {
  const expected = resolveBuildStats(
    build.items.map((i) => i.stats || {}),
    damagePrefs,
    resistancePrefs
  );
  const keys = new Set([...Object.keys(expected), ...Object.keys(build.total_stats)]);
  for (const key of keys) {
    assertClose(
      build.total_stats[key] || 0,
      expected[key] || 0,
      `${label}: total_stats[${key}] matches sum of item stats`
    );
  }
}

// ---------------------------------------------------------------------------
// Element resolver unit tests
// ---------------------------------------------------------------------------
function testElementResolver() {
  section('elementResolver unit tests');

  // Weighted elements first (desc weight, ties alphabetical), then the rest
  assertEqual(
    inferElementPreferencesFromWeights({ Fire_Mastery: 7, Earth_Mastery: 7, HP: 4 }),
    ['Earth', 'Fire', 'Water', 'Air'],
    'infer prefs: ties broken alphabetically'
  );
  assertEqual(
    inferElementPreferencesFromWeights({ Water_Mastery: 9, Air_Mastery: 3 }),
    ['Water', 'Air', 'Fire', 'Earth'],
    'infer prefs: by descending weight, then default order'
  );
  assertEqual(
    inferElementPreferencesFromWeights({ HP: 5 }),
    ['Fire', 'Water', 'Earth', 'Air'],
    'infer prefs: no elemental weights -> default order'
  );

  // Multi_Element_Mastery_2 goes to the first 2 damage preferences
  const resolved = resolveElementStats(
    { Multi_Element_Mastery_2: 40, HP: 100 },
    ['Water', 'Earth', 'Fire', 'Air'],
    ['Fire', 'Water', 'Earth', 'Air']
  );
  assertEqual(resolved.Water_Mastery, 40, 'Multi_Element_Mastery_2 -> 1st pref');
  assertEqual(resolved.Earth_Mastery, 40, 'Multi_Element_Mastery_2 -> 2nd pref');
  assert(!('Multi_Element_Mastery_2' in resolved), 'random mastery key removed');
  assertEqual(resolved.HP, 100, 'other stats untouched');

  // Short preference lists get completed so _3/_4 do not lose stats
  const resolved3 = resolveElementStats(
    { Multi_Element_Mastery_3: 25 },
    ['Air'],
    []
  );
  assertEqual(resolved3.Air_Mastery, 25, 'completed prefs: 1st');
  assertEqual(resolved3.Fire_Mastery, 25, 'completed prefs: 2nd');
  assertEqual(resolved3.Water_Mastery, 25, 'completed prefs: 3rd');
  assert(!('Earth_Mastery' in resolved3), 'completed prefs: 4th element unused');

  // Global Elemental_Mastery stays AND spreads to all 4 elements
  const resolvedGlobal = resolveElementStats(
    { Elemental_Mastery: 10, Fire_Mastery: 5 },
    ['Fire', 'Water', 'Earth', 'Air'],
    ['Fire', 'Water', 'Earth', 'Air']
  );
  assertEqual(resolvedGlobal.Elemental_Mastery, 10, 'global mastery key kept');
  assertEqual(resolvedGlobal.Fire_Mastery, 15, 'global mastery added to existing');
  assertEqual(resolvedGlobal.Air_Mastery, 10, 'global mastery added to all elements');

  // Random resistances
  const resolvedRes = resolveElementStats(
    { Random_Elemental_Resistance_2: 15 },
    ['Fire', 'Water', 'Earth', 'Air'],
    ['Earth', 'Air', 'Fire', 'Water']
  );
  assertEqual(resolvedRes.Earth_Resistance, 15, 'random resistance -> 1st resist pref');
  assertEqual(resolvedRes.Air_Resistance, 15, 'random resistance -> 2nd resist pref');

  // resolveBuildStats accumulates then resolves
  const buildStats = resolveBuildStats(
    [{ HP: 10, Multi_Element_Mastery_1: 20 }, { HP: 5, Multi_Element_Mastery_1: 30 }],
    ['Fire', 'Water', 'Earth', 'Air'],
    ['Fire', 'Water', 'Earth', 'Air']
  );
  assertEqual(buildStats.HP, 15, 'build stats: HP summed');
  assertEqual(buildStats.Fire_Mastery, 50, 'build stats: random masteries summed then resolved');
}

// ---------------------------------------------------------------------------
// Synthetic fixture tests (ported/adapted from api/tests/test_solver.py)
// ---------------------------------------------------------------------------
function makeFixtureItems() {
  nextId = 1000;
  return [
    // Regular gear, level ~225, rarity 3 (available in every tier)
    makeItem({ slot: 'HEAD', stats: { HP: 50, AP: 1 }, difficulty: 30 }),
    makeItem({ slot: 'CHEST', stats: { HP: 80, MP: 1 }, difficulty: 20, source_type: 'harvest', drop_sources: [] }),
    makeItem({ slot: 'LEGS', stats: { HP: 60, MP: 1 }, difficulty: 25 }),
    makeItem({ slot: 'BACK', stats: { HP: 40, AP: 1 }, difficulty: 22 }),
    makeItem({ slot: 'NECK', stats: { HP: 30, AP: 1 }, difficulty: 28 }),
    makeItem({ slot: 'BELT', stats: { HP: 45 }, difficulty: 18 }),
    makeItem({ slot: 'SHOULDERS', stats: { HP: 35 }, difficulty: 21 }),
    // Rings: two duplicates by name (different ids/rarities) + one distinct
    makeItem({ item_id: 2001, name: 'Twin Ring', name_es: 'Anillo Gemelo', slot: 'LEFT_HAND', rarity: 3, stats: { HP: 90, AP: 1 }, difficulty: 20 }),
    makeItem({ item_id: 2002, name: 'Twin Ring L', name_es: 'Anillo Gemelo', slot: 'LEFT_HAND', rarity: 4, stats: { HP: 95, AP: 1 }, difficulty: 25 }),
    makeItem({ item_id: 2003, name: 'Other Ring', name_es: 'Otro Anillo', slot: 'LEFT_HAND', rarity: 3, stats: { HP: 40 }, difficulty: 15 }),
    // Weapons: a strong 2H, a weaker 1H, and a strong off-hand
    makeItem({ item_id: 2101, name: 'Big Hammer', slot: 'FIRST_WEAPON', blocks_second_weapon: true, stats: { HP: 200, AP: 2 }, difficulty: 30 }),
    makeItem({ item_id: 2102, name: 'Small Sword', slot: 'FIRST_WEAPON', stats: { HP: 60, AP: 1 }, difficulty: 20 }),
    makeItem({ item_id: 2103, name: 'Nice Shield', slot: 'SECOND_WEAPON', stats: { HP: 80, AP: 1 }, difficulty: 20 }),
    // Pet (level 0, always eligible)
    makeItem({ item_id: 2201, name: 'Test Pet', slot: 'PET', level: 0, rarity: 1, stats: { HP: 40 }, difficulty: 10 }),
    // Epic + Relic (rarity 7 / 5-with-relic-flag), extended level range
    makeItem({ item_id: 2301, name: 'Epic Helmet', slot: 'HEAD', level: 235, rarity: 7, is_epic: true, stats: { HP: 300, AP: 2 }, difficulty: 80 }),
    makeItem({ item_id: 2302, name: 'Relic Ring', slot: 'LEFT_HAND', name_es: 'Anillo Reliquia', level: 235, rarity: 5, is_relic: true, stats: { HP: 250, AP: 2 }, difficulty: 90 }),
    // Legendaries (rarity 5) for the medium max-1 constraint
    makeItem({ item_id: 2401, name: 'Legend Belt', slot: 'BELT', rarity: 5, stats: { HP: 150, AP: 1 }, difficulty: 60 }),
    makeItem({ item_id: 2402, name: 'Legend Shoulders', slot: 'SHOULDERS', rarity: 5, stats: { HP: 150, AP: 1 }, difficulty: 60 }),
    // Items that must be filtered out globally:
    makeItem({ item_id: 2501, name: 'Too Low', slot: 'HEAD', level: 100, stats: { HP: 999, AP: 9 }, difficulty: 1 }),
    makeItem({ item_id: 2502, name: 'Inusual Hat', slot: 'HEAD', rarity: 2, stats: { HP: 999, AP: 9 }, difficulty: 1 }),
    makeItem({ item_id: 2503, name: 'Souvenir', slot: 'HEAD', rarity: 6, is_relic: false, stats: { HP: 999, AP: 9 }, difficulty: 1 }),
    makeItem({ item_id: 2504, name: 'No Slot', slot: null, stats: { HP: 999 } }),
  ];
}

async function testSyntheticFixture() {
  section('synthetic fixture (ported from test_solver.py)');

  const fixture = makeFixtureItems();
  const weights = { HP: 1.0, AP: 2.0 };
  const builds = await solveBuild(fixture, {
    level_max: 230,
    stat_weights: weights,
  });

  // test_solver_returns_all_build_types (adapted to 5 tiers) + response shape
  checkResponseShape(builds, 'fixture');

  const damagePrefs = inferElementPreferencesFromWeights(weights);
  const resistPrefs = ['Fire', 'Water', 'Earth', 'Air'];

  for (const tier of TIERS) {
    const build = builds[tier];
    const label = `fixture/${tier}`;

    // test_solver_respects_max_level: normal items <= level_max,
    // high-rarity (5/6/7) may extend to level_max + 10; PET exempt
    for (const item of build.items) {
      if (item.slot === 'PET') continue;
      const cap = [5, 6, 7].includes(item.rarity) ? 240 : 230;
      assert(item.level <= cap, `${label}: item ${item.item_id} level ${item.level} <= ${cap}`);
    }

    // test_solver_respects_max_epic / max_relic
    assert(countEpics(build) <= 1, `${label}: at most 1 epic`);
    assert(countRelics(build) <= 1, `${label}: at most 1 relic`);

    // test_solver_one_item_per_slot (LEFT_HAND allows 2)
    checkSlots(build, label);

    // Ring duplicates by base name (name_es) can't both be equipped
    const ringNames = build.items
      .filter((i) => i.slot === 'LEFT_HAND')
      .map((i) => i.name_es || i.name_en || i.name);
    assert(
      new Set(ringNames).size === ringNames.length,
      `${label}: no duplicate ring base names (${ringNames.join(', ')})`
    );

    // 2H weapon excludes SECOND_WEAPON
    const fixtureById = new Map(fixture.map((i) => [i.item_id, i]));
    const has2H = build.items.some(
      (i) => i.slot === 'FIRST_WEAPON' && fixtureById.get(i.item_id).blocks_second_weapon
    );
    const hasSecond = build.items.some((i) => i.slot === 'SECOND_WEAPON');
    assert(!(has2H && hasSecond), `${label}: no 2H weapon together with second weapon`);

    // total_stats must match the resolved sum of the chosen items' stats
    checkTotalStats(build, damagePrefs, resistPrefs, label);

    // Globally filtered items must never appear
    for (const badId of [2501, 2502, 2503, 2504]) {
      assert(
        !build.items.some((i) => i.item_id === badId),
        `${label}: filtered-out item ${badId} not selected`
      );
    }

    // Serialized item shape (router contract)
    for (const item of build.items) {
      for (const key of [
        'item_id', 'name', 'name_es', 'name_en', 'name_fr', 'level', 'slot',
        'rarity', 'is_epic', 'is_relic', 'difficulty', 'gfx_id', 'stats',
        'source_type', 'has_gem_slot', 'metadata', 'drop_sources', 'alternatives',
      ]) {
        assert(key in item, `${label}: serialized item has '${key}'`);
      }
      assert(Array.isArray(item.alternatives), `${label}: alternatives is array`);
      assert(item.alternatives.length <= 3, `${label}: at most 3 alternatives`);
      for (const alt of item.alternatives) {
        assert(alt.slot === item.slot, `${label}: alternative in same slot`);
        assert('item_power' in alt && 'power_difference' in alt, `${label}: alternative has power fields`);
      }
    }
  }

  // Tier-specific rarity/epic/relic rules
  assert(
    builds.easy.items.every((i) => i.rarity <= 3 && !i.is_epic && !i.is_relic),
    'fixture/easy: only rarity <= 3, no epic/relic'
  );
  assert(
    builds.easy.items.every((i) => i.difficulty <= 48.0),
    'fixture/easy (lvl>=80): difficulty <= 48'
  );
  assert(countEpics(builds.medium) === 0 && countRelics(builds.medium) === 0,
    'fixture/medium: no epics, no relics');
  assert(
    builds.medium.items.filter((i) => i.rarity === 5).length <= 1,
    'fixture/medium: at most 1 legendary'
  );
  assert(countEpics(builds.hard_epic) === 1, 'fixture/hard_epic: exactly 1 epic (epics available)');
  assert(countRelics(builds.hard_epic) === 0, 'fixture/hard_epic: no relics');
  assert(countRelics(builds.hard_relic) === 1, 'fixture/hard_relic: exactly 1 relic (relics available)');
  assert(countEpics(builds.hard_relic) === 0, 'fixture/hard_relic: no epics');
  assert(countEpics(builds.full) === 1, 'fixture/full: exactly 1 epic');
  assert(countRelics(builds.full) === 1, 'fixture/full: exactly 1 relic');

  // total_difficulty is the AVERAGE item difficulty (Python behavior)
  for (const tier of TIERS) {
    const build = builds[tier];
    if (build.items.length > 0) {
      const avg = build.items.reduce((s, i) => s + i.difficulty, 0) / build.items.length;
      assertClose(build.total_difficulty, avg, `fixture/${tier}: total_difficulty is average difficulty`);
    }
  }
}

async function testParamFilters() {
  section('parameter filters (ignored ids, only_droppable, monster_types, pet/accessory)');

  const fixture = makeFixtureItems();
  const weights = { HP: 1.0, AP: 2.0 };

  // ignored_item_ids: the strong 2H hammer is excluded
  const buildsIgnored = await solveBuild(fixture, {
    level_max: 230,
    stat_weights: weights,
    ignored_item_ids: [2101],
  });
  for (const tier of TIERS) {
    assert(
      !buildsIgnored[tier].items.some((i) => i.item_id === 2101),
      `ignored/${tier}: item 2101 excluded`
    );
  }

  // include_pet=false: no PET slot in any build
  const buildsNoPet = await solveBuild(fixture, {
    level_max: 230,
    stat_weights: weights,
    include_pet: false,
  });
  for (const tier of TIERS) {
    assert(
      !buildsNoPet[tier].items.some((i) => i.slot === 'PET'),
      `no_pet/${tier}: no PET items`
    );
  }

  // only_droppable: CHEST item has no drop sources (harvest) -> excluded
  const buildsDrop = await solveBuild(fixture, {
    level_max: 230,
    stat_weights: weights,
    only_droppable: true,
  });
  for (const tier of TIERS) {
    assert(
      !buildsDrop[tier].items.some((i) => i.slot === 'CHEST'),
      `droppable/${tier}: harvest-only chest excluded`
    );
  }

  // monster_types: nothing drops from 'archmonster'; only non-drop items remain
  const buildsMt = await solveBuild(fixture, {
    level_max: 230,
    stat_weights: weights,
    monster_types: ['archmonster'],
  });
  for (const tier of TIERS) {
    for (const item of buildsMt[tier].items) {
      assert(
        item.source_type !== 'drop',
        `monster_types/${tier}: drop item ${item.item_id} from unselected type excluded`
      );
    }
  }

  // monster_types + only_droppable: nothing qualifies -> empty builds
  const buildsMtOd = await solveBuild(fixture, {
    level_max: 230,
    stat_weights: weights,
    monster_types: ['archmonster'],
    only_droppable: true,
  });
  for (const tier of TIERS) {
    assertEqual(
      buildsMtOd[tier].items.length, 0,
      `monster_types+droppable/${tier}: empty build`
    );
  }
}

async function testLowLevelAdaptive() {
  section('low level (< 80) adaptive rarity rules');

  nextId = 3000;
  const items = [
    makeItem({ slot: 'HEAD', level: 45, rarity: 1, stats: { HP: 20 }, difficulty: 10 }),
    makeItem({ slot: 'HEAD', level: 46, rarity: 4, stats: { HP: 60, AP: 1 }, difficulty: 50 }),
    makeItem({ slot: 'CHEST', level: 44, rarity: 3, stats: { HP: 30, MP: 1 }, difficulty: 20 }),
    makeItem({ slot: 'BELT', level: 45, rarity: 5, stats: { HP: 80, AP: 1 }, difficulty: 60 }),
  ];
  const builds = await solveBuild(items, { level_max: 50, stat_weights: { HP: 1.0, AP: 2.0 } });

  // EASY (lvl<80): rarity <= 3 only (no mythics/legendaries)
  assert(
    builds.easy.items.every((i) => i.rarity <= 3),
    'lowlvl/easy: only rarity <= 3'
  );
  // MEDIUM (lvl<80): rarity <= 3 only (no legendaries at all)
  assert(
    builds.medium.items.every((i) => i.rarity <= 3),
    'lowlvl/medium: only rarity <= 3'
  );
  // hard tiers may take the mythic/legendary
  assert(
    builds.full.items.some((i) => i.rarity >= 4),
    'lowlvl/full: higher rarities allowed'
  );
}

// ---------------------------------------------------------------------------
// Integration test with the real items.json
// ---------------------------------------------------------------------------
async function testIntegration() {
  section('integration: frontend/public/data/items.json');

  const itemsPath = path.resolve(__dirname, '..', 'public', 'data', 'items.json');
  const allItems = JSON.parse(readFileSync(itemsPath, 'utf-8'));
  console.log(`  loaded ${allItems.length} items`);

  const params = {
    level_max: 230,
    stat_weights: {
      AP: 5,
      MP: 4,
      HP: 1,
      Critical_Hit: 3,
      Distance_Mastery: 5,
      Fire_Mastery: 5,
      Water_Mastery: 3,
    },
    include_pet: true,
    include_accessory: true,
    only_droppable: false,
    damage_preferences: ['Fire', 'Water', 'Earth', 'Air'],
    resistance_preferences: ['Fire', 'Water', 'Earth', 'Air'],
    ignored_item_ids: [],
    monster_types: [],
  };

  const t0 = Date.now();
  const builds = await solveBuild(allItems, params);
  const elapsed = Date.now() - t0;
  console.log(`  solved all five tiers in ${elapsed} ms`);

  assert(elapsed < 30000, `integration: all five tiers solved in < 30s (took ${elapsed} ms)`);

  checkResponseShape(builds, 'integration');

  const itemsById = new Map(allItems.map((i) => [i.item_id, i]));

  for (const tier of TIERS) {
    const build = builds[tier];
    const label = `integration/${tier}`;
    console.log(
      `  ${tier}: ${build.items.length} items, avg difficulty ${build.total_difficulty.toFixed(1)}`
    );

    assert(build.items.length > 0, `${label}: build is not empty`);
    assert(build.items.length <= 15, `${label}: at most 15 items (14 slots + 2nd ring)`);

    // Slot validity
    checkSlots(build, label);

    // Level constraints
    for (const item of build.items) {
      if (item.slot === 'PET') continue;
      const cap = [5, 6, 7].includes(item.rarity) ? 240 : 230;
      assert(item.level <= cap, `${label}: item ${item.item_id} level ${item.level} <= ${cap}`);
      assert(item.level >= 220, `${label}: item ${item.item_id} level ${item.level} >= 220`);
    }

    // Epic/relic limits per tier
    const epics = countEpics(build);
    const relics = countRelics(build);
    if (tier === 'easy' || tier === 'medium') {
      assert(epics === 0, `${label}: no epics (got ${epics})`);
      assert(relics === 0, `${label}: no relics (got ${relics})`);
    } else if (tier === 'hard_epic') {
      assert(epics === 1, `${label}: exactly 1 epic (got ${epics})`);
      assert(relics === 0, `${label}: no relics (got ${relics})`);
    } else if (tier === 'hard_relic') {
      assert(relics === 1, `${label}: exactly 1 relic (got ${relics})`);
      assert(epics === 0, `${label}: no epics (got ${epics})`);
    } else if (tier === 'full') {
      assert(epics === 1, `${label}: exactly 1 epic (got ${epics})`);
      assert(relics === 1, `${label}: exactly 1 relic (got ${relics})`);
    }

    // Tier rarity rules
    if (tier === 'easy') {
      assert(
        build.items.every((i) => i.rarity <= 3 && i.difficulty <= 48.0),
        `${label}: rarity <= 3 and difficulty <= 48`
      );
    }
    if (tier === 'medium') {
      assert(
        build.items.filter((i) => i.rarity === 5).length <= 1,
        `${label}: at most 1 legendary`
      );
    }

    // 2H weapon excludes second weapon (check via source data flag)
    const has2H = build.items.some((i) => {
      const src = itemsById.get(i.item_id);
      return i.slot === 'FIRST_WEAPON' && src && src.blocks_second_weapon;
    });
    const hasSecond = build.items.some((i) => i.slot === 'SECOND_WEAPON');
    assert(!(has2H && hasSecond), `${label}: no 2H weapon together with second weapon`);

    // No duplicate ring base names
    const ringNames = build.items
      .filter((i) => i.slot === 'LEFT_HAND')
      .map((i) => i.name_es || i.name_en || i.name);
    assert(
      new Set(ringNames).size === ringNames.length,
      `${label}: no duplicate ring base names`
    );

    // total_stats equals resolved sum of chosen items' stats
    checkTotalStats(build, params.damage_preferences, params.resistance_preferences, label);
  }
}

// ---------------------------------------------------------------------------
// Runner
// ---------------------------------------------------------------------------
async function main() {
  const t0 = Date.now();
  testElementResolver();
  await testSyntheticFixture();
  await testParamFilters();
  await testLowLevelAdaptive();
  await testIntegration();

  console.log(`\n${passed} passed, ${failed} failed (${Date.now() - t0} ms total)`);
  if (failed > 0) {
    console.error('\nFailures:');
    for (const f of failures) console.error(` - ${f}`);
    process.exit(1);
  }
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
