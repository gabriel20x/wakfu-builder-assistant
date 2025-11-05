<template>
  <div class="build-history">
    <div class="history-header">
      <h3>{{ showSaved ? t('builds.savedBuilds') : t('builds.history') }}</h3>
      <div class="header-actions">
        <button 
          @click="showSaved = false" 
          :class="['tab-btn', { active: !showSaved }]"
        >
          🕐 {{ t('builds.history') }}
        </button>
        <button 
          @click="showSaved = true" 
          :class="['tab-btn', { active: showSaved }]"
        >
          ⭐ {{ t('builds.saved') }}
        </button>
      </div>
    </div>

    <div class="builds-list">
      <!-- Saved Builds -->
      <div v-if="showSaved">
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
            <button @click="$emit('load-build', build)" class="btn-load" :title="t('builds.load')">
              📂
            </button>
            <button @click="deleteBuild(build.id)" class="btn-delete" :title="t('builds.delete')">
              🗑️
            </button>
          </div>
        </div>
      </div>

      <!-- History -->
      <div v-else>
        <div v-if="buildHistory.length === 0" class="empty-state">
          <p>{{ t('builds.noHistory') }}</p>
        </div>
        <div 
          v-for="build in buildHistory" 
          :key="build.id"
          class="build-item"
        >
          <div class="build-info">
            <div class="build-date">{{ formatDate(build.timestamp) }}</div>
            <div class="build-level">Niv. {{ build.config.level_max }}</div>
            <div class="build-stats">
              {{ getTopStats(build.config.stat_weights).join(', ') }}
            </div>
          </div>
          <div class="build-actions">
            <button @click="$emit('load-build', build)" class="btn-load" :title="t('builds.load')">
              📂
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue';
import { useI18n } from '../composables/useI18n';
import { useBuildPersistence } from '../composables/useBuildPersistence';

export default {
  name: 'BuildHistory',
  emits: ['load-build'],
  setup() {
    const { t } = useI18n();
    const { savedBuilds, buildHistory, deleteSavedBuild } = useBuildPersistence();
    
    const showSaved = ref(false);

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

    const getTopStats = (statWeights) => {
      if (!statWeights) return [];
      return Object.entries(statWeights)
        .sort(([,a], [,b]) => b - a)
        .slice(0, 3)
        .map(([stat]) => stat);
    };

    const deleteBuild = (buildId) => {
      if (confirm(t('builds.deleteConfirm'))) {
        deleteSavedBuild(buildId);
      }
    };

    return {
      t,
      showSaved,
      savedBuilds,
      buildHistory,
      formatDate,
      getTopStats,
      deleteBuild
    };
  }
};
</script>

<style scoped>
.build-history {
  background: rgba(26, 35, 50, 0.6);
  border-radius: 12px;
  padding: 1rem;
}

.history-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 0.75rem;
  border-bottom: 2px solid rgba(255, 255, 255, 0.1);
}

.history-header h3 {
  margin: 0;
  color: #e0e0e0;
  font-size: 1.1rem;
}

.header-actions {
  display: flex;
  gap: 0.5rem;
}

.tab-btn {
  padding: 0.4rem 0.8rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 6px;
  color: #a0a0a0;
  cursor: pointer;
  font-size: 0.85rem;
  transition: all 0.3s;
}

.tab-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  color: #e0e0e0;
}

.tab-btn.active {
  background: rgba(102, 126, 234, 0.3);
  border-color: #667eea;
  color: #667eea;
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
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  padding: 0.75rem;
  margin-bottom: 0.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: all 0.3s;
}

.build-item:hover {
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(102, 126, 234, 0.5);
}

.build-item.saved {
  border-left: 3px solid #667eea;
}

.build-info {
  flex: 1;
  min-width: 0;
}

.build-name {
  font-weight: 600;
  color: #e0e0e0;
  margin-bottom: 0.25rem;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.build-date {
  font-size: 0.85rem;
  color: #a0a0a0;
  margin-bottom: 0.25rem;
}

.build-level {
  display: inline-block;
  padding: 0.15rem 0.4rem;
  background: rgba(102, 126, 234, 0.3);
  border-radius: 4px;
  font-size: 0.8rem;
  color: #667eea;
  margin-right: 0.5rem;
}

.build-stats {
  font-size: 0.8rem;
  color: #888;
  display: inline;
}

.build-actions {
  display: flex;
  gap: 0.5rem;
}

.btn-load,
.btn-delete {
  background: rgba(255, 255, 255, 0.1);
  border: none;
  width: 32px;
  height: 32px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
}

.btn-load:hover {
  background: rgba(76, 175, 80, 0.3);
}

.btn-delete:hover {
  background: rgba(244, 67, 54, 0.3);
}

.empty-state {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.empty-state p {
  margin: 0;
  font-style: italic;
}
</style>

