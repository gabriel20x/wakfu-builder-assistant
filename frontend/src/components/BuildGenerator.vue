<template>
  <div class="build-generator">
    <div class="generator-grid">
      <!-- Configuration Panel -->
      <div class="config-panel">
        <div class="panel-header">
          <div class="header-title">
            <h2>{{ t('config.title') }}</h2>
          </div>
          <div class="header-actions">
            <p-button 
              :label="isLoading ? t('config.generating') : t('config.generateButton')"
              :disabled="isLoading || enabledStatsCount === 0"
              :loading="isLoading"
              icon="pi pi-sparkles"
              class="generate-button-header"
              @click="generateBuilds"
              size="small"
            />
            <p-button 
              v-if="builds"
              :label="t('builds.saveBuild')"
              icon="pi pi-save"
              class="save-button-header"
              severity="secondary"
              size="small"
              @click="saveCurrentBuildWithName"
            />
          </div>
        </div>
        
        <div class="panel-content">
          <!-- Character Level (AL INICIO - DROPDOWN) -->
          <div class="config-section level-section-top">
            <label>{{ t('config.characterLevel') }}</label>
            <p-dropdown
              v-model="characterLevel"
              :options="levelOptions"
              option-label="label"
              option-value="value"
              placeholder="Select level"
              class="level-dropdown"
            >
              <template #value="slotProps">
                <div v-if="slotProps.value" class="flex align-items-center">
                  <i class="pi pi-star-fill mr-2" style="color: #ffd700;"></i>
                  <span class="font-semibold">Nivel {{ slotProps.value }}</span>
                </div>
                <span v-else>{{ slotProps.placeholder }}</span>
              </template>
              <template #option="slotProps">
                <div class="flex align-items-center">
                  <i class="pi pi-star mr-2" style="color: #9fa8da;"></i>
                  <span>Nivel {{ slotProps.option.value }}</span>
                </div>
              </template>
            </p-dropdown>
          </div>
          
          <!-- Quick Start - Presets -->
          <div class="config-section">
            <ClassPresetSelector 
              @preset-applied="onPresetApplied"
            />
          </div>

          <!-- Stat Weights -->
          <div class="config-section">
            <div class="section-header-with-actions">
              <div>
                <h3>
                  {{ t('config.statPriority') }}
                  <span class="stat-counter">{{ enabledStatsCount }} / {{ totalStatsCount }}</span>
                </h3>
                <p class="help-text">{{ t('config.statPriorityHelp') }}</p>
              </div>
              <div class="quick-actions">
                <p-button 
                  :label="t('config.selectAll')" 
                  size="small"
                  severity="secondary"
                  text
                  @click="selectAllStats"
                />
                <p-button 
                  :label="t('config.selectNone')" 
                  size="small"
                  severity="secondary"
                  text
                  @click="clearAllStats"
                />
              </div>
            </div>
            
            <!-- Características (Principales) -->
            <div class="stat-category">
              <div class="category-header" @click="toggleCategory('main')">
                <i class="pi pi-star-fill category-icon"></i>
                <span>{{ t('stats.main') }}</span>
                <i class="pi" :class="categories.main ? 'pi-chevron-up' : 'pi-chevron-down'"></i>
              </div>
              <div v-show="categories.main" class="category-content">
                <StatWeightInput 
                  v-for="stat in statGroups.main" 
                  :key="stat.key"
                  :stat="stat"
                />
              </div>
            </div>

            <!-- Dominios y Resistencias -->
            <div class="stat-category">
              <div class="category-header" @click="toggleCategory('masteries')">
                <i class="pi pi-bolt category-icon"></i>
                <span>{{ t('stats.masteries') }}</span>
                <i class="pi" :class="categories.masteries ? 'pi-chevron-up' : 'pi-chevron-down'"></i>
              </div>
              <div v-show="categories.masteries" class="category-content">
                <StatWeightInput 
                  v-for="stat in statGroups.masteries" 
                  :key="stat.key"
                  :stat="stat"
                />
              </div>
            </div>

            <!-- Combate -->
            <div class="stat-category">
              <div class="category-header" @click="toggleCategory('combat')">
                <i class="pi pi-shield category-icon"></i>
                <span>{{ t('stats.combat') }}</span>
                <i class="pi" :class="categories.combat ? 'pi-chevron-up' : 'pi-chevron-down'"></i>
              </div>
              <div v-show="categories.combat" class="category-content">
                <StatWeightInput 
                  v-for="stat in statGroups.combat" 
                  :key="stat.key"
                  :stat="stat"
                />
              </div>
            </div>

            <!-- Secundarias -->
            <div class="stat-category">
              <div class="category-header" @click="toggleCategory('secondary')">
                <i class="pi pi-chart-bar category-icon"></i>
                <span>{{ t('stats.secondary') }}</span>
                <i class="pi" :class="categories.secondary ? 'pi-chevron-up' : 'pi-chevron-down'"></i>
              </div>
              <div v-show="categories.secondary" class="category-content">
                <StatWeightInput 
                  v-for="stat in statGroups.secondary" 
                  :key="stat.key"
                  :stat="stat"
                />
              </div>
            </div>
          </div>

          <!-- Preferencias de Elementos -->
          <div class="config-section">
            <ElementPreferences 
              v-model:damage-preferences="damagePreferences"
              v-model:resistance-preferences="resistancePreferences"
            />
          </div>

          <!-- Opciones Avanzadas -->
          <div class="config-section">
            <h3>{{ t('config.advancedOptions') }}</h3>
            <p class="help-text">{{ t('config.advancedHelp') }}</p>
            
            <div class="advanced-options">
              <div class="option-item">
                <p-checkbox 
                  v-model="includePet" 
                  :binary="true" 
                  input-id="include-pet"
                />
                <label for="include-pet" class="option-label">
                  <span class="option-icon">🐾</span>
                  <span>{{ t('config.includePet') }}</span>
                  <span class="option-hint">{{ t('config.includePetHint') }}</span>
                </label>
              </div>
              
              <div class="option-item">
                <p-checkbox 
                  v-model="includeAccessory" 
                  :binary="true" 
                  input-id="include-accessory"
                />
                <label for="include-accessory" class="option-label">
                  <span class="option-icon">⭐</span>
                  <span>{{ t('config.includeEmblem') }}</span>
                  <span class="option-hint">{{ t('config.includeEmblemHint') }}</span>
                </label>
              </div>
            </div>
          </div>

          <!-- Error Display -->
          <div v-if="error" class="error-message">
            <i class="pi pi-exclamation-triangle"></i>
            <span>{{ error }}</span>
          </div>
        </div>
      </div>

      <!-- Results Panel - Items -->
      <div class="results-panel">
        <div class="panel-header">
          <h2>{{ t('results.title') }}</h2>
        </div>
        
        <div v-if="isLoading" class="loading-state">
          <p-progressSpinner />
          <p>{{ t('results.loading') }}</p>
        </div>

        <div v-else-if="builds" class="builds-container">
          <p-tabView class="builds-tabview" v-model:activeIndex="activeTabIndex">
            <p-tabPanel :header="t('builds.easy')">
              <BuildResult :build="builds.easy" :difficulty="t('builds.easy')" :show-stats="false" @edit-metadata="onEditMetadata" />
            </p-tabPanel>
            
            <p-tabPanel :header="t('builds.medium')">
              <BuildResult :build="builds.medium" :difficulty="t('builds.medium')" :show-stats="false" @edit-metadata="onEditMetadata" />
            </p-tabPanel>
            
            <p-tabPanel :header="t('builds.hardEpic')">
              <BuildResult :build="builds.hard_epic" :difficulty="t('builds.hardEpic')" :show-stats="false" @edit-metadata="onEditMetadata" />
            </p-tabPanel>
            
            <p-tabPanel :header="t('builds.hardRelic')">
              <BuildResult :build="builds.hard_relic" :difficulty="t('builds.hardRelic')" :show-stats="false" @edit-metadata="onEditMetadata" />
            </p-tabPanel>
            
            <p-tabPanel :header="t('builds.full')">
              <BuildResult :build="builds.full" :difficulty="t('builds.full')" :show-stats="false" @edit-metadata="onEditMetadata" />
            </p-tabPanel>
          </p-tabView>
        </div>

        <div v-else class="empty-state">
          <i class="pi pi-info-circle"></i>
          <h3>{{ t('results.emptyTitle') }}</h3>
          <p>{{ t('results.emptyText') }}</p>
          <p class="help-text">{{ t('results.emptyHelp') }}</p>
        </div>
      </div>

      <!-- Stats Panel -->
      <div v-if="builds" class="stats-panel">
        <div class="panel-header">
          <h2>{{ t('statsPanel.title') }}</h2>
        </div>
        
        <div class="panel-content">
          <BuildStatSheet 
            v-if="currentBuildStats" 
            :stats="currentBuildStats" 
            :character-level="characterLevel"
          />
          
          <!-- Damage Estimator -->
          <div class="damage-section">
            <DamageEstimator v-if="currentBuildStats" :build-stats="currentBuildStats" />
          </div>
          
          <!-- Build History/Saved -->
          <div class="history-section">
            <BuildHistory @load-build="loadBuild" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, reactive, onMounted, watch } from 'vue'
