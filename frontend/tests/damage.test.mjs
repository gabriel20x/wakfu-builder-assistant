/**
 * Tests for frontend/src/lib/damage/damageCalculator.js
 *
 * Run with: node frontend/tests/damage.test.mjs
 *
 * Assertions are ported from api/tests/test_damage_calculator.py.
 * NOTE: several tests in that Python file target an older DamageInput API
 * (resistances_target, critical_hit, backstab_or_position_mod, damage_reduction,
 * fractional final_damage_bonus semantics) whose fields pydantic silently
 * ignores — those assertions do not pass against the CURRENT Python service
 * either. Here they are ported against the current service's actual outputs,
 * captured in fixtures/python_reference.json by running the real Python code
 * (see the "exact parity" section, which compares full response shapes
 * key-for-key and in key order).
 */

import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

import {
  estimateDamage,
  calculateWithCustomResistances,
  calculateDetailed,
} from '../src/lib/damage/damageCalculator.js';

const here = dirname(fileURLToPath(import.meta.url));
const REF = JSON.parse(readFileSync(join(here, 'fixtures', 'python_reference.json'), 'utf-8'));

let passed = 0;
let failed = 0;

function test(name, fn) {
  try {
    fn();
    passed += 1;
    console.log(`  ok - ${name}`);
  } catch (err) {
    failed += 1;
    console.error(`  FAIL - ${name}`);
    console.error(`    ${err.message}`);
  }
}

function assertEqual(actual, expected, label = 'value') {
  if (actual !== expected) {
    throw new Error(`${label}: expected ${JSON.stringify(expected)}, got ${JSON.stringify(actual)}`);
  }
}

function assertTrue(cond, label = 'condition') {
  if (!cond) throw new Error(`${label}: expected truthy`);
}

/**
 * Exact structural equality: same values, same nesting AND same key order,
 * exactly as the FastAPI router would serialize it.
 */
function assertJsonExact(actual, expected, label = 'response') {
  const a = JSON.stringify(actual);
  const e = JSON.stringify(expected);
  if (a !== e) {
    // Find first divergence for a readable error
    let i = 0;
    while (i < Math.min(a.length, e.length) && a[i] === e[i]) i += 1;
    const ctx = (s) => s.slice(Math.max(0, i - 60), i + 60);
    throw new Error(`${label} mismatch at char ${i}:\n    expected ...${ctx(e)}...\n    actual   ...${ctx(a)}...`);
  }
}

// ---------------------------------------------------------------------------
console.log('calculateDetailed (POST /damage/calculate)');

test('basic damage calculation without modifiers (test_basic_damage_calculation)', () => {
  const result = calculateDetailed({ base_spell_damage: 100.0, elemental_mastery: 1000.0 });
  // With 1000 mastery: 100 * (1 + 1000/100) = 1100
  assertEqual(result.total_mastery, 1000, 'total_mastery');
  assertEqual(result.preliminary_damage, 1100, 'preliminary_damage');
  assertEqual(result.final_damage, 1100, 'final_damage');
});

test('damage with flat resistance 200 (test_damage_with_resistance, current formula)', () => {
  // 200 flat resist -> 1 - 0.8^2 = 36% -> 1100 * 0.64 = 704
  const result = calculateDetailed({
    base_spell_damage: 100.0,
    elemental_mastery: 1000.0,
    flat_resistance: 200.0,
  });
  assertEqual(result.effective_damage, 704, 'effective_damage');
  assertEqual(result.details.resistance_percent, 36, 'details.resistance_percent');
});

test('critical hit damage (test_critical_damage, current formula)', () => {
  // Total mastery: 1000 + 400 = 1400 -> 100 * (1 + 1400/100) = 1500
  const result = calculateDetailed({
    base_spell_damage: 100.0,
    elemental_mastery: 1000.0,
    is_critical: true,
    critical_mastery: 400.0,
  });
  assertEqual(result.total_mastery, 1400, 'total_mastery');
  assertEqual(result.preliminary_damage, 1500, 'preliminary_damage');
  assertEqual(result.final_damage, 1500, 'final_damage');
});

test('damage reduction from armor (test_damage_with_armor)', () => {
  // 100 * (1 + 500/100) = 600; after armor: 600 - 200 = 400
  const result = calculateDetailed({
    base_spell_damage: 100.0,
    elemental_mastery: 500.0,
    armor: 200.0,
  });
  assertEqual(result.final_damage, 600, 'final_damage');
  assertEqual(result.damage_after_armor, 400, 'damage_after_armor');
});

