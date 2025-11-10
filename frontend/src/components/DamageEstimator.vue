<template>
  <div class="damage-estimator">
    <div class="estimator-header">
      <h3>
        <i class="pi pi-chart-line"></i>
        {{ t('ui.damageEstimation') }}
      </h3>
      <p class="help-text">
        {{ t('ui.damageEstimationDesc', { type: isMelee ? t('ui.melee') : t('ui.distance') }) }}<br>
        <small>{{ t('ui.resistanceFormula') }}</small>
      </p>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading" class="loading-state">
      <p-progressSpinner style="width: 30px; height: 30px" />
      <span>{{ t('ui.calculating') }} {{ t('ui.damage').toLowerCase() }}...</span>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="error-state">
      <i class="pi pi-exclamation-triangle"></i>
      <span>{{ error }}</span>
    </div>

    <!-- Results -->
    <div v-else-if="damageEstimates" class="estimates-container">
      <!-- Resistance Presets Toggle -->
      <div class="controls">
        <div class="control-group">
          <label>{{ t('ui.resistancesToShow') }}:</label>
          <div class="resistance-toggles">
            <p-button
              v-for="preset in availablePresets"
              :key="preset"
              :label="`${preset}`"
              size="small"
              :severity="selectedPresets.includes(preset) ? 'primary' : 'secondary'"
              :outlined="!selectedPresets.includes(preset)"
              @click="togglePreset(preset)"
              class="preset-btn"
            />
          </div>
        </div>

        <div class="control-row">
          <div class="control-group">
            <label>{{ t('ui.damageType') }}:</label>
            <div class="damage-type-selector">
              <p-button
                :label="`⚔️ ${t('ui.melee')}`"
                size="small"
                :severity="isMelee ? 'primary' : 'secondary'"
                :outlined="!isMelee"
                @click="isMelee = true"
                class="damage-type-btn"
              />
              <p-button
                :label="`🏹 ${t('ui.distance')}`"
                size="small"
                :severity="!isMelee ? 'primary' : 'secondary'"
                :outlined="isMelee"
                @click="isMelee = false"
                class="damage-type-btn"
              />
            </div>
          </div>

          <div class="control-group">
            <p-checkbox
              v-model="showCritical"
              :binary="true"
              input-id="show-critical"
            />
            <label for="show-critical" class="checkbox-label">{{ t('ui.showCritical') }}</label>
          </div>
        </div>
      </div>

      <!-- Damage Comparison Chart -->
      <div class="damage-chart">
        <div 
          v-for="estimate in damageEstimates.estimates"
          :key="estimate.element"
          class="element-row"
        >
          <div class="element-header" :class="`element-${estimate.element.toLowerCase()}`">
            <span class="element-icon">{{ getElementIcon(estimate.element) }}</span>
            <div class="element-info">
              <span class="element-name">{{ estimate.element }}</span>
              <span class="element-mastery">{{ Math.round(estimate.base_mastery) }} {{ t('ui.mastery') }}</span>
            </div>
          </div>

          <div class="damage-bars">
            <div
              v-for="scenario in getFilteredScenarios(estimate.resistance_scenarios)"
              :key="scenario.flat_resistance"
              class="damage-scenario"
            >
              <div class="scenario-label">
                <div class="resistance-flat">{{ scenario.flat_resistance }} res</div>
                <div class="resistance-percent">({{ scenario.resistance_percent }}%)</div>
              </div>
              <div class="damage-values">
                <!-- Normal Damage -->
                <div class="damage-bar-container">
                  <div class="damage-bar-label">⚔️ {{ t('ui.normal') }}</div>
                  <div 
                    class="damage-bar normal"
                    :style="{ width: getDamageBarWidth(scenario.normal_damage) }"
                    v-if="scenario.normal_damage > 0"
                  >
                    <span class="damage-value">{{ Math.round(scenario.normal_damage) }}</span>
                  </div>
                  <div v-else class="no-damage">
                    <span>0</span>
                  </div>
                </div>
                
                <!-- Critical Damage -->
                <div v-if="showCritical && scenario.critical_damage !== null" class="damage-bar-container">
                  <div class="damage-bar-label">💥 {{ t('ui.critical') }}</div>
                  <div 
                    class="damage-bar critical"
                    :style="{ width: getDamageBarWidth(scenario.critical_damage) }"
                    v-if="scenario.critical_damage > 0"
                  >
                    <span class="damage-value">{{ Math.round(scenario.critical_damage) }}</span>
                  </div>
                  <div v-else class="no-damage">
                    <span>0</span>
                  </div>
                </div>
                
                <!-- Backstab Damage -->
                <div v-if="scenario.backstab_damage !== null" class="damage-bar-container">
                  <div class="damage-bar-label">🎯 {{ t('ui.backstab') }}</div>
                  <div 
                    class="damage-bar backstab"
                    :style="{ width: getDamageBarWidth(scenario.backstab_damage) }"
                    v-if="scenario.backstab_damage > 0"
                  >
                    <span class="damage-value">{{ Math.round(scenario.backstab_damage) }}</span>
                  </div>
                  <div v-else class="no-damage">
                    <span>0</span>
                  </div>
                </div>
                
                <!-- Backstab + Critical Damage -->
                <div v-if="showCritical && scenario.backstab_critical_damage !== null" class="damage-bar-container">
                  <div class="damage-bar-label">🎯💥 {{ t('ui.backstabCritical') }}</div>
                  <div 
                    class="damage-bar backstab-critical"
                    :style="{ width: getDamageBarWidth(scenario.backstab_critical_damage) }"
                    v-if="scenario.backstab_critical_damage > 0"
                  >
                    <span class="damage-value">{{ Math.round(scenario.backstab_critical_damage) }}</span>
                  </div>
                  <div v-else class="no-damage">
                    <span>0</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Best Element Recommendation -->
      <div class="recommendation">
        <i class="pi pi-info-circle"></i>
        <div class="recommendation-content">
          <strong>{{ t('ui.recommendation') }}:</strong>
          <span>{{ getBestElementRecommendation() }}</span>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else class="empty-state">
      <i class="pi pi-chart-line"></i>
      <p>{{ t('ui.noDamageStats') }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { damageAPI } from '../services/api'
import { useI18n } from '../composables/useI18n'

const { t } = useI18n()

const props = defineProps({
  buildStats: {
    type: Object,
    required: true
  }
})

const isLoading = ref(false)
const error = ref(null)
const damageEstimates = ref(null)
const showCritical = ref(true)
const isMelee = ref(true) // true = Melee, false = Distance
const availablePresets = [0, 100, 200, 300, 400, 500]
const selectedPresets = ref([0, 100, 200, 300])

// Element icons
const elementIcons = {
  Fire: '🔥',
  Water: '💧',
  Earth: '🌍',
  Air: '💨'
}

const getElementIcon = (element) => elementIcons[element] || '⚡'

// Filter scenarios based on selected presets
const getFilteredScenarios = (scenarios) => {
  return scenarios.filter(s => selectedPresets.value.includes(s.flat_resistance))
}

// Toggle resistance preset
const togglePreset = (preset) => {
  const index = selectedPresets.value.indexOf(preset)
  if (index > -1) {
    if (selectedPresets.value.length > 1) {
      selectedPresets.value.splice(index, 1)
    }
  } else {
    selectedPresets.value.push(preset)
    selectedPresets.value.sort((a, b) => a - b)
  }
}

// Calculate bar width based on damage
const maxDamage = computed(() => {
  if (!damageEstimates.value?.estimates) return 0
  
  let max = 0
  damageEstimates.value.estimates.forEach(estimate => {
    estimate.resistance_scenarios.forEach(scenario => {
      max = Math.max(max, scenario.normal_damage || 0)
      if (showCritical.value && scenario.critical_damage) {
        max = Math.max(max, scenario.critical_damage)
      }
      if (scenario.backstab_damage) {
        max = Math.max(max, scenario.backstab_damage)
      }
      if (showCritical.value && scenario.backstab_critical_damage) {
        max = Math.max(max, scenario.backstab_critical_damage)
      }
    })
  })
  return max
})

const getDamageBarWidth = (damage) => {
  if (!damage || maxDamage.value === 0) return '0%'
  return `${(damage / maxDamage.value) * 100}%`
}

// Get best element recommendation
const getBestElementRecommendation = () => {
  if (!damageEstimates.value?.estimates) return 'N/A'
  
  // Find element with highest average damage across selected resistances
  let bestElement = null
  let bestAvgDamage = 0
  
  damageEstimates.value.estimates.forEach(estimate => {
    const filteredScenarios = getFilteredScenarios(estimate.resistance_scenarios)
    const avgDamage = filteredScenarios.reduce((sum, s) => sum + s.normal_damage, 0) / filteredScenarios.length
    
    if (avgDamage > bestAvgDamage) {
      bestAvgDamage = avgDamage
      bestElement = estimate.element
    }
  })
  
  return bestElement 
    ? `${getElementIcon(bestElement)} ${bestElement} ${t('ui.bestElementDamage')} (${Math.round(bestAvgDamage)} ${t('ui.perSpell')})`
    : t('ui.noData')
}

// Load damage estimates
const loadDamageEstimates = async () => {
  if (!props.buildStats || Object.keys(props.buildStats).length === 0) {
    damageEstimates.value = null
    return
  }

  isLoading.value = true
  error.value = null

  try {
    const response = await damageAPI.estimateDamage(props.buildStats, {
      baseSpellDamage: 100,
      resistancePresets: availablePresets,
      includeCritical: true,
      isMelee: isMelee.value
    })
    
    damageEstimates.value = response.data
  } catch (err) {
    console.error('Error loading damage estimates:', err)
    error.value = t('ui.errorCalculating')
  } finally {
    isLoading.value = false
  }
}

// Watch for stats changes and damage type changes
watch(() => props.buildStats, () => {
  loadDamageEstimates()
}, { deep: true, immediate: true })

watch(isMelee, () => {
  if (damageEstimates.value) {
    loadDamageEstimates()
  }
})
</script>

<style lang="scss" scoped>
.damage-estimator {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.estimator-header {
  h3 {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin: 0 0 0.5rem 0;
    font-size: 1.1rem;
    color: #fff;
    
    i {
      color: #5c6bc0;
    }
  }
  
  .help-text {
    margin: 0;
    color: #a0a0a0;
    font-size: 0.875rem;
  }
}

.loading-state,
.error-state,
.empty-state {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  padding: 2rem;
  text-align: center;
  color: #a0a0a0;
  font-size: 0.95rem;
}

.error-state {
  color: #f44336;
  background: rgba(244, 67, 54, 0.1);
  border: 1px solid rgba(244, 67, 54, 0.3);
  border-radius: 6px;
}

.empty-state {
  flex-direction: column;
  
  i {
    font-size: 2rem;
    opacity: 0.5;
  }
}

.controls {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding: 1rem;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 8px;
  margin-bottom: 1rem;
  
  .control-row {
    display: flex;
    gap: 1.5rem;
    align-items: center;
    flex-wrap: wrap;
    
    @media (max-width: 768px) {
      flex-direction: column;
      align-items: flex-start;
      gap: 1rem;
    }
  }
  
  .control-group {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    
    label {
      font-size: 0.875rem;
      color: #a0a0a0;
      font-weight: 500;
    }
    
    .checkbox-label {
      cursor: pointer;
      color: #e0e0e0;
      margin-left: 0.5rem;
      
      &:hover {
        color: #fff;
      }
    }
  }
  
  .resistance-toggles {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
    
    .preset-btn {
      min-width: 60px;
      font-weight: 600;
    }
  }
  
  .damage-type-selector {
    display: flex;
    gap: 0.5rem;
    
    .damage-type-btn {
      min-width: 100px;
      font-weight: 600;
      
      &:deep(.p-button-label) {
        display: flex;
        align-items: center;
        gap: 0.25rem;
      }
    }
  }
}

.damage-chart {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.element-row {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.element-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem;
  border-radius: 6px;
  background: rgba(0, 0, 0, 0.3);
  
  &.element-fire {
    border-left: 4px solid #ff6b6b;
  }
  
  &.element-water {
    border-left: 4px solid #4dabf7;
  }
  
  &.element-earth {
    border-left: 4px solid #8bc34a;
  }
  
  &.element-air {
    border-left: 4px solid #ffd93d;
  }
  
  .element-icon {
    font-size: 1.5rem;
  }
  
  .element-info {
    display: flex;
    flex-direction: column;
    
    .element-name {
      font-weight: 600;
      color: #fff;
      font-size: 1rem;
    }
    
    .element-mastery {
      font-size: 0.875rem;
      color: #a0a0a0;
    }
  }
}

.damage-bars {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  padding-left: 1rem;
}

.damage-scenario {
  display: grid;
  grid-template-columns: 100px 1fr;
  gap: 0.75rem;
  align-items: flex-start;
  
  .scenario-label {
    display: flex;
    flex-direction: column;
    
    .resistance-flat {
      font-size: 0.875rem;
      color: #e0e0e0;
      font-weight: 600;
    }
    
    .resistance-percent {
      font-size: 0.75rem;
      color: #a0a0a0;
    }
  }
  
  .damage-values {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .damage-bar-container {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    
    .damage-bar-label {
      min-width: 110px;
      font-size: 0.75rem;
      color: #a0a0a0;
      font-weight: 600;
      display: flex;
      align-items: center;
      gap: 0.25rem;
    }
  }
  
  .damage-bar-container > div:not(.damage-bar-label) {
    flex: 1;
    height: 28px;
    background: rgba(0, 0, 0, 0.3);
    border-radius: 4px;
    overflow: hidden;
    position: relative;
  }
  
  .damage-bar {
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: flex-end;
    padding-right: 0.5rem;
    border-radius: 4px;
    transition: width 0.3s ease;
    min-width: 40px;
    
    &.normal {
      background: linear-gradient(90deg, rgba(92, 107, 192, 0.6) 0%, rgba(92, 107, 192, 0.8) 100%);
    }
    
    &.critical {
      background: linear-gradient(90deg, rgba(255, 107, 107, 0.6) 0%, rgba(255, 107, 107, 0.8) 100%);
    }
    
    &.backstab {
      background: linear-gradient(90deg, rgba(255, 193, 7, 0.6) 0%, rgba(255, 193, 7, 0.8) 100%);
    }
    
    &.backstab-critical {
      background: linear-gradient(90deg, rgba(156, 39, 176, 0.6) 0%, rgba(156, 39, 176, 0.8) 100%);
    }
    
    .damage-value {
      font-weight: 700;
      color: #fff;
      font-size: 0.875rem;
      text-shadow: 0 1px 2px rgba(0, 0, 0, 0.5);
    }
  }
  
  .no-damage {
    height: 100%;
    display: flex;
    align-items: center;
    padding-left: 0.5rem;
    
    span {
      font-size: 0.875rem;
      color: #666;
      font-style: italic;
    }
  }
}

.recommendation {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  padding: 1rem;
  background: rgba(92, 107, 192, 0.1);
  border: 1px solid rgba(92, 107, 192, 0.3);
  border-radius: 6px;
  margin-top: 1rem;
  
  i {
    color: #5c6bc0;
    font-size: 1.25rem;
    margin-top: 0.125rem;
  }
  
  .recommendation-content {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
    
    strong {
      color: #fff;
      font-size: 0.95rem;
    }
    
    span {
      color: #e0e0e0;
      font-size: 0.875rem;
    }
  }
}
</style>

