<template>
  <div class="build-stat-sheet">
    <!-- Toggle: Solo Equipo vs Con Stats Base -->
    <div class="stats-toggle-container">
      <div class="toggle-option" :class="{ active: !includeBaseStats }" @click="includeBaseStats = false">
        <i class="pi pi-box"></i>
        <span>{{ t('statsPanel.equipmentOnly') }}</span>
      </div>
      <div class="toggle-option" :class="{ active: includeBaseStats }" @click="includeBaseStats = true">
        <i class="pi pi-user"></i>
        <span>{{ t('statsPanel.withBase') }}</span>
      </div>
    </div>
    
    <!-- Main Stats (HP, AP, MP, WP) -->
    <div class="flex justify-content-between w-full px-2 mb-3">
      <div class="main-stat-box">
        <div class="flex align-items-center my-1">
          <p-image class="stat-icon" src="https://tmktahu.github.io/WakfuAssets/statistics/health_points.png" />
          <span class="ml-1">{{ getStatLabel('HP') }}</span>
        </div>
        <div class="stat-value py-1">
          {{ displayStats.HP }}
          <span v-if="includeBaseStats && baseStats.HP > 0" class="base-stat-indicator">
            (+{{ baseStats.HP }})
          </span>
        </div>
      </div>
      
      <div class="main-stat-box">
        <div class="flex align-items-center my-1">
          <p-image class="stat-icon" src="https://tmktahu.github.io/WakfuAssets/statistics/action_points.png" />
          <span class="ml-1">{{ getStatLabel('AP') }}</span>
        </div>
        <div class="stat-value py-1">
          {{ displayStats.AP }}
          <span v-if="includeBaseStats && baseStats.AP > 0" class="base-stat-indicator">
            (+{{ baseStats.AP }})
          </span>
        </div>
      </div>
      
      <div class="main-stat-box">
        <div class="flex align-items-center my-1">
          <p-image class="stat-icon" src="https://tmktahu.github.io/WakfuAssets/statistics/movement_points.png" />
          <span class="ml-1">{{ getStatLabel('MP') }}</span>
        </div>
        <div class="stat-value py-1">
          {{ displayStats.MP }}
          <span v-if="includeBaseStats && baseStats.MP > 0" class="base-stat-indicator">
            (+{{ baseStats.MP }})
          </span>
        </div>
      </div>
      
      <div class="main-stat-box">
        <div class="flex align-items-center my-1">
          <p-image class="stat-icon" src="https://tmktahu.github.io/WakfuAssets/statistics/wakfu_points.png" />
          <span class="ml-1">{{ getStatLabel('WP') }}</span>
        </div>
        <div class="stat-value py-1">
          {{ displayStats.WP }}
          <span v-if="includeBaseStats && baseStats.WP > 0" class="base-stat-indicator">
            (+{{ baseStats.WP }})
          </span>
        </div>
      </div>
    </div>

    <!-- Elemental Masteries & Resistances -->
    <div class="main-stat-area flex flex-column pb-2">
      <div class="section-header py-1 mb-1">{{ t('stats.elementalMasteries') }}</div>
      <div class="flex pl-1">
        <div class="flex flex-column flex-grow-1" style="max-width: 50%">
          <div class="stat-block pr-2">
            <p-image class="stat-icon element" src="https://tmktahu.github.io/WakfuAssets/statistics/water_coin.png" />
            <span class="ml-1">{{ t('element.Water') }}</span>
            <div class="flex-grow-1" />
            <span>{{ stats.Water_Mastery || 0 }}</span>
          </div>

          <div class="stat-block pr-2">
            <p-image class="stat-icon element" src="https://tmktahu.github.io/WakfuAssets/statistics/air_coin.png" />
            <span class="ml-1">{{ t('element.Air') }}</span>
            <div class="flex-grow-1" />
            <span>{{ stats.Air_Mastery || 0 }}</span>
          </div>
        </div>
        <div class="flex flex-column flex-grow-1" style="max-width: 50%">
          <div class="stat-block pr-2">
            <p-image class="stat-icon element" src="https://tmktahu.github.io/WakfuAssets/statistics/earth_coin.png" />
            <span class="ml-1">{{ t('element.Earth') }}</span>
            <div class="flex-grow-1" />
            <span>{{ stats.Earth_Mastery || 0 }}</span>
          </div>

          <div class="stat-block pr-2">
            <p-image class="stat-icon element" src="https://tmktahu.github.io/WakfuAssets/statistics/fire_coin.png" />
            <span class="ml-1">{{ t('element.Fire') }}</span>
            <div class="flex-grow-1" />
            <span>{{ stats.Fire_Mastery || 0 }}</span>
          </div>
        </div>
      </div>

      <div class="section-header py-1 mb-1">{{ t('stats.elementalResistances') }}</div>
      <div class="flex pl-1">
        <div class="flex flex-column flex-grow-1" style="max-width: 50%">
          <div class="stat-block pr-2">
            <p-image class="stat-icon element" src="https://tmktahu.github.io/WakfuAssets/statistics/water_coin.png" />
            <span class="ml-1">{{ t('element.Water') }}</span>
            <div class="flex-grow-1" />
            <span>{{ calcResistancePercentage(stats.Water_Resistance) }}% ({{ stats.Water_Resistance || 0 }})</span>
          </div>

          <div class="stat-block pr-2">
            <p-image class="stat-icon element" src="https://tmktahu.github.io/WakfuAssets/statistics/air_coin.png" />
            <span class="ml-1">{{ t('element.Air') }}</span>
            <div class="flex-grow-1" />
            <span>{{ calcResistancePercentage(stats.Air_Resistance) }}% ({{ stats.Air_Resistance || 0 }})</span>
          </div>
        </div>
        <div class="flex flex-column flex-grow-1" style="max-width: 50%">
          <div class="stat-block pr-2">
            <p-image class="stat-icon element" src="https://tmktahu.github.io/WakfuAssets/statistics/earth_coin.png" />
            <span class="ml-1">{{ t('element.Earth') }}</span>
            <div class="flex-grow-1" />
            <span>{{ calcResistancePercentage(stats.Earth_Resistance) }}% ({{ stats.Earth_Resistance || 0 }})</span>
          </div>

          <div class="stat-block pr-2">
            <p-image class="stat-icon element" src="https://tmktahu.github.io/WakfuAssets/statistics/fire_coin.png" />
            <span class="ml-1">{{ t('element.Fire') }}</span>
            <div class="flex-grow-1" />
            <span>{{ calcResistancePercentage(stats.Fire_Resistance) }}% ({{ stats.Fire_Resistance || 0 }})</span>
          </div>
        </div>
      </div>

      <!-- Combat Stats -->
      <div class="flex flex-column">
        <div class="section-header py-1 mb-1">{{ t('stats.combat') }}</div>
        <div class="flex pl-1">
          <div class="flex flex-column flex-grow-1" style="max-width: 50%">
            <div class="stat-block pr-2">
              <p-image class="stat-icon" src="https://tmktahu.github.io/WakfuAssets/statistics/damage_inflicted.png" />
              <span class="ml-1">{{ getStatLabel('Damage_Inflicted') }}</span>
              <div class="flex-grow-1" />
              <span>{{ stats.Damage_Inflicted || 0 }}%</span>
            </div>

            <div class="stat-block pr-2">
              <p-image class="stat-icon" src="https://tmktahu.github.io/WakfuAssets/statistics/critical_hit.png" />
              <span class="ml-1">{{ getStatLabel('Critical_Hit') }}</span>
              <div class="flex-grow-1" />
              <span>
                {{ displayStats.Critical_Hit || 0 }}%
                <span v-if="includeBaseStats && baseStats.Critical_Hit > 0" class="base-stat-hint">
                  (+{{ baseStats.Critical_Hit }}%)
                </span>
              </span>
            </div>

            <div class="stat-block pr-2">
              <p-image class="stat-icon" src="https://tmktahu.github.io/WakfuAssets/statistics/initiative.png" />
              <span class="ml-1">{{ getStatLabel('Initiative') }}</span>
              <div class="flex-grow-1" />
              <span>{{ stats.Initiative || 0 }}</span>
            </div>

            <div class="stat-block pr-2">
              <p-image class="stat-icon" src="https://tmktahu.github.io/WakfuAssets/statistics/dodge.png" />
              <span class="ml-1">{{ getStatLabel('Dodge') }}</span>
              <div class="flex-grow-1" />
              <span>{{ stats.Dodge || 0 }}</span>
            </div>

            <div class="stat-block pr-2">
              <p-image class="stat-icon" src="https://tmktahu.github.io/WakfuAssets/statistics/wisdom.png" />
              <span class="ml-1">{{ getStatLabel('Wisdom') }}</span>
              <div class="flex-grow-1" />
              <span>{{ stats.Wisdom || 0 }}</span>
            </div>

            <div class="stat-block pr-2">
              <p-image class="stat-icon" src="https://tmktahu.github.io/WakfuAssets/statistics/control.png" />
              <span class="ml-1">{{ getStatLabel('Control') }}</span>
              <div class="flex-grow-1" />
              <span>{{ stats.Control || 0 }}</span>
            </div>
          </div>
          <div class="flex flex-column flex-grow-1" style="max-width: 50%">
            <div class="stat-block pr-2">
              <p-image class="stat-icon" src="https://tmktahu.github.io/WakfuAssets/statistics/heals_performed.png" />
              <span class="ml-1">{{ getStatLabel('Heals_Performed') }}</span>
              <div class="flex-grow-1" />
              <span>{{ stats.Heals_Performed || 0 }}%</span>
            </div>

            <div class="stat-block pr-2">
              <p-image class="stat-icon" src="https://tmktahu.github.io/WakfuAssets/statistics/block.png" />
              <span class="ml-1">{{ getStatLabel('Block') }}</span>
              <div class="flex-grow-1" />
              <span>{{ stats.Block || 0 }}%</span>
            </div>

            <div class="stat-block pr-2">
              <p-image class="stat-icon" src="https://tmktahu.github.io/WakfuAssets/statistics/range.png" />
              <span class="ml-1">{{ getStatLabel('Range') }}</span>
              <div class="flex-grow-1" />
              <span>{{ stats.Range || 0 }}</span>
            </div>

            <div class="stat-block pr-2">
              <p-image class="stat-icon" src="https://tmktahu.github.io/WakfuAssets/statistics/lock.png" />
              <span class="ml-1">{{ getStatLabel('Lock') }}</span>
              <div class="flex-grow-1" />
              <span>{{ stats.Lock || 0 }}</span>
            </div>

            <div class="stat-block pr-2">
              <p-image class="stat-icon" src="https://tmktahu.github.io/WakfuAssets/statistics/prospecting.png" />
              <span class="ml-1">{{ getStatLabel('Prospecting') }}</span>
              <div class="flex-grow-1" />
              <span>{{ stats.Prospecting || 0 }}</span>
            </div>

            <div class="stat-block pr-2">
              <p-image class="stat-icon" src="https://tmktahu.github.io/WakfuAssets/statistics/force_of_will.png" />
              <span class="ml-1">{{ getStatLabel('Force_Of_Will') }}</span>
              <div class="flex-grow-1" />
              <span>{{ stats.Force_Of_Will || 0 }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Secondary Stats -->
      <div class="flex flex-column">
        <div class="section-header py-1 mb-1">{{ t('stats.secondary') }}</div>
        <div class="flex pl-1">
          <div class="flex flex-column flex-grow-1" style="max-width: 50%">
            <div class="stat-block pr-2">
              <p-image class="stat-icon" src="https://tmktahu.github.io/WakfuAssets/statistics/critical_mastery.png" />
              <span class="ml-1">{{ getStatLabel('Critical_Mastery') }}</span>
              <div class="flex-grow-1" />
              <span>{{ stats.Critical_Mastery || 0 }}</span>
            </div>

            <div class="stat-block pr-2">
              <p-image class="stat-icon" src="https://tmktahu.github.io/WakfuAssets/statistics/rear_mastery.png" />
              <span class="ml-1">{{ getStatLabel('Rear_Mastery') }}</span>
              <div class="flex-grow-1" />
              <span>{{ stats.Rear_Mastery || 0 }}</span>
            </div>

            <div class="stat-block pr-2">
              <p-image class="stat-icon" src="https://tmktahu.github.io/WakfuAssets/statistics/melee_mastery.png" />
              <span class="ml-1">{{ getStatLabel('Melee_Mastery') }}</span>
              <div class="flex-grow-1" />
              <span>{{ stats.Melee_Mastery || 0 }}</span>
            </div>

            <div class="stat-block pr-2">
              <p-image class="stat-icon" src="https://tmktahu.github.io/WakfuAssets/statistics/distance_mastery.png" />
              <span class="ml-1">{{ getStatLabel('Distance_Mastery') }}</span>
              <div class="flex-grow-1" />
              <span>{{ stats.Distance_Mastery || 0 }}</span>
            </div>

            <div class="stat-block pr-2">
              <p-image class="stat-icon" src="https://tmktahu.github.io/WakfuAssets/statistics/healing_mastery.png" />
              <span class="ml-1">{{ getStatLabel('Healing_Mastery') }}</span>
              <div class="flex-grow-1" />
              <span>{{ stats.Healing_Mastery || 0 }}</span>
            </div>

            <div class="stat-block pr-2">
              <p-image class="stat-icon" src="https://tmktahu.github.io/WakfuAssets/statistics/berserk_mastery.png" />
              <span class="ml-1">{{ getStatLabel('Berserk_Mastery') }}</span>
              <div class="flex-grow-1" />
              <span>{{ stats.Berserk_Mastery || 0 }}</span>
            </div>
          </div>
          <div class="flex flex-column flex-grow-1" style="max-width: 50%">
            <div class="stat-block pr-2">
              <p-image class="stat-icon" src="https://tmktahu.github.io/WakfuAssets/statistics/critical_resistance.png" />
              <span class="ml-1">{{ getStatLabel('Critical_Resistance') }}</span>
              <div class="flex-grow-1" />
              <span>{{ stats.Critical_Resistance || 0 }}</span>
            </div>

            <div class="stat-block pr-2">
              <p-image class="stat-icon" src="https://tmktahu.github.io/WakfuAssets/statistics/rear_resistance.png" />
              <span class="ml-1">{{ getStatLabel('Rear_Resistance') }}</span>
              <div class="flex-grow-1" />
              <span>{{ stats.Rear_Resistance || 0 }}</span>
            </div>

            <div class="stat-block pr-2">
              <p-image class="stat-icon" src="https://tmktahu.github.io/WakfuAssets/statistics/armor_given.png" />
              <span class="ml-1">{{ getStatLabel('Armor_Given') }}</span>
              <div class="flex-grow-1" />
              <span>{{ stats.Armor_Given || 0 }}%</span>
            </div>

            <div class="stat-block pr-2">
              <p-image class="stat-icon" src="https://tmktahu.github.io/WakfuAssets/statistics/armor_received.png" />
              <span class="ml-1">{{ getStatLabel('Armor_Received') }}</span>
              <div class="flex-grow-1" />
              <span>{{ stats.Armor_Received || 0 }}%</span>
            </div>

            <div class="stat-block pr-2">
              <p-image class="stat-icon" src="https://tmktahu.github.io/WakfuAssets/statistics/indirect_damage.png" />
              <span class="ml-1">{{ getStatLabel('Indirect_Damage') }}</span>
              <div class="flex-grow-1" />
              <span>{{ stats.Indirect_Damage || 0 }}%</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useI18n } from '../composables/useI18n'
