<template>
  <div class="metadata-admin">
    <div class="admin-header">
      <h1>{{ t('metadata.title') }}</h1>
      <p class="description">{{ t('metadata.description') }}</p>
    </div>

    <!-- Statistics Panel -->
    <div class="stats-panel" v-if="stats">
      <div class="stat-card progress-card">
        <div class="stat-value">{{ stats.total_items_with_metadata }} / {{ stats.total_items_in_game }}</div>
        <div class="stat-label">{{ t('metadata.coverage') }}</div>
        <div class="progress-bar">
          <div class="progress-fill" :style="{ width: stats.coverage_percent + '%' }"></div>
        </div>
        <div class="progress-percent">{{ stats.coverage_percent }}%</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">{{ stats.items_with_drop || 0 }}</div>
        <div class="stat-label">💀 {{ t('metadata.methodDrop') }}</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">{{ stats.items_with_recipe || 0 }}</div>
        <div class="stat-label">🔨 {{ t('metadata.methodRecipe') }}</div>
      </div>
      <div class="stat-card relic-highlight">
        <div class="stat-value">{{ stats.items_with_fragments || 0 }}</div>
        <div class="stat-label">🔮 {{ t('metadata.methodFragments') }}</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">{{ stats.items_with_crupier || 0 }}</div>
        <div class="stat-label">💰 {{ t('metadata.methodCrupier') }}</div>
      </div>
    </div>

    <!-- Search Section -->
    <div class="search-section">
      <div class="search-box">
        <input 
          v-model="searchQuery" 
          @keyup.enter="searchItems"
          type="text" 
          :placeholder="t('metadata.searchPlaceholder')"
          class="search-input"
        />
        <button @click="searchItems" class="btn-search" :disabled="loading">
          <span v-if="!loading">🔍 {{ t('metadata.search') }}</span>
          <span v-else>⏳ {{ t('metadata.searching') }}</span>
        </button>
      </div>
    </div>

    <!-- Search Results -->
    <div class="results-section" v-if="searchResults.length > 0">
      <h2>{{ t('metadata.results') }} ({{ searchResults.length }})</h2>
      <div class="items-grid">
        <div 
          v-for="item in searchResults" 
          :key="item.item_id"
          class="item-card"
          :class="{ 
            'has-metadata': item.has_metadata,
            'selected': selectedItem && selectedItem.item_id === item.item_id
          }"
          @click="selectItem(item)"
        >
          <div class="item-header">
            <span class="item-name">{{ getItemName(item) }}</span>
            <span class="item-level">Niv. {{ item.level }}</span>
          </div>
          <div class="item-info">
            <span class="item-slot">{{ item.slot }}</span>
            <span class="item-rarity" :class="`rarity-${item.rarity}`">
              {{ getRarityName(item.rarity) }}
            </span>
          </div>
          <div class="item-source">
            <span>{{ t('metadata.source') }}: {{ item.source_type || 'unknown' }}</span>
          </div>
          <div class="metadata-badge" v-if="item.has_metadata">
            ✅ {{ t('metadata.hasMetadata') }}
          </div>
        </div>
      </div>
    </div>

    <!-- Edit Form -->
    <div class="edit-section" v-if="selectedItem">
      <div class="edit-header">
        <div class="header-info">
          <h2>{{ getItemName(selectedItem) }}</h2>
          <div class="item-badges">
            <span class="badge-level">Niv. {{ selectedItem.level }}</span>
            <span class="badge-rarity" :class="`rarity-${selectedItem.rarity}`">
              {{ getRarityName(selectedItem.rarity) }}
            </span>
            <span class="badge-slot">{{ selectedItem.slot }}</span>
          </div>
        </div>
        <button @click="closeEditor" class="btn-close">✕</button>
      </div>

      <div class="edit-form">


        <!-- Acquisition Methods Section -->
        <div class="section-divider">
          <h3>{{ t('metadata.acquisitionMethodsTitle') }}</h3>
          <p class="section-subtitle">{{ t('metadata.acquisitionMethodsSubtitle') }}</p>
        </div>

        <!-- Drop Method -->
        <div class="acquisition-method-card compact">
          <label class="checkbox-label method-header">
            <input 
              type="checkbox" 
              v-model="editForm.acquisition_methods.drop.enabled"
            />
            <strong>💀 {{ t('metadata.methodDrop') }}</strong>
          </label>
          
          <div v-if="editForm.acquisition_methods.drop.enabled" class="method-details">
            <div class="rate-list">
              <div 
                v-for="(rate, index) in editForm.acquisition_methods.drop.drop_rates" 
                :key="index"
                class="rate-item"
              >
                <input 
                  v-model.number="editForm.acquisition_methods.drop.drop_rates[index]" 
                  type="number" 
                  step="0.01"
                  min="0"
                  max="100"
                  :placeholder="t('metadata.dropRatePlaceholder')"
                  class="input-rate"
                />
                <span>%</span>
                <button @click="removeDropRate(index)" class="btn-remove-inline">✕</button>
              </div>
              <button @click="addDropRate" class="btn-add-inline">+ {{ t('metadata.addRate') }}</button>
            </div>
          </div>
        </div>

        <!-- Recipe/Craft Method -->
        <div class="acquisition-method-card compact">
          <label class="checkbox-label method-header">
            <input 
              type="checkbox" 
              v-model="editForm.acquisition_methods.recipe.enabled"
            />
            <strong>🔨 {{ t('metadata.methodRecipe') }}</strong>
          </label>
        </div>

        <!-- Fragments Method -->
        <div class="acquisition-method-card compact" v-if="selectedItem.rarity >= 5">
          <label class="checkbox-label method-header">
            <input 
              type="checkbox" 
              v-model="editForm.acquisition_methods.fragments.enabled"
            />
            <strong>🔮 {{ t('metadata.methodFragments') }}</strong>
          </label>
          
          <div v-if="editForm.acquisition_methods.fragments.enabled" class="method-details">
            <div class="rate-list">
              <div 
                v-for="(rate, index) in editForm.acquisition_methods.fragments.fragment_rates" 
                :key="index"
                class="rate-item"
              >
                <input 
                  v-model.number="editForm.acquisition_methods.fragments.fragment_rates[index]" 
                  type="number" 
                  step="0.01"
                  min="0"
                  max="100"
                  :placeholder="t('metadata.fragmentRatePlaceholder')"
                  class="input-rate"
                />
                <span>%</span>
                <button @click="removeFragmentRate(index)" class="btn-remove-inline">✕</button>
              </div>
              <button @click="addFragmentRate" class="btn-add-inline">+ {{ t('metadata.addRate') }}</button>
            </div>
          </div>
        </div>

        <!-- Crupier Method -->
        <div class="acquisition-method-card compact">
          <label class="checkbox-label method-header">
            <input 
              type="checkbox" 
              v-model="editForm.acquisition_methods.crupier.enabled"
            />
            <strong>💰 {{ t('metadata.methodCrupier') }}</strong>
          </label>
        </div>

        <!-- Challenge/Reward Method -->
        <div class="acquisition-method-card compact">
          <label class="checkbox-label method-header">
            <input 
              type="checkbox" 
              v-model="editForm.acquisition_methods.challenge_reward.enabled"
            />
            <strong>🏆 {{ t('metadata.methodChallengeReward') }}</strong>
          </label>
        </div>

        <!-- Quest Method -->
        <div class="acquisition-method-card compact">
          <label class="checkbox-label method-header">
            <input 
              type="checkbox" 
              v-model="editForm.acquisition_methods.quest.enabled"
            />
            <strong>📜 {{ t('metadata.methodQuest') }}</strong>
          </label>
        </div>

        <!-- Other Method -->
        <div class="acquisition-method-card compact">
          <label class="checkbox-label method-header">
            <input 
              type="checkbox" 
              v-model="editForm.acquisition_methods.other.enabled"
            />
            <strong>➕ {{ t('metadata.methodOther') }}</strong>
          </label>
        </div>

        <div class="form-actions">
          <button @click="saveMetadata" class="btn-save" :disabled="saving">
            {{ saving ? t('metadata.saving') : t('metadata.save') }}
          </button>
          <button @click="deleteMetadata" class="btn-delete" :disabled="!selectedItem.has_metadata || saving">
            {{ t('metadata.delete') }}
          </button>
          <button @click="closeEditor" class="btn-cancel">
            {{ t('metadata.cancel') }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useLanguage } from '../composables/useLanguage';
