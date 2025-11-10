<template>
  <div class="build-generator">
    <div class="generator-grid">
      <!-- Configuration Panel -->
      <div class="config-panel">
        <div class="panel-header">
          <div class="header-row header-title-row">
            <h2>{{ t('config.title') }}</h2>
          </div>
          <div class="header-row header-actions-row">
            <p-button 
              icon="pi pi-folder-open"
              :label="t('builds.loadBuild')"
              class="load-button-header"
              severity="secondary"
              size="small"
              @click="showHistoryModal = true"
            />
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
              icon="pi pi-save"
              :label="t('builds.saveBuild')"
              class="save-button-header"
              severity="success"
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
                  <span class="font-semibold">{{ t('ui.level') }} {{ slotProps.value }}</span>
                </div>
                <span v-else>{{ slotProps.placeholder }}</span>
              </template>
              <template #option="slotProps">
                <div class="flex align-items-center">
                  <i class="pi pi-star mr-2" style="color: #9fa8da;"></i>
                  <span>{{ t('ui.level') }} {{ slotProps.option.value }}</span>
                </div>
              </template>
            </p-dropdown>
          </div>
          
          <!-- Quick Start - Presets -->
          <div class="config-section">
            <ClassPresetSelector 
              ref="classPresetSelectorRef"
              @preset-applied="onPresetApplied"
            />
            
            <!-- Display selected class/role -->
            <div v-if="selectedClass && selectedRole" class="preset-display">
              <div class="preset-info">
                <i class="pi pi-check-circle"></i>
                <span class="preset-text">
                  <strong>{{ selectedClass }}</strong> - {{ selectedRole }}
                </span>
              </div>
            </div>
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

          <!-- Monster Type Filter -->
          <div class="config-section">
            <MonsterTypeFilter v-model="selectedMonsterTypes" />
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
              
              <div class="option-item">
                <p-checkbox 
                  v-model="onlyDroppable" 
                  :binary="true" 
                  input-id="only-droppable"
                />
                <label for="only-droppable" class="option-label">
                  <span class="option-icon">💀</span>
                  <span>{{ t('config.onlyDroppable') }}</span>
                  <span class="option-hint">{{ t('config.onlyDroppableHint') }}</span>
                </label>
              </div>
            </div>
          </div>

          <!-- Ignored Items Manager -->
          <div class="config-section">
            <IgnoredItemsManager />
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
          <!-- Equipment Slots -->
          <div class="equipment-section">
            <EquipmentSlots 
              v-if="currentBuildItems" 
              :items="currentBuildItems"
              :selected-class="selectedClass"
              @item-click="scrollToItem"
            />
          </div>
          
          <BuildStatSheet 
            v-if="currentBuildStats" 
            :stats="currentBuildStats" 
            :character-level="characterLevel"
          />
        </div>
      </div>
    </div>
    
    <!-- Build History Modal -->
    <BuildHistory 
      v-model:visible="showHistoryModal" 
      @load-build="loadBuild" 
    />
  </div>
</template>

<script setup>
import { ref, computed, reactive, onMounted, watch } from 'vue'
import { useToast } from 'primevue/usetoast'
import { builderAPI } from '../services/api'
import { STAT_NAMES, getStatLabel } from '../composables/useStats'
import { useI18n } from '../composables/useI18n'
import { useBuildPersistence } from '../composables/useBuildPersistence'
import { useIgnoredItems } from '../composables/useIgnoredItems'
import BuildResult from './BuildResult.vue'
import StatWeightInput from './StatWeightInput.vue'
import ElementPreferences from './ElementPreferences.vue'
import BuildStatSheet from './BuildStatSheet.vue'
import ClassPresetSelector from './ClassPresetSelector.vue'
import EquipmentSlots from './EquipmentSlots.vue'
import BuildHistory from './BuildHistory.vue'
import IgnoredItemsManager from './IgnoredItemsManager.vue'
import MonsterTypeFilter from './MonsterTypeFilter.vue'

const toast = useToast()
const { t } = useI18n()
const { 
  saveCurrentBuild, 
  saveCurrentConfig, 
  getCurrentBuild, 
  getCurrentConfig,
  saveBuildWithName 
} = useBuildPersistence()
const { ignoredItemIds } = useIgnoredItems()

const emit = defineEmits(['edit-metadata'])

const characterLevel = ref(230)
const includePet = ref(true)
const includeAccessory = ref(true)
const onlyDroppable = ref(false)
const selectedMonsterTypes = ref([])  // Monster type filter
const builds = ref(null)
const isLoading = ref(false)
const error = ref(null)
const activeTabIndex = ref(0)
const showHistoryModal = ref(false)
const selectedClass = ref(null)
const selectedRole = ref(null)
const classPresetSelectorRef = ref(null)

