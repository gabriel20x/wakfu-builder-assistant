<template>
  <Teleport to="body">
    <div v-if="isOpen" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content alternatives-modal">
        <!-- Header -->
        <div class="modal-header">
          <h2>{{ t('alternatives.title') }}</h2>
          <button class="btn-close" @click="closeModal">✕</button>
        </div>

        <!-- Main Item -->
        <div class="main-item-section">
          <div class="item-showcase">
            <div class="item-image-container">
              <img
                :src="mainItem.itemImageUrl"
                :alt="mainItem.itemName"
                class="showcase-image"
              />
            </div>
            <div class="item-details">
              <div class="item-name-large">{{ mainItem.itemName }}</div>
              <div class="item-meta">
                <span class="level-badge">Nivel {{ mainItem.item.level }}</span>
                <span class="rarity-badge" :style="{ background: mainItem.rarityColor }">
                  {{ mainItem.rarityName }}
                </span>
              </div>
              <div class="item-power-display">
                <span class="power-label">{{ t('alternatives.itemPower') }}</span>
                <span class="power-value">{{ mainItem.itemPower.toFixed(2) }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Alternatives List -->
        <div class="alternatives-section">
          <h3>{{ t('alternatives.betterAlternatives') }}</h3>
          
          <div v-if="alternatives.length === 0" class="no-alternatives">
            {{ t('alternatives.noAlternatives') }}
          </div>

          <div v-else class="alternatives-list">
            <div
              v-for="(alt, index) in alternatives"
              :key="alt.item_id"
              class="alternative-item"
              :class="{ 'has-stats-change': hasStatsChange(alt) }"
            >
              <!-- Rank badge -->
              <div class="rank-badge">{{ index + 1 }}</div>

              <!-- Item image -->
              <div class="alt-image-container">
                <img
                  :src="getItemImageUrl(alt)"
                  :alt="alt.name"
                  class="alt-image"
                />
              </div>

              <!-- Item info -->
              <div class="alt-info">
                <div class="alt-name">{{ getItemName(alt) }}</div>
                <div class="alt-meta">
                  <span class="level-small">Nivel {{ alt.level }}</span>
                  <span class="rarity-small" :style="{ color: getRarityColor(alt) }">
                    {{ getRarityName(alt) }}
                  </span>
                </div>
              </div>

              <!-- Power comparison -->
              <div class="power-comparison">
                <div class="power-value">{{ alt.item_power?.toFixed(2) || 'N/A' }}</div>
                <div class="power-diff" :class="getPowerDiffClass(alt)">
                  {{ getPowerDiffDisplay(alt) }}
                </div>
              </div>

              <!-- Stats comparison -->
              <div class="stats-comparison">
                <div
                  v-for="(statChange, statName) in getStatsComparison(alt)"
                  :key="statName"
                  class="stat-change"
                  :class="getStatChangeClass(statChange)"
                  :title="`${statName}: ${statChange.mainValue} → ${statChange.altValue}`"
                >
                  <span class="stat-name">{{ statName }}</span>
                  <span class="stat-delta" :class="getStatDeltaClass(statChange)">
                    {{ getStatDeltaDisplay(statChange) }}
                  </span>
                </div>
              </div>

              <!-- Difficulty -->
              <div class="alt-difficulty">
                <i class="pi pi-star-fill"></i>
                <span>{{ alt.difficulty?.toFixed(1) || 'N/A' }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Footer -->
        <div class="modal-footer">
          <button class="btn-primary" @click="closeModal">
            {{ t('ui.close') }}
          </button>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { computed, ref } from 'vue';
import { useLanguage } from '../composables/useLanguage';
import { useI18n } from '../composables/useI18n';

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false,
  },
  item: {
    type: Object,
    required: true,
  },
  alternatives: {
    type: Array,
    default: () => [],
  },
  itemPower: {
    type: Number,
    default: 0,
  },
});

const emit = defineEmits(['close']);

const { getItemName: getItemNameLang, currentLanguage } = useLanguage();
const { t } = useI18n();

const closeModal = () => {
  emit('close');
};

// Get item name with language support
const getItemName = (item) => {
  const lang = currentLanguage.value;
  if (lang === 'es' && item.name_es) return item.name_es;
  if (lang === 'en' && item.name_en) return item.name_en;
  if (lang === 'fr' && item.name_fr) return item.name_fr;
  return item.name || 'Unknown Item';
};

// Get item image URL
const getItemImageUrl = (item) => {
  if (item.gfx_id) {
    return `https://vertylo.github.io/wakassets/items/${item.gfx_id}.png`;
  }
  return `https://vertylo.github.io/wakassets/items/${item.item_id}.png`;
};