test('backstab bonus 1.25 with rear mastery', () => {
  const result = calculateDetailed({
    base_spell_damage: 100.0,
    elemental_mastery: 1000.0,
    is_backstab: true,
    rear_mastery: 250.0,
    flat_resistance: 150.0,
  });
  assertEqual(result.details.backstab_bonus, 1.25, 'backstab_bonus');
  assertEqual(result.details.secondary_mastery, 250, 'secondary_mastery');
  assertJsonExact(result, REF.calc_backstab, 'backstab response');
});

test('sidestab bonus 1.10 with rear mastery', () => {
  const result = calculateDetailed({
    base_spell_damage: 100.0,
    elemental_mastery: 800.0,
    is_sidestab: true,
    rear_mastery: 100.0,
  });
  assertEqual(result.details.backstab_bonus, 1.1, 'backstab_bonus');
  assertJsonExact(result, REF.calc_sidestab, 'sidestab response');
});

test('exact parity with Python: calc_basic / calc_resist200 / calc_crit / calc_armor / calc_defaults', () => {
  assertJsonExact(
    calculateDetailed({ base_spell_damage: 100.0, elemental_mastery: 1000.0 }),
    REF.calc_basic, 'calc_basic',
  );
  assertJsonExact(
    calculateDetailed({ base_spell_damage: 100.0, elemental_mastery: 1000.0, flat_resistance: 200.0 }),
    REF.calc_resist200, 'calc_resist200',
  );
  assertJsonExact(
    calculateDetailed({ base_spell_damage: 100.0, elemental_mastery: 1000.0, is_critical: true, critical_mastery: 400.0 }),
    REF.calc_crit, 'calc_crit',
  );
  assertJsonExact(
    calculateDetailed({ base_spell_damage: 100.0, elemental_mastery: 500.0, armor: 200.0 }),
    REF.calc_armor, 'calc_armor',
  );
  assertJsonExact(calculateDetailed(), REF.calc_defaults, 'calc_defaults');
  assertJsonExact(calculateDetailed({}), REF.calc_defaults, 'calc_defaults ({})');
});

test('exact parity with Python: all fields set at once (calc_full)', () => {
  const result = calculateDetailed({
    base_spell_damage: 123.0,
    elemental_mastery: 987.0,
    critical_mastery: 321.0,
    berserk_mastery: 111.0,
    melee_mastery: 0.0,
    distance_mastery: 222.0,
    rear_mastery: 99.0,
    single_target_mastery: 0.0,
    aoe_mastery: 77.0,
    flat_resistance: 333.0,
    is_critical: true,
    is_berserk: true,
    is_backstab: true,
    is_melee: false,
    is_single_target: false,
    final_damage_bonus: 17.0,
    armor: 50.0,
  });
  assertJsonExact(result, REF.calc_full, 'calc_full');
});

// ---------------------------------------------------------------------------
console.log('estimateDamage (POST /damage/estimate)');

const ESTIMATE_BUILD_STATS = {
  Fire_Mastery: 1200,
  Water_Mastery: 800,
  Earth_Mastery: 1000,
  Air_Mastery: 600,
  Elemental_Mastery: 400,
  Critical_Mastery: 300,
};

test('elemental damage estimation structure (test_estimate_elemental_damage)', () => {
  const response = estimateDamage(ESTIMATE_BUILD_STATS, {
    baseSpellDamage: 100.0,
    resistancePresets: [0, 100, 200],
    includeCritical: true,
  });

  // Should return 4 elements
  assertEqual(response.estimates.length, 4, 'estimates.length');

  // Check Fire element
  const fire = response.estimates.find((r) => r.element === 'Fire');
  assertEqual(fire.base_mastery, 1600, 'Fire base_mastery'); // 1200 + 400
  assertEqual(fire.resistance_scenarios.length, 3, 'Fire scenarios length'); // 0, 100, 200

  // Damage decreases with resistance
  const s = fire.resistance_scenarios;
  assertTrue(s[0].normal_damage > s[1].normal_damage, 'damage decreases 0 -> 100');
  assertTrue(s[1].normal_damage > s[2].normal_damage, 'damage decreases 100 -> 200');
});

