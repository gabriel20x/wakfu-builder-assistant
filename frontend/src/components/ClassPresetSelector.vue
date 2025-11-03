<template>
  <div class="class-preset-selector">
    <div class="selector-header">
      <i class="pi pi-star-fill"></i>
      <span>Quick Start - Presets por Clase</span>
    </div>
    <p class="help-text">Selecciona tu clase y rol para autoconfigurar los stats</p>
    
    <div class="selectors-grid">
      <!-- Class Selector -->
      <div class="selector-group">
        <label>Clase</label>
        <p-dropdown
          v-model="selectedClass"
          :options="classes"
          option-label="name"
          option-value="id"
          placeholder="Selecciona tu clase"
          :loading="loadingClasses"
          @change="onClassChange"
          class="w-full"
        >
          <template #value="slotProps">
            <div v-if="slotProps.value" class="flex align-items-center">
              <img 
                :src="`https://tmktahu.github.io/WakfuAssets/classes/${slotProps.value}.png`" 
                :alt="slotProps.value"
                class="class-icon mr-2"
                @error="onImageError"
              />
              <span>{{ getClassName(slotProps.value) }}</span>
            </div>
            <span v-else>{{ slotProps.placeholder }}</span>
          </template>
          
          <template #option="slotProps">
            <div class="flex align-items-center">
              <img 
                :src="`https://tmktahu.github.io/WakfuAssets/classes/${slotProps.option.id}.png`" 
                :alt="slotProps.option.id"
                class="class-icon mr-2"
                @error="onImageError"
              />
              <span>{{ slotProps.option.name }}</span>
            </div>
          </template>
        </p-dropdown>
      </div>

      <!-- Role Selector -->
      <div class="selector-group">
        <label>Rol / Build</label>
        <p-dropdown
          v-model="selectedRole"
          :options="roles"
          option-label="name"
          option-value="id"
          placeholder="Selecciona rol"
          :disabled="!selectedClass"
          :loading="loadingRoles"
          class="w-full"
        >
          <template #value="slotProps">
            <div v-if="slotProps.value" class="flex align-items-center">
              <i :class="getRoleIcon(slotProps.value)" class="mr-2"></i>
              <span>{{ getRoleName(slotProps.value) }}</span>
            </div>
            <span v-else>{{ slotProps.placeholder }}</span>
          </template>
          
          <template #option="slotProps">
            <div class="flex flex-column">
              <div class="flex align-items-center mb-1">
                <i :class="getRoleIcon(slotProps.option.id)" class="mr-2"></i>
                <span class="font-semibold">{{ slotProps.option.name }}</span>
                <p-tag v-if="slotProps.option.is_primary" value="Principal" severity="success" class="ml-2" />
              </div>
              <small class="text-sm opacity-70">{{ slotProps.option.description }}</small>
              <div v-if="slotProps.option.elements.length" class="flex gap-1 mt-1">
                <p-tag 
                  v-for="element in slotProps.option.elements" 
                  :key="element"
                  :value="getElementEmoji(element)"
                  severity="secondary"
                  class="element-tag"
                />
              </div>
            </div>
          </template>
        </p-dropdown>
      </div>
    </div>

    <!-- Apply Button -->
    <p-button
      :label="loadingPreset ? 'Aplicando...' : 'Aplicar Preset'"
      icon="pi pi-check"
      :disabled="!selectedClass || !selectedRole"
      :loading="loadingPreset"
      @click="applyPreset"
      class="apply-button"
    />

    <!-- Preview Stats (opcional) -->
    <div v-if="previewStats" class="preset-preview">
      <div class="preview-header">
        <i class="pi pi-eye"></i>
        <span>Vista Previa de Stats</span>
      </div>
      <div class="preview-stats">
        <div v-for="(weight, stat) in topStats" :key="stat" class="preview-stat">
          <span class="stat-name">{{ getStatLabel(stat) }}</span>
          <div class="stat-bar">
            <div class="stat-bar-fill" :style="{ width: `${weight * 10}%` }"></div>
            <span class="stat-value">{{ weight.toFixed(1) }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useToast } from 'primevue/usetoast'
import { presetsAPI } from '../services/api'
import { getStatLabel } from '../composables/useStats'

const emit = defineEmits(['preset-applied'])
const toast = useToast()

const selectedClass = ref(null)
const selectedRole = ref(null)
const classes = ref([])
const roles = ref([])
const previewStats = ref(null)

const loadingClasses = ref(false)
const loadingRoles = ref(false)
const loadingPreset = ref(false)

// Top 6 stats for preview
const topStats = computed(() => {
  if (!previewStats.value) return {}
  
  const sorted = Object.entries(previewStats.value)
    .sort(([, a], [, b]) => b - a)
    .slice(0, 6)
  
  return Object.fromEntries(sorted)
})

// Load classes on mount
const loadClasses = async () => {
  loadingClasses.value = true
  try {
    const response = await presetsAPI.getClasses()
    classes.value = response.data
  } catch (error) {
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: 'No se pudieron cargar las clases',
      life: 3000
    })
  } finally {
    loadingClasses.value = false
  }
}

// Load roles when class changes
const onClassChange = async () => {
  if (!selectedClass.value) {
    roles.value = []
    selectedRole.value = null
    previewStats.value = null
    return
  }
  
  loadingRoles.value = true
  try {
    const response = await presetsAPI.getClassRoles(selectedClass.value)
    roles.value = response.data
    
    // Auto-select primary role
    const primaryRole = roles.value.find(r => r.is_primary)
    selectedRole.value = primaryRole?.id || roles.value[0]?.id || null
    
    // Load preview if role selected
    if (selectedRole.value) {
      await loadPreview()
    }
  } catch (error) {
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: 'No se pudieron cargar los roles',
      life: 3000
    })
  } finally {
    loadingRoles.value = false
  }
}