// Rarity helpers
const getRarityColor = (item) => {
  if (item.is_epic) return '#D946EF';
  if (item.is_relic) return '#E91E63';
  if (item.rarity === 6 && !item.is_relic) return '#87CEFA';
  
  const colors = {
    1: '#999999', // Común
    2: '#4CAF50', // Poco común
    3: '#2196F3', // Raro
    4: '#9C27B0', // Mítico
    5: '#FFD700', // Legendario
    6: '#E91E63', // Reliquia
    7: '#FF4500', // Épico
  };
  return colors[item.rarity] || '#999999';
};

const getRarityName = (item) => {
  if (item.is_epic) return 'Épico';
  if (item.is_relic) return 'Reliquia';
  if (item.rarity === 6 && !item.is_relic) return 'Recuerdo';
  
  const names = {
    1: 'Común',
    2: 'Poco Común',
    3: 'Raro',
    4: 'Mítico',
    5: 'Legendario',
    6: 'Reliquia',
    7: 'Épico',
  };
  return names[item.rarity] || 'Desconocido';
};

// Main item display data
const mainItem = computed(() => ({
  item: props.item,
  itemName: getItemName(props.item),
  itemPower: props.itemPower,
  rarityColor: getRarityColor(props.item),
  rarityName: getRarityName(props.item),
  itemImageUrl: getItemImageUrl(props.item),
}));

// Stats comparison logic
const getStatsComparison = (alt) => {
  const mainStats = props.item.stats || {};
  const altStats = alt.stats || {};
  
  // Get all stat names from both items
  const allStats = new Set([...Object.keys(mainStats), ...Object.keys(altStats)]);
  
  const comparison = {};
  
  allStats.forEach((statName) => {
    const mainValue = mainStats[statName] || 0;
    const altValue = altStats[statName] || 0;
    const delta = altValue - mainValue;
    
    // Only show stats that have differences
    if (delta !== 0) {
      comparison[statName] = {
        mainValue,
        altValue,
        delta,
      };
    }
  });
  
  return comparison;
};

const hasStatsChange = (alt) => {
  return Object.keys(getStatsComparison(alt)).length > 0;
};

const getPowerDiffClass = (alt) => {
  const diff = alt.power_difference || 0;
  return diff < 0 ? 'negative' : 'positive';
};

const getPowerDiffDisplay = (alt) => {
  const diff = alt.power_difference || 0;
  const sign = diff >= 0 ? '+' : '';
  return `${sign}${diff.toFixed(2)}`;
};

const getStatChangeClass = (statChange) => {
  if (statChange.delta > 0) return 'stat-gain';
  if (statChange.delta < 0) return 'stat-loss';
  return 'stat-neutral';
};

const getStatDeltaClass = (statChange) => {
  if (statChange.delta > 0) return 'delta-gain';
  if (statChange.delta < 0) return 'delta-loss';
  return 'delta-neutral';
};

const getStatDeltaDisplay = (statChange) => {
  const sign = statChange.delta > 0 ? '+' : '';
  return `${sign}${statChange.delta}`;
};
</script>

<style scoped lang="scss">
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
  animation: fadeIn 0.2s ease-in-out;

  @keyframes fadeIn {
    from {
      opacity: 0;
    }
    to {
      opacity: 1;
    }
  }
}

.modal-content {
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
  border: 2px solid #0f3460;
  border-radius: 12px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.8);
  max-width: 900px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 2px solid #0f3460;
  background: linear-gradient(135deg, #0f3460 0%, #16213e 100%);

  h2 {
    margin: 0;
    color: #00d4ff;
    font-size: 1.5rem;
  }

  .btn-close {
    background: none;
    border: none;
    color: #00d4ff;
    font-size: 1.5rem;
    cursor: pointer;
    padding: 0;
    width: 30px;
    height: 30px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    transition: all 0.2s;

    &:hover {
      background: rgba(0, 212, 255, 0.1);
      color: #fff;
    }
  }
}

.main-item-section {
  padding: 20px;
  border-bottom: 2px solid #0f3460;
  background: rgba(15, 52, 96, 0.3);

  .item-showcase {
    display: flex;
    gap: 20px;
    align-items: center;

    .item-image-container {
      width: 100px;
      height: 100px;
      background: rgba(0, 212, 255, 0.1);
      border: 2px solid #00d4ff;
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;

      .showcase-image {
        max-width: 90%;
        max-height: 90%;
        object-fit: contain;
      }
    }

    .item-details {
      flex: 1;

      .item-name-large {
        font-size: 1.3rem;
        font-weight: bold;
        color: #fff;
        margin-bottom: 8px;
      }

      .item-meta {
        display: flex;
        gap: 10px;
        margin-bottom: 12px;

        .level-badge,
        .rarity-badge {
          padding: 4px 10px;
          border-radius: 6px;
          font-size: 0.85rem;
          font-weight: 600;
          color: #fff;
          background: rgba(0, 212, 255, 0.2);
          border: 1px solid #00d4ff;
        }

        .rarity-badge {
          border: none;
        }
      }

      .item-power-display {
        display: flex;
        align-items: baseline;
        gap: 10px;

        .power-label {
          color: #aaa;
          font-size: 0.9rem;
        }

        .power-value {
          font-size: 1.5rem;
          font-weight: bold;
          color: #00d4ff;
        }
      }
    }
  }
}

