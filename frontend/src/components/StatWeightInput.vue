<template>
  <div class="stat-weight-input" :class="{ disabled: !stat.enabled }">
    <div class="stat-info">
      <p-checkbox 
        v-model="stat.enabled"
        :binary="true"
        :input-id="`stat-${stat.key}`"
        class="stat-checkbox"
      />
      <div class="stat-icon" v-if="stat.icon">
        {{ stat.icon }}
      </div>
      <label :for="`stat-${stat.key}`">
        {{ stat.label }}
      </label>
    </div>
    
    <div class="stat-controls">
      <p-inputNumber 
        v-model="stat.weight"
        :min="0"
        :max="10"
        :step="0.5"
        :min-fraction-digits="1"
        :max-fraction-digits="1"
        :disabled="!stat.enabled"
        show-buttons
        button-layout="horizontal"
        decrement-button-icon="pi pi-minus"
        increment-button-icon="pi pi-plus"
        class="weight-input"
      />
    </div>
  </div>
</template>

<script setup>
defineProps({
  stat: {
    type: Object,
    required: true
  }
})
</script>

<style lang="scss" scoped>
.stat-weight-input {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.5rem 0.75rem;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 4px;
  transition: all 0.2s;
  border: 1px solid rgba(255, 255, 255, 0.05);
  
  &:hover {
    background: rgba(0, 0, 0, 0.4);
    border-color: rgba(255, 255, 255, 0.1);
  }
  
  &.disabled {
    opacity: 0.5;
  }
}

.stat-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex: 1;
  
  .stat-checkbox {
    flex-shrink: 0;
  }
  
  .stat-icon {
    width: 24px;
    height: 24px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.25rem;
    flex-shrink: 0;
  }
  
  label {
    margin: 0;
    cursor: pointer;
    font-size: 0.9rem;
    color: #e0e0e0;
    transition: color 0.2s;
  }
}

.stat-controls {
  flex-shrink: 0;
  
  .weight-input {
    :deep(.p-inputnumber) {
      width: 120px;
    }
    
    :deep(.p-inputnumber-input) {
      background: rgba(0, 0, 0, 0.5);
      border: 1px solid rgba(255, 255, 255, 0.2);
      color: #e0e0e0;
      padding: 0.375rem 0.5rem;
      text-align: center;
      font-size: 0.9rem;
      font-weight: 600;
      width: 50px;
      
      &:focus {
        border-color: rgba(92, 107, 192, 0.5);
        box-shadow: 0 0 0 2px rgba(92, 107, 192, 0.2);
      }
      
      &:disabled {
        opacity: 0.4;
        cursor: not-allowed;
        background: rgba(0, 0, 0, 0.3);
      }
    }
    
    :deep(.p-inputnumber-button) {
      background: rgba(92, 107, 192, 0.3);
      border: 1px solid rgba(92, 107, 192, 0.4);
      color: #e0e0e0;
      width: 2rem;
      
      &:hover:not(:disabled) {
        background: rgba(92, 107, 192, 0.5);
        border-color: rgba(92, 107, 192, 0.6);
      }
      
      &:disabled {
        opacity: 0.3;
        cursor: not-allowed;
      }
    }
  }
}
</style>