import { getStatLabel } from '../composables/useStats'

const { t } = useI18n()

const props = defineProps({
  stats: {
    type: Object,
    required: true
  },
  characterLevel: {
    type: Number,
    default: 1
  }
})

// Toggle para mostrar stats base o no
const includeBaseStats = ref(false)

// Calcular stats base del personaje según nivel
const baseStats = computed(() => {
  const level = props.characterLevel
  return {
    HP: 60 + (level - 1) * 10,
    AP: 6,
    MP: 3,
    WP: 6,
    Critical_Hit: 3
  }
})

// Stats a mostrar (equipo + base si está activado)
const displayStats = computed(() => {
  if (!includeBaseStats.value) {
    return props.stats
  }
  
  // Combinar stats del equipo con stats base
  const combined = { ...props.stats }
  Object.keys(baseStats.value).forEach(stat => {
    combined[stat] = (combined[stat] || 0) + baseStats.value[stat]
  })
  
  return combined
})

// Tabla de conversión Flat Resistance -> % Resistance (Wakfu oficial)
// Basado en la tabla de conversión del juego (update 1.68+, cap 90%)
const resistanceTable = [
  { percent: 0, min: 0, max: 4 },
  { percent: 1, min: 5, max: 9 },
  { percent: 2, min: 10, max: 13 },
  { percent: 3, min: 14, max: 18 },
  { percent: 4, min: 19, max: 22 },
  { percent: 5, min: 23, max: 27 },
  { percent: 6, min: 28, max: 32 },
  { percent: 7, min: 33, max: 37 },
  { percent: 8, min: 38, max: 42 },
  { percent: 9, min: 43, max: 47 },
  { percent: 10, min: 48, max: 52 },
  { percent: 11, min: 53, max: 57 },
  { percent: 12, min: 58, max: 62 },
  { percent: 13, min: 63, max: 67 },
  { percent: 14, min: 68, max: 72 },
  { percent: 15, min: 73, max: 78 },
  { percent: 16, min: 79, max: 83 },
  { percent: 17, min: 84, max: 88 },
  { percent: 18, min: 89, max: 94 },
  { percent: 19, min: 95, max: 100 },
  { percent: 20, min: 101, max: 105 },
  { percent: 21, min: 106, max: 111 },
  { percent: 22, min: 112, max: 117 },
  { percent: 23, min: 118, max: 122 },
  { percent: 24, min: 123, max: 128 },
  { percent: 25, min: 129, max: 134 },
  { percent: 26, min: 135, max: 141 },
  { percent: 27, min: 142, max: 147 },
  { percent: 28, min: 148, max: 153 },
  { percent: 29, min: 154, max: 159 },
  { percent: 30, min: 160, max: 166 },
  { percent: 31, min: 167, max: 172 },
  { percent: 32, min: 173, max: 179 },
  { percent: 33, min: 180, max: 186 },
  { percent: 34, min: 187, max: 193 },
  { percent: 35, min: 194, max: 200 },
  { percent: 36, min: 201, max: 207 },
  { percent: 37, min: 208, max: 214 },
  { percent: 38, min: 215, max: 221 },
  { percent: 39, min: 222, max: 228 },
  { percent: 40, min: 229, max: 236 },
  { percent: 41, min: 237, max: 244 },
  { percent: 42, min: 245, max: 251 },
  { percent: 43, min: 252, max: 259 },
  { percent: 44, min: 260, max: 267 },
  { percent: 45, min: 268, max: 276 },
  { percent: 46, min: 277, max: 284 },
  { percent: 47, min: 285, max: 293 },
  { percent: 48, min: 294, max: 301 },
  { percent: 49, min: 302, max: 310 },
  { percent: 50, min: 311, max: 319 },
  { percent: 51, min: 320, max: 328 },
  { percent: 52, min: 329, max: 338 },
  { percent: 53, min: 339, max: 347 },
  { percent: 54, min: 348, max: 357 },
  { percent: 55, min: 358, max: 367 },
  { percent: 56, min: 368, max: 378 },
  { percent: 57, min: 379, max: 388 },
  { percent: 58, min: 389, max: 399 },
  { percent: 59, min: 400, max: 410 },
  { percent: 60, min: 411, max: 421 },
  { percent: 61, min: 422, max: 433 },
  { percent: 62, min: 434, max: 445 },
  { percent: 63, min: 446, max: 457 },
  { percent: 64, min: 458, max: 470 },
  { percent: 65, min: 471, max: 483 },
  { percent: 66, min: 484, max: 496 },
  { percent: 67, min: 497, max: 510 },
  { percent: 68, min: 511, max: 524 },
  { percent: 69, min: 525, max: 539 },
  { percent: 70, min: 540, max: 554 },
  { percent: 71, min: 555, max: 570 },
  { percent: 72, min: 571, max: 586 },
  { percent: 73, min: 587, max: 603 },
  { percent: 74, min: 604, max: 621 },
  { percent: 75, min: 622, max: 639 },
  { percent: 76, min: 640, max: 658 },
  { percent: 77, min: 659, max: 678 },
  { percent: 78, min: 679, max: 699 },
  { percent: 79, min: 700, max: 721 },
  { percent: 80, min: 722, max: 744 },
  { percent: 81, min: 745, max: 768 },
  { percent: 82, min: 769, max: 794 },
  { percent: 83, min: 795, max: 821 },
  { percent: 84, min: 822, max: 850 },
  { percent: 85, min: 851, max: 881 },
  { percent: 86, min: 882, max: 914 },
  { percent: 87, min: 915, max: 950 },
  { percent: 88, min: 951, max: 989 },
  { percent: 89, min: 990, max: 1031 },
  { percent: 90, min: 1032, max: Infinity }, // Cap at 90% (update 1.68)
]