const onEditMetadata = (item) => {
  emit('edit-metadata', item)
}

// Restore builds on mount - DISABLED (now using BuildViewer)
// BuildGenerator should start fresh, builds are managed in BuildViewer
onMounted(async () => {
  // Restore last generated build + config
  const persistedConfig = getCurrentConfig()
  const persistedBuild = getCurrentBuild()

  if (persistedConfig) {
    // Basic fields
    characterLevel.value = persistedConfig.level_max || characterLevel.value
    includePet.value = persistedConfig.include_pet !== false
    includeAccessory.value = persistedConfig.include_accessory !== false
    onlyDroppable.value = persistedConfig.only_droppable === true
    if (Array.isArray(persistedConfig.damage_preferences)) {
      damagePreferences.value = persistedConfig.damage_preferences
    }
    if (Array.isArray(persistedConfig.resistance_preferences)) {
      resistancePreferences.value = persistedConfig.resistance_preferences
    }
    if (Array.isArray(persistedConfig.monster_types)) {
      selectedMonsterTypes.value = persistedConfig.monster_types
    }
    // Restore active tab
    if (typeof persistedConfig.active_tab_index === 'number') {
      activeTabIndex.value = persistedConfig.active_tab_index
    }
    // Restore class + role
    if (persistedConfig.selectedClass) {
      selectedClass.value = persistedConfig.selectedClass
    }
    if (persistedConfig.selectedRole) {
      selectedRole.value = persistedConfig.selectedRole
    }
  }

  // Restore stat weights
  if (persistedConfig?.stat_weights) {
    allStats.value.forEach(stat => {
      stat.enabled = false
      stat.weight = 1.0
    })
    Object.entries(persistedConfig.stat_weights).forEach(([k, w]) => {
      const target = allStats.value.find(s => s.key === k)
      if (target) {
        target.enabled = true
        target.weight = w
      }
    })
  }

  // Restore builds payload
  if (persistedBuild?.builds) {
    builds.value = persistedBuild.builds
  }

  // If we have class/role, attempt to restore preset UI state
  if (classPresetSelectorRef.value && selectedClass.value && selectedRole.value) {
    try {
      await classPresetSelectorRef.value.restoreValues(selectedClass.value, selectedRole.value)
    } catch (e) {
      console.warn('Could not restore preset selector values:', e)
    }
  }
})

// Level options for dropdown
const levelOptions = computed(() => [
  { label: `${t('ui.level')} 20`, value: 20 },
  { label: `${t('ui.level')} 35`, value: 35 },
  { label: `${t('ui.level')} 50`, value: 50 },
  { label: `${t('ui.level')} 65`, value: 65 },
  { label: `${t('ui.level')} 80`, value: 80 },
  { label: `${t('ui.level')} 95`, value: 95 },
  { label: `${t('ui.level')} 110`, value: 110 },
  { label: `${t('ui.level')} 125`, value: 125 },
  { label: `${t('ui.level')} 140`, value: 140 },
  { label: `${t('ui.level')} 155`, value: 155 },
  { label: `${t('ui.level')} 170`, value: 170 },
  { label: `${t('ui.level')} 185`, value: 185 },
  { label: `${t('ui.level')} 200`, value: 200 },
  { label: `${t('ui.level')} 215`, value: 215 },
  { label: `${t('ui.level')} 230`, value: 230 }
])

// Element preferences
const damagePreferences = ref(['Fire', 'Water', 'Earth', 'Air'])
const resistancePreferences = ref(['Fire', 'Water', 'Earth', 'Air'])

// Persist active tab changes
watch(activeTabIndex, (idx) => {
  saveCurrentConfig({ active_tab_index: idx })
})

// Persist element preferences & monster types
watch([damagePreferences, resistancePreferences, selectedMonsterTypes], ([dmg, res, monsters]) => {
  saveCurrentConfig({
    damage_preferences: dmg,
    resistance_preferences: res,
    monster_types: monsters
  })
}, { deep: true })

// Persist basic toggles
watch([characterLevel, includePet, includeAccessory, onlyDroppable], ([lvl, pet, acc, drop]) => {
  saveCurrentConfig({
    level_max: lvl,
    include_pet: pet,
    include_accessory: acc,
    only_droppable: drop
  })
})

