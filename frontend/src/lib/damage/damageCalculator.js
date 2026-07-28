/**
 * Wakfu Damage Calculator (browser port of api/app/services/damage_calculator.py
 * + api/app/routers/damage_calculator.py).
 *
 * Calculates estimated damage output based on build stats and enemy resistances.
 * Implements the official Wakfu damage formulas from the wiki.
 *
 * Formula:
 * Elemental Damage = Base Damage * (Backstab Bonus) *
 *                    (1 + [Elemental Mastery + Secondary Mastery]/100) *
 *                    (1 - [Elemental Resistance %])
 *
 * Where:
 * - Elemental Resistance % = 1 - 0.8^(Flat Resist/100)
 * - Secondary Mastery = Critical + Berserk + Melee/Distance + Single Target/AoE
 * - Final Damage = Elemental Damage * (1 + Final Damage Bonus/100)
 *
 * The three exported entry points mirror the FastAPI endpoints exactly
 * (same key names, nesting and rounding):
 * - estimateDamage(...)                  -> POST /damage/estimate
 * - calculateWithCustomResistances(...)  -> POST /damage/custom-resistances
 * - calculateDetailed(...)               -> POST /damage/calculate
 */

/**
 * Python-compatible round() (banker's rounding: ties go to the nearest even).
 * Matches CPython's round(value, ndigits) for the value ranges used here.
 */
function pyRound(value, ndigits = 0) {
  if (!Number.isFinite(value)) return value;
  const m = Math.pow(10, ndigits);
  const scaled = ndigits === 0 ? value : value * m;
  const floor = Math.floor(scaled);
  const diff = scaled - floor;
  let rounded;
  if (diff > 0.5) {
    rounded = floor + 1;
  } else if (diff < 0.5) {
    rounded = floor;
  } else {
    // Exact tie: round half to even
    rounded = floor % 2 === 0 ? floor : floor + 1;
  }
  return ndigits === 0 ? rounded : rounded / m;
}

/** Default values mirroring the Python DamageInput pydantic model. */
const DAMAGE_INPUT_DEFAULTS = {
  base_spell_damage: 100.0,
  elemental_mastery: 0.0,
  // Secondary masteries
  critical_mastery: 0.0,
  berserk_mastery: 0.0,
  melee_mastery: 0.0,
  distance_mastery: 0.0,
  rear_mastery: 0.0,
  single_target_mastery: 0.0,
  aoe_mastery: 0.0,
  // Target resistance (FLAT value, not %)
  flat_resistance: 0.0,
  // Combat conditions
  is_critical: false,
  is_berserk: false, // Attacker below 50% HP
  is_backstab: false, // Attacking from behind
  is_sidestab: false, // Attacking from side
  is_melee: true, // 2 cells or closer (default melee)
  is_single_target: true, // Single target spell (default)
  // Final damage modifiers
  final_damage_bonus: 0.0,
  // Legacy support
  armor: 0.0,
};

/**
 * Apply DamageInput defaults (unknown extra keys are ignored, like pydantic).
 */
function normalizeDamageInput(params = {}) {
  const input = {};
  for (const key of Object.keys(DAMAGE_INPUT_DEFAULTS)) {
    input[key] = params[key] !== undefined && params[key] !== null
      ? params[key]
      : DAMAGE_INPUT_DEFAULTS[key];
  }
  return input;
}

/**
 * Convert flat resistance to percentage using the Wakfu formula
 * Elemental Resistance % = 1 - 0.8^(Flat Resist/100)
 *
 * Examples:
 * - 0 flat resist = 0% resist
 * - 100 flat resist = 20% resist
 * - 200 flat resist = 36% resist
 * - 500 flat resist = 67.23% resist
 */
export function convertFlatResistanceToPercent(flatResistance) {
  if (flatResistance <= 0) {
    return 0.0;
  }
  return (1 - Math.pow(0.8, flatResistance / 100)) * 100;
}

/**
 * Core damage calculation (port of calculate_damage). Expects a normalized
 * DamageInput-shaped object; returns the DamageOutput dict shape.
 */
