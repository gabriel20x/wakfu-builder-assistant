<template>
  <div class="enchantment-panel">
    <div v-if="!catalogsLoaded" class="loading-state">
      <p-progressSpinner style="width: 40px; height: 40px" />
      <span>{{ t('enchant.loading') }}</span>
    </div>

    <div v-else class="panel-columns">
      <!-- Columna 1: engarces por objeto -->
      <section class="column column-slots">
        <header class="column-header">
          <h3>{{ t('enchant.myRunes') }}</h3>
          <button
            v-if="hasAny"
            class="icon-button"
            :title="t('enchant.clearAll')"
            @click="onClearAll"
          >
            <i class="pi pi-trash" />
          </button>
        </header>

        <div class="column-body">
          <div v-if="!enchantableItems.length" class="empty-hint">
            {{ t('enchant.noItems') }}
          </div>

          <div
            v-for="item in enchantableItems"
            :key="item.item_id"
            class="item-row"
            :class="{ focused: focusedSlot === item.slot }"
            @click="focusSlot(item.slot)"
          >
            <img
              class="item-image"
              :src="itemImage(item)"
              :alt="itemName(item)"
              loading="lazy"
              @error="onImageError"
            />

            <div class="item-main">
              <div class="item-name" :style="{ color: rarityColor(item.rarity) }">
                {{ itemName(item) }}
              </div>

              <div class="rune-strip">
                <button
                  v-for="index in itemShardSlots(item)"
                  :key="index"
                  class="rune-slot"
                  :class="[`color-${colorKey(slotColor(item.slot, index - 1))}`, { filled: runeAt(item.slot, index - 1).runeId }]"
                  :title="runeTooltip(item, index - 1)"
                  @click.stop="openRuneEditor(item, index - 1)"
                >
                  <span v-if="runeAt(item.slot, index - 1).runeId" class="rune-level">
                    {{ runeAt(item.slot, index - 1).level }}
                  </span>
                </button>
              </div>
            </div>

            <button
              class="sub-slot"
              :class="{
                filled: subFor(item.slot),
                invalid: subFor(item.slot) && !subFits(item.slot, subFor(item.slot)),
              }"
              :title="subTooltip(item.slot)"
              @click.stop="focusSlot(item.slot)"
            >
              <template v-if="subFor(item.slot)">
                <span class="sub-name">{{ localizedName(subFor(item.slot)) }}</span>
                <i
                  class="pi pi-times remove-sub"
                  @click.stop="setSublimation(buildKey, item.slot, null)"
                />
              </template>
              <span v-else class="sub-placeholder">{{ t('enchant.subSlot') }}</span>
            </button>
          </div>

          <!-- Objetos de la build que el juego no deja encantar -->
          <p v-if="skippedItems.length" class="skipped-note">
            {{ t('enchant.notEnchantable') }}
            <span class="skipped-names">
              {{ skippedItems.map(itemName).join(', ') }}
            </span>
          </p>

          <!-- Sublimaciones épica y relicaria (una por build) -->
          <div class="special-subs">
            <button
              v-for="kind in ['epic', 'relic']"
              :key="kind"
              class="special-slot"
              :class="[kind, { filled: specialSub(kind), active: focusedSlot === kind }]"
              @click="focusSlot(kind)"
            >
              <span class="special-label">{{ t(`enchant.${kind}Sub`) }}</span>
              <template v-if="specialSub(kind)">
                <span class="sub-name">{{ localizedName(specialSub(kind)) }}</span>
                <i
                  class="pi pi-times remove-sub"
                  @click.stop="setSpecialSublimation(buildKey, kind, null)"
                />
              </template>
            </button>
          </div>
        </div>
      </section>

      <!-- Columna 2: catálogo de runas -->
      <section class="column column-runes">
        <header class="column-header">
          <h3>{{ t('enchant.runes') }}</h3>
        </header>

        <div class="column-body">
          <div class="rune-level-control">
            <label>{{ t('enchant.runeLevel') }}</label>
            <input
              v-model.number="selectedRuneLevel"
              type="range"
              min="1"
              :max="MAX_RUNE_LEVEL"
              class="level-slider"
            />
            <span class="level-value">{{ selectedRuneLevel }}</span>
          </div>

          <p class="hint" :class="{ 'hint-active': activeRuneTarget }">
            {{ activeRuneTarget ? t('enchant.pickRuneFor', { slot: t(`slot.${activeRuneTarget.slot}`) }) : t('enchant.pickSlotFirst') }}
          </p>

          <button
            v-for="rune in runes"
            :key="rune.id"
            class="rune-entry"
            :class="[`color-${colorKey(rune.color)}`, { disabled: !activeRuneTarget }]"
            :disabled="!activeRuneTarget"
            @click="applyRune(rune)"
          >
            <span class="rune-chip" :class="`color-${colorKey(rune.color)}`" />
            <span class="rune-entry-name">{{ localizedName(rune) }}</span>
            <span class="rune-entry-value">
              +{{ previewRuneValue(rune) }}
              <i
                v-if="isDoubled(rune)"
                class="pi pi-angle-double-up doubled"
                :title="t('enchant.doubleBonus')"
              />
            </span>
          </button>
        </div>
      </section>

      <!-- Columna 3: catálogo de sublimaciones -->
      <section class="column column-subs">
        <header class="column-header">
          <h3>{{ t('enchant.sublimations') }}</h3>
          <input
            v-model="subSearch"
            class="search-input"
            type="search"
            :placeholder="t('enchant.search')"
          />
        </header>

        <div class="column-body">
          <p class="hint">
            {{ focusedSlot ? focusHint : t('enchant.pickSlotFirst') }}
          </p>

          <button
            v-for="sub in filteredSublimations"
            :key="sub.id"
            class="sub-entry"
            :class="{ fits: subFits(focusedItemSlot, sub), disabled: !focusedSlot }"
            :disabled="!focusedSlot"
            @click="applySublimation(sub)"
          >
            <div class="sub-entry-head">
              <span class="sub-entry-name">{{ localizedName(sub) }}</span>
              <span v-if="sub.pattern.length" class="pattern">
                <span
                  v-for="(color, i) in sub.pattern"
                  :key="i"
                  class="pattern-dot"
                  :class="`color-${colorKey(color)}`"
                />
              </span>
              <span v-else class="pattern-special" :class="sub.is_epic ? 'epic' : 'relic'">
                {{ sub.is_epic ? t('enchant.epicShort') : t('enchant.relicShort') }}
              </span>
            </div>
            <div v-if="effectLines(sub).length" class="sub-effect">
              <span
                v-for="(line, i) in effectLines(sub)"
                :key="i"
                :class="{ indented: line.indented }"
              >
                {{ line.text }}
              </span>
            </div>
            <div v-if="sub.max_stack" class="sub-stack">
              {{ t('enchant.maxStack', { n: sub.max_stack }) }}
            </div>
          </button>

          <div v-if="!filteredSublimations.length" class="empty-hint">
            {{ t('enchant.noResults') }}
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, watch, onMounted } from 'vue'
import { useI18n } from '../composables/useI18n'
import { useLanguage } from '../composables/useLanguage'
import { useEnchantments } from '../composables/useEnchantments'
import { getRarityColor } from '../composables/useStats'
import {
  MAX_RUNE_SLOTS,
  MAX_RUNE_LEVEL,
  COLOR_META,
  canSublimationFit,
  renderSublimationEffect,
  runeValue,
  maxRuneLevelForItem,
  isEnchantableItem,
  itemShardSlots,
} from '../lib/enchantments'