import { useToast } from 'primevue/usetoast'
import { builderAPI } from '../services/api'
import { STAT_NAMES } from '../composables/useStats'
import { useI18n } from '../composables/useI18n'
import { useBuildPersistence } from '../composables/useBuildPersistence'
import BuildResult from './BuildResult.vue'
import StatWeightInput from './StatWeightInput.vue'
import ElementPreferences from './ElementPreferences.vue'
import BuildStatSheet from './BuildStatSheet.vue'
import ClassPresetSelector from './ClassPresetSelector.vue'
import DamageEstimator from './DamageEstimator.vue'
import BuildHistory from './BuildHistory.vue'

const toast = useToast()
const { t } = useI18n()
const { 
  saveCurrentBuild, 
  saveCurrentConfig, 
  getCurrentBuild, 
  getCurrentConfig,
  saveBuildWithName 
} = useBuildPersistence()

const emit = defineEmits(['edit-metadata'])

const characterLevel = ref(230)
const includePet = ref(true)
const includeAccessory = ref(true)
const builds = ref(null)
const isLoading = ref(false)
const error = ref(null)
const activeTabIndex = ref(0)
const showSaveBuildDialog = ref(false)
const buildNameInput = ref('')

const onEditMetadata = (item) => {
  emit('edit-metadata', item)
}

