<template>
  <div class="ignored-items-manager">
    <div class="manager-header">
      <h3>
        <i class="pi pi-ban"></i>
        {{ t('ignoredItems.title') }}
        <span class="count-badge">{{ ignoredItemsCount }}</span>
      </h3>
      <p class="help-text">{{ t('ignoredItems.description') }}</p>
    </div>

    <div v-if="ignoredItemsCount === 0" class="empty-state">
      <i class="pi pi-info-circle"></i>
      <p>{{ t('ignoredItems.empty') }}</p>
      <p class="help-text">{{ t('ignoredItems.emptyHelp') }}</p>
    </div>

    <div v-else class="ignored-items-list">
      <div
        v-for="item in ignoredItems"
        :key="item.item_id"
        class="ignored-item"
      >
        <div class="item-info">
          <div class="item-name" :style="{ color: getRarityColor(item.rarity) }">
            {{ item.name }}
          </div>
          <div class="item-meta">
            <span class="item-level">Niv. {{ item.level }}</span>
            <span class="item-slot">{{ formatSlot(item.slot) }}</span>
            <span class="item-rarity">{{ getRarityName(item.rarity) }}</span>
          </div>
          <div class="item-date">
            {{ t('ignoredItems.ignoredAt') }}: {{ formatDate(item.ignored_at) }}
          </div>
        </div>

        <button
          class="btn-unignore"
          @click="handleUnignore(item.item_id)"
          :title="t('ignoredItems.unignore')"
        >
          <i class="pi pi-check"></i>
          {{ t('ignoredItems.restore') }}
        </button>
      </div>

      <div class="manager-actions">
        <button
          class="btn-clear-all"
          @click="handleClearAll"
          :disabled="ignoredItemsCount === 0"
        >
          <i class="pi pi-trash"></i>
          {{ t('ignoredItems.clearAll') }}
        </button>

        <button class="btn-export" @click="handleExport">
          <i class="pi pi-download"></i>
          {{ t('ignoredItems.export') }}
        </button>

        <button class="btn-import" @click="handleImport">
          <i class="pi pi-upload"></i>
          {{ t('ignoredItems.import') }}
        </button>
      </div>
    </div>

    <!-- Hidden file input for import -->
    <input
      ref="fileInput"
      type="file"
      accept=".json"
      style="display: none"
      @change="onFileSelected"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useIgnoredItems } from '../composables/useIgnoredItems'
import { getRarityColor, getRarityName } from '../composables/useStats'
import { useI18n } from '../composables/useI18n'
import { useToast } from 'primevue/usetoast'

const { t } = useI18n()
const toast = useToast()
const {
  ignoredItems,
  ignoredItemsCount,
  unignoreItem,
  clearAllIgnoredItems,
  importIgnoredItems,
  exportIgnoredItems
} = useIgnoredItems()

const fileInput = ref(null)

const formatSlot = (slot) => {
  const slotNames = {
    HEAD: 'Cabeza',
    NECK: 'Cuello',
    CHEST: 'Pecho',
    LEGS: 'Piernas',
    BACK: 'Espalda',
    SHOULDERS: 'Hombros',
    BELT: 'Cinturón',
    FIRST_WEAPON: 'Arma',
    SECOND_WEAPON: 'Arma 2',
    ACCESSORY: 'Accesorio',
    LEFT_HAND: 'Anillo',
    RIGHT_HAND: 'Anillo',
    PET: 'Mascota',
    MOUNT: 'Montura',
  }
  return slotNames[slot] || slot
}

