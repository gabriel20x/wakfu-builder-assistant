<template>
  <div class="build-result">
    <div class="build-content">
      <div class="build-header">
        <h3>Build {{ difficulty }}</h3>
        <div class="difficulty-badge" :class="difficultyClass">
          Dificultad: {{ build.total_difficulty?.toFixed(2) || 'N/A' }}
        </div>
      </div>

      <!-- Total Stats Summary -->
      <div v-if="showStats" class="stats-summary">
        <h4>Stats Totales</h4>
        <BuildStatSheet :stats="build.total_stats" />
      </div>

      <!-- Items -->
      <div class="items-section">
        <h4>Items Recomendados ({{ build.items?.length || 0 }})</h4>
        <div v-if="build.items && build.items.length > 0" class="items-grid">
          <ItemCard 
            v-for="item in build.items" 
            :key="item.item_id"
            :item="item"
            :metadata="item.metadata"
            :show-metadata-button="true"
            @edit-metadata="onEditMetadata"
          />
        </div>
        <div v-else class="no-items">
          <p>No se encontraron items para este build</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import ItemCard from './ItemCard.vue'
import BuildStatSheet from './BuildStatSheet.vue'

const props = defineProps({
  build: {
    type: Object,
    required: true
  },
  difficulty: {
    type: String,
    required: true
  },
  showStats: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['edit-metadata'])

const difficultyClass = computed(() => {
  const diff = props.build.total_difficulty || 0
  if (diff < 40) return 'easy'
  if (diff < 65) return 'medium'
  return 'hard'
})

const onEditMetadata = (item) => {
  emit('edit-metadata', item)
}
</script>

<style lang="scss" scoped>
.build-result {
  width: 100%;
  height: 100%;
}

.build-content {
  padding: 1.5rem;
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

.build-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid rgba(255, 255, 255, 0.1);
  
  h3 {
    margin: 0;
    font-size: 1.5rem;
    color: #fff;
  }
}

.difficulty-badge {
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-weight: 600;
  font-size: 0.875rem;
  
  &.easy {
    background: rgba(76, 175, 80, 0.2);
    color: #4caf50;
    border: 1px solid rgba(76, 175, 80, 0.4);
  }
  
  &.medium {
    background: rgba(255, 165, 0, 0.2);
    color: #ffa500;
    border: 1px solid rgba(255, 165, 0, 0.4);
  }
  
  &.hard {
    background: rgba(244, 67, 54, 0.2);
    color: #f44336;
    border: 1px solid rgba(244, 67, 54, 0.4);
  }
}

.stats-summary {
  margin-bottom: 2rem;
  
  h4 {
    margin: 0 0 1rem 0;
    color: #fff;
    font-size: 1.1rem;
  }
}

.items-section {
  h4 {
    margin: 0 0 1rem 0;
    color: #fff;
    font-size: 1.1rem;
  }
}

.items-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1rem;
  padding-bottom: 2rem;
  
  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
}

.no-items {
  padding: 2rem;
  text-align: center;
  color: #808080;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 8px;
  border: 1px dashed rgba(255, 255, 255, 0.1);
}
</style>

