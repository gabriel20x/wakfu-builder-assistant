<template>
  <div id="app">
    <p-toast />
    <div class="header">
      <div class="header-content">
        <div>
          <h1>Wakfu Builder Assistant</h1>
          <p>Generate optimized equipment builds for your character</p>
        </div>
        
        <div class="language-selector">
          <label for="language">{{ currentLanguage === 'es' ? 'Idioma' : currentLanguage === 'fr' ? 'Langue' : 'Language' }}:</label>
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
    </div>
    
    <div class="main-container">
      <BuildGenerator />
    </div>
  </div>
</template>

<script setup>
import { useLanguage } from './composables/useLanguage'
import BuildGenerator from './components/BuildGenerator.vue'

const { currentLanguage, setLanguage, languageOptions } = useLanguage()

const onLanguageChange = (event) => {
  setLanguage(event.value)
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
</style>