const calcResistancePercentage = (resistance) => {
  if (!resistance || resistance <= 0) return 0
  
  // Buscar en la tabla
  const entry = resistanceTable.find(
    row => resistance >= row.min && resistance <= row.max
  )
  
  return entry ? entry.percent : 90 // Cap at 90%
}
</script>

<style lang="scss" scoped>
.build-stat-sheet {
  width: 100%;
  padding: 0;
  background: transparent;
}

.stats-toggle-container {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
  padding: 0.5rem;
  background: rgba(26, 35, 50, 0.6);
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.toggle-option {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
  color: #a0a0a0;
  font-size: 0.85rem;
  font-weight: 500;
  
  i {
    font-size: 1rem;
  }
  
  &:hover {
    background: rgba(92, 107, 192, 0.2);
    border-color: rgba(92, 107, 192, 0.3);
    color: #e0e0e0;
  }
  
  &.active {
    background: rgba(92, 107, 192, 0.4);
    border-color: rgba(92, 107, 192, 0.6);
    color: #fff;
    font-weight: 600;
    box-shadow: 0 0 10px rgba(92, 107, 192, 0.3);
  }
}

.base-stat-indicator {
  display: block;
  font-size: 0.65rem;
  color: #9fa8da;
  font-weight: 500;
  margin-top: 0.125rem;
}

.base-stat-hint {
  font-size: 0.7rem;
  color: #9fa8da;
  margin-left: 0.25rem;
  font-weight: 500;
}

.main-stat-box {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
  width: 60px;
  background-color: rgba(26, 35, 50, 0.8);
  border-radius: 6px;
  border: 1px solid rgba(255, 255, 255, 0.2);

  .flex {
    font-size: 0.7rem;
  }

  .stat-value {
    border-top: 1px solid rgba(255, 255, 255, 0.2);
    width: 100%;
    text-align: center;
    font-weight: 600;
    color: #fff;
    font-size: 0.9rem;
  }
}

.main-stat-area {
  background-color: rgba(0, 0, 0, 0.3);
  border-radius: 6px;
}

.section-header {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  background-color: rgba(92, 107, 192, 0.2);
  color: #9fa8da;
  font-weight: 600;
  font-size: 0.75rem;
  padding: 0.25rem;
}

.stat-block {
  display: flex;
  align-items: center;
  padding-left: 4px;
  padding-top: 2px;
  padding-bottom: 2px;
  font-size: 0.7rem;
  color: #e0e0e0;

  span {
    white-space: nowrap;
  }

  :deep(.p-image) {
    display: flex;
    align-items: center;
    background: rgba(255, 255, 255, 0.8);
    border-radius: 3px;
    height: 16px;
  }
}

:deep(.stat-icon) {
  width: 16px;
  height: 16px;
  display: flex;
  justify-content: center;

  img {
    width: 16px;
  }
}
</style>

