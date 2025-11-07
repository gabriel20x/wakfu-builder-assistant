<template>
  <div class="build-viewer">
    <div class="viewer-grid">
      <!-- Left Sidebar - Build History -->
      <div class="builds-sidebar">
        <div class="sidebar-header">
          <h2>{{ t('myBuilds.title') }}</h2>
          <p-button
            icon="pi pi-plus"
            :label="t('myBuilds.createNew')"
            severity="success"
            size="small"
            @click="goToBuilder"
          />
        </div>
        
        <div class="builds-list">
          <div v-if="isLoading" class="loading-state">
            <p-progressSpinner style="width: 40px; height: 40px" />
            <p>{{ t('myBuilds.loading') }}</p>
          </div>
          
          <div v-else-if="buildHistory.length === 0" class="empty-state">
            <i class="pi pi-inbox"></i>
            <h3>{{ t('myBuilds.noBuildsSaved') }}</h3>
            <p>{{ t('myBuilds.startByCreating') }}</p>
            <p-button
              icon="pi pi-sparkles"
              :label="t('myBuilds.goToBuilder')"
              @click="goToBuilder"
            />
          </div>
          
          <div 
            v-else
            v-for="build in buildHistory" 
            :key="build.id"
            class="build-card"
            :class="{ active: selectedBuildId === build.id }"
            @click="selectBuild(build)"
          >
            <div class="build-card-header">
              <h3>{{ build.name || t('myBuilds.unnamedBuild') }}</h3>
              <span class="build-date">{{ formatDate(build.saved_at) }}</span>
            </div>
            
            <div class="build-info">
              <div v-if="build.config?.selectedClass && build.config?.selectedRole" class="build-preset">
                <i class="pi pi-star-fill"></i>
                <span><strong>{{ build.config.selectedClass }}</strong> - {{ build.config.selectedRole }}</span>
              </div>
              
              <div class="build-meta">
                <span class="meta-item">
                  <i class="pi pi-chart-line"></i>
                  Nivel {{ build.config?.level_max || 230 }}
                </span>
                <span class="meta-item">
                  <i class="pi pi-bolt"></i>
                  {{ countStats(build.config?.stat_weights) }} stats
                </span>
              </div>
            </div>
            
            <div class="build-actions">
              <p-button
                icon="pi pi-trash"
                severity="danger"
                text
                rounded
                size="small"
                @click.stop="confirmDelete(build)"
              />
            </div>
          </div>
        </div>
      </div>
      
      <!-- Center - Build Display -->
      <div class="build-display">
        <div v-if="!selectedBuild" class="empty-display">
          <i class="pi pi-arrow-left"></i>
          <h2>{{ t('myBuilds.selectBuild') }}</h2>
          <p>{{ t('myBuilds.selectBuildDescription') }}</p>
        </div>
        
        <div v-else class="build-content">
          <!-- Build Header -->
          <div class="build-header-display">
            <div>
              <h1>{{ selectedBuild.name || t('myBuilds.unnamedBuild') }}</h1>
              <div class="build-metadata">
                <span v-if="selectedBuild.config?.selectedClass && selectedBuild.config?.selectedRole" class="preset-badge">
                  <i class="pi pi-star-fill"></i>
                  {{ selectedBuild.config.selectedClass }} - {{ selectedBuild.config.selectedRole }}
                </span>
                <span class="level-badge">
                  <i class="pi pi-chart-line"></i>
                  Nivel {{ selectedBuild.config?.level_max || 230 }}
                </span>
                <span class="date-badge">
                  <i class="pi pi-calendar"></i>
                  {{ formatDate(selectedBuild.saved_at) }}
                </span>
              </div>
            </div>
            
            <div class="header-actions">
              <p-button
                icon="pi pi-copy"
                :label="t('myBuilds.loadInBuilder')"
                severity="info"
                @click="loadInBuilder"
              />
              <p-button
                icon="pi pi-pencil"
                :label="t('myBuilds.rename')"
                outlined
                @click="showRenameDialog = true"
              />
            </div>
          </div>
          
          <!-- Builds Tabs -->
          <p-tabView class="builds-tabview" v-model:activeIndex="activeTabIndex">
            <p-tabPanel :header="t('builds.easy')">
              <BuildResult :build="selectedBuild.builds.easy" :difficulty="t('builds.easy')" :show-stats="false" />
            </p-tabPanel>
            
            <p-tabPanel :header="t('builds.medium')">
              <BuildResult :build="selectedBuild.builds.medium" :difficulty="t('builds.medium')" :show-stats="false" />
            </p-tabPanel>
            
            <p-tabPanel :header="t('builds.hardEpic')">
              <BuildResult :build="selectedBuild.builds.hard_epic" :difficulty="t('builds.hardEpic')" :show-stats="false" />
            </p-tabPanel>
            
            <p-tabPanel :header="t('builds.hardRelic')">
              <BuildResult :build="selectedBuild.builds.hard_relic" :difficulty="t('builds.hardRelic')" :show-stats="false" />
            </p-tabPanel>
            
            <p-tabPanel :header="t('builds.full')">
              <BuildResult :build="selectedBuild.builds.full" :difficulty="t('builds.full')" :show-stats="false" />
            </p-tabPanel>
          </p-tabView>
        </div>
      </div>
      
      <!-- Right Panel - Stats -->
      <div v-if="selectedBuild" class="stats-panel">
        <div class="panel-header">
          <h2>{{ t('statsPanel.title') }}</h2>
        </div>
        
        <div class="panel-content">
          <!-- Equipment Slots -->
          <div class="equipment-section">
            <EquipmentSlots 
              v-if="currentBuildItems" 
              :items="currentBuildItems"
              :selected-class="selectedBuild.config?.selectedClass"
            />
          </div>
          
          <BuildStatSheet 
            v-if="currentBuildStats" 
            :stats="currentBuildStats" 
            :character-level="selectedBuild.config?.level_max || 230"
          />
        </div>
      </div>
    </div>
    
    <!-- Rename Dialog -->
    <p-dialog 
      v-model:visible="showRenameDialog" 
      :header="t('myBuilds.renameBuild')"
      :modal="true"
      :style="{ width: '450px' }"
    >
      <div class="rename-form">
        <label for="buildName">{{ t('myBuilds.buildName') }}</label>
        <p-inputText 
          id="buildName"
          v-model="newBuildName" 
          :placeholder="t('myBuilds.enterBuildName')"
          style="width: 100%"
        />
      </div>
      
      <template #footer>
        <p-button :label="t('common.cancel')" severity="secondary" @click="showRenameDialog = false" />
        <p-button :label="t('common.save')" @click="renameBuild" />
      </template>
    </p-dialog>
    
    <!-- Delete Confirmation Dialog -->
    <p-dialog 
      v-model:visible="showDeleteDialog" 
      :header="t('myBuilds.deleteBuild')"
      :modal="true"
      :style="{ width: '450px' }"
    >
      <p>{{ t('myBuilds.deleteConfirmation') }}</p>
      <p><strong>{{ buildToDelete?.name || t('myBuilds.unnamedBuild') }}</strong></p>
      
      <template #footer>
        <p-button :label="t('common.cancel')" severity="secondary" @click="showDeleteDialog = false" />
        <p-button :label="t('common.delete')" severity="danger" @click="deleteBuild" />
      </template>
    </p-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useToast } from 'primevue/usetoast'
