<template>
  <p-dialog 
    v-model:visible="dialogVisible" 
    modal
    :header="t('builds.savedBuilds')" 
    :style="{ width: '700px' }"
    :closable="true"
    :dismissableMask="true"
    :blockScroll="true"
    :draggable="false"
    position="center"
    appendTo="body"
  >
    <div class="build-history-modal">
      <div class="builds-list">
        <div v-if="savedBuilds.length === 0" class="empty-state">
          <p>{{ t('builds.noSavedBuilds') }}</p>
        </div>
        <div 
          v-for="build in savedBuilds" 
          :key="build.id"
          class="build-item saved"
        >
          <div class="build-info">
            <div class="build-name">{{ build.name }}</div>
            <div class="build-date">{{ formatDate(build.timestamp) }}</div>
            <div class="build-level">Niv. {{ build.config.level_max }}</div>
          </div>
          <div class="build-actions">
            <button @click="loadAndClose(build)" class="btn-load" :title="t('builds.load')">
              📂
            </button>
            <button @click="deleteBuild(build.id)" class="btn-delete" :title="t('builds.delete')">
              🗑️
            </button>
          </div>
        </div>
      </div>
    </div>
  </p-dialog>
</template>

<script>
import { ref, computed } from 'vue';
import { useI18n } from '../composables/useI18n';
import { useBuildPersistence } from '../composables/useBuildPersistence';

export default {
  name: 'BuildHistory',
  props: {
    visible: {
      type: Boolean,
      required: true
    }
  },
  emits: ['update:visible', 'load-build'],
  setup(props, { emit }) {
    const { t } = useI18n();
    const { savedBuilds, deleteSavedBuild } = useBuildPersistence();
    
    const dialogVisible = computed({
      get: () => props.visible,
      set: (value) => emit('update:visible', value)
    });

    const formatDate = (timestamp) => {
      const date = new Date(timestamp);
      return date.toLocaleString('es-ES', {
        day: '2-digit',
        month: '2-digit',
        year: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      });
    };

    const deleteBuild = (buildId) => {
      if (confirm(t('builds.deleteConfirm'))) {
        deleteSavedBuild(buildId);
      }
    };

    const loadAndClose = (build) => {
      emit('load-build', build);
      emit('update:visible', false);
    };

    return {
      t,
      dialogVisible,
      savedBuilds,
      formatDate,
      deleteBuild,
      loadAndClose
    };
  }
};
</script>

<style scoped>
:deep(.p-dialog) {
  z-index: 10000 !important;
}

:deep(.p-dialog-mask) {
  z-index: 9999 !important;
  background-color: rgba(0, 0, 0, 0.6) !important;
}

.build-history-modal {
  min-height: 400px;
}


.builds-list {
  max-height: 400px;
  overflow-y: auto;
}

.builds-list::-webkit-scrollbar {
  width: 6px;
}

.builds-list::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 3px;
}

.builds-list::-webkit-scrollbar-thumb {
  background: rgba(102, 126, 234, 0.5);
  border-radius: 3px;
}

.build-item {
  background: white;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  padding: 1rem;
  margin-bottom: 0.75rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: all 0.3s;
}

.build-item:hover {
  background: #f9f9f9;
  border-color: #667eea;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.15);
}

.build-item.saved {
  border-left: 4px solid #667eea;
}

.build-info {
  flex: 1;
  min-width: 0;
}

.build-name {
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 0.35rem;
  font-size: 1.05rem;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.build-date {
  font-size: 0.85rem;
  color: #666;
  margin-bottom: 0.35rem;
}

.build-level {
  display: inline-block;
  padding: 0.25rem 0.6rem;
  background: #667eea;
  border-radius: 5px;
  font-size: 0.85rem;
  color: white;
  margin-right: 0.5rem;
  font-weight: 600;
}

.build-stats {
  font-size: 0.85rem;
  color: #888;
  display: inline;
}

.build-actions {
  display: flex;
  gap: 0.5rem;
}

.btn-load,
.btn-delete {
  background: #f5f5f5;
  border: 2px solid #e0e0e0;
  width: 36px;
  height: 36px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1.1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
}

.btn-load:hover {
  background: #4caf50;
  border-color: #4caf50;
  transform: scale(1.05);
}

.btn-delete:hover {
  background: #f44336;
  border-color: #f44336;
  transform: scale(1.05);
}

.empty-state {
  text-align: center;
  padding: 3rem;
  color: #999;
}

.empty-state p {
  margin: 0;
  font-style: italic;
  font-size: 1.05rem;
}
</style>