import { useI18n } from '../composables/useI18n';
import api from '../services/api';

export default {
  name: 'ItemMetadataAdmin',
  props: {
    preselectedItem: {
      type: Object,
      default: null
    }
  },
  setup(props) {
    const { t } = useI18n();
    const { currentLanguage } = useLanguage();
    
    const searchQuery = ref('');
    const searchResults = ref([]);
    const selectedItem = ref(null);
    const stats = ref(null);
    const loading = ref(false);
    const saving = ref(false);
    
    const editForm = ref({
      acquisition_methods: {
        drop: {
          enabled: false,
          drop_rate_percent: null,
          drop_sources: []
        },
        recipe: {
          enabled: false,
          is_craftable: null
        },
        fragments: {
          enabled: false,
          fragment_item_id: null,
          fragment_name: '',
          fragments_required: 100,
          fragment_drop_sources: []
        },
        crupier: {
          enabled: false,
          currency_item_id: null,
          currency_name: '',
          currency_amount: null,
          notes: ''
        },
        challenge_reward: {
          enabled: false,
          challenge_type: '',
          notes: ''
        },
        quest: {
          enabled: false,
          quest_name: '',
          notes: ''
        },
        other: {
          enabled: false,
          method_name: '',
          notes: ''
        }
      },
      is_obtainable: true,
      source_notes: '',
      corrected_source_type: null,
      manual_difficulty_override: null,
      added_by: ''
    });

    const getItemName = (item) => {
      if (currentLanguage.value === 'es' && item.name_es) return item.name_es;
      if (currentLanguage.value === 'en' && item.name_en) return item.name_en;
      return item.name;
    };

    const getRarityName = (rarity) => {
      const rarityNames = {
        1: t('rarity.common'),
        2: t('rarity.unusual'),
        3: t('rarity.rare'),
        4: t('rarity.mythic'),
        5: t('rarity.legendary'),
        6: t('rarity.relic'),
        7: t('rarity.epic')
      };
      return rarityNames[rarity] || 'Unknown';
    };

    const loadStats = async () => {
      try {
        const response = await api.getMetadataStats();
        console.log('Stats response:', response);
        if (response.data && response.data.success) {
          stats.value = response.data.data;
        }
      } catch (error) {
        console.error('Error loading stats:', error);
      }
    };

    const searchItems = async () => {
      console.log('Search query:', searchQuery.value);
      if (!searchQuery.value || searchQuery.value.length < 2) {
        alert(t('metadata.searchMinLength'));
        return;
      }

      loading.value = true;
      try {
        const response = await api.searchItemsForMetadata(searchQuery.value);
        console.log('Search response:', response);
        if (response.data && response.data.success) {
          searchResults.value = response.data.data.items;
          console.log('Search results set to:', searchResults.value);
        }
      } catch (error) {
        console.error('Error searching items:', error);
        alert(t('metadata.searchError'));
      } finally {
        loading.value = false;
      }
    };

    const getDefaultForm = () => ({
      acquisition_methods: {
        drop: { enabled: false, drop_rates: [] },
        recipe: { enabled: false },
        fragments: { enabled: false, fragment_rates: [] },
        crupier: { enabled: false },
        challenge_reward: { enabled: false },
        quest: { enabled: false },
        other: { enabled: false }
      }
    });

    const selectItem = (item) => {
      console.log('Selecting item:', item);
      selectedItem.value = item;
      
      const defaultForm = getDefaultForm();
      
      // Load existing metadata if available
      if (item.metadata && Object.keys(item.metadata).length > 0) {
        console.log('Item has metadata:', item.metadata);
        
        const meta = item.metadata.acquisition_methods || {};
        
        editForm.value = {
          acquisition_methods: {
            drop: { 
              enabled: meta.drop?.enabled || false, 
              drop_rates: meta.drop?.drop_rates || [] 
            },
            recipe: { 
              enabled: meta.recipe?.enabled || false 
            },
            fragments: { 
              enabled: meta.fragments?.enabled || false, 
              fragment_rates: meta.fragments?.fragment_rates || [] 
            },
            crupier: { 
              enabled: meta.crupier?.enabled || false 
            },
            challenge_reward: { 
              enabled: meta.challenge_reward?.enabled || false 
            },
            quest: { 
              enabled: meta.quest?.enabled || false 
            },
            other: { 
              enabled: meta.other?.enabled || false 
            }
          }
        };
      } else {
        console.log('Item has no metadata, using default form');
        editForm.value = defaultForm;
      }
      
      console.log('Edit form set to:', editForm.value);
      console.log('Selected item set to:', selectedItem.value);
    };

    const addDropRate = () => {
      editForm.value.acquisition_methods.drop.drop_rates.push(null);
    };

    const removeDropRate = (index) => {
      editForm.value.acquisition_methods.drop.drop_rates.splice(index, 1);
    };

    const addFragmentRate = () => {
      editForm.value.acquisition_methods.fragments.fragment_rates.push(null);
    };

    const removeFragmentRate = (index) => {
      editForm.value.acquisition_methods.fragments.fragment_rates.splice(index, 1);
    };

    const closeEditor = () => {
      selectedItem.value = null;
      editForm.value = getDefaultForm();
    };

    const saveMetadata = async () => {
      if (!selectedItem.value) return;

      saving.value = true;
      try {
        // Prepare payload with item_id
        const payload = {
          item_id: selectedItem.value.item_id,
          name: getItemName(selectedItem.value),
          ...editForm.value
        };
        
        console.log('Saving metadata with payload:', payload);
        const response = await api.updateItemMetadata(selectedItem.value.item_id, payload);
        console.log('Save response:', response);
        if (response.data && response.data.success) {
          alert(t('metadata.saveSuccess'));
          // Update the item in search results
          const index = searchResults.value.findIndex(i => i.item_id === selectedItem.value.item_id);
          if (index !== -1) {
            searchResults.value[index].has_metadata = true;
            searchResults.value[index].metadata = response.data.data;
          }
          // Reload stats
          await loadStats();
          closeEditor();
        }
      } catch (error) {
        console.error('Error saving metadata:', error);
        alert(t('metadata.saveError'));
      } finally {
        saving.value = false;
      }
    };

    const deleteMetadata = async () => {
      if (!selectedItem.value || !selectedItem.value.has_metadata) return;
      
      if (!confirm(t('metadata.deleteConfirm'))) return;

      saving.value = true;
      try {
        const response = await api.deleteItemMetadata(selectedItem.value.item_id);
        console.log('Delete response:', response);
        if (response.data && response.data.success) {
          alert(t('metadata.deleteSuccess'));
          // Update the item in search results
          const index = searchResults.value.findIndex(i => i.item_id === selectedItem.value.item_id);
          if (index !== -1) {
            searchResults.value[index].has_metadata = false;
            searchResults.value[index].metadata = {};
          }
          // Reload stats
          await loadStats();
          closeEditor();
        }
      } catch (error) {
        console.error('Error deleting metadata:', error);
        alert(t('metadata.deleteError'));
      } finally {
        saving.value = false;
      }
    };

    onMounted(async () => {
      await loadStats();
      
      // Auto-select preselected item if provided
      if (props.preselectedItem) {
        console.log('Preselected item detected:', props.preselectedItem);
        // Set as selected directly
        selectItem(props.preselectedItem);
        // Also add to search results for visibility
        searchResults.value = [props.preselectedItem];
      }
    });

    return {
      t,
      searchQuery,
      searchResults,
      selectedItem,
      stats,
      loading,
      saving,
      editForm,
      getItemName,
      getRarityName,
      searchItems,
      selectItem,
      closeEditor,
      saveMetadata,
      deleteMetadata,
      addDropRate,
      removeDropRate,
      addFragmentRate,
      removeFragmentRate
    };
  }
};
</script>

