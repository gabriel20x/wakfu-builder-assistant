<template>
  <div class="my-characters">
    <!-- Sidebar: lista de personajes -->
    <div class="characters-sidebar">
      <div class="sidebar-header">
        <h2>👥 {{ t('characters.title') }}</h2>
        <p-button
          icon="pi pi-plus"
          :label="t('characters.new')"
          size="small"
          @click="addCharacter"
        />
      </div>

      <div v-if="!characters.length" class="empty-list">
        {{ t('characters.empty') }}
      </div>

      <div
        v-for="character in characters"
        :key="character.id"
        :class="['character-card', { active: character.id === selectedId }]"
        @click="selectedId = character.id"
      >
        <img
          v-if="character.classId"
          :src="classIconUrl(character.classId)"
          class="class-icon"
          :alt="character.classId"
        />
        <div v-else class="class-icon placeholder">❓</div>
        <div class="character-info">
          <span class="character-name">{{ character.name }}</span>
          <span class="character-meta">
            {{ getClassName(character.classId) }} · {{ t('characters.level') }} {{ character.level }}
          </span>
        </div>
        <p-button
          icon="pi pi-trash"
          text
          severity="danger"
          class="delete-btn"
          @click.stop="removeCharacter(character)"
        />
      </div>
    </div>

    <!-- Editor -->
    <div v-if="selected" class="character-editor">
      <!-- Datos básicos -->
      <div class="editor-panel basics-panel">
        <div class="basics-grid">
          <div class="field">
            <label>{{ t('characters.name') }}</label>
            <p-inputText v-model="selected.name" @change="persistSelected" />
          </div>
          <div class="field">
            <label>{{ t('characters.class') }}</label>
            <p-dropdown
              v-model="selected.classId"
              :options="classes"
              option-label="name"
              option-value="id"
              :placeholder="t('quickStart.selectClass')"
              show-clear
              @change="persistSelected"
            >
              <template #value="slotProps">
                <div v-if="slotProps.value" class="dropdown-class-item">
                  <img :src="classIconUrl(slotProps.value)" class="class-icon-small" />
                  <span>{{ getClassName(slotProps.value) }}</span>
                </div>
                <span v-else>{{ slotProps.placeholder }}</span>
              </template>
              <template #option="slotProps">
                <div class="dropdown-class-item">
                  <img :src="classIconUrl(slotProps.option.id)" class="class-icon-small" />
                  <span>{{ slotProps.option.name }}</span>
                </div>
              </template>
            </p-dropdown>
          </div>
          <div class="field">
            <label>{{ t('characters.level') }}</label>
            <p-inputNumber
              v-model="selected.level"
              :min="1"
              :max="MAX_CHARACTER_LEVEL"
              show-buttons
              @update:model-value="persistSelected"
            />
          </div>
        </div>

        <!-- Código de características -->
        <div class="code-section">
          <label>{{ t('characters.code') }}</label>
          <div class="code-input-row">
            <p-inputText
              v-model="codeInput"
              :placeholder="t('characters.codePlaceholder')"
              class="code-input"
              @keyup.enter="importCode"
            />
            <p-button
              icon="pi pi-download"
              :label="t('characters.import')"
              @click="importCode"
            />
          </div>
          <p class="help-text">{{ t('characters.codeHelp') }}</p>

          <div v-if="currentCode" class="code-export-row">
            <code class="current-code">{{ currentCode }}</code>
            <p-button
              icon="pi pi-copy"
              text
              :title="t('characters.copyCode')"
              @click="copyCode"
            />
          </div>
        </div>
      </div>

      <!-- Secciones de características -->
      <div class="sections-grid">
        <div
          v-for="section in SECTIONS"
          :key="section"
          class="editor-panel section-panel"
        >
          <div class="section-header">
            <h3>{{ t(`charac.section.${section}`) }}</h3>
            <span :class="['remaining-badge', { overspent: validation.sections[section].overspent }]">
              {{ t('characters.remaining') }}: {{ validation.sections[section].remaining }}
            </span>
          </div>

          <div
            v-for="aptitude in getAptitudesBySection(section)"
            :key="aptitude.id"
            class="aptitude-row"
          >
            <span class="aptitude-icon">{{ aptitude.emoji }}</span>
            <span class="aptitude-label">{{ t(`charac.${aptitude.key}`) }}</span>
            <span v-if="aptitude.cap" class="aptitude-cap">
              {{ pointsFor(aptitude) }}/{{ aptitude.cap }}
            </span>
            <div class="aptitude-controls">
              <p-button
                icon="pi pi-minus"
                text
                rounded
                size="small"
                :disabled="pointsFor(aptitude) <= 0"
                @click="adjustPoints(aptitude, -1)"
              />
              <span :class="['aptitude-value', { positive: pointsFor(aptitude) > 0 }]">
                {{ pointsFor(aptitude) }}
              </span>
              <p-button
                icon="pi pi-plus"
                text
                rounded
                size="small"
                :disabled="!canAddPoint(aptitude)"
                @click="adjustPoints(aptitude, 1)"
              />
            </div>
          </div>
        </div>

        <!-- Resumen de bonos -->
        <div class="editor-panel section-panel bonus-panel">
          <div class="section-header">
            <h3>📊 {{ t('characters.bonusTitle') }}</h3>
          </div>
          <div v-if="!bonusEntries.length" class="empty-bonus">
            {{ t('characters.noBonus') }}
          </div>
          <div v-for="[statKey, value] in bonusEntries" :key="statKey" class="bonus-row">
            <span class="bonus-label">{{ bonusLabel(statKey) }}</span>
            <span class="bonus-value">+{{ value }}{{ bonusSuffix(statKey) }}</span>
          </div>
        </div>

        <!-- Builds guardadas de este personaje -->
        <div class="editor-panel section-panel builds-panel">
          <div class="section-header">
            <h3>🗂️ {{ t('characters.buildsTitle') }}</h3>
            <span class="builds-count">{{ characterBuilds.length }}</span>
          </div>

          <div v-if="!characterBuilds.length" class="empty-bonus">
            {{ t('characters.noBuilds') }}
          </div>

          <div
            v-for="build in characterBuilds"
            :key="build.id"
            class="build-row"
            @click="emit('open-build', build)"
          >
            <div class="build-info">
              <span class="build-name">{{ build.name }}</span>
              <span class="build-meta">
                {{ t('characters.level') }} {{ build.config?.level_max || '?' }} ·
                {{ formatDate(build.saved_at) }}
              </span>
            </div>
            <i class="pi pi-arrow-right" />
          </div>
        </div>
      </div>

      <!-- Acciones -->
      <div class="editor-actions">
        <p-button
          icon="pi pi-refresh"
          :label="t('characters.reset')"
          severity="secondary"
          outlined
          @click="resetAllocation"
        />
        <p-button
          icon="pi pi-arrow-right"
          :label="t('characters.useInBuilder')"
          @click="useInBuilder"
        />
      </div>
    </div>

    <div v-else class="editor-empty">
      <span class="empty-emoji">🧙</span>
      <p>{{ t('characters.selectPrompt') }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useToast } from 'primevue/usetoast'