// Restore builds on mount
onMounted(() => {
  const savedBuild = getCurrentBuild()
  const savedConfig = getCurrentConfig()
  
  if (savedBuild) {
    console.log('Restoring saved build:', savedBuild)
    builds.value = savedBuild.builds
  }
  
  if (savedConfig) {
    console.log('Restoring saved config:', savedConfig)
    characterLevel.value = savedConfig.level_max || 230
    includePet.value = savedConfig.include_pet !== false
    includeAccessory.value = savedConfig.include_accessory !== false
    
    // Restore stat weights
    if (savedConfig.stat_weights) {
      Object.keys(savedConfig.stat_weights).forEach(stat => {
        if (statWeights[stat] !== undefined) {
          statWeights[stat].enabled = true
          statWeights[stat].weight = savedConfig.stat_weights[stat]
        }
      })
    }
    
    // Restore element preferences
    if (savedConfig.damage_preferences) {
      damagePreferences.value = savedConfig.damage_preferences
    }
    if (savedConfig.resistance_preferences) {
      resistancePreferences.value = savedConfig.resistance_preferences
    }
  }
})

// Watch builds and save automatically
watch(builds, (newBuilds) => {
  if (newBuilds) {
    const config = {
      level_max: characterLevel.value,
      stat_weights: activeStatWeights.value,
      include_pet: includePet.value,
      include_accessory: includeAccessory.value,
      damage_preferences: damagePreferences.value,
      resistance_preferences: resistancePreferences.value
    }
    saveCurrentBuild(newBuilds, config)
  }
}, { deep: true })