// Current build stats based on active tab
const currentBuildStats = computed(() => {
  if (!builds.value) return null
  
  const buildTypes = ['easy', 'medium', 'hard_epic', 'hard_relic', 'full']
  const activeBuildType = buildTypes[activeTabIndex.value]
  
  return builds.value[activeBuildType]?.total_stats || null
})

const currentBuildItems = computed(() => {
  if (!builds.value) return []
  
  const buildTypes = ['easy', 'medium', 'hard_epic', 'hard_relic', 'full']
  const activeBuildType = buildTypes[activeTabIndex.value]
  
  return builds.value[activeBuildType]?.items || []
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
    { key: 'HP', label: computed(() => getStatLabel('HP')), icon: '❤️', enabled: true, weight: 1.0 },
    { key: 'AP', label: computed(() => getStatLabel('AP')), icon: '⭐', enabled: true, weight: 2.5 },
    { key: 'WP', label: computed(() => getStatLabel('WP')), icon: '💧', enabled: false, weight: 1.5 },
    { key: 'MP', label: computed(() => getStatLabel('MP')), icon: '⚡', enabled: true, weight: 2.0 },
  ],
  masteries: [
    { key: 'Elemental_Mastery', label: computed(() => getStatLabel('Elemental_Mastery')), icon: '🔮', enabled: false, weight: 2.0 },
    { key: 'Fire_Mastery', label: computed(() => getStatLabel('Fire_Mastery')), icon: '🔥', enabled: false, weight: 1.8 },
    { key: 'Water_Mastery', label: computed(() => getStatLabel('Water_Mastery')), icon: '💧', enabled: false, weight: 1.8 },
    { key: 'Earth_Mastery', label: computed(() => getStatLabel('Earth_Mastery')), icon: '🌍', enabled: false, weight: 1.8 },
    { key: 'Air_Mastery', label: computed(() => getStatLabel('Air_Mastery')), icon: '💨', enabled: false, weight: 1.8 },
    { key: 'Elemental_Resistance', label: computed(() => getStatLabel('Elemental_Resistance')), icon: '🛡️', enabled: false, weight: 1.0 },
    { key: 'Fire_Resistance', label: computed(() => getStatLabel('Fire_Resistance')), icon: '🔥', enabled: false, weight: 1.0 },
    { key: 'Water_Resistance', label: computed(() => getStatLabel('Water_Resistance')), icon: '💧', enabled: false, weight: 1.0 },
    { key: 'Earth_Resistance', label: computed(() => getStatLabel('Earth_Resistance')), icon: '🌍', enabled: false, weight: 1.0 },
    { key: 'Air_Resistance', label: computed(() => getStatLabel('Air_Resistance')), icon: '💨', enabled: false, weight: 1.0 },
  ],
  combat: [
    { key: 'Critical_Hit', label: computed(() => getStatLabel('Critical_Hit')), icon: '💥', enabled: false, weight: 1.5 },
    { key: 'Block', label: computed(() => getStatLabel('Block')), icon: '🛡️', enabled: false, weight: 1.2 },
    { key: 'Initiative', label: computed(() => getStatLabel('Initiative')), icon: '⚔️', enabled: false, weight: 1.0 },
    { key: 'Range', label: computed(() => getStatLabel('Range')), icon: '🎯', enabled: false, weight: 2.0 },
    { key: 'Dodge', label: computed(() => getStatLabel('Dodge')), icon: '💨', enabled: false, weight: 1.0 },
    { key: 'Lock', label: computed(() => getStatLabel('Lock')), icon: '🔒', enabled: false, weight: 1.0 },
    { key: 'Control', label: computed(() => getStatLabel('Control')), icon: '👑', enabled: false, weight: 1.2 },
    { key: 'Force_Of_Will', label: computed(() => getStatLabel('Force_Of_Will')), icon: '💪', enabled: false, weight: 1.0 },
  ],
  secondary: [
    { key: 'Critical_Mastery', label: computed(() => getStatLabel('Critical_Mastery')), icon: '💥', enabled: false, weight: 2.0 },
    { key: 'Critical_Resistance', label: computed(() => getStatLabel('Critical_Resistance')), icon: '🛡️', enabled: false, weight: 1.0 },
    { key: 'Rear_Mastery', label: computed(() => getStatLabel('Rear_Mastery')), icon: '🎯', enabled: false, weight: 1.5 },
    { key: 'Rear_Resistance', label: computed(() => getStatLabel('Rear_Resistance')), icon: '🛡️', enabled: false, weight: 1.0 },
    { key: 'Melee_Mastery', label: computed(() => getStatLabel('Melee_Mastery')), icon: '⚔️', enabled: false, weight: 2.0 },
    { key: 'Distance_Mastery', label: computed(() => getStatLabel('Distance_Mastery')), icon: '🏹', enabled: false, weight: 2.0 },
    { key: 'Armor_Given', label: computed(() => getStatLabel('Armor_Given')), icon: '🛡️', enabled: false, weight: 1.0 },
    { key: 'Armor_Received', label: computed(() => getStatLabel('Armor_Received')), icon: '🛡️', enabled: false, weight: 1.0 },
    { key: 'Healing_Mastery', label: computed(() => getStatLabel('Healing_Mastery')), icon: '💚', enabled: false, weight: 1.5 },
    { key: 'Berserk_Mastery', label: computed(() => getStatLabel('Berserk_Mastery')), icon: '😈', enabled: false, weight: 1.5 },
    { key: 'Wisdom', label: computed(() => getStatLabel('Wisdom')), icon: '📖', enabled: false, weight: 1.0 },
    { key: 'Prospecting', label: computed(() => getStatLabel('Prospecting')), icon: '💎', enabled: false, weight: 0.8 },
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

// Persist stat weights when they change (enabled/weight)
watch(() => allStats.value.map(s => ({ key: s.key, enabled: s.enabled, weight: s.weight })), (statsSnapshot) => {
  const weights = {}
  statsSnapshot.forEach(s => {
    if (s.enabled && s.weight > 0) {
      weights[s.key] = s.weight
    }
  })
  saveCurrentConfig({ stat_weights: weights })
}, { deep: true })

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
  
  // Save class and role info
  selectedClass.value = className
  selectedRole.value = roleName

  // Persist class/role immediately
  saveCurrentConfig({ selectedClass: className, selectedRole: roleName })
  
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
      only_droppable: onlyDroppable.value,
      damage_preferences: damagePreferences.value,
      resistance_preferences: resistancePreferences.value,
      ignored_item_ids: ignoredItemIds.value,
      monster_types: selectedMonsterTypes.value
    })
    
    builds.value = response.data

    // Persist generated builds + full config snapshot
    const configSnapshot = {
      level_max: characterLevel.value,
      stat_weights: activeStatWeights.value,
      include_pet: includePet.value,
      include_accessory: includeAccessory.value,
      only_droppable: onlyDroppable.value,
      damage_preferences: damagePreferences.value,
      resistance_preferences: resistancePreferences.value,
      monster_types: selectedMonsterTypes.value,
      selectedClass: selectedClass.value,
      selectedRole: selectedRole.value,
      active_tab_index: activeTabIndex.value
    }
    saveCurrentConfig(configSnapshot)
    saveCurrentBuild(builds.value, configSnapshot)
    
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
      only_droppable: onlyDroppable.value,
      damage_preferences: damagePreferences.value,
      resistance_preferences: resistancePreferences.value,
      monster_types: selectedMonsterTypes.value,
      selectedClass: selectedClass.value,
      selectedRole: selectedRole.value,
      active_tab_index: activeTabIndex.value
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