import { useI18n } from '../composables/useI18n'
import { useBuildPersistence } from '../composables/useBuildPersistence'
import BuildResult from './BuildResult.vue'
import BuildStatSheet from './BuildStatSheet.vue'
import EquipmentSlots from './EquipmentSlots.vue'

const emit = defineEmits(['go-to-builder', 'load-build'])
const toast = useToast()
const { t } = useI18n()
const { getBuildHistory, deleteBuildFromHistory, renameBuildInHistory } = useBuildPersistence()

const buildHistory = ref([])
const selectedBuildId = ref(null)
const selectedBuild = ref(null)
const isLoading = ref(true)
const activeTabIndex = ref(0)
const showRenameDialog = ref(false)
const showDeleteDialog = ref(false)
const newBuildName = ref('')
const buildToDelete = ref(null)

const currentBuildStats = computed(() => {
  if (!selectedBuild.value) return null
  
  const buildTypes = ['easy', 'medium', 'hard_epic', 'hard_relic', 'full']
  const activeBuildType = buildTypes[activeTabIndex.value]
  
  return selectedBuild.value.builds[activeBuildType]?.total_stats || null
})

const currentBuildItems = computed(() => {
  if (!selectedBuild.value) return []
  
  const buildTypes = ['easy', 'medium', 'hard_epic', 'hard_relic', 'full']
  const activeBuildType = buildTypes[activeTabIndex.value]
  
  return selectedBuild.value.builds[activeBuildType]?.items || []
})

const loadBuildHistory = () => {
  isLoading.value = true
  try {
    const history = getBuildHistory()
    buildHistory.value = history
    
    // Auto-select last build
    if (history.length > 0) {
      selectBuild(history[0])
    }
  } catch (error) {
    console.error('Error loading build history:', error)
    toast.add({
      severity: 'error',
      summary: t('toast.error'),
      detail: t('myBuilds.errorLoading'),
      life: 3000
    })
  } finally {
    isLoading.value = false
  }
}

const selectBuild = (build) => {
  selectedBuildId.value = build.id
  selectedBuild.value = build
  activeTabIndex.value = 0
}

