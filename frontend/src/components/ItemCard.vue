<template>
  <div class="item-card" :style="{ borderColor: rarityColor }">
    <!-- Edit Metadata Button -->
    <button
      v-if="showMetadataButton"
      class="btn-edit-metadata"
      @click.stop="onEditMetadata"
      :title="t('metadata.editMetadata')"
    >
      ⚙️
    </button>

    <div class="item-header" :style="{ background: rarityGradient }">
      <div class="item-image-wrapper">
        <img
          :src="itemImageUrl"
          :alt="item.name"
          class="item-image"
          @error="onImageError"
        />
      </div>

      <div class="item-basic-info">
        <div class="item-name">{{ itemName }}</div>
        <div class="item-meta">
          <span class="item-level">Nivel {{ item.level }}</span>
          <span v-if="item.slot" class="item-slot">{{
            formatSlot(item.slot)
          }}</span>
        </div>
        <div class="item-tags">
          <span
            class="tag rarity-tag"
            :class="
              item.is_epic
                ? 'rarity-epic'
                : item.is_relic
                ? 'rarity-relic'
                : `rarity-${item.rarity}`
            "
            :style="{ borderColor: rarityColor, color: rarityColor }"
          >
            {{ rarityName }}
          </span>
          <span v-if="item.is_relic || item.is_epic" class="tag special-tag"
            >⚡ Única</span
          >
          <span v-if="item.has_gem_slot" class="tag gem">💎 Gema</span>
          <span
            v-if="hasExtendedMetadata"
            class="tag metadata-tag"
            @mouseenter="showMetadataPopover"
            @mouseleave="hideMetadataPopover"
            :ref="(el) => (metadataTagRef = el)"
          >
            📊 {{ t("metadata.hasMetadata") }}
          </span>
        </div>
      </div>
    </div>

    <div class="item-body">
      <!-- Stats -->
      <ItemStatList :stats="item.stats" />

      <!-- Item Info -->
      <div class="item-footer">
        <div class="item-source">
          <i class="pi pi-map-marker"></i>
          <span>{{ formatSourceType(item.source_type) }}</span>
        </div>
        <div class="item-difficulty" :class="difficultyClass">
          <i class="pi pi-star-fill"></i>
          <span>{{ item.difficulty?.toFixed(1) || "N/A" }}</span>
        </div>
      </div>
    </div>

    <!-- Popover con metadata usando Teleport -->
    <Teleport to="body">
      <div
        v-if="showPopover && hasExtendedMetadata"
        class="metadata-popover"
        :style="popoverStyle"
        @mouseenter="showMetadataPopover"
        @mouseleave="hideMetadataPopover"
      >
        <!-- Acquisition Methods (excluding drops - shown below) -->
        <div v-if="hasNonDropMetadata" class="popover-section">
          <div class="popover-header">
            <strong>{{ t("metadata.acquisitionMethodsTitle") }}</strong>
          </div>
          <div class="popover-grid">
            <div v-if="metadataMethods.recipe" class="popover-row">
              <div class="popover-label">
                🔨 {{ t("metadata.methodRecipe") }}:
              </div>
              <div class="popover-value">
                <span v-if="recipeDetails">
                  {{ recipeDetails.ingredientCount }} {{ t("metadata.ingredients") }}
                </span>
                <span v-else>✓</span>
              </div>
            </div>
            <div v-if="metadataMethods.fragments" class="popover-row">
              <div class="popover-label">
                🔮 {{ t("metadata.methodFragments") }}:
              </div>
              <div class="popover-value">{{ metadataMethods.fragments }}</div>
            </div>
            <div v-if="metadataMethods.crupier" class="popover-row">
              <div class="popover-label">
                💰 {{ t("metadata.methodCrupier") }}:
              </div>
              <div class="popover-value">✓</div>
            </div>
            <div v-if="metadataMethods.challenge_reward" class="popover-row">
              <div class="popover-label">
                🏆 {{ t("metadata.methodChallengeReward") }}:
              </div>
              <div class="popover-value">✓</div>
            </div>
            <div v-if="metadataMethods.quest" class="popover-row">
              <div class="popover-label">📜 {{ t("metadata.methodQuest") }}:</div>
              <div class="popover-value">✓</div>
            </div>
            <div v-if="metadataMethods.other" class="popover-row">
              <div class="popover-label">
                ➕ {{ t("metadata.methodOther") }}:
              </div>
              <div class="popover-value">✓</div>
            </div>
          </div>
        </div>

        <!-- Drop Sources from Database (unified source) -->
        <div v-if="hasDropSources" class="popover-section drop-section">
          <div class="popover-header">
            <strong>{{ t("metadata.dropSourcesDetected") }}</strong>
          </div>
          <div class="drop-list">
            <div
              v-for="drop in dropSources"
              :key="drop.monsterId"
              class="drop-entry"
            >
              <img
                :src="drop.imageUrl"
                :alt="`Monster ${drop.monsterId}`"
                class="drop-monster-image"
                @error="onMonsterImageError"
              />
              <div class="drop-info">
                <div class="drop-monster-id">
                  {{ drop.displayName }}
                </div>
                <div class="drop-chance">
                  <span class="drop-rate-chip">
                    {{ formatDropRate(drop.ratePercent) }}
                  </span>
                  <span class="drop-rate-note">
                    {{ drop.rate.toFixed(4) }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { computed, ref } from "vue";
import { getRarityColor, getRarityName } from "../composables/useStats";
import { useLanguage } from "../composables/useLanguage";
import { useI18n } from "../composables/useI18n";
import ItemStatList from "./ItemStatList.vue";

const props = defineProps({
  item: {
    type: Object,
    required: true,
  },
  metadata: {
    type: Object,
    default: null,
  },
  showMetadataButton: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits(["edit-metadata"]);

const { getItemName, currentLanguage } = useLanguage();
const { t } = useI18n();

const hasManualMetadata = computed(() => {
  return props.metadata && Object.keys(props.metadata).length > 0;
});

const resolveMonsterName = (monsterName, monsterId) => {
  const lang = currentLanguage.value;

  if (monsterName) {
    if (typeof monsterName === "string") {
      return monsterName;
    }
    if (typeof monsterName === "object") {
      return (
        monsterName[lang] ||
        monsterName.en ||
        monsterName.es ||
        monsterName.fr ||
        null
      );
    }
  }

  return t("metadata.monsterIdFallback", { id: monsterId });
};

const dropSources = computed(() => {
  const sources = Array.isArray(props.item?.drop_sources)
    ? props.item.drop_sources
    : [];

  return sources.map((drop) => {
    const ratePercent =
      drop.drop_rate_percent ?? (drop.drop_rate ?? 0) * 100;
    return {
      monsterId: drop.monster_id,
      rate: drop.drop_rate ?? ratePercent / 100,
      ratePercent,
      imageUrl:
        drop.image_url ||
        `https://vertylo.github.io/wakassets/monsters/${drop.monster_id}.png`,
      displayName: resolveMonsterName(drop.monster_name, drop.monster_id),
    };
  });
});

const hasDropSources = computed(() => dropSources.value.length > 0);

// Check if has non-drop metadata (to avoid showing empty section)
const hasNonDropMetadata = computed(() => {
  if (!hasManualMetadata.value) return false;
  const methods = props.metadata.acquisition_methods || {};
  return (
    methods.recipe?.enabled ||
    methods.fragments?.enabled ||
    methods.crupier?.enabled ||
    methods.challenge_reward?.enabled ||
    methods.quest?.enabled ||
    methods.other?.enabled
  );
});

const hasExtendedMetadata = computed(
  () => hasNonDropMetadata.value || hasDropSources.value
);

const recipeDetails = computed(() => {
  if (!hasManualMetadata.value) return null;
  const methods = props.metadata.acquisition_methods || {};
  if (!methods.recipe?.enabled) return null;
  
  const ingredients = methods.recipe.ingredients || [];
  return {
    ingredientCount: ingredients.length,
    ingredients: ingredients
  };
});

const metadataMethods = computed(() => {
  if (!hasManualMetadata.value) return {};

  const methods = props.metadata.acquisition_methods || {};
  const result = {};

  // Note: drops are now handled by drop_sources from DB, not metadata
  if (methods.recipe?.enabled) {
    result.recipe = true;
  }

  if (methods.fragments?.enabled) {
    const rates = methods.fragments.fragment_rates || [];
    result.fragments =
      rates.length > 0 ? rates.join("%, ") + "%" : t("metadata.yes");
  }

  if (methods.crupier?.enabled) result.crupier = true;
  if (methods.challenge_reward?.enabled) result.challenge_reward = true;
  if (methods.quest?.enabled) result.quest = true;
  if (methods.other?.enabled) result.other = true;

  return result;
});

const showPopover = ref(false);
const metadataTagRef = ref(null);

const popoverStyle = computed(() => {
  if (!metadataTagRef.value) return {};

  const rect = metadataTagRef.value.getBoundingClientRect();

  return {
    position: "fixed",
    top: `${rect.top - 8}px`,
    left: `${rect.left + rect.width / 2}px`,
    transform: "translate(-50%, -100%)",
  };
});

const showMetadataPopover = () => {
  showPopover.value = true;
};

const hideMetadataPopover = () => {
  showPopover.value = false;
};

const formatDropRate = (value) => {
  if (value === undefined || value === null || Number.isNaN(Number(value))) {
    return "—";
  }
  const numeric = Number(value);
  const decimals =
    numeric >= 10
      ? numeric % 1 === 0
        ? 0
        : 1
      : numeric >= 1
      ? 2
      : 2;
  return `${numeric.toFixed(decimals)}%`;
};

const onMonsterImageError = (event) => {
  event.target.style.display = "none";
};

const onEditMetadata = () => {
  emit("edit-metadata", props.item);
};

const itemName = computed(() => getItemName(props.item));

const rarityColor = computed(() => {
  // Épicos se identifican con flag is_epic
  if (props.item.is_epic) {
    return "#D946EF"; // Épico - Púrpura
  }
  // Reliquias se identifican con flag is_relic (prioridad sobre rarity)
  if (props.item.is_relic) {
    return "#E91E63"; // Reliquia - Fucsia
  }
  // ✅ Recuerdos (rarity 6 pero NO is_relic)
  if (props.item.rarity === 6 && !props.item.is_relic) {
    return "#87CEFA"; // Recuerdo - Celeste/Azul claro (PVP items)
  }
  return getRarityColor(props.item.rarity);
});

const rarityName = computed(() => {
  // Épicos tienen su propio nombre
  if (props.item.is_epic) {
    return "Épico";
  }
  // Reliquias tienen su propio nombre (prioridad sobre rarity)
  if (props.item.is_relic) {
    return "Reliquia";
  }
  // ✅ FIX: Recuerdos (rarity 6 pero NO is_relic)
  if (props.item.rarity === 6 && !props.item.is_relic) {
    return "Recuerdo";
  }
  return getRarityName(props.item.rarity);
});

const rarityGradient = computed(() => {
  const color = rarityColor.value;
  return `linear-gradient(135deg, ${color}22 0%, ${color}11 100%)`;
});

// Image sources with proper fallbacks
const imageSources = computed(() => {
  const sources = [];
  
  // Primary source: gfx_id from graphicParameters (most accurate)
  if (props.item.gfx_id) {
    sources.push(`https://vertylo.github.io/wakassets/items/${props.item.gfx_id}.png`);
  }
  
  // Fallback: Try accessing from raw_data if available
  if (props.item.raw_data?.definition?.item?.graphicParameters?.gfxId) {
    const gfxId = props.item.raw_data.definition.item.graphicParameters.gfxId;
    if (!sources.includes(`https://vertylo.github.io/wakassets/items/${gfxId}.png`)) {
      sources.push(`https://vertylo.github.io/wakassets/items/${gfxId}.png`);
    }
  }
  
  // Legacy fallback: old format (may not work for all items)
  if (props.item.type_id && props.item.item_id) {
    sources.push(`https://vertylo.github.io/wakassets/items/${props.item.type_id}${props.item.item_id}.png`);
  }
  
  return sources;
});

const itemImageUrl = computed(() => imageSources.value[0]);

let currentSourceIndex = 0;

const difficultyClass = computed(() => {
  const diff = props.item.difficulty || 0;
  if (diff < 40) return "easy";
  if (diff < 65) return "medium";
  return "hard";
});

const formatSlot = (slot) => {
  const slotNames = {
    HEAD: "Cabeza",
    NECK: "Cuello",
    CHEST: "Pecho",
    LEGS: "Piernas",
    BACK: "Espalda",
    SHOULDERS: "Hombros",
    BELT: "Cinturón",
    FIRST_WEAPON: "Arma",
    SECOND_WEAPON: "Arma 2",
    ACCESSORY: "Accesorio",
    LEFT_HAND: "Anillo",
    RIGHT_HAND: "Anillo",
    PET: "Mascota",
    MOUNT: "Montura",
  };
  return slotNames[slot] || slot;
};

const formatSourceType = (sourceType) => {
  const sourceNames = {
    drop: "Drop de Monstruo",
    craft: "Crafteo",
    quest: "Misión",
    shop: "Tienda",
    dungeon: "Mazmorra",
  };
  return sourceNames[sourceType] || sourceType || "Desconocido";
};

const onImageError = (event) => {
  currentSourceIndex++;

  // Try next source if available
  if (currentSourceIndex < imageSources.value.length) {
    event.target.src = imageSources.value[currentSourceIndex];
    return;
  }

  // All sources failed - use slot-based icon placeholder
  const slotIcons = {
    HEAD: "⛑️",
    NECK: "📿",
    CHEST: "👕",
    LEGS: "👖",
    BACK: "🎒",
    SHOULDERS: "🦾",
    BELT: "⚡",
    FIRST_WEAPON: "⚔️",
    SECOND_WEAPON: "🗡️",
    ACCESSORY: "💫",
    LEFT_HAND: "💍",
    RIGHT_HAND: "💍",
    PET: "🐾",
    MOUNT: "🐴",
  };

  const icon = slotIcons[props.item.slot] || "⚡";
  const color = rarityColor.value.replace("#", "");

  // Create a better looking placeholder with emoji
  event.target.src = `data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='64' height='64' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' fill='%23${color}' opacity='0.2'/%3E%3Ctext x='50%25' y='50%25' text-anchor='middle' dy='.3em' font-size='32'%3E${icon}%3C/text%3E%3C/svg%3E`;
};
</script>

<style lang="scss" scoped>
.item-card {
  background: rgba(26, 35, 50, 0.8);
  border: 2px solid;
  border-radius: 12px;
  overflow: visible;
  transition: box-shadow 0.2s, border-color 0.2s;
  position: relative;

  &:hover {
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4),
      0 0 0 2px rgba(102, 126, 234, 0.3);
  }
}

.btn-edit-metadata {
  position: absolute;
  top: 8px;
  right: 8px;
  background: rgba(102, 126, 234, 0.9);
  border: none;
  width: 32px;
  height: 32px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1.1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10;
  transition: all 0.3s;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);

  &:hover {
    background: rgba(102, 126, 234, 1);
    transform: scale(1.1);
  }
}

.item-header {
  padding: 1rem;
  display: flex;
  gap: 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px 12px 0 0;
  overflow: hidden;
}

.item-image-wrapper {
  width: 64px;
  height: 64px;
  flex-shrink: 0;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid rgba(255, 255, 255, 0.2);
}

.item-image {
  width: 56px;
  height: 56px;
  object-fit: contain;
}

.item-basic-info {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.item-name {
  font-size: 1.1rem;
  font-weight: 600;
  color: #fff;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.item-meta {
  display: flex;
  gap: 0.75rem;
  font-size: 0.875rem;
  color: #a0a0a0;
}

.item-tags {
  display: flex;
  gap: 0.5rem;
  margin-top: 0.25rem;
}

.tag {
  padding: 0.125rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;

  &.rarity-tag {
    background: rgba(0, 0, 0, 0.4);
    border: 1px solid;
    backdrop-filter: blur(4px);
  }

  // Colores específicos por rareza (según tabla oficial de Wakfu)
  &.rarity-0,
  &.rarity-1 {
    // Común - Gris
    background: rgba(128, 128, 128, 0.15);
    border-color: #808080;
    color: #b0b0b0;
  }

  &.rarity-2 {
    // Inusual - Gris claro
    background: rgba(158, 158, 158, 0.15);
    border-color: #9e9e9e;
    color: #bdbdbd;
  }

  &.rarity-3 {
    // Raro - Verde
    background: rgba(76, 175, 80, 0.15);
    border-color: #4caf50;
    color: #66bb6a;
  }

  &.rarity-4 {
    // Mítico - Naranja
    background: rgba(255, 152, 0, 0.15);
    border-color: #ff9800;
    color: #ffb74d;
  }

  &.rarity-5 {
    // Reliquia - Fucsia/Rosa
    background: rgba(233, 30, 99, 0.15);
    border-color: #e91e63;
    color: #f06292;
    font-weight: 700;
    text-shadow: 0 0 8px rgba(233, 30, 99, 0.5);
  }

  &.rarity-6 {
    // Recuerdo (Souvenir) - Celeste/Azul claro
    background: rgba(79, 195, 247, 0.15);
    border-color: #4fc3f7;
    color: #81d4fa;
    font-weight: 700;
    text-shadow: 0 0 8px rgba(79, 195, 247, 0.5);
  }

  &.rarity-7 {
    // Legendario - Dorado/Amarillo
    background: rgba(255, 215, 0, 0.15);
    border-color: #ffd700;
    color: #ffd700;
    font-weight: 700;
    text-shadow: 0 0 8px rgba(255, 215, 0, 0.5);
  }

  &.rarity-epic {
    // Épico - Fucsia/Rosa (tono más púrpura)
    background: rgba(217, 70, 239, 0.15);
    border-color: #d946ef;
    color: #e879f9;
    font-weight: 700;
    text-shadow: 0 0 8px rgba(217, 70, 239, 0.5);
  }

  &.rarity-relic {
    // Reliquia (cuando is_relic=true)
    background: rgba(233, 30, 99, 0.15);
    border-color: #e91e63;
    color: #f06292;
    font-weight: 700;
    text-shadow: 0 0 8px rgba(233, 30, 99, 0.5);
  }

  &.gem {
    background: rgba(156, 39, 176, 0.2);
    color: #9c27b0;
    border: 1px solid rgba(156, 39, 176, 0.4);
  }

  &.special-tag {
    background: rgba(255, 215, 0, 0.2);
    color: #ffd700;
    border: 1px solid rgba(255, 215, 0, 0.4);
    font-size: 0.7rem;
  }

  &.metadata-tag {
    background: rgba(76, 175, 80, 0.2);
    color: #4caf50;
    border: 1px solid rgba(76, 175, 80, 0.4);
    font-size: 0.7rem;
    cursor: pointer;
    position: relative;
    z-index: 1;

    &:hover {
      background: rgba(76, 175, 80, 0.3);
      border-color: #4caf50;
      z-index: 1001;
    }
  }
}

.metadata-popover {
  position: fixed;
  background: #424242;
  border-radius: 8px;
  padding: 0;
  min-width: 300px;
  max-width: 350px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5);
  z-index: 9999;
  animation: popoverFadeIn 0.2s ease;
  color: white;
  font-size: 0.875rem;
  overflow: hidden;
  pointer-events: auto;

  &::after {
    content: "";
    position: absolute;
    top: 100%;
    left: 50%;
    transform: translateX(-50%);
    border: 8px solid transparent;
    border-top-color: #424242;
  }
}

@keyframes popoverFadeIn {
  from {
    opacity: 0;
    transform: translate(-50%, -100%) translateY(4px);
  }
  to {
    opacity: 1;
    transform: translate(-50%, -100%);
  }
}

.popover-section + .popover-section {
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.popover-header {
  background: rgba(255, 255, 255, 0.1);
  padding: 0.75rem 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.15);
  font-size: 0.9rem;
  text-align: center;

  strong {
    color: #ffffff;
    font-weight: 600;
  }
}

.popover-grid {
  padding: 0.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.drop-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  padding: 0.75rem 1rem 1rem;
}

.drop-entry {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  padding: 0.6rem 0.75rem;
  transition: background 0.2s;

  &:hover {
    background: rgba(255, 255, 255, 0.08);
  }
}

.drop-monster-image {
  width: 40px;
  height: 40px;
  object-fit: contain;
  border-radius: 6px;
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.drop-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.drop-monster-id {
  font-weight: 600;
  color: #ffffff;
  font-size: 0.85rem;
}

.drop-chance {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.7);
}

.drop-rate-chip {
  padding: 0.15rem 0.5rem;
  border-radius: 999px;
  background: rgba(76, 175, 80, 0.2);
  color: #8bc34a;
  border: 1px solid rgba(76, 175, 80, 0.35);
  font-weight: 600;
}

.drop-rate-note {
  font-size: 0.75rem;
  color: rgba(255, 255, 255, 0.45);
}

.popover-row {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 1rem;
  align-items: center;
  padding: 0.5rem 0.75rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 6px;
  transition: background 0.2s;

  &:hover {
    background: rgba(255, 255, 255, 0.08);
  }
}

.popover-label {
  color: rgba(255, 255, 255, 0.9);
  font-size: 0.85rem;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 0.35rem;
}

.popover-value {
  color: #4caf50;
  font-weight: 600;
  font-size: 0.9rem;
  text-align: right;
  white-space: nowrap;
}

.item-body {
  padding: 1rem;
  border-radius: 0 0 12px 12px;
  overflow: hidden;
}

.item-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  font-size: 0.875rem;
}

.item-source {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #a0a0a0;

  i {
    font-size: 0.875rem;
  }
}

.item-difficulty {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-weight: 600;

  &.easy {
    background: rgba(76, 175, 80, 0.2);
    color: #4caf50;
  }

  &.medium {
    background: rgba(255, 165, 0, 0.2);
    color: #ffa500;
  }

  &.hard {
    background: rgba(244, 67, 54, 0.2);
    color: #f44336;
  }

  i {
    font-size: 0.75rem;
  }
}
</style>