const props = defineProps({
  /** Items de la build (ya resueltos por el solver). */
  items: {
    type: Array,
    default: () => [],
  },
  /** Clave de persistencia devuelta por buildKeyFor(buildId, tier). */
  buildKey: {
    type: String,
    required: true,
  },
})

const { t } = useI18n()
const { currentLanguage } = useLanguage()
const {
  catalogsLoaded,
  loadCatalogs,
  runes,
  runesById,
  sublimations,
  getSlotEnchantment,
  getSlotColors,
  setRune,
  setSublimation,
  setSpecialSublimation,
  clearBuildEnchantments,
  hasEnchantments,
  getBuildEnchantments,
} = useEnchantments()

const focusedSlot = ref(null)
const activeRuneTarget = ref(null)
const selectedRuneLevel = ref(MAX_RUNE_LEVEL)
const subSearch = ref('')

onMounted(loadCatalogs)

// Al cambiar de build, limpiar la selección para no aplicar runas al objeto equivocado
watch(
  () => props.buildKey,
  () => {
    focusedSlot.value = null
    activeRuneTarget.value = null
  }
)

const lang = computed(() => currentLanguage.value || 'es')

// Solo los objetos que realmente admiten engarces. Quedan fuera armas
// secundarias, insignias, mascotas y monturas, más las piezas sueltas de
// otros slots que el gamedata marca con 0 engarces.
const enchantableItems = computed(() =>
  props.items.filter((item) => isEnchantableItem(item))
)