import { useI18n } from '../composables/useI18n'
import { useCharacters } from '../composables/useCharacters'
import { useBuildPersistence } from '../composables/useBuildPersistence'
import { getStatLabel, getStatSuffix } from '../composables/useStats'
import {
  SECTIONS,
  MAX_CHARACTER_LEVEL,
  getAptitudesBySection,
  parseCharacteristicsCode,
  serializeCharacteristicsCode,
  validateAllocation,
  allocationToBonusStats
} from '../lib/characteristics'

const emit = defineEmits(['use-in-builder', 'open-build'])

const { t } = useI18n()
const toast = useToast()
const { getBuildsForCharacter } = useBuildPersistence()
const { characters, createCharacter, updateCharacter, deleteCharacter } = useCharacters()

const selectedId = ref(characters.value[0]?.id || null)
const codeInput = ref('')
const classes = ref([])

const selected = computed(() =>
  characters.value.find(c => c.id === selectedId.value) || null
)

const validation = computed(() =>
  validateAllocation(selected.value?.allocation || {}, selected.value?.level || 1)
)

const currentCode = computed(() =>
  selected.value ? serializeCharacteristicsCode(selected.value.allocation) : ''
)

const bonusEntries = computed(() =>
  Object.entries(allocationToBonusStats(selected.value?.allocation || {}))
)

// Builds guardadas asociadas a este personaje, más recientes primero
const characterBuilds = computed(() => {
  if (!selected.value) return []
  return [...getBuildsForCharacter(selected.value.id)].sort(
    (a, b) => new Date(b.saved_at) - new Date(a.saved_at)
  )
})

const formatDate = (iso) => {
  if (!iso) return ''
  return new Date(iso).toLocaleDateString()
}

// Claves especiales que no son stats de equipo — usan etiquetas propias
const SPECIAL_BONUS_LABELS = {
  HP_Percent: 'charac.percentHp',
  Armor_Percent: 'charac.armorHp',
  Barrier: 'charac.barrier'
}

const PERCENT_BONUS_KEYS = ['HP_Percent', 'Armor_Percent']

onMounted(async () => {
  try {
    const response = await fetch('/class-presets.json')
    const data = await response.json()
    classes.value = data.classes.map(cls => ({ id: cls.id, name: cls.name }))
  } catch (error) {
    console.error('Error loading classes:', error)
  }
})

const classIconUrl = (classId) =>
  `https://tmktahu.github.io/WakfuAssets/classes/${classId}.png`

