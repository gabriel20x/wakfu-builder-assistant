<template>
  <div class="item-card" :style="{ borderColor: rarityColor }">
    <div class="item-header" :style="{ background: rarityGradient }">
      <div class="item-image-wrapper">
        <img 
          :src="itemImageUrl" 
          :alt="item.name"
          class="item-image"
          @error="onImageError"
        />
      </div>
      
      <div class="item-basic-info">
        <div class="item-name">{{ itemName }}</div>
        <div class="item-meta">
          <span class="item-level">Nivel {{ item.level }}</span>
          <span v-if="item.slot" class="item-slot">{{ formatSlot(item.slot) }}</span>
        </div>
        <div class="item-tags">
          <span class="tag rarity-tag" :class="`rarity-${item.rarity}`" :style="{ borderColor: rarityColor, color: rarityColor }">
            {{ rarityName }}
          </span>
          <span v-if="item.has_gem_slot" class="tag gem">Gema</span>
        </div>
      </div>
    </div>

    <div class="item-body">
      <!-- Stats -->
      <ItemStatList :stats="item.stats" />
      
      <!-- Item Info -->
      <div class="item-footer">
        <div class="item-source">
          <i class="pi pi-map-marker"></i>
          <span>{{ formatSourceType(item.source_type) }}</span>
        </div>
        <div class="item-difficulty" :class="difficultyClass">
          <i class="pi pi-star-fill"></i>
          <span>{{ item.difficulty?.toFixed(1) || 'N/A' }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { getRarityColor, getRarityName } from '../composables/useStats'
import { useLanguage } from '../composables/useLanguage'
import ItemStatList from './ItemStatList.vue'

const props = defineProps({
  item: {
    type: Object,
    required: true
  }
})

const { getItemName } = useLanguage()

const itemName = computed(() => getItemName(props.item))

const rarityColor = computed(() => getRarityColor(props.item.rarity))

const rarityName = computed(() => getRarityName(props.item.rarity))

const rarityGradient = computed(() => {
  const color = rarityColor.value
  return `linear-gradient(135deg, ${color}22 0%, ${color}11 100%)`
})

const itemImageUrl = computed(() => {
  // Try to get image from WakfuAssets
  return `https://tmktahu.github.io/WakfuAssets/items/${props.item.item_id}.png`
})

const difficultyClass = computed(() => {
  const diff = props.item.difficulty || 0
  if (diff < 3) return 'easy'
  if (diff < 6) return 'medium'
  return 'hard'
})

const formatSlot = (slot) => {
  const slotNames = {
    'HEAD': 'Cabeza',
    'NECK': 'Cuello',
    'CHEST': 'Pecho',
    'LEGS': 'Piernas',
    'BACK': 'Espalda',
    'SHOULDERS': 'Hombros',
    'BELT': 'Cinturón',
    'FIRST_WEAPON': 'Arma',
    'SECOND_WEAPON': 'Arma 2',
    'ACCESSORY': 'Accesorio',
    'LEFT_HAND': 'Anillo',
    'RIGHT_HAND': 'Anillo',
    'PET': 'Mascota'
  }
  return slotNames[slot] || slot
}

const formatSourceType = (sourceType) => {
  const sourceNames = {
    'drop': 'Drop de Monstruo',
    'craft': 'Crafteo',
    'quest': 'Misión',
    'shop': 'Tienda',
    'dungeon': 'Mazmorra'
  }
  return sourceNames[sourceType] || sourceType || 'Desconocido'
}

const onImageError = (event) => {
  const shortName = itemName.value.substring(0, 2)
  event.target.src = 'https://via.placeholder.com/64?text=' + encodeURIComponent(shortName)
}
</script>

<style lang="scss" scoped>
.item-card {
  background: rgba(26, 35, 50, 0.8);
  border: 2px solid;
  border-radius: 12px;
  overflow: hidden;
  transition: transform 0.2s, box-shadow 0.2s;
  
  &:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
  }
}

.item-header {
  padding: 1rem;
  display: flex;
  gap: 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.item-image-wrapper {
  width: 64px;
  height: 64px;
  flex-shrink: 0;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid rgba(255, 255, 255, 0.2);
}

.item-image {
  width: 56px;
  height: 56px;
  object-fit: contain;
}

.item-basic-info {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.item-name {
  font-size: 1.1rem;
  font-weight: 600;
  color: #fff;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.item-meta {
  display: flex;
  gap: 0.75rem;
  font-size: 0.875rem;
  color: #a0a0a0;
}

.item-tags {
  display: flex;
  gap: 0.5rem;
  margin-top: 0.25rem;
}

.tag {
  padding: 0.125rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  
  &.rarity-tag {
    background: rgba(0, 0, 0, 0.4);
    border: 1px solid;
    backdrop-filter: blur(4px);
  }
  
  // Colores específicos por rareza
  &.rarity-1 { // Común - Gris
    background: rgba(128, 128, 128, 0.15);
    border-color: #808080;
    color: #b0b0b0;
  }
  
  &.rarity-2 { // Poco común - Verde
    background: rgba(76, 175, 80, 0.15);
    border-color: #4CAF50;
    color: #66BB6A;
  }
  
  &.rarity-3 { // Raro - Naranja
    background: rgba(255, 165, 0, 0.15);
    border-color: #FFA500;
    color: #FFB74D;
  }
  
  &.rarity-4 { // Mítico - Morado
    background: rgba(156, 39, 176, 0.15);
    border-color: #9C27B0;
    color: #BA68C8;
  }
  
  &.rarity-5 { // Legendario - Amarillo
    background: rgba(255, 215, 0, 0.15);
    border-color: #FFD700;
    color: #FFD700;
    font-weight: 700;
    text-shadow: 0 0 8px rgba(255, 215, 0, 0.5);
  }
  
  &.rarity-6 { // Reliquia - Cyan
    background: rgba(0, 188, 212, 0.15);
    border-color: #00BCD4;
    color: #4DD0E1;
    font-weight: 700;
    text-shadow: 0 0 8px rgba(0, 188, 212, 0.5);
  }
  
  &.rarity-7 { // Épico - Rojo
    background: rgba(255, 23, 68, 0.15);
    border-color: #FF1744;
    color: #FF5252;
    font-weight: 700;
    text-shadow: 0 0 8px rgba(255, 23, 68, 0.5);
  }
  
  &.gem {
    background: rgba(156, 39, 176, 0.2);
    color: #9c27b0;
    border: 1px solid rgba(156, 39, 176, 0.4);
  }
}

.item-body {
  padding: 1rem;
}

.item-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  font-size: 0.875rem;
}

.item-source {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #a0a0a0;
  
  i {
    font-size: 0.875rem;
  }
}

.item-difficulty {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-weight: 600;
  
  &.easy {
    background: rgba(76, 175, 80, 0.2);
    color: #4caf50;
  }
  
  &.medium {
    background: rgba(255, 165, 0, 0.2);
    color: #ffa500;
  }
  
  &.hard {
    background: rgba(244, 67, 54, 0.2);
    color: #f44336;
  }
  
  i {
    font-size: 0.75rem;
  }
}
</style>