// Watch role changes to update preview
watch(selectedRole, async (newRole) => {
  if (newRole && selectedClass.value) {
    await loadPreview()
  }
})

// Load preview stats
const loadPreview = async () => {
  try {
    const response = await presetsAPI.getClassPreset(selectedClass.value, selectedRole.value)
    previewStats.value = response.data.weights
  } catch (error) {
    console.error('Error loading preview:', error)
  }
}

// Apply the preset
const applyPreset = async () => {
  if (!selectedClass.value || !selectedRole.value) return
  
  loadingPreset.value = true
  try {
    const response = await presetsAPI.getClassPreset(selectedClass.value, selectedRole.value)
    const preset = response.data
    
    emit('preset-applied', {
      weights: preset.weights,
      damagePreferences: preset.damage_preferences,
      resistancePreferences: preset.resistance_preferences,
      className: getClassName(selectedClass.value),
      roleName: getRoleName(selectedRole.value)
    })
    
    toast.add({
      severity: 'success',
      summary: 'Preset Aplicado',
      detail: `${getClassName(selectedClass.value)} - ${getRoleName(selectedRole.value)}`,
      life: 3000
    })
  } catch (error) {
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: 'No se pudo aplicar el preset',
      life: 3000
    })
  } finally {
    loadingPreset.value = false
  }
}

// Helper functions
const getClassName = (classId) => {
  return classes.value.find(c => c.id === classId)?.name || classId
}

const getRoleName = (roleId) => {
  return roles.value.find(r => r.id === roleId)?.name || roleId
}

const getRoleIcon = (roleId) => {
  const icons = {
    'tank': 'pi pi-shield',
    'dps_melee': 'pi pi-bolt',
    'dps_distance': 'pi pi-arrow-up-right',
    'healer': 'pi pi-heart-fill',
    'support': 'pi pi-users',
    'berserker': 'pi pi-star-fill'
  }
  
  // Check if roleId contains any of the keys
  for (const [key, icon] of Object.entries(icons)) {
    if (roleId?.includes(key)) return icon
  }
  
  return 'pi pi-star'
}

const getElementEmoji = (element) => {
  const emojis = {
    'Fire': '🔥',
    'Water': '💧',
    'Earth': '🌍',
    'Air': '💨'
  }
  return emojis[element] || '⚡'
}

const onImageError = (event) => {
  event.target.style.display = 'none'
}

// Load classes on mount
loadClasses()
</script>

<style lang="scss" scoped>
.class-preset-selector {
  background: rgba(0, 0, 0, 0.3);
  border-radius: 8px;
  padding: 1rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.selector-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
  
  i {
    color: #ffd700;
    font-size: 1.1rem;
  }
  
  span {
    font-weight: 600;
    font-size: 1rem;
    color: #fff;
  }
}

.help-text {
  margin: 0 0 1rem 0;
  color: #808080;
  font-size: 0.875rem;
}

.selectors-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.75rem;
  margin-bottom: 1rem;
  
  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
}

.selector-group {
  label {
    display: block;
    margin-bottom: 0.5rem;
    color: #a0a0a0;
    font-size: 0.875rem;
    font-weight: 500;
  }
}

.class-icon {
  width: 24px;
  height: 24px;
  object-fit: contain;
  border-radius: 4px;
}

.element-tag {
  font-size: 0.7rem;
  padding: 0.15rem 0.4rem;
}

.apply-button {
  width: 100%;
  font-weight: 600;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  
  &:hover:not(:disabled) {
    background: linear-gradient(135deg, #7c8ff0 0%, #8c5bb2 100%);
  }
}

.preset-preview {
  margin-top: 1rem;
  padding: 0.75rem;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 6px;
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.preview-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
  
  i {
    color: #9fa8da;
  }
  
  span {
    font-size: 0.875rem;
    font-weight: 600;
    color: #9fa8da;
  }
}

.preview-stats {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.preview-stat {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.stat-name {
  font-size: 0.75rem;
  color: #a0a0a0;
}

.stat-bar {
  position: relative;
  height: 20px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 4px;
  overflow: hidden;
}

.stat-bar-fill {
  position: absolute;
  left: 0;
  top: 0;
  height: 100%;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
  transition: width 0.3s ease;
}

.stat-value {
  position: absolute;
  right: 0.5rem;
  top: 50%;
  transform: translateY(-50%);
  font-size: 0.75rem;
  font-weight: 600;
  color: #fff;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.5);
}

:deep(.p-dropdown) {
  background: rgba(0, 0, 0, 0.4);
  border: 1px solid rgba(255, 255, 255, 0.2);
  
  .p-dropdown-label {
    color: #e0e0e0;
  }
  
  &:hover {
    border-color: rgba(92, 107, 192, 0.5);
  }
}

:deep(.p-dropdown-panel) {
  background: rgba(26, 35, 50, 0.95);
  border: 1px solid rgba(255, 255, 255, 0.2);
  
  .p-dropdown-item {
    color: #e0e0e0;
    
    &:hover {
      background: rgba(92, 107, 192, 0.3);
    }
    
    &.p-highlight {
      background: rgba(92, 107, 192, 0.5);
    }
  }
}
</style>