const getClassName = (classId) =>
  classes.value.find(c => c.id === classId)?.name || t('characters.noClass')

const pointsFor = (aptitude) => selected.value?.allocation[aptitude.id] || 0

const canAddPoint = (aptitude) => {
  if (!selected.value) return false
  const current = pointsFor(aptitude)
  if (aptitude.cap !== null && current >= aptitude.cap) return false
  return validation.value.sections[aptitude.section].remaining > 0
}

const persistSelected = () => {
  if (!selected.value) return
  updateCharacter(selected.value.id, {})
}

const adjustPoints = (aptitude, delta) => {
  if (!selected.value) return
  const current = pointsFor(aptitude)
  const next = Math.max(0, current + delta)
  const allocation = { ...selected.value.allocation }
  if (next === 0) {
    delete allocation[aptitude.id]
  } else {
    allocation[aptitude.id] = next
  }
  updateCharacter(selected.value.id, { allocation })
}

const addCharacter = () => {
  const character = createCharacter({
    name: `${t('characters.defaultName')} ${characters.value.length + 1}`
  })
  selectedId.value = character.id
}

const removeCharacter = (character) => {
  if (!window.confirm(t('characters.deleteConfirm'))) return
  deleteCharacter(character.id)
  if (selectedId.value === character.id) {
    selectedId.value = characters.value[0]?.id || null
  }
}

// Nivel mínimo que cubre la asignación (para autoajustar al importar)
const minimumLevelFor = (allocation) => {
  for (let level = 1; level <= MAX_CHARACTER_LEVEL; level++) {
    const check = validateAllocation(allocation, level)
    if (!Object.values(check.sections).some(s => s.overspent)) {
      return level
    }
  }
  return MAX_CHARACTER_LEVEL
}

const importCode = () => {
  if (!selected.value) return
  const { allocation, errors } = parseCharacteristicsCode(codeInput.value)

  if (errors.length > 0) {
    toast.add({
      severity: 'error',
      summary: t('toast.error'),
      detail: t('characters.codeInvalid'),
      life: 4000
    })
    return
  }

  const changes = { allocation }
  const minLevel = minimumLevelFor(allocation)
  if (selected.value.level < minLevel) {
    changes.level = minLevel
    toast.add({
      severity: 'info',
      summary: t('characters.levelAdjusted'),
      detail: t('characters.levelAdjustedDetail', { level: minLevel }),
      life: 5000
    })
  }

  updateCharacter(selected.value.id, changes)
  codeInput.value = ''
  toast.add({
    severity: 'success',
    summary: t('toast.success'),
    detail: t('characters.codeImported'),
    life: 3000
  })
}

const copyCode = async () => {
  try {
    await navigator.clipboard.writeText(currentCode.value)
    toast.add({
      severity: 'success',
      summary: t('characters.codeCopied'),
      life: 2000
    })
  } catch (error) {
    console.error('Clipboard error:', error)
  }
}

const resetAllocation = () => {
  if (!selected.value) return
  if (!window.confirm(t('characters.resetConfirm'))) return
  updateCharacter(selected.value.id, { allocation: {} })
}

const bonusLabel = (statKey) => {
  if (SPECIAL_BONUS_LABELS[statKey]) {
    return t(SPECIAL_BONUS_LABELS[statKey])
  }
  return getStatLabel(statKey)
}

const bonusSuffix = (statKey) => {
  if (PERCENT_BONUS_KEYS.includes(statKey)) return '%'
  return getStatSuffix(statKey)
}

const useInBuilder = () => {
  if (!selected.value) return
  emit('use-in-builder', JSON.parse(JSON.stringify(selected.value)))
}
</script>

<style lang="scss" scoped>
.my-characters {
  display: grid;
  grid-template-columns: 300px 1fr;
  gap: 1.5rem;

  @media (max-width: 900px) {
    grid-template-columns: 1fr;
  }
}

.characters-sidebar {
  .sidebar-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;

    h2 {
      margin: 0;
      font-size: 1.3rem;
    }
  }

  .empty-list {
    color: #a0a0a0;
    font-size: 0.9rem;
    padding: 1rem;
    background: rgba(255, 255, 255, 0.03);
    border-radius: 8px;
  }
}

.character-card {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem;
  margin-bottom: 0.5rem;
  background: rgba(255, 255, 255, 0.05);
  border: 2px solid transparent;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;

  &:hover {
    background: rgba(255, 255, 255, 0.1);
  }

  &.active {
    border-color: #667eea;
    background: rgba(102, 126, 234, 0.15);
  }

  .class-icon {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    object-fit: cover;

    &.placeholder {
      display: flex;
      align-items: center;
      justify-content: center;
      background: rgba(255, 255, 255, 0.08);
      font-size: 1.2rem;
    }
  }

  .character-info {
    display: flex;
    flex-direction: column;
    flex: 1;
    min-width: 0;

    .character-name {
      font-weight: 600;
      color: #e0e0e0;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    .character-meta {
      font-size: 0.8rem;
      color: #a0a0a0;
    }
  }

  .delete-btn {
    opacity: 0;
    transition: opacity 0.2s;
  }

  &:hover .delete-btn {
    opacity: 1;
  }
}