// Level options for dropdown
const levelOptions = [
  { label: 'Nivel 20', value: 20 },
  { label: 'Nivel 35', value: 35 },
  { label: 'Nivel 50', value: 50 },
  { label: 'Nivel 65', value: 65 },
  { label: 'Nivel 80', value: 80 },
  { label: 'Nivel 95', value: 95 },
  { label: 'Nivel 110', value: 110 },
  { label: 'Nivel 125', value: 125 },
  { label: 'Nivel 140', value: 140 },
  { label: 'Nivel 155', value: 155 },
  { label: 'Nivel 170', value: 170 },
  { label: 'Nivel 185', value: 185 },
  { label: 'Nivel 200', value: 200 },
  { label: 'Nivel 215', value: 215 },
  { label: 'Nivel 230', value: 230 }
]

// Element preferences
const damagePreferences = ref(['Fire', 'Water', 'Earth', 'Air'])
const resistancePreferences = ref(['Fire', 'Water', 'Earth', 'Air'])

// Current build stats based on active tab
const currentBuildStats = computed(() => {
  if (!builds.value) return null
  
  const buildTypes = ['easy', 'medium', 'hard_epic', 'hard_relic', 'full']
  const activeBuildType = buildTypes[activeTabIndex.value]
  
  return builds.value[activeBuildType]?.total_stats || null
})

// Category collapse state
const categories = reactive({
  main: true,
  masteries: true,
  combat: false,
  secondary: false
})

// Organized stat groups
const statGroups = reactive({
  main: [
    { key: 'HP', label: 'PdV', icon: '❤️', enabled: true, weight: 1.0 },
    { key: 'AP', label: 'PA', icon: '⭐', enabled: true, weight: 2.5 },
    { key: 'WP', label: 'PW', icon: '💧', enabled: false, weight: 1.5 },
    { key: 'MP', label: 'PM', icon: '⚡', enabled: true, weight: 2.0 },
  ],
  masteries: [
    { key: 'Elemental_Mastery', label: 'Dominio elem.', icon: '🔮', enabled: false, weight: 2.0 },
    { key: 'Fire_Mastery', label: 'Dominio de fuego', icon: '🔥', enabled: false, weight: 1.8 },
    { key: 'Water_Mastery', label: 'Dominio de agua', icon: '💧', enabled: false, weight: 1.8 },
    { key: 'Earth_Mastery', label: 'Dominio de tierra', icon: '🌍', enabled: false, weight: 1.8 },
    { key: 'Air_Mastery', label: 'Dominio de aire', icon: '💨', enabled: false, weight: 1.8 },
    { key: 'Elemental_Resistance', label: 'Resistencia elem.', icon: '🛡️', enabled: false, weight: 1.0 },
    { key: 'Fire_Resistance', label: 'Resistencia al fuego', icon: '🔥', enabled: false, weight: 1.0 },
    { key: 'Water_Resistance', label: 'Resistencia al agua', icon: '💧', enabled: false, weight: 1.0 },
    { key: 'Earth_Resistance', label: 'Resistencia a la tierra', icon: '🌍', enabled: false, weight: 1.0 },
    { key: 'Air_Resistance', label: 'Resistencia al aire', icon: '💨', enabled: false, weight: 1.0 },
  ],
  combat: [
    { key: 'Critical_Hit', label: 'Golpe crítico', icon: '💥', enabled: false, weight: 1.5 },
    { key: 'Block', label: 'Anticipación', icon: '🛡️', enabled: false, weight: 1.2 },
    { key: 'Initiative', label: 'Iniciativa', icon: '⚔️', enabled: false, weight: 1.0 },
    { key: 'Range', label: 'Alcance', icon: '🎯', enabled: false, weight: 2.0 },
    { key: 'Dodge', label: 'Esquiva', icon: '💨', enabled: false, weight: 1.0 },
    { key: 'Lock', label: 'Placaje', icon: '🔒', enabled: false, weight: 1.0 },
    { key: 'Control', label: 'Control', icon: '👑', enabled: false, weight: 1.2 },
    { key: 'Force_Of_Will', label: 'Voluntad', icon: '💪', enabled: false, weight: 1.0 },
  ],
  secondary: [
    { key: 'Critical_Mastery', label: 'Dominio crítico', icon: '💥', enabled: false, weight: 2.0 },
    { key: 'Critical_Resistance', label: 'Resistencia crítica', icon: '🛡️', enabled: false, weight: 1.0 },
    { key: 'Rear_Mastery', label: 'Dominio espalda', icon: '🎯', enabled: false, weight: 1.5 },
    { key: 'Rear_Resistance', label: 'Resistencia por la espalda', icon: '🛡️', enabled: false, weight: 1.0 },
    { key: 'Melee_Mastery', label: 'Dominio de melé', icon: '⚔️', enabled: false, weight: 2.0 },
    { key: 'Distance_Mastery', label: 'Dominio distancia', icon: '🏹', enabled: false, weight: 2.0 },
    { key: 'Armor_Given', label: 'Armadura dada', icon: '🛡️', enabled: false, weight: 1.0 },
    { key: 'Armor_Received', label: 'Armadura recibida', icon: '🛡️', enabled: false, weight: 1.0 },
    { key: 'Healing_Mastery', label: 'Dominio cura', icon: '💚', enabled: false, weight: 1.5 },
    { key: 'Berserk_Mastery', label: 'Dominio berserker', icon: '😈', enabled: false, weight: 1.5 },
    { key: 'Wisdom', label: 'Sabiduría', icon: '📖', enabled: false, weight: 1.0 },
    { key: 'Prospecting', label: 'Prospección', icon: '💎', enabled: false, weight: 0.8 },
  ]
})

