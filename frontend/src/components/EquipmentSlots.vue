<template>
  <div class="equipment-slots">
    <div class="equipment-header">
      <h3>Equipamiento</h3>
    </div>
    
    <div class="slots-container">
      <!-- Left Column -->
      <div class="slots-column left-column">
        <EquipmentSlot 
          slot-name="head"
          label="Cabeza"
          :item="getItemBySlot('HEAD')"
        />
        <EquipmentSlot 
          slot-name="neck"
          label="Cuello"
          :item="getItemBySlot('NECK')"
        />
        <EquipmentSlot 
          slot-name="chest"
          label="Pechera"
          :item="getItemBySlot('CHEST')"
        />
        <EquipmentSlot 
          slot-name="ring"
          label="Anillo 1"
          :item="getItemBySlot('LEFT_HAND', 0) || getItemBySlot('RIGHT_HAND', 0)"
        />
        <EquipmentSlot 
          slot-name="boots"
          label="Botas"
          :item="getItemBySlot('LEGS')"
        />
      </div>
      
      <!-- Center (Class Icon) -->
      <div class="character-display">
        <div class="character-placeholder">
          <img 
            v-if="selectedClass"
            :src="classIconUrl"
            :alt="selectedClass"
            class="class-icon"
            @error="onClassImageError"
          />
          <i v-else class="pi pi-user" style="font-size: 4rem; color: rgba(255, 255, 255, 0.2);"></i>
        </div>
      </div>
      
      <!-- Right Column -->
      <div class="slots-column right-column">
        <EquipmentSlot 
          slot-name="back"
          label="Capa"
          :item="getItemBySlot('BACK')"
        />
        <EquipmentSlot 
          slot-name="shoulders"
          label="Hombros"
          :item="getItemBySlot('SHOULDERS')"
        />
        <EquipmentSlot 
          slot-name="belt"
          label="Cinturón"
          :item="getItemBySlot('BELT')"
        />
        <EquipmentSlot 
          slot-name="ring2"
          label="Anillo 2"
          :item="getItemBySlot('LEFT_HAND', 1) || getItemBySlot('RIGHT_HAND', 0)"
        />
        <EquipmentSlot 
          slot-name="pet"
          label="Mascota"
          :item="getItemBySlot('PET')"
        />
      </div>
    </div>
    
    <!-- Bottom Row for Weapons and Accessory -->
    <div class="bottom-slots">
      <EquipmentSlot 
        slot-name="weapon2"
        label="Arma Secundaria"
        :item="getItemBySlot('SECOND_WEAPON')"
      />
      <EquipmentSlot 
        slot-name="weapon1"
        label="Arma Principal"
        :item="getItemBySlot('FIRST_WEAPON')"
      />
      <EquipmentSlot 
        slot-name="accessory"
        label="Insignia"
        :item="getItemBySlot('ACCESSORY')"
      />
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import EquipmentSlot from './EquipmentSlot.vue'

const props = defineProps({
  items: {
    type: Array,
    default: () => []
  },
  selectedClass: {
    type: String,
    default: null
  }
})

const getItemBySlot = (slotName, index = 0) => {
  if (!props.items || props.items.length === 0) return null
  const items = props.items.filter(item => item.slot === slotName)
  return items[index] || null
}

const classIconUrl = computed(() => {
  if (!props.selectedClass) return ''
  return `https://tmktahu.github.io/WakfuAssets/classes/${props.selectedClass}.png`
})

const onClassImageError = (event) => {
  // Alternative spellings for class names
  const alternativeUrls = {
    'sacrieur': 'https://tmktahu.github.io/WakfuAssets/classes/sacrier.png',
    'enutrof': 'https://tmktahu.github.io/WakfuAssets/classes/enutrof.png',
    'zobal': 'https://tmktahu.github.io/WakfuAssets/classes/masqueraider.png',
    'steamer': 'https://tmktahu.github.io/WakfuAssets/classes/foggernaut.png'
  }
  
  if (alternativeUrls[props.selectedClass] && !event.target.dataset.triedAlternative) {
    event.target.dataset.triedAlternative = 'true'
    event.target.src = alternativeUrls[props.selectedClass]
    return
  }
  
  // Fallback to generic icon
  event.target.src = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="120" height="120" viewBox="0 0 120 120"%3E%3Ctext x="50%25" y="50%25" text-anchor="middle" dy=".3em" fill="%23667eea" font-size="80" font-weight="bold"%3E⚔%3C/text%3E%3C/svg%3E'
}
</script>

<style lang="scss" scoped>
.equipment-slots {
  width: 100%;
  padding: 1rem;
  background: rgba(26, 35, 50, 0.6);
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.equipment-header {
  text-align: center;
  margin-bottom: 1.5rem;
  
  h3 {
    margin: 0;
    color: #fff;
    font-size: 1.2rem;
    font-weight: 600;
  }
}

.slots-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
}

.slots-column {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  flex: 1;
  
  &.left-column {
    align-items: flex-end;
  }
  
  &.right-column {
    align-items: flex-start;
  }
}

.character-display {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.character-placeholder {
  width: 120px;
  height: 180px;
  background: rgba(0, 0, 0, 0.3);
  border: 2px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  
  .class-icon {
    width: 100px;
    height: 100px;
    object-fit: contain;
    filter: drop-shadow(0 0 10px rgba(92, 107, 192, 0.5));
  }
}

.bottom-slots {
  display: flex;
  justify-content: center;
  gap: 0.75rem;
  padding-top: 1rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

@media (max-width: 768px) {
  .slots-container {
    flex-direction: column;
  }
  
  .slots-column {
    width: 100%;
    
    &.left-column,
    &.right-column {
      align-items: center;
    }
  }
  
  .bottom-slots {
    flex-wrap: wrap;
  }
}
</style>