const skippedItems = computed(() =>
  props.items.filter((item) => !isEnchantableItem(item))
)

const hasAny = computed(() => hasEnchantments(props.buildKey))

const focusedItemSlot = computed(() =>
  focusedSlot.value && !['epic', 'relic'].includes(focusedSlot.value)
    ? focusedSlot.value
    : null
)

const focusedItem = computed(() =>
  enchantableItems.value.find((item) => item.slot === focusedItemSlot.value) || null
)

const focusHint = computed(() => {
  if (focusedSlot.value === 'epic') return t('enchant.pickEpic')
  if (focusedSlot.value === 'relic') return t('enchant.pickRelic')
  return t('enchant.pickSubFor', { slot: t(`slot.${focusedSlot.value}`) })
})

const filteredSublimations = computed(() => {
  const catalog = sublimations.value
  let pool = catalog.normal
  if (focusedSlot.value === 'epic') pool = catalog.epic
  else if (focusedSlot.value === 'relic') pool = catalog.relic

  const query = subSearch.value.trim().toLowerCase()
  const matches = query
    ? pool.filter((sub) => localizedName(sub).toLowerCase().includes(query))
    : pool

  // Las que encajan con los colores actuales primero
  if (!focusedItemSlot.value) return matches
  return [...matches].sort((a, b) => {
    const fitA = subFits(focusedItemSlot.value, a) ? 0 : 1
    const fitB = subFits(focusedItemSlot.value, b) ? 0 : 1
    return fitA - fitB
  })
})

const localizedName = (entry) => entry?.name?.[lang.value] || entry?.name?.en || ''

const itemName = (item) =>
  item[`name_${lang.value}`] || item.name_es || item.name || ''

const itemImage = (item) =>
  `https://vertylo.github.io/wakassets/items/${item.gfx_id}.png`

const onImageError = (event) => {
  event.target.style.visibility = 'hidden'
}

const rarityColor = (rarity) => getRarityColor(rarity)

const colorKey = (color) => COLOR_META[color]?.key || 'white'

const runeAt = (slot, index) =>
  getSlotEnchantment(props.buildKey, slot).runes[index] || {}

const slotColor = (slot, index) => runeAt(slot, index).color

const subFor = (slot) => {
  const id = getSlotEnchantment(props.buildKey, slot).subId
  return id ? sublimations.value.byId[id] : null
}

const specialSub = (kind) => {
  const build = getBuildEnchantments(props.buildKey)
  const id = kind === 'epic' ? build?.epicSubId : build?.relicSubId
  return id ? sublimations.value.byId[id] : null
}

const subFits = (slot, sub) => {
  if (!slot || !sub) return false
  if (!sub.pattern?.length) return true
  return canSublimationFit(getSlotColors(props.buildKey, slot), sub)
}

const effectLines = (sub) => renderSublimationEffect(sub, lang.value)

/**
 * Enfoca un objeto (o el slot épico/relicario) para elegirle sublimación.
 * Nunca alterna a "sin foco": desenfocar al volver a hacer clic desactivaría
 * el catálogo de sublimaciones justo cuando se quiere usar. Para soltar el
 * foco se hace clic en otro objeto.
 */
const focusSlot = (slot) => {
  focusedSlot.value = slot
  if (slot !== activeRuneTarget.value?.slot) {
    activeRuneTarget.value = null
  }
}

const openRuneEditor = (item, index) => {
  const current = activeRuneTarget.value
  if (current && current.slot === item.slot && current.index === index) {
    activeRuneTarget.value = null
    return
  }
  focusedSlot.value = item.slot
  activeRuneTarget.value = { slot: item.slot, index, itemLevel: item.level }
}

