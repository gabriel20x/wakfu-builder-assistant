<template>
  <div class="build-stat-sheet">
    <!-- Toggle: Solo Equipo vs Con Stats Base -->
    <div class="stats-toggle-container">
      <div class="toggle-option" :class="{ active: !includeBaseStats }" @click="includeBaseStats = false">
        <i class="pi pi-box"></i>
        <span>Solo Equipo</span>
      </div>
      <div class="toggle-option" :class="{ active: includeBaseStats }" @click="includeBaseStats = true">
        <i class="pi pi-user"></i>
        <span>Con Stats Base</span>
      </div>
    </div>
    
    <!-- Main Stats (HP, AP, MP, WP) -->
    <div class="flex justify-content-between w-full px-2 mb-3">
      <div class="main-stat-box">
        <div class="flex align-items-center my-1">
          <p-image class="stat-icon" src="https://tmktahu.github.io/WakfuAssets/statistics/health_points.png" />
          <span class="ml-1">PdV</span>
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
          <span class="ml-1">PA</span>
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
          <span class="ml-1">PM</span>
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
          <span class="ml-1">PW</span>
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
      <div class="section-header py-1 mb-1">Dominios Elementales</div>
      <div class="flex pl-1">
        <div class="flex flex-column flex-grow-1" style="max-width: 50%">
          <div class="stat-block pr-2">
            <p-image class="stat-icon element" src="https://tmktahu.github.io/WakfuAssets/statistics/water_coin.png" />
            <span class="ml-1">Agua</span>
            <div class="flex-grow-1" />
            <span>{{ stats.Water_Mastery || 0 }}</span>
          </div>

          <div class="stat-block pr-2">
            <p-image class="stat-icon element" src="https://tmktahu.github.io/WakfuAssets/statistics/air_coin.png" />
            <span class="ml-1">Aire</span>
            <div class="flex-grow-1" />
            <span>{{ stats.Air_Mastery || 0 }}</span>
          </div>
        </div>
        <div class="flex flex-column flex-grow-1" style="max-width: 50%">
          <div class="stat-block pr-2">
            <p-image class="stat-icon element" src="https://tmktahu.github.io/WakfuAssets/statistics/earth_coin.png" />
            <span class="ml-1">Tierra</span>
            <div class="flex-grow-1" />
            <span>{{ stats.Earth_Mastery || 0 }}</span>
          </div>

          <div class="stat-block pr-2">
            <p-image class="stat-icon element" src="https://tmktahu.github.io/WakfuAssets/statistics/fire_coin.png" />
            <span class="ml-1">Fuego</span>
            <div class="flex-grow-1" />
            <span>{{ stats.Fire_Mastery || 0 }}</span>
          </div>
        </div>
      </div>

      <div class="section-header py-1 mb-1">Resistencias Elementales</div>
      <div class="flex pl-1">
        <div class="flex flex-column flex-grow-1" style="max-width: 50%">
          <div class="stat-block pr-2">
            <p-image class="stat-icon element" src="https://tmktahu.github.io/WakfuAssets/statistics/water_coin.png" />
            <span class="ml-1">Agua</span>
            <div class="flex-grow-1" />
            <span>{{ calcResistancePercentage(stats.Water_Resistance) }}% ({{ stats.Water_Resistance || 0 }})</span>
          </div>

          <div class="stat-block pr-2">
            <p-image class="stat-icon element" src="https://tmktahu.github.io/WakfuAssets/statistics/air_coin.png" />
            <span class="ml-1">Aire</span>
            <div class="flex-grow-1" />
            <span>{{ calcResistancePercentage(stats.Air_Resistance) }}% ({{ stats.Air_Resistance || 0 }})</span>
          </div>
        </div>
        <div class="flex flex-column flex-grow-1" style="max-width: 50%">
          <div class="stat-block pr-2">
            <p-image class="stat-icon element" src="https://tmktahu.github.io/WakfuAssets/statistics/earth_coin.png" />
            <span class="ml-1">Tierra</span>
            <div class="flex-grow-1" />
            <span>{{ calcResistancePercentage(stats.Earth_Resistance) }}% ({{ stats.Earth_Resistance || 0 }})</span>
          </div>

          <div class="stat-block pr-2">
            <p-image class="stat-icon element" src="https://tmktahu.github.io/WakfuAssets/statistics/fire_coin.png" />
            <span class="ml-1">Fuego</span>
            <div class="flex-grow-1" />
            <span>{{ calcResistancePercentage(stats.Fire_Resistance) }}% ({{ stats.Fire_Resistance || 0 }})</span>
          </div>
        </div>
      </div>

      <!-- Combat Stats -->
      <div class="flex flex-column">
        <div class="section-header py-1 mb-1">Combate</div>
        <div class="flex pl-1">
          <div class="flex flex-column flex-grow-1" style="max-width: 50%">
            <div class="stat-block pr-2">
              <p-image class="stat-icon" src="https://tmktahu.github.io/WakfuAssets/statistics/damage_inflicted.png" />
              <span class="ml-1">Daños finales</span>
              <div class="flex-grow-1" />
              <span>{{ stats.Damage_Inflicted || 0 }}%</span>
            </div>

            <div class="stat-block pr-2">
              <p-image class="stat-icon" src="https://tmktahu.github.io/WakfuAssets/statistics/critical_hit.png" />
              <span class="ml-1">Golpe crítico</span>
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
              <span class="ml-1">Iniciativa</span>
              <div class="flex-grow-1" />
              <span>{{ stats.Initiative || 0 }}</span>
            </div>

            <div class="stat-block pr-2">
              <p-image class="stat-icon" src="https://tmktahu.github.io/WakfuAssets/statistics/dodge.png" />
              <span class="ml-1">Esquiva</span>
              <div class="flex-grow-1" />
              <span>{{ stats.Dodge || 0 }}</span>
            </div>

            <div class="stat-block pr-2">
              <p-image class="stat-icon" src="https://tmktahu.github.io/WakfuAssets/statistics/wisdom.png" />
              <span class="ml-1">Sabiduría</span>
              <div class="flex-grow-1" />
              <span>{{ stats.Wisdom || 0 }}</span>
            </div>

            <div class="stat-block pr-2">
              <p-image class="stat-icon" src="https://tmktahu.github.io/WakfuAssets/statistics/control.png" />
              <span class="ml-1">Control</span>
              <div class="flex-grow-1" />
              <span>{{ stats.Control || 0 }}</span>
            </div>
          </div>
          <div class="flex flex-column flex-grow-1" style="max-width: 50%">
            <div class="stat-block pr-2">
              <p-image class="stat-icon" src="https://tmktahu.github.io/WakfuAssets/statistics/heals_performed.png" />
              <span class="ml-1">Curas finales</span>
              <div class="flex-grow-1" />
              <span>{{ stats.Heals_Performed || 0 }}%</span>
            </div>

            <div class="stat-block pr-2">
              <p-image class="stat-icon" src="https://tmktahu.github.io/WakfuAssets/statistics/block.png" />
              <span class="ml-1">Anticipación</span>
              <div class="flex-grow-1" />
              <span>{{ stats.Block || 0 }}%</span>
            </div>

            <div class="stat-block pr-2">
              <p-image class="stat-icon" src="https://tmktahu.github.io/WakfuAssets/statistics/range.png" />
              <span class="ml-1">Alcance</span>
              <div class="flex-grow-1" />
              <span>{{ stats.Range || 0 }}</span>
            </div>

            <div class="stat-block pr-2">
              <p-image class="stat-icon" src="https://tmktahu.github.io/WakfuAssets/statistics/lock.png" />
              <span class="ml-1">Placaje</span>
              <div class="flex-grow-1" />
              <span>{{ stats.Lock || 0 }}</span>
            </div>

            <div class="stat-block pr-2">
              <p-image class="stat-icon" src="https://tmktahu.github.io/WakfuAssets/statistics/prospecting.png" />
              <span class="ml-1">Prospección</span>
              <div class="flex-grow-1" />
              <span>{{ stats.Prospecting || 0 }}</span>
            </div>

            <div class="stat-block pr-2">
              <p-image class="stat-icon" src="https://tmktahu.github.io/WakfuAssets/statistics/force_of_will.png" />
              <span class="ml-1">Voluntad</span>
              <div class="flex-grow-1" />
              <span>{{ stats.Force_Of_Will || 0 }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Secondary Stats -->
      <div class="flex flex-column">
        <div class="section-header py-1 mb-1">Secundarias</div>
        <div class="flex pl-1">
          <div class="flex flex-column flex-grow-1" style="max-width: 50%">
            <div class="stat-block pr-2">
              <p-image class="stat-icon" src="https://tmktahu.github.io/WakfuAssets/statistics/critical_mastery.png" />
              <span class="ml-1">Dominio crítico</span>
              <div class="flex-grow-1" />
              <span>{{ stats.Critical_Mastery || 0 }}</span>
            </div>

            <div class="stat-block pr-2">
              <p-image class="stat-icon" src="https://tmktahu.github.io/WakfuAssets/statistics/rear_mastery.png" />
              <span class="ml-1">Dominio espalda</span>
              <div class="flex-grow-1" />
              <span>{{ stats.Rear_Mastery || 0 }}</span>
            </div>

            <div class="stat-block pr-2">
              <p-image class="stat-icon" src="https://tmktahu.github.io/WakfuAssets/statistics/melee_mastery.png" />
              <span class="ml-1">Dominio de melé</span>
              <div class="flex-grow-1" />
              <span>{{ stats.Melee_Mastery || 0 }}</span>
            </div>

            <div class="stat-block pr-2">
              <p-image class="stat-icon" src="https://tmktahu.github.io/WakfuAssets/statistics/distance_mastery.png" />
              <span class="ml-1">Dominio distancia</span>
              <div class="flex-grow-1" />
              <span>{{ stats.Distance_Mastery || 0 }}</span>
            </div>

            <div class="stat-block pr-2">
              <p-image class="stat-icon" src="https://tmktahu.github.io/WakfuAssets/statistics/healing_mastery.png" />
              <span class="ml-1">Dominio cura</span>
              <div class="flex-grow-1" />
              <span>{{ stats.Healing_Mastery || 0 }}</span>
            </div>

            <div class="stat-block pr-2">
              <p-image class="stat-icon" src="https://tmktahu.github.io/WakfuAssets/statistics/berserk_mastery.png" />
              <span class="ml-1">Dominio berserker</span>
              <div class="flex-grow-1" />
              <span>{{ stats.Berserk_Mastery || 0 }}</span>
            </div>
          </div>
          <div class="flex flex-column flex-grow-1" style="max-width: 50%">
            <div class="stat-block pr-2">
              <p-image class="stat-icon" src="https://tmktahu.github.io/WakfuAssets/statistics/critical_resistance.png" />
              <span class="ml-1">Resistencia crítica</span>
              <div class="flex-grow-1" />
              <span>{{ stats.Critical_Resistance || 0 }}</span>
            </div>

            <div class="stat-block pr-2">
              <p-image class="stat-icon" src="https://tmktahu.github.io/WakfuAssets/statistics/rear_resistance.png" />
              <span class="ml-1">Resistencia espalda</span>
              <div class="flex-grow-1" />
              <span>{{ stats.Rear_Resistance || 0 }}</span>
            </div>

            <div class="stat-block pr-2">
              <p-image class="stat-icon" src="https://tmktahu.github.io/WakfuAssets/statistics/armor_given.png" />
              <span class="ml-1">Armadura dada</span>
              <div class="flex-grow-1" />
              <span>{{ stats.Armor_Given || 0 }}%</span>
            </div>

            <div class="stat-block pr-2">
              <p-image class="stat-icon" src="https://tmktahu.github.io/WakfuAssets/statistics/armor_received.png" />
              <span class="ml-1">Armadura recibida</span>
              <div class="flex-grow-1" />
              <span>{{ stats.Armor_Received || 0 }}%</span>
            </div>

            <div class="stat-block pr-2">
              <p-image class="stat-icon" src="https://tmktahu.github.io/WakfuAssets/statistics/indirect_damage.png" />
              <span class="ml-1">Daños indirectos</span>
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

// Formula: ((100 * resistance) / (1000 + resistance))
const calcResistancePercentage = (resistance) => {
  if (!resistance || resistance <= 0) return 0
  const percentage = (100 * resistance) / (1000 + resistance)
  return percentage.toFixed(1)
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