function calculateDamage(params) {
  // Step 1: Backstab bonus
  let backstabBonus = 1.0;
  if (params.is_backstab) {
    backstabBonus = 1.25;
  } else if (params.is_sidestab) {
    backstabBonus = 1.10;
  }

  // Step 2: Total secondary mastery (additive)
  let secondaryMastery = 0.0;
  if (params.is_critical) {
    secondaryMastery += params.critical_mastery;
  }
  if (params.is_berserk) {
    secondaryMastery += params.berserk_mastery;
  }
  if (params.is_melee) {
    secondaryMastery += params.melee_mastery;
  } else {
    secondaryMastery += params.distance_mastery;
  }
  if (params.is_backstab || params.is_sidestab) {
    secondaryMastery += params.rear_mastery;
  }
  if (params.is_single_target) {
    secondaryMastery += params.single_target_mastery;
  } else {
    secondaryMastery += params.aoe_mastery;
  }

  const totalMastery = params.elemental_mastery + secondaryMastery;

  // Step 3: Convert flat resistance to percentage
  const resistancePercent = convertFlatResistanceToPercent(params.flat_resistance);
  const resistanceMultiplier = 1 - resistancePercent / 100;

  // Step 4: Elemental damage (official formula)
  const elementalDamage =
    params.base_spell_damage *
    backstabBonus *
    (1 + totalMastery / 100) *
    resistanceMultiplier;

  // Step 5: Final damage modifiers
  const finalDamage = elementalDamage * (1 + params.final_damage_bonus / 100);

  // Step 6: Armor (subtracts from final damage, cannot go below 0)
  const damageAfterArmor = Math.max(0, finalDamage - params.armor);

  return {
    total_mastery: pyRound(totalMastery),
    preliminary_damage: pyRound(elementalDamage),
    effective_damage: pyRound(elementalDamage),
    final_damage: pyRound(finalDamage),
    damage_after_armor: pyRound(damageAfterArmor),
    details: {
      flat_resistance: params.flat_resistance,
      resistance_percent: pyRound(resistancePercent, 2),
      backstab_bonus: backstabBonus,
      secondary_mastery: pyRound(secondaryMastery),
      is_critical: params.is_critical,
      is_berserk: params.is_berserk,
      is_melee: params.is_melee,
      is_single_target: params.is_single_target,
      final_damage_bonus: params.final_damage_bonus,
    },
  };
}

/**
 * POST /damage/calculate
 *
 * Calculate damage with specific parameters (full control over all
 * DamageInput fields, snake_case, all optional with the Python defaults).
 */
export function calculateDetailed(params = {}) {
  return calculateDamage(normalizeDamageInput(params));
}

/**
 * POST /damage/estimate
 *
 * Estimate damage output for each element at different resistance levels.
 *
 * @param {Object} buildStats - dict of build stat totals (Fire_Mastery, ...)
 * @param {Object} [options]
 * @param {number} [options.baseSpellDamage=100.0]
 * @param {number[]|null} [options.resistancePresets=null] - flat resistance values (default [0,100,200,300,400,500])
 * @param {boolean} [options.includeCritical=true]
 * @param {boolean} [options.isMelee=true] - true = Melee (<=2 cells), false = Distance (>=3 cells)
 */