// Get all stats as flat array
const allStats = computed(() => {
  return [
    ...statGroups.main,
    ...statGroups.masteries,
    ...statGroups.combat,
    ...statGroups.secondary
  ]
})

// Total count of available stats
const totalStatsCount = computed(() => {
  return allStats.value.length
})

// Computed stat weights - only include enabled stats
const activeStatWeights = computed(() => {
  const weights = {}
  allStats.value.forEach(stat => {
    if (stat.enabled && stat.weight > 0) {
      weights[stat.key] = stat.weight
    }
  })
  return weights
})

// Count of enabled stats
const enabledStatsCount = computed(() => {
  return allStats.value.filter(s => s.enabled).length
})

// Toggle category collapse
const toggleCategory = (category) => {
  categories[category] = !categories[category]
}

// Quick selection functions
const selectAllStats = () => {
  allStats.value.forEach(stat => {
    stat.enabled = true
  })
}

const clearAllStats = () => {
  allStats.value.forEach(stat => {
    stat.enabled = false
  })
}

// Apply preset from ClassPresetSelector
const onPresetApplied = (preset) => {
  const { weights, damagePreferences: dmgPrefs, resistancePreferences: resPrefs, className, roleName } = preset
  
  // Apply stat weights
  allStats.value.forEach(stat => {
    if (weights[stat.key]) {
      stat.enabled = true
      stat.weight = weights[stat.key]
    } else {
      stat.enabled = false
      stat.weight = 1.0
    }
  })
  
  // Apply element preferences
  damagePreferences.value = dmgPrefs
  resistancePreferences.value = resPrefs
  
  // Show success message
  toast.add({
    severity: 'success',
    summary: t('toast.presetApplied'),
    detail: `${className} - ${roleName}`,
    life: 3000
  })
}