const scrollToItem = (item) => {
  if (!item || !item.item_id) return
  
  // Wait for next tick to ensure DOM is updated
  setTimeout(() => {
    // Since multiple tabs can have items with the same ID, we need to find the visible one
    const elements = document.querySelectorAll(`[id="item-${item.item_id}"]`)
    
    // Find the element that's in a visible container (active tab)
    let visibleElement = null
    let visibleContainer = null
    
    for (const el of elements) {
      const container = el.closest('.build-content')
      if (container && container.offsetParent !== null) {
        visibleElement = el
        visibleContainer = container
        break
      }
    }
    
    if (visibleElement && visibleContainer) {
      const offset = 100 // Top offset in pixels
      const containerRect = visibleContainer.getBoundingClientRect()
      const elementRect = visibleElement.getBoundingClientRect()
      const relativeTop = elementRect.top - containerRect.top + visibleContainer.scrollTop
      
      visibleContainer.scrollTo({
        top: relativeTop - offset,
        behavior: 'smooth'
      })
      
      // Add a brief highlight effect
      visibleElement.style.transition = 'box-shadow 0.3s ease'
      visibleElement.style.boxShadow = '0 0 20px 5px rgba(92, 107, 192, 0.8)'
      setTimeout(() => {
        visibleElement.style.boxShadow = ''
      }, 1500)
    }
  }, 100)
}

