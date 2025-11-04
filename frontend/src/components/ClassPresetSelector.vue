<template>
  <div class="class-preset-selector">
    <div class="selector-header">
      <i class="pi pi-star-fill"></i>
      <span>{{ t('quickStart.title') }}</span>
    </div>
    <p class="help-text">{{ t('quickStart.help') }}</p>
    
    <!-- Class Selector -->
    <div class="selector-group">
      <label>{{ t('quickStart.class') }}</label>
      <p-dropdown
        v-model="selectedClass"
        :options="classes"
        option-label="name"
        option-value="id"
        :placeholder="t('quickStart.selectClass')"
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
      <label>{{ t('quickStart.role') }}</label>
      <p-dropdown
        v-model="selectedRole"
        :options="roles"
        option-label="name"
        option-value="id"
        :placeholder="t('quickStart.selectRole')"
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
            <div class="flex align-items-center">
              <i :class="getRoleIcon(slotProps.option.id)" class="mr-2"></i>
              <span class="font-semibold">{{ slotProps.option.name }}</span>
              <div v-if="slotProps.option.elements && slotProps.option.elements.length" class="flex gap-1 ml-auto">
                <span
                  v-for="element in slotProps.option.elements" 
                  :key="element"
                  class="element-emoji"
                >{{ getElementEmoji(element) }}</span>
              </div>
            </div>
          </template>
        </p-dropdown>
      </div>

    <!-- Preview Stats (opcional) -->
    <div v-if="previewStats && Object.keys(previewStats).length > 0" class="preset-preview">
      <div class="preview-header">
        <i class="pi pi-eye"></i>
        <span>{{ t('quickStart.previewTitle') }}</span>
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
import { getStatLabel } from '../composables/useStats'
import { useI18n } from '../composables/useI18n'

const emit = defineEmits(['preset-applied'])
const toast = useToast()
const { t } = useI18n()

const selectedClass = ref(null)
const selectedRole = ref(null)
const classes = ref([])
const roles = ref([])
const previewStats = ref(null)
const classPresetsData = ref(null)

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

// Load classes from local JSON file
const loadClasses = async () => {
  loadingClasses.value = true
  try {
    const response = await fetch('/class-presets.json')
    classPresetsData.value = await response.json()
    classes.value = classPresetsData.value.classes.map(cls => ({
      id: cls.id,
      name: cls.name,
      description: cls.description
    }))
  } catch (error) {
    console.error('Error loading class presets:', error)
    toast.add({
      severity: 'error',
      summary: t('toast.error'),
      detail: t('toast.presetError'),
      life: 3000
    })
  } finally {
    loadingClasses.value = false
  }
}

// Load roles when class changes
const onClassChange = async () => {
  if (!selectedClass.value || !classPresetsData.value) {
    roles.value = []
    selectedRole.value = null
    previewStats.value = null
    return
  }
  
  loadingRoles.value = true
  try {
    const classData = classPresetsData.value.classes.find(c => c.id === selectedClass.value)
    if (classData) {
      roles.value = classData.roles
      
      // Auto-select primary role
      const primaryRole = roles.value.find(r => r.is_primary)
      selectedRole.value = primaryRole?.id || roles.value[0]?.id || null
      
      // Load preview if role selected
      if (selectedRole.value) {
        loadPreview()
      }
    }
  } catch (error) {
    console.error('Error loading roles:', error)
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

// Watch role changes to update preview AND auto-apply
watch(selectedRole, (newRole) => {
  if (newRole && selectedClass.value) {
    loadPreview()
    // Auto-apply preset when role changes
    applyPreset()
  }
})

// Load preview stats from local data
const loadPreview = () => {
  if (!classPresetsData.value || !selectedClass.value || !selectedRole.value) return
  
  const classData = classPresetsData.value.classes.find(c => c.id === selectedClass.value)
  if (classData) {
    const roleData = classData.roles.find(r => r.id === selectedRole.value)
    if (roleData) {
      previewStats.value = roleData.stat_priorities
    }
  }
}

// Apply the preset from local data
const applyPreset = () => {
  if (!selectedClass.value || !selectedRole.value || !classPresetsData.value) return
  
  loadingPreset.value = true
  try {
    const classData = classPresetsData.value.classes.find(c => c.id === selectedClass.value)
    if (!classData) throw new Error('Class not found')
    
    const roleData = classData.roles.find(r => r.id === selectedRole.value)
    if (!roleData) throw new Error('Role not found')
    
    // Build damage and resistance preferences from role elements
    // ✅ FIX: Always include all 4 elements, but prioritize role elements first
    const allElements = ['Fire', 'Water', 'Earth', 'Air']
    const damagePrefs = []
    
    // Add role elements first (priority)
    if (roleData.elements && roleData.elements.length > 0) {
      roleData.elements.forEach(elem => {
        if (!damagePrefs.includes(elem)) {
          damagePrefs.push(elem)
        }
      })
    }
    
    // Complete with remaining elements
    allElements.forEach(elem => {
      if (!damagePrefs.includes(elem)) {
        damagePrefs.push(elem)
      }
    })
    
    const resistancePrefs = ['Fire', 'Water', 'Earth', 'Air']
    
    emit('preset-applied', {
      weights: roleData.stat_priorities,
      damagePreferences: damagePrefs,
      resistancePreferences: resistancePrefs,
      className: classData.name,
      roleName: roleData.name,
      roleData: roleData // Pass full role data for reference
    })
    
    toast.add({
      severity: 'success',
      summary: t('toast.presetApplied'),
      detail: `${classData.name} - ${roleData.name}`,
      life: 3000
    })
  } catch (error) {
    console.error('Error applying preset:', error)
    toast.add({
      severity: 'error',
      summary: t('toast.error'),
      detail: t('toast.presetError'),
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
  // If class icon fails to load, show a generic icon
  event.target.src = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"%3E%3Ctext x="50%25" y="50%25" text-anchor="middle" dy=".3em" fill="%23667eea" font-size="16" font-weight="bold"%3E⚔%3C/text%3E%3C/svg%3E'
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

.selector-group {
  margin-bottom: 1rem;
  
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

.element-emoji {
  font-size: 1rem;
  margin: 0 0.125rem;
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
  align-items: center;
  gap: 0.5rem;
  padding: 0.4rem 0.6rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 4px;
}

.stat-name {
  font-size: 0.7rem;
  color: #a0a0a0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  flex: 1;
}

.stat-bar {
  position: relative;
  width: 40px;
  height: 16px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 3px;
  overflow: hidden;
  flex-shrink: 0;
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
  right: 0.25rem;
  top: 50%;
  transform: translateY(-50%);
  font-size: 0.65rem;
  font-weight: 600;
  color: #fff;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.8);
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
  background: rgba(26, 35, 50, 0.98);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.6);
  
  .p-dropdown-items {
    padding: 0.5rem;
  }
  
  .p-dropdown-item {
    color: #e0e0e0;
    padding: 0.75rem 1rem;
    border-radius: 6px;
    margin-bottom: 0.25rem;
    
    &:hover {
      background: rgba(92, 107, 192, 0.3);
    }
    
    &.p-highlight {
      background: rgba(92, 107, 192, 0.5);
    }
  }
}
</style>

