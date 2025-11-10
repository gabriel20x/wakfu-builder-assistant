<template>
  <div class="monster-type-filter">
    <div class="filter-header">
      <h3>{{ t('monsterTypeFilter.title') }}</h3>
      <p class="filter-description">{{ t('monsterTypeFilter.description') }}</p>
    </div>
    
    <div v-if="loading" class="loading">
      <span>{{ t('common.loading') }}</span>
    </div>
    
    <div v-else-if="error" class="error">
      <span>{{ t('monsterTypeFilter.error') }}: {{ error }}</span>
    </div>
    
    <div v-else class="monster-types">
      <div class="select-all-controls">
        <button @click="selectAll" class="btn-small">{{ t('monsterTypeFilter.selectAll') }}</button>
        <button @click="deselectAll" class="btn-small">{{ t('monsterTypeFilter.deselectAll') }}</button>
      </div>
      
      <div class="type-checkboxes">
        <label 
          v-for="type in availableTypes" 
          :key="type"
          class="type-checkbox"
          :class="{ 'selected': isTypeSelected(type) }"
        >
          <input
            type="checkbox"
            :value="type"
            v-model="selectedTypes"
            @change="emitChange"
          />
          <span class="type-label">
            <span class="type-icon" :class="`icon-${type}`">
              {{ getTypeIcon(type) }}
            </span>
            <span class="type-name">{{ getTypeName(type) }}</span>
            <span class="type-count">({{ typeCounts[type] || 0 }})</span>
          </span>
        </label>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { gamedataAPI } from '@/services/api'
import { useI18n } from '@/composables/useI18n'

export default {
  name: 'MonsterTypeFilter',
  emits: ['update:modelValue'],
  props: {
    modelValue: {
      type: Array,
      default: () => []
    }
  },
  setup(props, { emit }) {
    const { t } = useI18n()
    const availableTypes = ref([])
    const typeCounts = ref({})
    const selectedTypes = ref([...props.modelValue])
    const loading = ref(false)
    const error = ref(null)

    // Type translations and icons
    const typeTranslations = {
      'monster': { en: 'Monster', es: 'Monstruo', fr: 'Monstre', icon: '👹' },
      'boss': { en: 'Boss', es: 'Jefe', fr: 'Boss', icon: '👑' },
      'archmonster': { en: 'Archmonster', es: 'Archimonstruo', fr: 'Archimonstre', icon: '💀' },
      'ultimate_boss': { en: 'Ultimate Boss', es: 'Jefe Supremo', fr: 'Boss Ultime', icon: '🔥' },
      'dominant': { en: 'Dominant', es: 'Dominante', fr: 'Dominant', icon: '⚔️' }
    }

    const loadMonsterTypes = async () => {
      loading.value = true
      error.value = null
      
      try {
        const response = await gamedataAPI.getMonsterTypes()
        availableTypes.value = response.data.types || []
        typeCounts.value = response.data.counts || {}
        
        // If no types are selected, select all by default
        if (selectedTypes.value.length === 0) {
          selectedTypes.value = [...availableTypes.value]
          emitChange()
        }
      } catch (err) {
        console.error('Error loading monster types:', err)
        error.value = err.message || 'Failed to load monster types'
      } finally {
        loading.value = false
      }
    }

    const getTypeName = (type) => {
      const lang = localStorage.getItem('language') || 'en'
      return typeTranslations[type]?.[lang] || type
    }

    const getTypeIcon = (type) => {
      return typeTranslations[type]?.icon || '🎯'
    }

    const isTypeSelected = (type) => {
      return selectedTypes.value.includes(type)
    }

    const selectAll = () => {
      selectedTypes.value = [...availableTypes.value]
      emitChange()
    }

    const deselectAll = () => {
      selectedTypes.value = []
      emitChange()
    }

    const emitChange = () => {
      emit('update:modelValue', selectedTypes.value)
    }

    onMounted(() => {
      loadMonsterTypes()
    })

    return {
      t,
      availableTypes,
      typeCounts,
      selectedTypes,
      loading,
      error,
      getTypeName,
      getTypeIcon,
      isTypeSelected,
      selectAll,
      deselectAll,
      emitChange
    }
  }
}
</script>

<style scoped lang="scss">
.monster-type-filter {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.filter-header {
  margin-bottom: 1rem;
  
  h3 {
    margin: 0 0 0.5rem 0;
    color: #ffd700;
    font-size: 1.2rem;
  }
  
  .filter-description {
    margin: 0;
    color: rgba(255, 255, 255, 0.7);
    font-size: 0.9rem;
  }
}

.loading, .error {
  padding: 1rem;
  text-align: center;
  color: rgba(255, 255, 255, 0.7);
}

.error {
  color: #ff6b6b;
}

.select-all-controls {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
  
  .btn-small {
    padding: 0.4rem 0.8rem;
    font-size: 0.85rem;
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 4px;
    color: white;
    cursor: pointer;
    transition: all 0.2s;
    
    &:hover {
      background: rgba(255, 255, 255, 0.15);
      border-color: rgba(255, 255, 255, 0.3);
    }
  }
}

.type-checkboxes {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 0.75rem;
}

.type-checkbox {
  display: flex;
  align-items: center;
  padding: 0.75rem;
  background: rgba(255, 255, 255, 0.05);
  border: 2px solid rgba(255, 255, 255, 0.1);
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
  
  &:hover {
    background: rgba(255, 255, 255, 0.08);
    border-color: rgba(255, 255, 255, 0.2);
  }
  
  &.selected {
    background: rgba(255, 215, 0, 0.15);
    border-color: #ffd700;
  }
  
  input[type="checkbox"] {
    margin-right: 0.75rem;
    cursor: pointer;
    width: 18px;
    height: 18px;
  }
  
  .type-label {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    flex: 1;
  }
  
  .type-icon {
    font-size: 1.2rem;
  }
  
  .type-name {
    font-weight: 500;
    color: white;
  }
  
  .type-count {
    color: rgba(255, 255, 255, 0.6);
    font-size: 0.85rem;
    margin-left: auto;
  }
}
</style>