<style scoped>
.metadata-admin {
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
}

.admin-header {
  margin-bottom: 2rem;
}

.admin-header h1 {
  font-size: 2rem;
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

.description {
  color: #666;
  font-size: 1rem;
}

.stats-panel {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

@media (max-width: 1200px) {
  .stats-panel {
    grid-template-columns: 1fr;
  }
  
  .stat-card.progress-card {
    grid-column: 1;
  }
}

.stat-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 1.5rem;
  border-radius: 12px;
  text-align: center;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.stat-card.relic-highlight {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  border: 2px solid rgba(255, 215, 0, 0.3);
}

.stat-card.progress-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  grid-column: 1 / -1;
}

.progress-bar {
  width: 100%;
  height: 8px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 4px;
  overflow: hidden;
  margin-top: 0.5rem;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #4caf50 0%, #8bc34a 100%);
  transition: width 0.5s ease;
  border-radius: 4px;
}

.progress-percent {
  text-align: center;
  margin-top: 0.5rem;
  font-size: 1.2rem;
  font-weight: bold;
  opacity: 0.9;
}

.stat-value {
  font-size: 2.5rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
}

.stat-label {
  font-size: 0.9rem;
  opacity: 0.9;
}

.search-section {
  margin-bottom: 2rem;
}

.search-box {
  display: flex;
  gap: 1rem;
}

.search-input {
  flex: 1;
  padding: 0.75rem 1rem;
  border: 2px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

.search-input:focus {
  outline: none;
  border-color: #667eea;
}

.btn-search {
  padding: 0.75rem 2rem;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.3s;
}

.btn-search:hover:not(:disabled) {
  background: #5568d3;
}

.btn-search:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.results-section {
  margin-bottom: 2rem;
}

.results-section h2 {
  font-size: 1.5rem;
  color: #2c3e50;
  margin-bottom: 1rem;
}

.items-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1rem;
}

.item-card {
  background: white;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  padding: 1rem;
  cursor: pointer;
  transition: all 0.3s;
  position: relative;
}

.item-card:hover {
  border-color: #667eea;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2), 0 0 0 1px rgba(102, 126, 234, 0.3);
}

.item-card.has-metadata {
  border-color: #4caf50;
}

.item-card.selected {
  border-color: #667eea;
  background: rgba(102, 126, 234, 0.05);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3), 0 0 0 1px rgba(102, 126, 234, 0.4);
}

