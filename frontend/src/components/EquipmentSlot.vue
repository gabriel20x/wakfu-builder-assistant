<template>
  <div 
    class="equipment-slot" 
    :class="{ 'has-item': hasItem, 'empty-slot': !hasItem, 'clickable': hasItem }"
    :title="itemName"
    @click="onSlotClick"
  >
    <div class="slot-border" :style="{ borderColor: rarityColor }">
      <div v-if="hasItem" class="item-image-container">
        <img
          :src="itemImageUrl"
          :alt="itemName"
          class="item-image"
          @error="onImageError"
        />
      </div>
      <div v-else class="empty-slot-icon">
        <i :class="slotIcon"></i>
      </div>
    </div>
    <div class="slot-label">{{ label }}</div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { getRarityColor } from '../composables/useStats'
import { useLanguage } from '../composables/useLanguage'

const props = defineProps({
  slotName: {
    type: String,
    required: true
  },
  label: {
    type: String,
    required: true
  },
  item: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['item-click'])

const { getItemName } = useLanguage()

const onSlotClick = () => {
  if (hasItem.value) {
    emit('item-click', props.item)
  }
}

const hasItem = computed(() => props.item !== null && props.item !== undefined)

const itemName = computed(() => {
  if (!hasItem.value) return props.label
  return getItemName(props.item)
})

const rarityColor = computed(() => {
  if (!hasItem.value) return '#808080'
  
  if (props.item.is_epic) return '#D946EF'
  if (props.item.is_relic) return '#E91E63'
  if (props.item.rarity === 6 && !props.item.is_relic) return '#87CEFA'
  
  return getRarityColor(props.item.rarity)
})

const imageSources = computed(() => {
  if (!hasItem.value) return []
  
  const sources = []
  
  if (props.item.gfx_id) {
    sources.push(`https://vertylo.github.io/wakassets/items/${props.item.gfx_id}.png`)
  }
  
  if (props.item.raw_data?.definition?.item?.graphicParameters?.gfxId) {
    const gfxId = props.item.raw_data.definition.item.graphicParameters.gfxId
    if (!sources.includes(`https://vertylo.github.io/wakassets/items/${gfxId}.png`)) {
      sources.push(`https://vertylo.github.io/wakassets/items/${gfxId}.png`)
    }
  }
  
  if (props.item.type_id && props.item.item_id) {
    sources.push(`https://vertylo.github.io/wakassets/items/${props.item.type_id}${props.item.item_id}.png`)
  }
  
  return sources
})

const itemImageUrl = computed(() => {
  if (!hasItem.value || imageSources.value.length === 0) return ''
  return imageSources.value[0]
})

let currentSourceIndex = 0

const onImageError = (event) => {
  currentSourceIndex++
  
  if (currentSourceIndex < imageSources.value.length) {
    event.target.src = imageSources.value[currentSourceIndex]
    return
  }
  
  // Fallback to emoji icon
  const slotIcons = {
    head: '⛑️',
    neck: '📿',
    chest: '👕',
    boots: '👖',
    back: '🎒',
    shoulders: '🦾',
    belt: '⚡',
    weapon1: '⚔️',
    weapon2: '🗡️',
    accessory: '💫',
    ring: '💍',
    ring2: '💍',
    pet: '🐾',
    mount: '🐴'
  }
  
  const icon = slotIcons[props.slotName] || '⚡'
  const color = rarityColor.value.replace('#', '')
  
  event.target.src = `data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='64' height='64' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' fill='%23${color}' opacity='0.2'/%3E%3Ctext x='50%25' y='50%25' text-anchor='middle' dy='.3em' font-size='32'%3E${icon}%3C/text%3E%3C/svg%3E`
}

const slotIcon = computed(() => {
  const icons = {
    head: 'pi pi-shield',
    neck: 'pi pi-circle',
    chest: 'pi pi-box',
    boots: 'pi pi-minus',
    back: 'pi pi-flag',
    shoulders: 'pi pi-th-large',
    belt: 'pi pi-minus',
    weapon1: 'pi pi-bolt',
    weapon2: 'pi pi-bolt',
    accessory: 'pi pi-star',
    ring: 'pi pi-circle',
    ring2: 'pi pi-circle',
    pet: 'pi pi-heart',
    mount: 'pi pi-heart'
  }
  return icons[props.slotName] || 'pi pi-circle'
})
</script>

<style lang="scss" scoped>
.equipment-slot {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.25rem;
  transition: transform 0.2s;
  
  &.clickable {
    cursor: pointer;
    
    &:hover {
      transform: scale(1.05);
    }
    
    &:active {
      transform: scale(0.98);
    }
  }
}

.slot-border {
  width: 64px;
  height: 64px;
  border: 2px solid;
  border-radius: 8px;
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
  position: relative;
  overflow: hidden;
  
  .has-item & {
    box-shadow: 0 0 10px currentColor;
  }
  
  .empty-slot & {
    border-color: rgba(255, 255, 255, 0.2);
    background: rgba(0, 0, 0, 0.2);
  }
}

.item-image-container {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.item-image {
  width: 56px;
  height: 56px;
  object-fit: contain;
}

.empty-slot-icon {
  color: rgba(255, 255, 255, 0.2);
  font-size: 1.5rem;
}

.slot-label {
  font-size: 0.7rem;
  color: #a0a0a0;
  text-align: center;
  white-space: nowrap;
  font-weight: 500;
}

.has-item .slot-label {
  color: #e0e0e0;
}
</style>

