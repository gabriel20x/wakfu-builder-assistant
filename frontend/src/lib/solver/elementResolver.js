/**
 * Element Resolver
 *
 * Faithful port of api/app/services/element_resolver.py.
 *
 * Resolves random elemental stats (damages and resistances) based on user
 * preferences. When an item has stats like "Multi_Element_Mastery_3"
 * (3 random elemental masteries), this module applies them to the user's
 * preferred elements in order.
 */

// Mapping of random stat keys to their base stat type.
// NOTE: insertion order matters (mirrors Python dict iteration order).
export const RANDOM_MASTERY_STATS = {
  Multi_Element_Mastery_1: 1,
  Multi_Element_Mastery_2: 2,
  Multi_Element_Mastery_3: 3,
  Multi_Element_Mastery_4: 4,
  Elemental_Mastery_1_elements: 1,
  Elemental_Mastery_2_elements: 2,
  Elemental_Mastery_3_elements: 3,
  Elemental_Mastery_4_elements: 4,
  Random_Elemental_Mastery: 1,
};

export const RANDOM_RESISTANCE_STATS = {
  Random_Elemental_Resistance_1: 1,
  Random_Elemental_Resistance_2: 2,
  Random_Elemental_Resistance_3: 3,
  Random_Elemental_Resistance_4: 4,
  Elemental_Resistance_1_elements: 1,
  Elemental_Resistance_2_elements: 2,
  Elemental_Resistance_3_elements: 3,
  Elemental_Resistance_4_elements: 4,
  Random_Elemental_Resistance: 1,
};

// Global elemental stats
export const GLOBAL_MASTERY_STATS = ['Elemental_Mastery'];
export const GLOBAL_RESISTANCE_STATS = ['Elemental_Resistance'];

const ALL_ELEMENTS = ['Fire', 'Water', 'Earth', 'Air'];

/**
 * Infer user's element preferences from stat_weights.
 *
 * Returns ordered list based on weights:
 * - Elements with weight > 0 first (ordered by weight descending, ties alphabetically)
 * - Then remaining elements (in Fire, Water, Earth, Air order)
 *
 * @param {Object<string, number>} statWeights
 * @returns {string[]}
 */
export function inferElementPreferencesFromWeights(statWeights) {
  const elementWeights = [];
  for (const element of ALL_ELEMENTS) {
    const masteryKey = `${element}_Mastery`;
    if (
      Object.prototype.hasOwnProperty.call(statWeights, masteryKey) &&
      statWeights[masteryKey] > 0
    ) {
      elementWeights.push([element, statWeights[masteryKey]]);
    }
  }

  // Sort by weight (descending), then alphabetically (ascending)
  elementWeights.sort((a, b) => {
    if (b[1] !== a[1]) return b[1] - a[1];
    return a[0] < b[0] ? -1 : a[0] > b[0] ? 1 : 0;
  });

  const preferences = elementWeights.map(([elem]) => elem);
  for (const elem of ALL_ELEMENTS) {
    if (!preferences.includes(elem)) {
      preferences.push(elem);
    }
  }

  return preferences;
}

/**
 * Complete a preference list so it always contains the 4 elements.
 */
function completePreferences(preferences) {
  const complete = preferences ? preferences.slice() : [];
  for (const elem of ALL_ELEMENTS) {
    if (!complete.includes(elem)) {
      complete.push(elem);
    }
  }
  return complete;
}

/**
 * Resolve random elemental stats based on user preferences.
 *
 * @param {Object<string, number>} stats - item stats (may contain random elemental stats)
 * @param {string[]} damagePreferences - ordered element preferences for damage
 * @param {string[]} resistancePreferences - ordered element preferences for resistances
 * @returns {Object<string, number>} resolved stats (random stats converted to specific elements)
 */
export function resolveElementStats(stats, damagePreferences, resistancePreferences) {
  const resolvedStats = { ...stats };

  const completeDamagePrefs = completePreferences(damagePreferences);
  const completeResistancePrefs = completePreferences(resistancePreferences);

  // Process random mastery stats
  for (const [randomStat, numElements] of Object.entries(RANDOM_MASTERY_STATS)) {
    if (Object.prototype.hasOwnProperty.call(resolvedStats, randomStat)) {
      const value = resolvedStats[randomStat];
      delete resolvedStats[randomStat];

      // Apply to the first N preferred elements
      for (let i = 0; i < numElements; i++) {
        const element = completeDamagePrefs[i];
        const statKey = `${element}_Mastery`;
        resolvedStats[statKey] = (resolvedStats[statKey] || 0) + value;
      }
    }
  }

  // Process random resistance stats
  for (const [randomStat, numElements] of Object.entries(RANDOM_RESISTANCE_STATS)) {
    if (Object.prototype.hasOwnProperty.call(resolvedStats, randomStat)) {
      const value = resolvedStats[randomStat];
      delete resolvedStats[randomStat];

      for (let i = 0; i < numElements; i++) {
        const element = completeResistancePrefs[i];
        const statKey = `${element}_Resistance`;
        resolvedStats[statKey] = (resolvedStats[statKey] || 0) + value;
      }
    }
  }

  // Process global mastery stats (apply to all elements; the global stat itself is kept)
  for (const globalStat of GLOBAL_MASTERY_STATS) {
    if (Object.prototype.hasOwnProperty.call(resolvedStats, globalStat)) {
      const value = resolvedStats[globalStat];

      for (const element of completeDamagePrefs) {
        const statKey = `${element}_Mastery`;
        resolvedStats[statKey] = (resolvedStats[statKey] || 0) + value;
      }
    }
  }

  // Process global resistance stats (apply to all elements; the global stat itself is kept)
  for (const globalStat of GLOBAL_RESISTANCE_STATS) {
    if (Object.prototype.hasOwnProperty.call(resolvedStats, globalStat)) {
      const value = resolvedStats[globalStat];

      for (const element of completeResistancePrefs) {
        const statKey = `${element}_Resistance`;
        resolvedStats[statKey] = (resolvedStats[statKey] || 0) + value;
      }
    }
  }

  return resolvedStats;
}

/**
 * Resolve stats for an entire build (all items combined).
 *
 * @param {Array<Object<string, number>>} itemsStatsList - stat dicts of each item
 * @param {string[]} damagePreferences
 * @param {string[]} resistancePreferences
 * @returns {Object<string, number>} total resolved stats for the build
 */
export function resolveBuildStats(itemsStatsList, damagePreferences, resistancePreferences) {
  const totalStats = {};

  for (const itemStats of itemsStatsList) {
    for (const [statKey, statValue] of Object.entries(itemStats || {})) {
      totalStats[statKey] = (totalStats[statKey] || 0) + statValue;
    }
  }

  return resolveElementStats(totalStats, damagePreferences, resistancePreferences);
}