.alternatives-section {
  flex: 1;
  padding: 20px;
  overflow-y: auto;

  h3 {
    color: #00d4ff;
    margin: 0 0 15px 0;
    font-size: 1.1rem;
    border-bottom: 2px solid #0f3460;
    padding-bottom: 10px;
  }

  .no-alternatives {
    text-align: center;
    color: #888;
    padding: 30px;
    font-style: italic;
  }

  .alternatives-list {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  .alternative-item {
    background: rgba(0, 212, 255, 0.05);
    border: 1px solid rgba(0, 212, 255, 0.2);
    border-radius: 8px;
    padding: 12px;
    display: grid;
    grid-template-columns: 35px 70px 1fr auto auto auto;
    gap: 15px;
    align-items: center;
    transition: all 0.2s;

    &:hover {
      background: rgba(0, 212, 255, 0.1);
      border-color: rgba(0, 212, 255, 0.4);
    }

    .rank-badge {
      width: 35px;
      height: 35px;
      background: linear-gradient(135deg, #00d4ff, #0099cc);
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: bold;
      color: #fff;
      font-size: 0.9rem;
    }

    .alt-image-container {
      width: 70px;
      height: 70px;
      background: rgba(0, 212, 255, 0.1);
      border: 1px solid #00d4ff;
      border-radius: 6px;
      display: flex;
      align-items: center;
      justify-content: center;

      .alt-image {
        max-width: 90%;
        max-height: 90%;
        object-fit: contain;
      }
    }

    .alt-info {
      .alt-name {
        color: #fff;
        font-weight: 600;
        margin-bottom: 4px;
      }

      .alt-meta {
        display: flex;
        gap: 8px;
        font-size: 0.85rem;

        .level-small {
          color: #aaa;
        }

        .rarity-small {
          font-weight: 600;
        }
      }
    }

    .power-comparison {
      text-align: right;

      .power-value {
        color: #00d4ff;
        font-weight: bold;
        font-size: 1rem;
      }

      .power-diff {
        font-size: 0.85rem;
        font-weight: 600;
        margin-top: 4px;

        &.negative {
          color: #ff6b6b;
        }

        &.positive {
          color: #51cf66;
        }
      }
    }

    .stats-comparison {
      display: flex;
      gap: 6px;
      flex-wrap: wrap;
      max-width: 300px;

      .stat-change {
        padding: 3px 8px;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 600;
        cursor: help;
        transition: all 0.2s;

        .stat-name {
          color: #ccc;
          display: inline;
        }

        .stat-delta {
          margin-left: 4px;
          font-weight: bold;

          &.delta-gain {
            color: #51cf66;
          }

          &.delta-loss {
            color: #ff6b6b;
          }

          &.delta-neutral {
            color: #888;
          }
        }

        &.stat-gain {
          background: rgba(81, 207, 102, 0.2);
          border: 1px solid rgba(81, 207, 102, 0.4);
          color: #51cf66;

          &:hover {
            background: rgba(81, 207, 102, 0.3);
          }
        }

        &.stat-loss {
          background: rgba(255, 107, 107, 0.2);
          border: 1px solid rgba(255, 107, 107, 0.4);
          color: #ff6b6b;

          &:hover {
            background: rgba(255, 107, 107, 0.3);
          }
        }

        &.stat-neutral {
          background: rgba(136, 136, 136, 0.2);
          border: 1px solid rgba(136, 136, 136, 0.4);
          color: #888;

          &:hover {
            background: rgba(136, 136, 136, 0.3);
          }
        }
      }
    }

    .alt-difficulty {
      display: flex;
      align-items: center;
      gap: 4px;
      color: #ffa500;
      font-size: 0.85rem;
    }
  }
}

.modal-footer {
  padding: 15px 20px;
  border-top: 2px solid #0f3460;
  display: flex;
  justify-content: flex-end;
  background: rgba(15, 52, 96, 0.3);

  .btn-primary {
    padding: 8px 20px;
    background: linear-gradient(135deg, #00d4ff, #0099cc);
    color: #fff;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-weight: 600;
    transition: all 0.2s;

    &:hover {
      transform: translateY(-2px);
      box-shadow: 0 5px 15px rgba(0, 212, 255, 0.3);
    }

    &:active {
      transform: translateY(0);
    }
  }
}

// Responsive
@media (max-width: 768px) {
  .modal-content {
    max-height: 95vh;
  }

  .main-item-section .item-showcase {
    flex-direction: column;
  }

  .alternative-item {
    grid-template-columns: 1fr !important;

    .rank-badge {
      justify-self: start;
    }

    .alt-image-container {
      justify-self: start;
      width: 60px;
      height: 60px;
    }

    .power-comparison {
      text-align: left;
    }

    .stats-comparison {
      max-width: 100%;
    }
  }
}
</style>