const cappedLevel = (rune, itemLevel) =>
  Math.min(selectedRuneLevel.value, maxRuneLevelForItem(rune, itemLevel))

const applyRune = (rune) => {
  const target = activeRuneTarget.value
  if (!target) return
  setRune(props.buildKey, target.slot, target.index, rune.id, cappedLevel(rune, target.itemLevel))
  // El engarce queda seleccionado: así se puede cambiar de runa o de nivel
  // sin volver a hacer clic. El usuario elige el siguiente engarce.
}

const applySublimation = (sub) => {
  if (focusedSlot.value === 'epic') {
    setSpecialSublimation(props.buildKey, 'epic', sub.id)
    return
  }
  if (focusedSlot.value === 'relic') {
    setSpecialSublimation(props.buildKey, 'relic', sub.id)
    return
  }
  if (focusedItemSlot.value) {
    setSublimation(props.buildKey, focusedItemSlot.value, sub.id)
  }
}

const previewRuneValue = (rune) => {
  const target = activeRuneTarget.value
  const level = target ? cappedLevel(rune, target.itemLevel) : selectedRuneLevel.value
  return runeValue(rune, level, target?.slot)
}

const isDoubled = (rune) =>
  activeRuneTarget.value && rune.double_bonus_slots?.includes(activeRuneTarget.value.slot)

const runeTooltip = (item, index) => {
  const state = runeAt(item.slot, index)
  if (!state.runeId) return t('enchant.emptySlot')
  const rune = runesById.value[state.runeId]
  if (!rune) return t('enchant.emptySlot')
  return `${localizedName(rune)} +${runeValue(rune, state.level, item.slot)}`
}

const subTooltip = (slot) => {
  const sub = subFor(slot)
  if (!sub) return t('enchant.subSlot')
  return subFits(slot, sub) ? localizedName(sub) : t('enchant.subMismatch')
}

const onClearAll = () => {
  if (window.confirm(t('enchant.confirmClear'))) {
    clearBuildEnchantments(props.buildKey)
    focusedSlot.value = null
    activeRuneTarget.value = null
  }
}
</script>

<style lang="scss" scoped>
.enchantment-panel {
  width: 100%;
  height: 100%;
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
  padding: 3rem 1rem;
  color: var(--primary-60);
}

.panel-columns {
  display: grid;
  grid-template-columns: minmax(320px, 1.4fr) minmax(220px, 0.9fr) minmax(260px, 1.1fr);
  gap: 1rem;
  align-items: start;
}

.column {
  display: flex;
  flex-direction: column;
  min-width: 0; // permite que el contenido encoja en lugar de desbordar
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid var(--highlight-50);
  border-radius: 8px;
  overflow: hidden;
}

.column-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.5rem;
  padding: 0.6rem 0.75rem;
  background: rgba(92, 107, 192, 0.2);
  border-bottom: 1px solid var(--highlight-50);

  h3 {
    margin: 0;
    font-size: 0.85rem;
    font-weight: 700;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    color: var(--primary-60);
    white-space: nowrap;
  }
}

.column-body {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
  padding: 0.6rem;
  max-height: 560px;
  overflow-y: auto;

  &::-webkit-scrollbar {
    width: 8px;
  }

  &::-webkit-scrollbar-track {
    background: rgba(0, 0, 0, 0.2);
  }

  &::-webkit-scrollbar-thumb {
    background: rgba(92, 107, 192, 0.5);
    border-radius: 4px;
  }
}

.icon-button {
  background: transparent;
  border: none;
  color: var(--primary-60);
  cursor: pointer;
  padding: 0.25rem;
  border-radius: 4px;

  &:hover {
    color: var(--error);
    background: var(--error-10);
  }
}

.search-input {
  flex: 1;
  min-width: 0;
  padding: 0.3rem 0.5rem;
  font-size: 0.75rem;
  color: #e0e0e0;
  background: rgba(0, 0, 0, 0.4);
  border: 1px solid var(--highlight-50);
  border-radius: 4px;

  &:focus {
    outline: none;
    border-color: var(--primary-40);
  }
}