const goToBuilder = () => {
  emit('go-to-builder')
}

const loadInBuilder = () => {
  emit('load-build', selectedBuild.value)
}

const formatDate = (timestamp) => {
  const date = new Date(timestamp)
  const now = new Date()
  const diffMs = now - date
  const diffMins = Math.floor(diffMs / 60000)
  const diffHours = Math.floor(diffMs / 3600000)
  const diffDays = Math.floor(diffMs / 86400000)
  
  if (diffMins < 1) return t('myBuilds.justNow')
  if (diffMins < 60) return t('myBuilds.minutesAgo', { count: diffMins })
  if (diffHours < 24) return t('myBuilds.hoursAgo', { count: diffHours })
  if (diffDays < 7) return t('myBuilds.daysAgo', { count: diffDays })
  
  return date.toLocaleDateString()
}

const countStats = (statWeights) => {
  if (!statWeights) return 0
  return Object.keys(statWeights).length
}

const confirmDelete = (build) => {
  buildToDelete.value = build
  showDeleteDialog.value = true
}

const deleteBuild = () => {
  if (!buildToDelete.value) return
  
  try {
    deleteBuildFromHistory(buildToDelete.value.id)
    
    // Reload history
    loadBuildHistory()
    
    // Clear selection if deleted build was selected
    if (selectedBuildId.value === buildToDelete.value.id) {
      selectedBuildId.value = null
      selectedBuild.value = null
    }
    
    toast.add({
      severity: 'success',
      summary: t('toast.success'),
      detail: t('myBuilds.buildDeleted'),
      life: 3000
    })
  } catch (error) {
    console.error('Error deleting build:', error)
    toast.add({
      severity: 'error',
      summary: t('toast.error'),
      detail: t('myBuilds.errorDeleting'),
      life: 3000
    })
  } finally {
    showDeleteDialog.value = false
    buildToDelete.value = null
  }
}

const renameBuild = () => {
  if (!selectedBuild.value || !newBuildName.value.trim()) return
  
  try {
    renameBuildInHistory(selectedBuild.value.id, newBuildName.value.trim())
    
    // Reload history
    loadBuildHistory()
    
    // Update selected build
    if (selectedBuildId.value) {
      const updated = buildHistory.value.find(b => b.id === selectedBuildId.value)
      if (updated) {
        selectedBuild.value = updated
      }
    }
    
    toast.add({
      severity: 'success',
      summary: t('toast.success'),
      detail: t('myBuilds.buildRenamed'),
      life: 3000
    })
    
    showRenameDialog.value = false
    newBuildName.value = ''
  } catch (error) {
    console.error('Error renaming build:', error)
    toast.add({
      severity: 'error',
      summary: t('toast.error'),
      detail: t('myBuilds.errorRenaming'),
      life: 3000
    })
  }
}

onMounted(() => {
  loadBuildHistory()
})
</script>

<style lang="scss" scoped>
.build-viewer {
  width: 100%;
}

.viewer-grid {
  display: grid;
  grid-template-columns: 320px 1fr 380px;
  gap: 1.5rem;
  min-height: calc(100vh - 250px);
  
  @media (max-width: 1600px) {
    grid-template-columns: 280px 1fr 350px;
    gap: 1rem;
  }
  
  @media (max-width: 1200px) {
    grid-template-columns: 1fr;
    
    .stats-panel {
      order: 2;
    }
    
    .build-display {
      order: 3;
    }
  }
}

.builds-sidebar,
.build-display,
.stats-panel {
  background: rgba(26, 35, 50, 0.6);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  max-height: calc(100vh - 250px);
}

.builds-sidebar {
  .sidebar-header {
    padding: 1.5rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    
    h2 {
      margin: 0 0 1rem 0;
      color: #fff;
      font-size: 1.3rem;
    }
  }
  
  .builds-list {
    flex: 1;
    overflow-y: auto;
    padding: 0.5rem;
    
    &::-webkit-scrollbar {
      width: 8px;
    }
    
    &::-webkit-scrollbar-track {
      background: rgba(0, 0, 0, 0.2);
    }
    
    &::-webkit-scrollbar-thumb {
      background: rgba(102, 126, 234, 0.5);
      border-radius: 4px;
      
      &:hover {
        background: rgba(102, 126, 234, 0.7);
      }
    }
  }
}