const loadBuild = async (buildData) => {
  console.log('Loading build:', buildData)
  
  // Close modal
  showHistoryModal.value = false
  
  // Restore builds
  builds.value = buildData.builds
  
  // Restore config
  const config = buildData.config
  characterLevel.value = config.level_max || 230
  includePet.value = config.include_pet !== false
  includeAccessory.value = config.include_accessory !== false
  onlyDroppable.value = config.only_droppable === true
  
  // Restore stat weights using statGroups
  if (config.stat_weights) {
    console.log('Restoring stat weights:', config.stat_weights)
    
    // Reset all stats first
    allStats.value.forEach(stat => {
      stat.enabled = false
      stat.weight = 1.0
    })
    
    // Apply saved weights
    Object.entries(config.stat_weights).forEach(([statName, weight]) => {
      const stat = allStats.value.find(s => s.key === statName)
      if (stat) {
        stat.enabled = true
        stat.weight = weight
        console.log(`Restored ${statName}: enabled=true, weight=${weight}`)
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
  
  // Restore class and role
  if (config.selectedClass && config.selectedRole) {
    selectedClass.value = config.selectedClass
    selectedRole.value = config.selectedRole
    console.log('Restored class:', config.selectedClass, 'role:', config.selectedRole)
    
    // Restore in ClassPresetSelector component
    if (classPresetSelectorRef.value) {
      await classPresetSelectorRef.value.restoreValues(config.selectedClass, config.selectedRole)
    }
  }

  // Restore active tab index (defaults to 0 if missing)
  if (typeof config.active_tab_index === 'number') {
    activeTabIndex.value = config.active_tab_index
  }

  // Persist restored config as current search context WITHOUT overriding last generated build (preview only)
  saveCurrentConfig({ ...config })
  
  toast.add({
    severity: 'info',
    summary: t('builds.buildLoaded'),
    detail: buildData.name || t('builds.historyBuild'),
    life: 3000
  })
  
  // Refresh items in the background with latest data from database
  refreshBuildItems(buildData.builds)
}

const refreshBuildItems = async (buildsData) => {
  try {
    // Collect all item IDs from all build types
    const itemIds = new Set()
    const buildTypes = ['easy', 'medium', 'hard_epic', 'hard_relic', 'full']
    
    buildTypes.forEach(buildType => {
      if (buildsData[buildType]?.items) {
        buildsData[buildType].items.forEach(item => {
          itemIds.add(item.item_id)
        })
      }
    })
    
    if (itemIds.size === 0) {
      return
    }
    
    console.log(`Refreshing ${itemIds.size} items with latest data...`)
    
    // Call refresh endpoint
    const response = await builderAPI.refreshItems(Array.from(itemIds))
    const refreshedItems = response.data.items
    
    // Create a map of refreshed items by item_id
    const itemsMap = new Map()
    refreshedItems.forEach(item => {
      itemsMap.set(item.item_id, item)
    })
    
    // Update all builds with refreshed data
    buildTypes.forEach(buildType => {
      if (buildsData[buildType]?.items) {
        buildsData[buildType].items = buildsData[buildType].items.map(item => {
          const refreshedItem = itemsMap.get(item.item_id)
          return refreshedItem || item // Use refreshed data if available, otherwise keep original
        })
      }
    })
    
    // Trigger reactivity
    builds.value = { ...buildsData }
    
    console.log('Items refreshed successfully with latest metadata')
    
  } catch (error) {
    console.error('Error refreshing items:', error)
    // Don't show error to user, it's a background operation
  }
}

// Expose methods for parent component
defineExpose({
  loadBuild
})
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
    
    .equipment-section {
      margin-bottom: 2rem;
      padding-bottom: 2rem;
      border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }
  }
}

.panel-header {
  background: rgba(92, 107, 192, 0.2);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  padding: 1rem 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  
  .header-row {
    display: flex;
    align-items: center;
  }
  
  .header-title-row {
    h2 {
      margin: 0;
      font-size: 1.5rem;
      color: #fff;
      font-weight: 700;
    }
  }
  
  .header-actions-row {
    justify-content: flex-end;
    gap: 0.75rem;
    
    @media (max-width: 768px) {
      flex-direction: column;
      
      :deep(.p-button) {
        width: 100%;
      }
    }
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

.save-button-header,
.history-button-header {
  flex-shrink: 0;
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

.preset-display {
  margin-top: 1rem;
  padding: 0.75rem 1rem;
  background: rgba(76, 175, 80, 0.15);
  border: 1px solid rgba(76, 175, 80, 0.3);
  border-radius: 8px;
  
  .preset-info {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    
    i {
      color: #4CAF50;
      font-size: 1.2rem;
    }
    
    .preset-text {
      color: #e0e0e0;
      font-size: 0.95rem;
      
      strong {
        color: #fff;
        font-weight: 600;
      }
    }
  }
}
</style>

