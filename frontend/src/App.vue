<template>
  <div id="app">
    <p-toast />
    <div class="header">
      <div class="header-content">
        <div>
          <h1>{{ t('app.title') }}</h1>
          <p>{{ t('app.subtitle') }}</p>
        </div>
        
        <div class="language-selector">
          <label for="language">{{ t('language') }}:</label>
          <p-dropdown 
            id="language"
            v-model="currentLanguage" 
            :options="languageOptions"
            option-label="label"
            option-value="value"
            @change="onLanguageChange"
            class="language-dropdown"
          />
        </div>
      </div>
      
      <!-- Navigation Tabs -->
      <div class="nav-tabs">
        <button 
          @click="currentView = 'builder'" 
          :class="['tab', { active: currentView === 'builder' }]"
        >
          🏗️ {{ t('nav.builder') }}
        </button>
        <button 
          @click="currentView = 'metadata'" 
          :class="['tab', { active: currentView === 'metadata' }]"
        >
          ⚙️ {{ t('nav.metadata') }}
        </button>
      </div>
    </div>
    
    <div class="main-container">
      <BuildGenerator 
        v-if="currentView === 'builder'" 
        @edit-metadata="handleEditMetadata"
      />
      <ItemMetadataAdmin 
        v-else-if="currentView === 'metadata'" 
        ref="metadataAdmin"
        :preselected-item="preselectedItem"
      />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useLanguage } from './composables/useLanguage'
import { useI18n } from './composables/useI18n'
import BuildGenerator from './components/BuildGenerator.vue'
import ItemMetadataAdmin from './components/ItemMetadataAdmin.vue'

const { currentLanguage, setLanguage, languageOptions } = useLanguage()
const { t } = useI18n()

const currentView = ref('builder')
const preselectedItem = ref(null)
const metadataAdmin = ref(null)

const onLanguageChange = (event) => {
  setLanguage(event.value)
}

const handleEditMetadata = (item) => {
  console.log('Switching to metadata view for item:', item)
  preselectedItem.value = item
  currentView.value = 'metadata'
}
</script>

<style lang="scss">
#app {
  min-height: 100vh;
  background: linear-gradient(180deg, #0a1929 0%, #1a2332 100%);
  color: #e0e0e0;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.header {
  background: rgba(26, 35, 50, 0.8);
  backdrop-filter: blur(10px);
  padding: 2rem;
  border-bottom: 2px solid rgba(255, 255, 255, 0.1);
  
  .header-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
    max-width: 1800px;
    margin: 0 auto;
    
    @media (max-width: 768px) {
      flex-direction: column;
      gap: 1rem;
    }
  }
  
  h1 {
    margin: 0;
    font-size: 2.5rem;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }
  
  p {
    margin: 0.5rem 0 0 0;
    color: #a0a0a0;
  }
  
  .language-selector {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    
    label {
      color: #e0e0e0;
      font-weight: 500;
      white-space: nowrap;
    }
    
    .language-dropdown {
      min-width: 140px;
    }
  }
}

.main-container {
  max-width: 1800px;
  margin: 0 auto;
  padding: 2rem;
}

.nav-tabs {
  display: flex;
  gap: 0.5rem;
  max-width: 1800px;
  margin: 0 auto;
  padding: 1rem 2rem 0 2rem;
  
  .tab {
    padding: 0.75rem 1.5rem;
    background: rgba(255, 255, 255, 0.05);
    border: 2px solid transparent;
    border-radius: 8px 8px 0 0;
    color: #a0a0a0;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s;
    
    &:hover {
      background: rgba(255, 255, 255, 0.1);
      color: #e0e0e0;
    }
    
    &.active {
      background: rgba(102, 126, 234, 0.2);
      border-color: #667eea;
      color: #667eea;
    }
  }
}
</style>