const generateBuilds = async () => {
  // Validate that at least one stat is enabled
  const enabledCount = enabledStatsCount.value
  
  if (enabledCount === 0) {
    toast.add({
      severity: 'warn',
      summary: t('toast.noStatsSelected'),
      detail: t('toast.noStatsSelectedDetail'),
      life: 3000
    })
    return
  }
  
  isLoading.value = true
  error.value = null
  
  try {
    const response = await builderAPI.solveBuild({
      level_max: characterLevel.value,
      stat_weights: activeStatWeights.value,
      include_pet: includePet.value,
      include_accessory: includeAccessory.value,
      damage_preferences: damagePreferences.value,
      resistance_preferences: resistancePreferences.value
    })
    
    builds.value = response.data
    
    toast.add({
      severity: 'success',
      summary: t('toast.buildsGenerated'),
      detail: `5 ${t('toast.buildsGeneratedDetail')} (${enabledCount} ${t('toast.statsSelected')})`,
      life: 3000
    })
  } catch (err) {
    error.value = err.response?.data?.detail || t('toast.errorGenerating')
    
    toast.add({
      severity: 'error',
      summary: t('toast.error'),
      detail: error.value,
      life: 5000
    })
  } finally {
    isLoading.value = false
  }
}

const saveCurrentBuildWithName = () => {
  const name = prompt(t('builds.enterBuildName'), `Build Niv. ${characterLevel.value}`)
  
  if (name && builds.value) {
    const config = {
      level_max: characterLevel.value,
      stat_weights: activeStatWeights.value,
      include_pet: includePet.value,
      include_accessory: includeAccessory.value,
      damage_preferences: damagePreferences.value,
      resistance_preferences: resistancePreferences.value
    }
    
    saveBuildWithName(builds.value, config, name)
    
    toast.add({
      severity: 'success',
      summary: t('builds.buildSaved'),
      detail: name,
      life: 3000
    })
  }
}

const loadBuild = (buildData) => {
  console.log('Loading build:', buildData)
  
  // Restore builds
  builds.value = buildData.builds
  
  // Restore config
  const config = buildData.config
  characterLevel.value = config.level_max || 230
  includePet.value = config.include_pet !== false
  includeAccessory.value = config.include_accessory !== false
  
  // Restore stat weights
  if (config.stat_weights) {
    // Reset all first
    Object.values(statWeights).forEach(stat => {
      stat.enabled = false
      stat.weight = 1.0
    })
    
    // Set from config
    Object.entries(config.stat_weights).forEach(([stat, weight]) => {
      if (statWeights[stat]) {
        statWeights[stat].enabled = true
        statWeights[stat].weight = weight
      }
    })
  }
  
  // Restore element preferences
  if (config.damage_preferences) {
    damagePreferences.value = config.damage_preferences
  }
  if (config.resistance_preferences) {
    resistancePreferences.value = config.resistance_preferences
  }
  
  toast.add({
    severity: 'info',
    summary: t('builds.buildLoaded'),
    detail: buildData.name || t('builds.historyBuild'),
    life: 3000
  })
}
</script>

<style lang="scss" scoped>
.build-generator {
  width: 100%;
}

.generator-grid {
  display: grid;
  grid-template-columns: 380px 1fr 380px;
  gap: 1.5rem;
  min-height: calc(100vh - 200px);
  
  @media (max-width: 1600px) {
    grid-template-columns: 350px 1fr 350px;
    gap: 1rem;
  }
  
  @media (max-width: 1200px) {
    grid-template-columns: 1fr;
    
    .stats-panel {
      order: 2;
    }
    
    .results-panel {
      order: 3;
    }
  }
}

.config-panel,
.results-panel,
.stats-panel {
  background: rgba(26, 35, 50, 0.6);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  max-height: calc(100vh - 250px);
}

.config-panel,
.stats-panel {
  .panel-content {
    overflow-y: auto;
    flex: 1;
    
    &::-webkit-scrollbar {
      width: 8px;
    }
    
    &::-webkit-scrollbar-track {
      background: rgba(0, 0, 0, 0.2);
      border-radius: 4px;
    }
    
    &::-webkit-scrollbar-thumb {
      background: rgba(92, 107, 192, 0.5);
      border-radius: 4px;
      
      &:hover {
        background: rgba(92, 107, 192, 0.7);
      }
    }
  }
}

.stats-panel {
  .panel-content {
    padding: 1rem;
    
    .damage-section {
      margin-top: 2rem;
      padding-top: 2rem;
      border-top: 1px solid rgba(255, 255, 255, 0.1);
    }
  }
}

