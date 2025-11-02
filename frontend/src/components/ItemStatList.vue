<template>
  <div class="item-stat-list">
    <div v-if="Object.keys(stats).length === 0" class="no-stats">
      <span>Sin stats</span>
    </div>
    
    <div v-else class="stats-table">
      <div 
        v-for="(value, stat) in stats" 
        :key="stat"
        class="stat-row"
        :class="{ positive: value > 0, negative: value < 0 }"
      >
        <div class="stat-icon-small">
          <img 
            :src="getStatIconUrl(stat)" 
            :alt="stat"
            @error="onImageError"
          />
        </div>
        <div class="stat-label-small">{{ getStatLabel(stat) }}</div>
        <div class="stat-value-small">
          <span class="value-number">{{ formatValue(stat, value) }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { getStatLabel, getStatIcon, getStatSuffix } from '../composables/useStats'

const props = defineProps({
  stats: {
    type: Object,
    required: true
  }
})

const getStatIconUrl = (stat) => {
  const icon = getStatIcon(stat)
  return `https://tmktahu.github.io/WakfuAssets/statistics/${icon}`
}

const formatValue = (stat, value) => {
  const suffix = getStatSuffix(stat)
  if (typeof value === 'number') {
    const prefix = value > 0 ? '+' : ''
    return `${prefix}${value.toFixed(0)}${suffix}`
  }
  return `${value}${suffix}`
}

const onImageError = (event) => {
  event.target.style.display = 'none'
}
</script>

<style lang="scss" scoped>
.item-stat-list {
  width: 100%;
}

.no-stats {
  padding: 1rem;
  text-align: center;
  color: #808080;
  font-style: italic;
}

.stats-table {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.stat-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 4px;
  font-size: 0.875rem;
  transition: background 0.2s;
  
  &:hover {
    background: rgba(0, 0, 0, 0.3);
  }
  
  &.positive {
    .value-number {
      color: #4caf50;
    }
  }
  
  &.negative {
    .value-number {
      color: #f44336;
    }
  }
}

.stat-icon-small {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 4px;
  
  img {
    width: 16px;
    height: 16px;
    object-fit: contain;
  }
}

.stat-label-small {
  flex: 1;
  color: #e0e0e0;
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.stat-value-small {
  font-weight: 600;
  color: #fff;
  flex-shrink: 0;
}

.value-number {
  font-family: 'Courier New', monospace;
}
</style>