test('exact parity with Python: melee estimate with crits (estimate_basic)', () => {
  const response = estimateDamage(ESTIMATE_BUILD_STATS, {
    baseSpellDamage: 100.0,
    resistancePresets: [0, 100, 200],
    includeCritical: true,
    isMelee: true,
  });
  assertJsonExact(response, REF.estimate_basic, 'estimate_basic');
});

test('exact parity with Python: distance estimate, no crit, default presets (estimate_distance_nocrit)', () => {
  const response = estimateDamage({
    Fire_Mastery: 850.0,
    Air_Mastery: 620.0,
    Elemental_Mastery: 150.0,
    Critical_Mastery: 410.0,
    Distance_Mastery: 275.0,
    Melee_Mastery: 180.0,
    Rear_Mastery: 130.0,
    Berserk_Mastery: 90.0,
  }, {
    includeCritical: false,
    isMelee: false,
  });
  // critical damage entries must be null when includeCritical is false
  assertEqual(response.estimates[0].resistance_scenarios[0].critical_damage, null, 'critical_damage null');
  // default presets echoed in the response
  assertEqual(response.resistance_presets.join(','), '0,100,200,300,400,500', 'default resistance_presets');
  assertJsonExact(response, REF.estimate_distance_nocrit, 'estimate_distance_nocrit');
});

test('estimateDamage defaults (no options object)', () => {
  const response = estimateDamage(ESTIMATE_BUILD_STATS);
  assertEqual(response.base_spell_damage, 100, 'base_spell_damage default');
  assertEqual(response.is_melee, true, 'is_melee default');
  assertEqual(response.resistance_presets.length, 6, 'default presets length');
  assertTrue(response.estimates[0].resistance_scenarios[0].critical_damage !== null, 'includeCritical default true');
});

// ---------------------------------------------------------------------------
console.log('calculateWithCustomResistances (POST /damage/custom-resistances)');

test('average damage per element (test_calculate_average_damage)', () => {
  const buildStats = {
    Fire_Mastery: 1200,
    Water_Mastery: 800,
    Elemental_Mastery: 400,
    Critical_Mastery: 300,
    Melee_Mastery: 200,
  };
  const enemyResistances = { Fire: 200, Water: 100, Earth: 150, Air: 50 };

  const response = calculateWithCustomResistances(buildStats, enemyResistances, 100.0);
  const results = response.damage_per_element;

  // All 4 elements present
  for (const el of ['Fire', 'Water', 'Earth', 'Air']) {
    assertTrue(el in results, `${el} in results`);
  }

  // Each element has normal, critical and average
  const fire = results.Fire;
  assertTrue('normal' in fire, 'normal in Fire');
  assertTrue('critical' in fire, 'critical in Fire');
  assertTrue('average' in fire, 'average in Fire');

  // Critical should be higher than normal
  assertTrue(fire.critical > fire.normal, 'critical > normal');
});

test('exact parity with Python: full custom-resistances response (custom_res)', () => {
  const response = calculateWithCustomResistances(
    {
      Fire_Mastery: 1200.0,
      Water_Mastery: 800.0,
      Elemental_Mastery: 400.0,
      Critical_Mastery: 300.0,
      Melee_Mastery: 200.0,
    },
    { Fire: 200.0, Water: 100.0, Earth: 150.0, Air: 50.0 },
    100.0,
  );
  // Spot-check the Python-computed numbers
  assertEqual(response.damage_per_element.Fire.normal, 1216, 'Fire normal');
  assertEqual(response.damage_per_element.Fire.critical, 1408, 'Fire critical');
  assertEqual(response.damage_per_element.Fire.average, 1312, 'Fire average');
  assertEqual(response.damage_per_element.Earth.average, 608.5, 'Earth average');
  assertEqual(response.damage_per_element.Air.resistance_percent, 10.6, 'Air resistance_percent');
  assertJsonExact(response, REF.custom_res, 'custom_res');
});

test('default baseSpellDamage is 100.0', () => {
  const response = calculateWithCustomResistances({ Fire_Mastery: 100 }, { Fire: 0 });
  assertEqual(response.base_spell_damage, 100, 'base_spell_damage');
  assertEqual(response.damage_per_element.Fire.normal, 200, 'Fire normal at 0 resist');
});

// ---------------------------------------------------------------------------
console.log('');
console.log(`${passed} passed, ${failed} failed`);
if (failed > 0) process.exit(1);