.build-card {
  background: rgba(0, 0, 0, 0.3);
  border: 2px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  padding: 1rem;
  margin-bottom: 0.5rem;
  cursor: pointer;
  transition: background 0.2s, border-color 0.2s, box-shadow 0.2s;
  position: relative;
  
  &:hover {
    background: rgba(0, 0, 0, 0.4);
    border-color: rgba(102, 126, 234, 0.5);
    box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
  }
  
  &.active {
    background: rgba(102, 126, 234, 0.2);
    border-color: #667eea;
    box-shadow: 0 2px 12px rgba(102, 126, 234, 0.4);
  }
  
  .build-card-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 0.5rem;
    
    h3 {
      margin: 0;
      font-size: 1rem;
      color: #fff;
      font-weight: 600;
    }
    
    .build-date {
      font-size: 0.75rem;
      color: #a0a0a0;
      white-space: nowrap;
    }
  }
  
  .build-info {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    
    .build-preset {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      padding: 0.5rem;
      background: rgba(76, 175, 80, 0.15);
      border-radius: 4px;
      font-size: 0.85rem;
      
      i {
        color: #4CAF50;
      }
      
      strong {
        color: #fff;
      }
    }
    
    .build-meta {
      display: flex;
      gap: 0.75rem;
      font-size: 0.8rem;
      color: #a0a0a0;
      
      .meta-item {
        display: flex;
        align-items: center;
        gap: 0.35rem;
        
        i {
          font-size: 0.75rem;
        }
      }
    }
  }
  
  .build-actions {
    position: absolute;
    bottom: 0.5rem;
    right: 0.5rem;
    opacity: 0;
    transition: opacity 0.2s;
  }
  
  &:hover .build-actions {
    opacity: 1;
  }
}

.loading-state,
.empty-state,
.empty-display {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem 2rem;
  text-align: center;
  color: #a0a0a0;
  
  i {
    font-size: 4rem;
    margin-bottom: 1rem;
    opacity: 0.5;
  }
  
  h2, h3 {
    margin: 0.5rem 0;
    color: #fff;
  }
  
  p {
    margin: 0.5rem 0 1.5rem 0;
    max-width: 400px;
  }
}

.build-display {
  .build-content {
    height: 100%;
    display: flex;
    flex-direction: column;
  }
}

.build-header-display {
  padding: 1.5rem;
  border-bottom: 2px solid rgba(255, 255, 255, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1rem;
  
  h1 {
    margin: 0 0 0.75rem 0;
    font-size: 1.8rem;
    color: #fff;
  }
  
  .build-metadata {
    display: flex;
    gap: 0.75rem;
    flex-wrap: wrap;
    
    span {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      padding: 0.5rem 0.75rem;
      border-radius: 6px;
      font-size: 0.9rem;
      
      &.preset-badge {
        background: rgba(76, 175, 80, 0.15);
        border: 1px solid rgba(76, 175, 80, 0.3);
        color: #4CAF50;
      }
      
      &.level-badge {
        background: rgba(102, 126, 234, 0.15);
        border: 1px solid rgba(102, 126, 234, 0.3);
        color: #667eea;
      }
      
      &.date-badge {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: #a0a0a0;
      }
    }
  }
  
  .header-actions {
    display: flex;
    gap: 0.5rem;
  }
}

.stats-panel {
  .panel-header {
    padding: 1.5rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    
    h2 {
      margin: 0;
      color: #fff;
      font-size: 1.3rem;
    }
  }
  
  .panel-content {
    flex: 1;
    overflow-y: auto;
    padding: 1.5rem;
    
    &::-webkit-scrollbar {
      width: 8px;
    }
    
    &::-webkit-scrollbar-track {
      background: rgba(0, 0, 0, 0.2);
    }
    
    &::-webkit-scrollbar-thumb {
      background: rgba(102, 126, 234, 0.5);
      border-radius: 4px;
      
      &:hover {
        background: rgba(102, 126, 234, 0.7);
      }
    }
  }
}

.equipment-section {
  margin-bottom: 1.5rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

:deep(.p-tabview) {
  height: 100%;
  display: flex;
  flex-direction: column;
  
  .p-tabview-nav {
    background: transparent;
    border: none;
    border-bottom: 2px solid rgba(255, 255, 255, 0.1);
    flex-shrink: 0;
    
    li {
      .p-tabview-nav-link {
        background: transparent;
        border: none;
        color: #a0a0a0;
        padding: 1rem 1.5rem;
        
        &:hover {
          background: rgba(255, 255, 255, 0.05);
          color: #fff;
        }
      }
      
      &.p-highlight .p-tabview-nav-link {
        background: rgba(92, 107, 192, 0.2);
        color: #fff;
        border-bottom: 2px solid #5c6bc0;
      }
    }
  }
  
  .p-tabview-panels {
    background: transparent;
    padding: 0;
    flex: 1;
    overflow: hidden;
    
    .p-tabview-panel {
      padding: 0;
      height: 100%;
    }
  }
}

.rename-form {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin: 1rem 0;
  
  label {
    font-weight: 600;
    color: #e0e0e0;
  }
}
</style>