.hint {
  margin: 0 0 0.25rem;
  font-size: 0.7rem;
  color: #8a93a5;
  font-style: italic;

  &.hint-active {
    color: var(--primary-60);
    font-style: normal;
  }
}

.empty-hint {
  padding: 1.5rem 0.75rem;
  text-align: center;
  font-size: 0.75rem;
  color: #808080;
}

// --- Columna 1: filas de objeto ---

.item-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.4rem;
  background: rgba(26, 35, 50, 0.6);
  border: 1px solid transparent;
  border-radius: 6px;
  cursor: pointer;
  transition: border-color 0.15s, background 0.15s;

  &:hover {
    background: rgba(92, 107, 192, 0.15);
  }

  &.focused {
    border-color: var(--primary-40);
    background: rgba(92, 107, 192, 0.2);
  }
}

.item-image {
  width: 34px;
  height: 34px;
  flex-shrink: 0;
  object-fit: contain;
}

.item-main {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.item-name {
  font-size: 0.72rem;
  font-weight: 600;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.rune-strip {
  display: flex;
  gap: 0.25rem;
}

.rune-slot {
  position: relative;
  width: 24px;
  height: 24px;
  flex-shrink: 0;
  border-radius: 4px;
  border: 2px solid;
  background: rgba(0, 0, 0, 0.35);
  cursor: pointer;
  padding: 0;
  transition: transform 0.12s;

  &:hover {
    transform: translateY(-1px);
  }

  &.color-white { border-color: var(--rune-white); }
  &.color-red { border-color: var(--rune-red); }
  &.color-green { border-color: var(--rune-green); }
  &.color-blue { border-color: var(--rune-blue); }

  &.filled {
    &.color-white { background: color-mix(in srgb, var(--rune-white) 30%, transparent); }
    &.color-red { background: color-mix(in srgb, var(--rune-red) 35%, transparent); }
    &.color-green { background: color-mix(in srgb, var(--rune-green) 35%, transparent); }
    &.color-blue { background: color-mix(in srgb, var(--rune-blue) 35%, transparent); }
  }
}

.rune-level {
  position: absolute;
  right: 1px;
  bottom: -1px;
  font-size: 0.55rem;
  font-weight: 700;
  color: #fff;
  text-shadow: 0 0 3px #000, 0 0 3px #000;
}

.sub-slot {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  width: 110px;
  flex-shrink: 0;
  padding: 0.3rem 0.4rem;
  font-size: 0.65rem;
  color: #b0b8c8;
  background: rgba(0, 0, 0, 0.3);
  border: 1px dashed var(--highlight-50);
  border-radius: 4px;
  cursor: pointer;

  &.filled {
    color: #e0e0e0;
    border-style: solid;
    border-color: var(--primary-40);
    background: rgba(92, 107, 192, 0.2);
  }

  &.invalid {
    border-color: var(--error-60);
    background: var(--error-10);
    color: #ffb3ae;
  }
}

.sub-name {
  flex: 1;
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  text-align: left;
}

.sub-placeholder {
  opacity: 0.7;
}

.remove-sub {
  font-size: 0.6rem;
  flex-shrink: 0;

  &:hover {
    color: var(--error);
  }
}

.skipped-note {
  margin: 0.4rem 0 0;
  font-size: 0.65rem;
  line-height: 1.4;
  color: #8a93a5;

  .skipped-names {
    color: #6f7787;
    font-style: italic;
  }
}

.special-subs {
  display: flex;
  gap: 0.4rem;
  margin-top: 0.4rem;
  padding-top: 0.6rem;
  border-top: 1px solid var(--highlight-50);
}

.special-slot {
  flex: 1;
  min-width: 0;
  display: flex;
  align-items: center;
  gap: 0.3rem;
  padding: 0.4rem 0.5rem;
  font-size: 0.65rem;
  color: #b0b8c8;
  background: rgba(0, 0, 0, 0.3);
  border: 1px dashed;
  border-radius: 6px;
  cursor: pointer;

  &.epic { border-color: color-mix(in srgb, var(--rune-epic) 60%, transparent); }
  &.relic { border-color: color-mix(in srgb, var(--rune-relic) 60%, transparent); }

  &.filled,
  &.active {
    border-style: solid;
    color: #fff;
  }

  &.epic.filled, &.epic.active { background: color-mix(in srgb, var(--rune-epic) 18%, transparent); }
  &.relic.filled, &.relic.active { background: color-mix(in srgb, var(--rune-relic) 18%, transparent); }
}

.special-label {
  font-weight: 600;
  white-space: nowrap;
  opacity: 0.85;
}

// --- Columna 2: runas ---

.rune-level-control {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding-bottom: 0.5rem;
  margin-bottom: 0.25rem;
  border-bottom: 1px solid var(--highlight-50);

  label {
    font-size: 0.68rem;
    color: #8a93a5;
    white-space: nowrap;
  }
}

.level-slider {
  flex: 1;
  min-width: 0;
  accent-color: var(--primary-40);
}

.level-value {
  width: 1.5rem;
  text-align: right;
  font-size: 0.75rem;
  font-weight: 700;
  color: #fff;
}

.rune-entry {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.35rem 0.5rem;
  font-size: 0.7rem;
  color: #e0e0e0;
  text-align: left;
  background: rgba(26, 35, 50, 0.6);
  border: 1px solid transparent;
  border-radius: 4px;
  cursor: pointer;

  &:hover:not(.disabled) {
    border-color: var(--primary-40);
    background: rgba(92, 107, 192, 0.2);
  }

  &.disabled {
    opacity: 0.45;
    cursor: not-allowed;
  }
}

.rune-chip {
  width: 10px;
  height: 10px;
  flex-shrink: 0;
  border-radius: 2px;

  &.color-white { background: var(--rune-white); }
  &.color-red { background: var(--rune-red); }
  &.color-green { background: var(--rune-green); }
  &.color-blue { background: var(--rune-blue); }
}

.rune-entry-name {
  flex: 1;
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.rune-entry-value {
  flex-shrink: 0;
  font-weight: 700;
  color: var(--primary-60);

  .doubled {
    font-size: 0.6rem;
    color: var(--secondary-50);
  }
}

// --- Columna 3: sublimaciones ---

.sub-entry {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  padding: 0.4rem 0.5rem;
  text-align: left;
  background: rgba(26, 35, 50, 0.6);
  border: 1px solid transparent;
  border-left: 3px solid transparent;
  border-radius: 4px;
  cursor: pointer;

  &:hover:not(.disabled) {
    background: rgba(92, 107, 192, 0.2);
  }

  &.fits {
    border-left-color: var(--secondary-50);
  }

  &.disabled {
    opacity: 0.45;
    cursor: not-allowed;
  }
}

.sub-entry-head {
  display: flex;
  align-items: center;
  gap: 0.4rem;
}

.sub-entry-name {
  flex: 1;
  min-width: 0;
  font-size: 0.72rem;
  font-weight: 600;
  color: #e0e0e0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.pattern {
  display: flex;
  gap: 2px;
  flex-shrink: 0;
}

.pattern-dot {
  width: 8px;
  height: 8px;
  border-radius: 2px;

  &.color-white { background: var(--rune-white); }
  &.color-red { background: var(--rune-red); }
  &.color-green { background: var(--rune-green); }
  &.color-blue { background: var(--rune-blue); }
}

.pattern-special {
  flex-shrink: 0;
  padding: 1px 5px;
  font-size: 0.6rem;
  font-weight: 700;
  border-radius: 3px;

  &.epic { background: color-mix(in srgb, var(--rune-epic) 25%, transparent); color: var(--rune-epic); }
  &.relic { background: color-mix(in srgb, var(--rune-relic) 25%, transparent); color: var(--rune-relic); }
}

.sub-effect {
  display: flex;
  flex-direction: column;
  font-size: 0.65rem;
  color: #9aa3b5;

  .indented {
    padding-left: 0.6rem;
  }
}

.sub-stack {
  font-size: 0.6rem;
  color: #6f7787;
}

@media (max-width: 1100px) {
  .panel-columns {
    grid-template-columns: 1fr;
  }

  // Apiladas en vertical, las tres listas completas harían la página
  // interminable: se recortan y cada una scrollea por dentro.
  .column-body {
    max-height: 300px;
  }
}

@media (max-width: 600px) {
  .item-row {
    flex-wrap: wrap;
  }

  .sub-slot {
    width: 100%;
  }
}
</style>