.item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.item-name {
  font-weight: bold;
  color: #2c3e50;
  font-size: 1rem;
}

.item-level {
  background: #667eea;
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.85rem;
}

.item-info {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
}

.item-slot {
  font-size: 0.85rem;
  color: #666;
}

.item-rarity {
  font-size: 0.85rem;
  font-weight: bold;
}

.rarity-1 { color: #999; }
.rarity-2 { color: #1eff00; }
.rarity-3 { color: #0070dd; }
.rarity-4 { color: #a335ee; }
.rarity-5 { color: #ff8000; }
.rarity-6 { color: #e6cc80; }
.rarity-7 { color: #e268a8; }

.item-source {
  font-size: 0.85rem;
  color: #666;
  margin-bottom: 0.5rem;
}

.metadata-badge {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  background: #4caf50;
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
}

.edit-section {
  background: white;
  border: 2px solid #667eea;
  border-radius: 12px;
  padding: 2rem;
  margin-top: 2rem;
}

.edit-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #e0e0e0;
}

.header-info {
  flex: 1;
}

.edit-header h2 {
  font-size: 1.5rem;
  color: #2c3e50;
  margin: 0 0 0.5rem 0;
}

.item-badges {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.badge-level,
.badge-rarity,
.badge-slot {
  padding: 0.35rem 0.75rem;
  border-radius: 6px;
  font-size: 0.9rem;
  font-weight: 600;
}

.badge-level {
  background: #667eea;
  color: white;
}

.badge-rarity {
  color: white;
  font-weight: bold;
}

.badge-rarity.rarity-1 { background: #999; }
.badge-rarity.rarity-2 { background: #1eff00; color: #000; }
.badge-rarity.rarity-3 { background: #0070dd; }
.badge-rarity.rarity-4 { background: #a335ee; }
.badge-rarity.rarity-5 { background: #ff8000; }
.badge-rarity.rarity-6 { background: #e6cc80; color: #000; }
.badge-rarity.rarity-7 { background: #e268a8; }

.badge-slot {
  background: #4caf50;
  color: white;
}

.btn-close {
  background: #f44336;
  color: white;
  border: none;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  cursor: pointer;
  font-size: 1.2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.3s;
}

.btn-close:hover {
  background: #d32f2f;
}

.edit-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group.full-width {
  grid-column: 1 / -1;
}

.form-group label {
  font-weight: bold;
  color: #2c3e50;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
}

.input-text,
.input-select,
.input-textarea,
.input-disabled {
  padding: 0.75rem;
  border: 2px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

.input-text:focus,
.input-select:focus,
.input-textarea:focus {
  outline: none;
  border-color: #667eea;
}

.input-disabled {
  background: #f5f5f5;
  color: #666;
  cursor: not-allowed;
}

.input-textarea {
  resize: vertical;
  font-family: inherit;
}

.form-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 2px solid #e0e0e0;
}

.btn-save,
.btn-delete,
.btn-cancel {
  padding: 0.75rem 2rem;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s;
  font-weight: bold;
}

.btn-save {
  background: #4caf50;
  color: white;
}

.btn-save:hover:not(:disabled) {
  background: #45a049;
}

.btn-delete {
  background: #f44336;
  color: white;
}

.btn-delete:hover:not(:disabled) {
  background: #d32f2f;
}

.btn-cancel {
  background: #9e9e9e;
  color: white;
}

.btn-cancel:hover {
  background: #757575;
}

.btn-save:disabled,
.btn-delete:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.section-divider {
  margin: 2rem 0 1rem 0;
  padding-top: 2rem;
  border-top: 2px solid #e0e0e0;
}

.section-divider h3 {
  font-size: 1.25rem;
  color: #667eea;
  margin: 0 0 0.5rem 0;
}

.section-subtitle {
  color: #999;
  font-size: 0.9rem;
  margin: 0;
}

.acquisition-method-card {
  background: white;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  padding: 1rem;
  margin-bottom: 1rem;
  transition: all 0.3s;
}

.acquisition-method-card:hover {
  border-color: #667eea;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.1);
}

.method-header {
  font-size: 1.1rem;
  margin-bottom: 0.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.method-details {
  margin-top: 1rem;
  padding-left: 2rem;
}

.info-text {
  color: #666;
  font-style: italic;
  margin: 0;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  font-weight: normal;
}

.checkbox-label input[type="checkbox"] {
  width: 20px;
  height: 20px;
  cursor: pointer;
}

.fragment-details {
  background: rgba(102, 126, 234, 0.05);
  padding: 1.5rem;
  border-radius: 8px;
  margin-top: 1rem;
}

.drop-sources-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.drop-source-item {
  display: grid;
  grid-template-columns: 2fr 1fr auto;
  gap: 0.5rem;
  align-items: center;
}

.input-text.small {
  max-width: 120px;
}

.btn-remove {
  background: #f44336;
  color: white;
  border: none;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  cursor: pointer;
  font-size: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.3s;
}

.btn-remove:hover {
  background: #d32f2f;
}

.btn-add-source {
  padding: 0.5rem 1rem;
  background: #4caf50;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background 0.3s;
  align-self: flex-start;
}

.btn-add-source:hover {
  background: #45a049;
}

.info-box {
  background: #f5f5f5;
  padding: 0.75rem 1rem;
  border-radius: 6px;
  margin-bottom: 1.5rem;
  color: #666;
}

.acquisition-method-card.compact {
  padding: 0.75rem 1rem;
}

.rate-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  align-items: center;
}

.rate-item {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  background: #f5f5f5;
  padding: 0.5rem;
  border-radius: 6px;
}

.input-rate {
  width: 80px;
  padding: 0.4rem 0.6rem;
  border: 2px solid #ddd;
  border-radius: 4px;
  font-size: 0.95rem;
  text-align: center;
}

.input-rate:focus {
  outline: none;
  border-color: #667eea;
}

.btn-remove-inline {
  background: #f44336;
  color: white;
  border: none;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  cursor: pointer;
  font-size: 0.85rem;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.3s;
}

.btn-remove-inline:hover {
  background: #d32f2f;
}

.btn-add-inline {
  padding: 0.4rem 0.8rem;
  background: #4caf50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.85rem;
  transition: background 0.3s;
}

.btn-add-inline:hover {
  background: #45a049;
}

@media (max-width: 768px) {
  .form-row {
    grid-template-columns: 1fr;
  }
  
  .items-grid {
    grid-template-columns: 1fr;
  }
  
  .rate-list {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>