.panel-header {
  background: rgba(92, 107, 192, 0.2);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  padding: 1rem 1.5rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  
  .header-title h2 {
    margin: 0;
    font-size: 1.25rem;
    color: #fff;
  }
  
  h2 {
    margin: 0;
    font-size: 1.5rem;
    color: #fff;
  }
  
  .header-actions {
    display: flex;
    gap: 0.5rem;
  }
}

.generate-button-header {
  flex-shrink: 0;
  font-weight: 600;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  
  &:hover:not(:disabled) {
    background: linear-gradient(135deg, #7c8ff0 0%, #8c5bb2 100%);
  }
  
  &:disabled {
    opacity: 0.6;
  }
}

.save-button-header {
  flex-shrink: 0;
}

.history-section {
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 2px solid rgba(255, 255, 255, 0.1);
}

.panel-content {
  padding: 1.5rem;
}

.config-section {
  margin-bottom: 2rem;
  
  &:last-child {
    margin-bottom: 0;
  }
  
  label {
    display: block;
    margin-bottom: 0.5rem;
    color: #a0a0a0;
    font-weight: 500;
  }
  
  h3 {
    margin: 0 0 0.5rem 0;
    font-size: 1.1rem;
    color: #fff;
  }
}

.help-text {
  margin: 0.5rem 0;
  color: #808080;
  font-size: 0.875rem;
}

.section-header-with-actions {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
  gap: 1rem;
  
  h3 {
    margin-bottom: 0.5rem;
    
    .stat-counter {
      display: inline-block;
      margin-left: 0.5rem;
      padding: 0.25rem 0.75rem;
      background: rgba(92, 107, 192, 0.3);
      border-radius: 12px;
      font-size: 0.875rem;
      font-weight: 600;
      color: #9fa8da;
    }
  }
  
  .quick-actions {
    display: flex;
    gap: 0.25rem;
    flex-shrink: 0;
    
    @media (max-width: 1400px) {
      flex-direction: column;
    }
  }
}

.level-section-top {
  margin-bottom: 1.5rem !important;
  
  label {
    margin-bottom: 0.75rem !important;
    font-size: 0.95rem !important;
  }
}

.level-dropdown {
  width: 100%;
  
  :deep(.p-dropdown) {
    background: rgba(0, 0, 0, 0.5);
    border: 2px solid rgba(255, 215, 0, 0.3);
    
    &:hover {
      border-color: rgba(255, 215, 0, 0.5);
    }
    
    .p-dropdown-label {
      color: #ffd700;
      font-weight: 700;
      font-size: 1.1rem;
      padding: 0.75rem 1rem;
    }
  }
}

.level-input-group {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  
  .level-input {
    :deep(.p-inputnumber) {
      width: 100%;
    }
    
    :deep(.p-inputnumber-input) {
      background: rgba(0, 0, 0, 0.5);
      border: 1px solid rgba(255, 255, 255, 0.2);
      color: #e0e0e0;
      padding: 0.75rem 1rem;
      text-align: center;
      font-size: 1.5rem;
      font-weight: 700;
      width: 100px;
      
      &:focus {
        border-color: rgba(92, 107, 192, 0.5);
        box-shadow: 0 0 0 3px rgba(92, 107, 192, 0.2);
      }
    }
    
    :deep(.p-inputnumber-button) {
      background: rgba(92, 107, 192, 0.4);
      border: 1px solid rgba(92, 107, 192, 0.5);
      color: #fff;
      width: 3rem;
      height: 100%;
      
      &:hover {
        background: rgba(92, 107, 192, 0.6);
        border-color: rgba(92, 107, 192, 0.7);
      }
      
      .pi {
        font-size: 1.25rem;
        font-weight: 700;
      }
    }
  }
  
  .level-quick-buttons {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
    justify-content: center;
    
    .quick-level-btn {
      min-width: 50px;
      font-weight: 600;
      
      &:deep(.p-button) {
        padding: 0.5rem 0.75rem;
      }
    }
  }
}

.stat-category {
  margin-bottom: 0.75rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  overflow: hidden;
  background: rgba(0, 0, 0, 0.2);
  
  .category-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.75rem 1rem;
    background: rgba(26, 35, 50, 0.6);
    cursor: pointer;
    user-select: none;
    transition: background 0.2s;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    
    &:hover {
      background: rgba(26, 35, 50, 0.8);
    }
    
    .category-icon {
      font-size: 1.1rem;
      flex-shrink: 0;
    }
    
    span {
      flex: 1;
      font-weight: 600;
      font-size: 0.95rem;
      color: #e0e0e0;
    }
    
    .pi-chevron-up,
    .pi-chevron-down {
      font-size: 0.875rem;
      color: #a0a0a0;
      transition: transform 0.2s;
    }
  }
  
  .category-content {
    padding: 0.5rem;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }
}