export function estimateDamage(buildStats, options = {}) {
  const {
    baseSpellDamage = 100.0,
    resistancePresets = null,
    includeCritical = true,
    isMelee = true,
  } = options;

  const presets = resistancePresets != null ? resistancePresets : [0, 100, 200, 300, 400, 500];

  const elements = [
    ['Fire', 'Fire_Mastery'],
    ['Water', 'Water_Mastery'],
    ['Earth', 'Earth_Mastery'],
    ['Air', 'Air_Mastery'],
  ];

  const stats = buildStats || {};
  const criticalMastery = stats.Critical_Mastery ?? 0;
  const meleeMastery = stats.Melee_Mastery ?? 0;
  const distanceMastery = stats.Distance_Mastery ?? 0;
  const rearMastery = stats.Rear_Mastery ?? 0;
  const elementalMastery = stats.Elemental_Mastery ?? 0;

  const estimates = [];

  for (const [elementName, masteryKey] of elements) {
    const elementMastery = stats[masteryKey] ?? 0;
    const totalElementMastery = elementMastery + elementalMastery;

    const resistanceScenarios = [];

    for (const flatResistance of presets) {
      // Normal hit (single target)
      const normalResult = calculateDamage(normalizeDamageInput({
        base_spell_damage: baseSpellDamage,
        elemental_mastery: totalElementMastery,
        melee_mastery: isMelee ? meleeMastery : 0,
        distance_mastery: !isMelee ? distanceMastery : 0,
        flat_resistance: flatResistance,
        is_critical: false,
        is_melee: isMelee,
        is_single_target: true,
      }));

      // Critical hit (single target)
      const critResult = calculateDamage(normalizeDamageInput({
        base_spell_damage: baseSpellDamage,
        elemental_mastery: totalElementMastery,
        critical_mastery: criticalMastery,
        melee_mastery: isMelee ? meleeMastery : 0,
        distance_mastery: !isMelee ? distanceMastery : 0,
        flat_resistance: flatResistance,
        is_critical: true,
        is_melee: isMelee,
        is_single_target: true,
      }));

      // Backstab (1.25x backstab bonus)
      const backstabResult = calculateDamage(normalizeDamageInput({
        base_spell_damage: baseSpellDamage,
        elemental_mastery: totalElementMastery,
        melee_mastery: isMelee ? meleeMastery : 0,
        distance_mastery: !isMelee ? distanceMastery : 0,
        rear_mastery: rearMastery,
        flat_resistance: flatResistance,
        is_critical: false,
        is_melee: isMelee,
        is_backstab: true,
        is_single_target: true,
      }));

      // Backstab + critical
      const backstabCritResult = calculateDamage(normalizeDamageInput({
        base_spell_damage: baseSpellDamage,
        elemental_mastery: totalElementMastery,
        critical_mastery: criticalMastery,
        melee_mastery: isMelee ? meleeMastery : 0,
        distance_mastery: !isMelee ? distanceMastery : 0,
        rear_mastery: rearMastery,
        flat_resistance: flatResistance,
        is_critical: true,
        is_melee: isMelee,
        is_backstab: true,
        is_single_target: true,
      }));

      // Only show positive damage (no healing enemy)
      const normalDamage = Math.max(0, normalResult.final_damage);
      const criticalDamage = includeCritical ? Math.max(0, critResult.final_damage) : null;
      const backstabDamage = Math.max(0, backstabResult.final_damage);
      const backstabCriticalDamage = includeCritical
        ? Math.max(0, backstabCritResult.final_damage)
        : null;

      const resistancePercent = convertFlatResistanceToPercent(flatResistance);

      resistanceScenarios.push({
        flat_resistance: flatResistance,
        resistance_percent: pyRound(resistancePercent, 1),
        normal_damage: normalDamage,
        critical_damage: criticalDamage,
        backstab_damage: backstabDamage,
        backstab_critical_damage: backstabCriticalDamage,
      });
    }

    estimates.push({
      element: elementName,
      base_mastery: totalElementMastery,
      resistance_scenarios: resistanceScenarios,
    });
  }

  return {
    estimates,
    base_spell_damage: baseSpellDamage,
    resistance_presets: presets,
    is_melee: isMelee,
  };
}

/**
 * POST /damage/custom-resistances
 *
 * Calculate average damage per element against an enemy with specific
 * FLAT resistances (e.g. {Fire: 200, Water: 150}).
 */
export function calculateWithCustomResistances(buildStats, enemyResistances, baseSpellDamage = 100.0) {
  const elements = {
    Fire: 'Fire_Mastery',
    Water: 'Water_Mastery',
    Earth: 'Earth_Mastery',
    Air: 'Air_Mastery',
  };

  const stats = buildStats || {};
  const resistances = enemyResistances || {};
  const elementalMastery = stats.Elemental_Mastery ?? 0;
  const criticalMastery = stats.Critical_Mastery ?? 0;
  const meleeMastery = stats.Melee_Mastery ?? 0;

  const damagePerElement = {};

  for (const [elementName, masteryKey] of Object.entries(elements)) {
    const elementMastery = stats[masteryKey] ?? 0;
    const totalElementMastery = elementMastery + elementalMastery;
    const flatResistance = resistances[elementName] ?? 0;

    // Normal damage (melee, single target)
    const normalResult = calculateDamage(normalizeDamageInput({
      base_spell_damage: baseSpellDamage,
      elemental_mastery: totalElementMastery,
      melee_mastery: meleeMastery,
      flat_resistance: flatResistance,
      is_critical: false,
      is_melee: true,
      is_single_target: true,
    }));
    const normalDamage = Math.max(0, normalResult.final_damage);

    // Critical damage (melee, single target)
    const critResult = calculateDamage(normalizeDamageInput({
      base_spell_damage: baseSpellDamage,
      elemental_mastery: totalElementMastery,
      critical_mastery: criticalMastery,
      melee_mastery: meleeMastery,
      flat_resistance: flatResistance,
      is_critical: true,
      is_melee: true,
      is_single_target: true,
    }));
    const critDamage = Math.max(0, critResult.final_damage);

    const resistancePercent = convertFlatResistanceToPercent(flatResistance);

    damagePerElement[elementName] = {
      normal: normalDamage,
      critical: critDamage,
      average: (normalDamage + critDamage) / 2,
      flat_resistance: flatResistance,
      resistance_percent: pyRound(resistancePercent, 1),
    };
  }

  return {
    damage_per_element: damagePerElement,
    enemy_resistances: resistances,
    base_spell_damage: baseSpellDamage,
  };
}
