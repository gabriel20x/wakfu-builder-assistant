<template>
  <div class="element-preferences">
    <h3>{{ t('elements.title') }}</h3>
    <p class="help-text">{{ t('elements.damageHelp') }}</p>
    
    <div class="preference-sections">
      <!-- Daños Elementales -->
      <div class="preference-section">
        <div class="section-header">
          <span class="section-icon">⚔️</span>
          <span>{{ t('elements.damagePrefs') }}</span>
        </div>
        <div class="draggable-list">
          <div 
            v-for="(element, index) in damageOrder" 
            :key="element.key"
            class="draggable-item"
            draggable="true"
            @dragstart="onDragStart(index, 'damage')"
            @dragover.prevent
            @drop="onDrop(index, 'damage')"
          >
            <i class="pi pi-bars drag-handle"></i>
            <span class="element-icon">{{ element.icon }}</span>
            <span class="element-label">{{ element.label }}</span>
            <span class="priority-badge">{{ index + 1 }}</span>
          </div>
        </div>
      </div>
      
      <!-- Resistencias Elementales -->
      <div class="preference-section">
        <div class="section-header">
          <span class="section-icon">🛡️</span>
          <span>{{ t('elements.resistancePrefs') }}</span>
        </div>
        <div class="draggable-list">
          <div 
            v-for="(element, index) in resistanceOrder" 
            :key="element.key"
            class="draggable-item"
            draggable="true"
            @dragstart="onDragStart(index, 'resistance')"
            @dragover.prevent
            @drop="onDrop(index, 'resistance')"
          >
            <i class="pi pi-bars drag-handle"></i>
            <span class="element-icon">{{ element.icon }}</span>
            <span class="element-label">{{ element.label }}</span>
            <span class="priority-badge">{{ index + 1 }}</span>
          </div>
        </div>
      </div>
    </div>
    
    <div class="reset-section">
      <p-button 
        label="Restablecer a predeterminado" 
        size="small"
        severity="secondary"
        text
        icon="pi pi-refresh"
        @click="resetToDefaults"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useI18n } from '../composables/useI18n'

const { t } = useI18n()

const props = defineProps({
  damagePreferences: {
    type: Array,
    default: () => ['Fire', 'Water', 'Earth', 'Air']
  },
  resistancePreferences: {
    type: Array,
    default: () => ['Fire', 'Water', 'Earth', 'Air']
  }
})

const emit = defineEmits(['update:damagePreferences', 'update:resistancePreferences'])

// Element definitions
const elements = [
  { key: 'Fire', label: 'Fuego', icon: '🔥' },
  { key: 'Water', label: 'Agua', icon: '💧' },
  { key: 'Earth', label: 'Tierra', icon: '🌍' },
  { key: 'Air', label: 'Aire', icon: '💨' }
]

// Initialize orders from props
const damageOrder = ref(
  props.damagePreferences.map(key => 
    elements.find(e => e.key === key)
  )
)

const resistanceOrder = ref(
  props.resistancePreferences.map(key => 
    elements.find(e => e.key === key)
  )
)

// Drag and drop state
let draggedIndex = null
let dragType = null

const onDragStart = (index, type) => {
  draggedIndex = index
  dragType = type
}

const onDrop = (targetIndex, type) => {
  if (draggedIndex === null || dragType !== type) return
  
  const list = type === 'damage' ? damageOrder : resistanceOrder
  const item = list.value[draggedIndex]
  
  // Remove from old position
  list.value.splice(draggedIndex, 1)
  
  // Insert at new position
  list.value.splice(targetIndex, 0, item)
  
  // Reset drag state
  draggedIndex = null
  dragType = null
  
  // Emit changes
  emitChanges()
}

const emitChanges = () => {
  emit('update:damagePreferences', damageOrder.value.map(e => e.key))
  emit('update:resistancePreferences', resistanceOrder.value.map(e => e.key))
}

const resetToDefaults = () => {
  damageOrder.value = [...elements]
  resistanceOrder.value = [...elements]
  emitChanges()
}

// Watch for prop changes
watch(() => props.damagePreferences, (newVal) => {
  damageOrder.value = newVal.map(key => elements.find(e => e.key === key))
}, { deep: true })

watch(() => props.resistancePreferences, (newVal) => {
  resistanceOrder.value = newVal.map(key => elements.find(e => e.key === key))
}, { deep: true })
</script>

<style lang="scss" scoped>
.element-preferences {
  h3 {
    margin: 0 0 0.5rem 0;
    font-size: 1.1rem;
    color: #fff;
  }
  
  .help-text {
    margin: 0.5rem 0 1rem 0;
    color: #808080;
    font-size: 0.875rem;
  }
}

.preference-sections {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.preference-section {
  background: rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  padding: 1rem;
  
  .section-header {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 0.75rem;
    font-weight: 600;
    color: #e0e0e0;
    
    .section-icon {
      font-size: 1.2rem;
    }
  }
}

.draggable-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.draggable-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  background: rgba(26, 35, 50, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 6px;
  cursor: move;
  transition: all 0.2s;
  
  &:hover {
    background: rgba(26, 35, 50, 0.8);
    border-color: rgba(92, 107, 192, 0.5);
    box-shadow: 0 2px 8px rgba(92, 107, 192, 0.3);
  }
  
  &:active {
    opacity: 0.5;
  }
  
  .drag-handle {
    color: #808080;
    font-size: 1rem;
  }
  
  .element-icon {
    font-size: 1.5rem;
  }
  
  .element-label {
    flex: 1;
    color: #e0e0e0;
    font-weight: 500;
  }
  
  .priority-badge {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 28px;
    height: 28px;
    background: rgba(92, 107, 192, 0.3);
    border: 1px solid rgba(92, 107, 192, 0.5);
    border-radius: 50%;
    font-size: 0.875rem;
    font-weight: 600;
    color: #9fa8da;
  }
}

.reset-section {
  margin-top: 1rem;
  text-align: center;
}
</style>

