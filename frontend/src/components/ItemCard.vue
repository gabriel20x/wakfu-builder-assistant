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
          <span 
            class="tag rarity-tag" 
            :class="item.is_epic ? 'rarity-epic' : `rarity-${item.rarity}`" 
            :style="{ borderColor: rarityColor, color: rarityColor }"
          >
            {{ rarityName }}
          </span>
          <span v-if="item.is_relic" class="tag special-tag">⚡ Única</span>
          <span v-if="item.is_epic" class="tag special-tag">⚡ Única</span>
          <span v-if="item.has_gem_slot" class="tag gem">💎 Gema</span>
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

const rarityColor = computed(() => {
  // Épicos se identifican con flag is_epic, no con rarity
  if (props.item.is_epic) {
    return '#D946EF' // Épico - Fucsia/Rosa (tono más púrpura)
  }
  return getRarityColor(props.item.rarity)
})

const rarityName = computed(() => {
  // Épicos tienen su propio nombre
  if (props.item.is_epic) {
    return 'Épico'
  }
  return getRarityName(props.item.rarity)
})

const rarityGradient = computed(() => {
  const color = rarityColor.value
  return `linear-gradient(135deg, ${color}22 0%, ${color}11 100%)`
})

const itemImageUrl = computed(() => {
  // Try to get image from WakfuAssets
  // If not available, will fallback to placeholder in onImageError
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
    'PET': 'Mascota',
    'MOUNT': 'Montura'
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
  // Fallback to a simple colored placeholder with first letter
  const firstLetter = itemName.value.charAt(0).toUpperCase()
  const color = rarityColor.value.replace('#', '')
  event.target.src = `https://via.placeholder.com/64/${color}/ffffff?text=${encodeURIComponent(firstLetter)}`
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
  
  // Colores específicos por rareza (según tabla oficial de Wakfu)
  &.rarity-0,
  &.rarity-1 { // Común - Gris
    background: rgba(128, 128, 128, 0.15);
    border-color: #808080;
    color: #b0b0b0;
  }
  
  &.rarity-2 { // Inusual - Gris claro
    background: rgba(158, 158, 158, 0.15);
    border-color: #9E9E9E;
    color: #BDBDBD;
  }
  
  &.rarity-3 { // Raro - Verde
    background: rgba(76, 175, 80, 0.15);
    border-color: #4CAF50;
    color: #66BB6A;
  }
  
  &.rarity-4 { // Mítico - Naranja
    background: rgba(255, 152, 0, 0.15);
    border-color: #FF9800;
    color: #FFB74D;
  }
  
  &.rarity-5 { // Reliquia - Fucsia/Rosa
    background: rgba(233, 30, 99, 0.15);
    border-color: #E91E63;
    color: #F06292;
    font-weight: 700;
    text-shadow: 0 0 8px rgba(233, 30, 99, 0.5);
  }
  
  &.rarity-6 { // Recuerdo (Souvenir) - Celeste/Azul claro
    background: rgba(79, 195, 247, 0.15);
    border-color: #4FC3F7;
    color: #81D4FA;
    font-weight: 700;
    text-shadow: 0 0 8px rgba(79, 195, 247, 0.5);
  }
  
  &.rarity-7 { // Legendario - Dorado/Amarillo
    background: rgba(255, 215, 0, 0.15);
    border-color: #FFD700;
    color: #FFD700;
    font-weight: 700;
    text-shadow: 0 0 8px rgba(255, 215, 0, 0.5);
  }
  
  &.rarity-epic { // Épico - Fucsia/Rosa (tono más púrpura)
    background: rgba(217, 70, 239, 0.15);
    border-color: #D946EF;
    color: #E879F9;
    font-weight: 700;
    text-shadow: 0 0 8px rgba(217, 70, 239, 0.5);
  }
  
  &.gem {
    background: rgba(156, 39, 176, 0.2);
    color: #9c27b0;
    border: 1px solid rgba(156, 39, 176, 0.4);
  }
  
  &.special-tag {
    background: rgba(255, 215, 0, 0.2);
    color: #FFD700;
    border: 1px solid rgba(255, 215, 0, 0.4);
    font-size: 0.7rem;
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