.editor-panel {
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 10px;
  padding: 1.25rem;
}

.basics-panel {
  margin-bottom: 1.5rem;

  .basics-grid {
    display: grid;
    grid-template-columns: 2fr 2fr 1fr;
    gap: 1rem;

    @media (max-width: 700px) {
      grid-template-columns: 1fr;
    }
  }

  .field {
    display: flex;
    flex-direction: column;
    gap: 0.4rem;

    label {
      font-size: 0.85rem;
      font-weight: 600;
      color: #a0b4d0;
    }
  }
}

.dropdown-class-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;

  .class-icon-small {
    width: 24px;
    height: 24px;
    border-radius: 50%;
  }
}

.code-section {
  margin-top: 1.25rem;

  label {
    font-size: 0.85rem;
    font-weight: 600;
    color: #a0b4d0;
    display: block;
    margin-bottom: 0.4rem;
  }

  .code-input-row {
    display: flex;
    gap: 0.5rem;

    .code-input {
      flex: 1;
      font-family: monospace;
    }
  }

  .help-text {
    font-size: 0.8rem;
    color: #808a9a;
    margin: 0.4rem 0 0 0;
  }

  .code-export-row {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-top: 0.75rem;

    .current-code {
      flex: 1;
      padding: 0.5rem 0.75rem;
      background: rgba(0, 0, 0, 0.3);
      border-radius: 6px;
      font-size: 0.8rem;
      color: #8fd18f;
      word-break: break-all;
    }
  }
}

.sections-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  gap: 1rem;
}

.section-panel {
  .section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.75rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);

    h3 {
      margin: 0;
      font-size: 1.05rem;
      color: #e0e0e0;
    }

    .remaining-badge {
      font-size: 0.8rem;
      font-weight: 700;
      padding: 0.2rem 0.6rem;
      border-radius: 10px;
      background: rgba(102, 126, 234, 0.2);
      color: #9fb0f0;

      &.overspent {
        background: rgba(244, 67, 54, 0.25);
        color: #ff8a80;
      }
    }
  }
}

.aptitude-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.3rem 0.25rem;
  border-radius: 6px;

  &:hover {
    background: rgba(255, 255, 255, 0.04);
  }

  .aptitude-icon {
    width: 1.4rem;
    text-align: center;
  }

  .aptitude-label {
    flex: 1;
    font-size: 0.85rem;
    color: #c8d2e0;
  }

  .aptitude-cap {
    font-size: 0.7rem;
    color: #808a9a;
  }

  .aptitude-controls {
    display: flex;
    align-items: center;
    gap: 0.15rem;

    .aptitude-value {
      min-width: 2rem;
      text-align: center;
      font-weight: 700;
      color: #6a7484;

      &.positive {
        color: #8fd18f;
      }
    }
  }
}

.bonus-panel {
  .empty-bonus {
    color: #808a9a;
    font-size: 0.85rem;
  }

  .bonus-row {
    display: flex;
    justify-content: space-between;
    padding: 0.25rem 0.25rem;
    font-size: 0.85rem;

    .bonus-label {
      color: #c8d2e0;
    }

    .bonus-value {
      font-weight: 700;
      color: #8fd18f;
    }
  }
}

.builds-panel {
  .empty-bonus {
    color: #808a9a;
    font-size: 0.85rem;
  }

  .builds-count {
    padding: 0.1rem 0.5rem;
    font-size: 0.75rem;
    font-weight: 700;
    color: var(--primary-60);
    background: rgba(92, 107, 192, 0.25);
    border-radius: 10px;
  }
}

.build-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem;
  margin-bottom: 0.35rem;
  background: rgba(0, 0, 0, 0.25);
  border: 1px solid transparent;
  border-radius: 6px;
  cursor: pointer;
  transition: border-color 0.15s, background 0.15s;

  &:hover {
    background: rgba(92, 107, 192, 0.2);
    border-color: var(--primary-40);
  }

  i {
    color: var(--primary-60);
    font-size: 0.8rem;
  }
}

.build-info {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
}

.build-name {
  font-size: 0.85rem;
  font-weight: 600;
  color: #e0e0e0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.build-meta {
  font-size: 0.72rem;
  color: #808a9a;
}

.editor-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  margin-top: 1.5rem;
}

.editor-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem;
  color: #808a9a;

  .empty-emoji {
    font-size: 3rem;
    margin-bottom: 1rem;
  }
}
</style>