.advanced-options {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-top: 1rem;
  padding: 1rem;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 8px;
  
  .option-item {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    
    .option-label {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      cursor: pointer;
      color: #fff;
      font-size: 0.95rem;
      margin: 0;
      
      .option-icon {
        font-size: 1.2rem;
      }
      
      .option-hint {
        color: #a0a0a0;
        font-size: 0.85rem;
        font-style: italic;
      }
      
      &:hover {
        color: #5c6bc0;
      }
    }
  }
}

.generate-button {
  width: 100%;
  padding: 0.75rem 1.5rem;
  font-size: 1.1rem;
  font-weight: 600;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  
  &:hover:not(:disabled) {
    background: linear-gradient(135deg, #7c8ff0 0%, #8c5bb2 100%);
  }
  
  &:disabled {
    opacity: 0.6;
  }
}

.error-message {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem;
  background: rgba(244, 67, 54, 0.1);
  border: 1px solid rgba(244, 67, 54, 0.3);
  border-radius: 6px;
  color: #f44336;
  
  i {
    font-size: 1.25rem;
  }
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  
  p {
    margin-top: 1rem;
    color: #a0a0a0;
  }
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  text-align: center;
  
  i {
    font-size: 4rem;
    color: #5c6bc0;
    margin-bottom: 1.5rem;
  }
  
  h3 {
    margin: 0 0 1rem 0;
    color: #fff;
  }
  
  p {
    margin: 0.5rem 0;
    color: #a0a0a0;
    max-width: 500px;
  }
}

.builds-container {
  padding: 0;
  height: 100%;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  
  .builds-tabview {
    height: 100%;
    display: flex;
    flex-direction: column;
  }
}

:deep(.p-tabview) {
  height: 100%;
  display: flex;
  flex-direction: column;
  
  .p-tabview-nav {
    background: transparent;
    border: none;
    border-bottom: 2px solid rgba(255, 255, 255, 0.1);
    flex-shrink: 0;
    
    li {
      .p-tabview-nav-link {
        background: transparent;
        border: none;
        color: #a0a0a0;
        padding: 1rem 1.5rem;
        
        &:hover {
          background: rgba(255, 255, 255, 0.05);
          color: #fff;
        }
      }
      
      &.p-highlight .p-tabview-nav-link {
        background: rgba(92, 107, 192, 0.2);
        color: #fff;
        border-bottom: 2px solid #5c6bc0;
      }
    }
  }
  
  .p-tabview-panels {
    background: transparent;
    padding: 0;
    flex: 1;
    overflow: hidden;
    
    .p-tabview-panel {
      padding: 0;
      height: 100%;
      overflow-y: auto;
      
      &::-webkit-scrollbar {
        width: 10px;
      }
      
      &::-webkit-scrollbar-track {
        background: rgba(0, 0, 0, 0.2);
        border-radius: 5px;
      }
      
      &::-webkit-scrollbar-thumb {
        background: rgba(92, 107, 192, 0.5);
        border-radius: 5px;
        
        &:hover {
          background: rgba(92, 107, 192, 0.7);
        }
      }
    }
  }
}
</style>