const formatDate = (isoString) => {
  try {
    const date = new Date(isoString)
    return date.toLocaleDateString('es-ES', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  } catch {
    return isoString
  }
}

const handleUnignore = (itemId) => {
  const success = unignoreItem(itemId)
  if (success) {
    toast.add({
      severity: 'success',
      summary: t('ignoredItems.restored'),
      detail: t('ignoredItems.restoredDetail'),
      life: 3000
    })
  }
}

const handleClearAll = () => {
  if (confirm(t('ignoredItems.confirmClearAll'))) {
    clearAllIgnoredItems()
    toast.add({
      severity: 'info',
      summary: t('ignoredItems.cleared'),
      detail: t('ignoredItems.clearedDetail'),
      life: 3000
    })
  }
}

const handleExport = () => {
  try {
    const data = exportIgnoredItems()
    const blob = new Blob([JSON.stringify(data, null, 2)], {
      type: 'application/json'
    })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `wakfu-ignored-items-${Date.now()}.json`
    a.click()
    URL.revokeObjectURL(url)
    
    toast.add({
      severity: 'success',
      summary: t('ignoredItems.exported'),
      detail: t('ignoredItems.exportedDetail'),
      life: 3000
    })
  } catch (error) {
    console.error('Export error:', error)
    toast.add({
      severity: 'error',
      summary: t('ignoredItems.exportError'),
      detail: error.message,
      life: 5000
    })
  }
}

const handleImport = () => {
  fileInput.value?.click()
}

const onFileSelected = async (event) => {
  const file = event.target.files?.[0]
  if (!file) return

  try {
    const text = await file.text()
    const data = JSON.parse(text)
    const success = importIgnoredItems(data)
    
    if (success) {
      toast.add({
        severity: 'success',
        summary: t('ignoredItems.imported'),
        detail: t('ignoredItems.importedDetail'),
        life: 3000
      })
    } else {
      throw new Error('Import failed')
    }
  } catch (error) {
    console.error('Import error:', error)
    toast.add({
      severity: 'error',
      summary: t('ignoredItems.importError'),
      detail: error.message,
      life: 5000
    })
  } finally {
    // Reset file input
    if (fileInput.value) {
      fileInput.value.value = ''
    }
  }
}
</script>

<style lang="scss" scoped>
.ignored-items-manager {
  background: rgba(26, 35, 50, 0.6);
  border-radius: 12px;
  padding: 1.5rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.manager-header {
  margin-bottom: 1.5rem;

  h3 {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin: 0 0 0.5rem 0;
    font-size: 1.2rem;
    color: #fff;

    i {
      color: #f44336;
    }
  }

  .help-text {
    margin: 0;
    color: #a0a0a0;
    font-size: 0.875rem;
  }
}

.count-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 24px;
  height: 24px;
  padding: 0 0.5rem;
  background: rgba(244, 67, 54, 0.2);
  color: #f44336;
  border-radius: 12px;
  font-size: 0.875rem;
  font-weight: 600;
  border: 1px solid rgba(244, 67, 54, 0.4);
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  padding: 3rem 2rem;
  text-align: center;
  color: #a0a0a0;

  i {
    font-size: 3rem;
    opacity: 0.5;
  }

  p {
    margin: 0;
    font-size: 1rem;
  }

  .help-text {
    font-size: 0.875rem;
    opacity: 0.7;
  }
}

.ignored-items-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.ignored-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  padding: 1rem;
  background: rgba(26, 35, 50, 0.8);
  border: 1px solid rgba(244, 67, 54, 0.3);
  border-radius: 8px;
  transition: all 0.3s;

  &:hover {
    background: rgba(26, 35, 50, 1);
    border-color: rgba(244, 67, 54, 0.5);
    box-shadow: 0 4px 12px rgba(244, 67, 54, 0.2);
  }
}

.item-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.item-name {
  font-size: 1rem;
  font-weight: 600;
}

.item-meta {
  display: flex;
  gap: 0.75rem;
  font-size: 0.875rem;
  color: #a0a0a0;

  span {
    display: flex;
    align-items: center;
    gap: 0.25rem;
  }
}

.item-date {
  font-size: 0.75rem;
  color: #808080;
  font-style: italic;
}

.btn-unignore {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: rgba(76, 175, 80, 0.2);
  color: #4caf50;
  border: 1px solid rgba(76, 175, 80, 0.4);
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  font-size: 0.875rem;
  transition: all 0.3s;

  &:hover {
    background: rgba(76, 175, 80, 0.3);
    border-color: #4caf50;
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(76, 175, 80, 0.3);
  }

  i {
    font-size: 0.875rem;
  }
}

.manager-actions {
  display: flex;
  gap: 0.75rem;
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.btn-clear-all,
.btn-export,
.btn-import {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.625rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  font-size: 0.875rem;
  transition: all 0.3s;
  border: 1px solid;

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  i {
    font-size: 0.875rem;
  }
}

.btn-clear-all {
  background: rgba(244, 67, 54, 0.2);
  color: #f44336;
  border-color: rgba(244, 67, 54, 0.4);

  &:hover:not(:disabled) {
    background: rgba(244, 67, 54, 0.3);
    border-color: #f44336;
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(244, 67, 54, 0.3);
  }
}

.btn-export {
  background: rgba(33, 150, 243, 0.2);
  color: #2196f3;
  border-color: rgba(33, 150, 243, 0.4);

  &:hover {
    background: rgba(33, 150, 243, 0.3);
    border-color: #2196f3;
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(33, 150, 243, 0.3);
  }
}

.btn-import {
  background: rgba(255, 152, 0, 0.2);
  color: #ff9800;
  border-color: rgba(255, 152, 0, 0.4);

  &:hover {
    background: rgba(255, 152, 0, 0.3);
    border-color: #ff9800;
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(255, 152, 0, 0.3);
  }
}
</style>



