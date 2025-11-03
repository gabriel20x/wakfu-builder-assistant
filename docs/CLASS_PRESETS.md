# 🎮 Class Presets - Guía Completa

Sistema de presets por clase y rol para Wakfu Builder Assistant.

## 📋 Contenido

- [Resumen](#resumen)
- [Clases Disponibles](#clases-disponibles)
- [Roles Base](#roles-base)
- [Endpoints de API](#endpoints-de-api)
- [Cómo Usar en el Frontend](#cómo-usar-en-el-frontend)

---

## Resumen

El sistema de presets permite a los usuarios generar builds optimizados automáticamente basándose en:
- **Clase del personaje** (Iop, Cra, Feca, etc.)
- **Rol deseado** (DPS, Tank, Healer, Support, etc.)
- **Elementos principales** (Fuego, Agua, Tierra, Aire)

Cada preset incluye:
- ✅ Pesos de stats optimizados (0-10)
- ✅ Orden de preferencia de elementos
- ✅ Stats primarios y secundarios recomendados

---

## Clases Disponibles

### 🛡️ Tanques / Defensores

#### Feca
- **Tank Protector** - Máxima supervivencia con glifos
  - Elementos: Agua, Tierra
  - Stats clave: HP (10), Lock (8), Block (8), Resistencias (7)
  
- **Support Glifo** - Buffs de equipo
  - Elementos: Fuego, Aire
  - Stats clave: AP (10), MP (7), Control (7)

#### Pandawa
- **Tank Soporte** - Control de posición
  - Elementos: Agua, Tierra
  - Stats clave: HP (10), Lock (8), AP (8)
  
- **DPS Melé** - Daño cuerpo a cuerpo
  - Elementos: Fuego, Aire
  - Stats clave: AP (10), Dominio Fuego (9), Melé (8)

#### Sacrier
- **Tank Agresivo** - Tanque con daño
  - Elementos: Fuego, Tierra
  - Stats clave: HP (10), AP (9), Fuego (8), Lock (7)
  
- **Berserker Puro** - Máximo Berserk
  - Elementos: Fuego
  - Stats clave: AP (10), Berserk (10), Fuego (9)

---

### ⚔️ DPS Melé

#### Iop
- **DPS Melé** - Máximo daño cuerpo a cuerpo
  - Elementos: Fuego, Aire
  - Stats clave: AP (10), Dominio Fuego (9), Melé (9), Crítico (8)
  
- **Berserker** - DPS con Berserk
  - Elementos: Fuego
  - Stats clave: AP (10), Berserk (10), Fuego (9)

#### Sram
- **Asesino Espalda** - Máximo daño por la espalda
  - Elementos: Fuego, Aire
  - Stats clave: AP (10), Rear (10), Fuego (9), Crítico (8)
  
- **Especialista en Trampas** - Control de zona
  - Elementos: Tierra, Agua
  - Stats clave: AP (10), MP (8), Tierra/Agua (8)

#### Ecaflip
- **DPS Crítico** - Máximo daño con críticos
  - Elementos: Fuego, Aire
  - Stats clave: AP (10), Crítico (10), Dominio Crítico (10), Fuego (9)
  
- **Tank Ágil** - Tanque con esquiva
  - Elementos: Agua, Tierra
  - Stats clave: HP (9), Dodge (8), Lock (7)

#### Ouginak
- **DPS Furia** - Daño con furia canina
  - Elementos: Fuego, Aire
  - Stats clave: AP (10), Fuego (9), Melé (9), Crítico (8)
  
- **Tank Presa** - Tanque con marcas
  - Elementos: Tierra, Agua
  - Stats clave: HP (9), Lock (8), AP (8)

---

### 🏹 DPS Distancia

#### Cra
- **Francotirador** - Máximo daño a distancia
  - Elementos: Fuego, Aire
  - Stats clave: AP (10), Distancia (10), Fuego (9), Range (8)
  
- **Support Beacon** - Buffs con beacons
  - Elementos: Agua, Tierra
  - Stats clave: AP (10), MP (7), Range (7)

#### Rogue
- **Bombardero** - Máximo daño con bombas
  - Elementos: Fuego, Aire
  - Stats clave: AP (10), Fuego (9), Crítico (9), Distancia (8)
  
- **Support Muros** - Control con muros
  - Elementos: Tierra, Agua
  - Stats clave: AP (10), MP (8), Control (8)

#### Foggernaut
- **DPS Railgun** - Daño a distancia con stasis
  - Elementos: Fuego, Agua
  - Stats clave: AP (10), Fuego (9), Distancia (8), Crítico (8)
  
- **Tank Fuego** - Tanque con daño de fuego
  - Elementos: Fuego, Tierra
  - Stats clave: HP (9), Fuego (8), Lock (7)

#### Eliotrope
- **DPS Portales** - Daño con portales
  - Elementos: Fuego, Aire
  - Stats clave: AP (10), Fuego (9), Distancia (8), Control (7)
  
- **Support Movilidad** - Soporte con portales
  - Elementos: Agua, Tierra
  - Stats clave: AP (10), MP (8), Control (8)

#### Huppermage
- **DPS Cuadrielemental** - Los 4 elementos
  - Elementos: Fuego, Agua, Tierra, Aire
  - Stats clave: AP (10), Todos Elementos (9), Elemental (8)
  
- **DPS Trielemental** - 3 elementos optimizado
  - Elementos: Fuego, Agua, Aire
  - Stats clave: AP (10), 3 Elementos (9), Crítico (8)

---

### 💚 Curanderos

#### Eniripsa
- **Curandero** - Máxima curación
  - Elementos: Agua
  - Stats clave: AP (10), Healing (10), WP (9), Heals Performed (9)
  
- **DPS Fuego** - Daño con marca
  - Elementos: Fuego
  - Stats clave: AP (10), Fuego (9), Crítico (8)

---

### 🌟 Soporte / Invocadores

#### Osamodas
- **Invocador** - Control de invocaciones
  - Elementos: Fuego, Tierra, Agua
  - Stats clave: AP (10), Control (9), Multi-Elemental (8)
  
- **DPS Elemental** - Daño directo
  - Elementos: Fuego, Aire
  - Stats clave: AP (10), Fuego (9), Aire (8), Crítico (8)

#### Sadida
- **Invocador Curandero** - Soporte con muñecos
  - Elementos: Agua
  - Stats clave: AP (10), Healing (8), Control (8)
  
- **DPS Veneno** - Daño con envenenamientos
  - Elementos: Tierra, Aire
  - Stats clave: AP (10), Tierra (9), Crítico (8)

#### Xelor
- **DPS Remoción AP** - Control temporal
  - Elementos: Fuego, Aire
  - Stats clave: AP (10), Fuego (9), Crítico (8), Distancia (7)
  
- **Support Temporal** - Control de tiempo
  - Elementos: Agua, Tierra
  - Stats clave: AP (10), MP (8), Control (7), Initiative (7)

#### Enutrof
- **Support MP Removal** - Control con remoción de MP
  - Elementos: Agua, Tierra
  - Stats clave: AP (10), MP (8), Lock (7), Agua/Tierra (8)
  
- **DPS Híbrido** - Daño melé/distancia
  - Elementos: Fuego, Aire
  - Stats clave: AP (10), Fuego (8), Melé/Distancia (7)

---

### 🎭 Versátiles

#### Masqueraider
- **DPS Versátil** - Daño adaptable con máscaras
  - Elementos: Fuego, Aire, Agua
  - Stats clave: AP (10), Multi-elemental (8), Melé (8)
  
- **Tank Máscara** - Tanque con evasión
  - Elementos: Tierra
  - Stats clave: HP (9), Dodge (8), Lock (7)

---

## Roles Base

### 🛡️ Tank
Maximiza supervivencia y control de zona
- **Stats Primarios**: HP, Lock, Block
- **Stats Secundarios**: Dodge, Force of Will, Initiative
- **Resistencias**: Elemental, Critical, Rear

### ⚔️ DPS Melé
Daño cuerpo a cuerpo
- **Stats Primarios**: AP, Melee Mastery, Critical Hit, Critical Mastery
- **Stats Secundarios**: Damage Inflicted, Rear Mastery, Berserk Mastery

### 🏹 DPS Distancia
Daño a distancia
- **Stats Primarios**: AP, Distance Mastery, Critical Hit, Range
- **Stats Secundarios**: Critical Mastery, Damage Inflicted, Rear Mastery

### 💚 Healer
Soporte y curación
- **Stats Primarios**: AP, WP, Healing Mastery, Heals Performed
- **Stats Secundarios**: HP, Critical Hit, Critical Mastery, Initiative

### 🌟 Support
Buffs, debuffs y control
- **Stats Primarios**: AP, MP, Control, Initiative
- **Stats Secundarios**: WP, HP, Critical Hit

### 💥 Berserker
DPS basado en Berserk
- **Stats Primarios**: AP, Berserk Mastery, Melee Mastery, Critical Hit
- **Stats Secundarios**: Critical Mastery, Damage Inflicted, HP

---

## Endpoints de API

### Listar todas las clases
```http
GET /presets/classes
```

**Respuesta:**
```json
[
  {
    "id": "iop",
    "name": "Iop",
    "icon": "iop",
    "primary_role": "dps_melee",
    "roles": ["dps_melee", "berserker"]
  },
  ...
]
```

### Obtener roles de una clase
```http
GET /presets/classes/{class_name}/roles
```

**Ejemplo:**
```http
GET /presets/classes/iop/roles
```

**Respuesta:**
```json
[
  {
    "id": "dps_melee",
    "name": "DPS Melé",
    "description": "Máximo daño cuerpo a cuerpo",
    "elements": ["Fire", "Air"],
    "is_primary": true
  },
  {
    "id": "berserker",
    "name": "Berserker",
    "description": "DPS con Berserk",
    "elements": ["Fire"],
    "is_primary": false
  }
]
```

### Obtener preset de build
```http
GET /presets/classes/{class_name}/preset?role={role}
```

**Ejemplo:**
```http
GET /presets/classes/iop/preset?role=dps_melee
```

**Respuesta:**
```json
{
  "weights": {
    "AP": 10.0,
    "Fire_Mastery": 9.0,
    "Air_Mastery": 8.0,
    "Melee_Mastery": 9.0,
    "Critical_Hit": 8.0,
    "Critical_Mastery": 8.0,
    "Damage_Inflicted": 8.0,
    "MP": 6.0,
    "Rear_Mastery": 7.0
  },
  "damage_preferences": ["Fire", "Air", "Water", "Earth"],
  "resistance_preferences": ["Fire", "Air", "Water", "Earth"]
}
```

### Obtener plantillas de roles
```http
GET /presets/roles
```

### Obtener detalles completos de una clase
```http
GET /presets/classes/{class_name}
```

---

## Cómo Usar en el Frontend

### 1. Selector de Clase y Rol

```vue
<template>
  <div class="class-selector">
    <!-- Selector de clase -->
    <p-dropdown
      v-model="selectedClass"
      :options="classes"
      option-label="name"
      option-value="id"
      placeholder="Selecciona tu clase"
      @change="onClassChange"
    />
    
    <!-- Selector de rol (se llena según la clase) -->
    <p-dropdown
      v-model="selectedRole"
      :options="roles"
      option-label="name"
      option-value="id"
      placeholder="Selecciona tu rol"
      @change="onRoleChange"
    />
    
    <!-- Botón para aplicar preset -->
    <p-button
      label="Aplicar Preset"
      icon="pi pi-check"
      @click="applyPreset"
    />
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import axios from 'axios'

const selectedClass = ref(null)
const selectedRole = ref(null)
const classes = ref([])
const roles = ref([])

// Cargar todas las clases al iniciar
const loadClasses = async () => {
  const response = await axios.get('/presets/classes')
  classes.value = response.data
}

// Cargar roles cuando cambia la clase
const onClassChange = async () => {
  const response = await axios.get(`/presets/classes/${selectedClass.value}/roles`)
  roles.value = response.data
  selectedRole.value = roles.value.find(r => r.is_primary)?.id || null
}

// Aplicar el preset
const applyPreset = async () => {
  const response = await axios.get(
    `/presets/classes/${selectedClass.value}/preset`,
    { params: { role: selectedRole.value } }
  )
  
  const preset = response.data
  
  // Aplicar pesos de stats
  applyStatWeights(preset.weights)
  
  // Aplicar preferencias de elementos
  applyElementPreferences(
    preset.damage_preferences,
    preset.resistance_preferences
  )
}

onMounted(() => {
  loadClasses()
})
</script>
```

### 2. Integración con BuildGenerator

Agregar selector de presets en `BuildGenerator.vue`:

```vue
<!-- Nuevo: Sección de Presets -->
<div class="config-section">
  <h3>Quick Start - Presets por Clase</h3>
  <ClassPresetSelector 
    @preset-applied="onPresetApplied"
  />
</div>
```

---

## 📊 Tabla de Pesos de Stats

### Escala de Importancia (0-10)

| Peso | Importancia | Descripción |
|------|-------------|-------------|
| 10   | Crítica     | Stat absolutamente esencial |
| 9    | Muy Alta    | Stat muy importante |
| 8    | Alta        | Stat importante |
| 7    | Media-Alta  | Stat útil |
| 6    | Media       | Stat secundario |
| 5    | Media-Baja  | Stat situacional |
| 4    | Baja        | Stat de baja prioridad |
| 3    | Muy Baja    | Stat marginal |

---

## 🔄 Conversión a Porcentajes

Si tu sistema requiere porcentajes:

```python
def normalize_weights(weights: dict) -> dict:
    """Convert weights to percentages"""
    total = sum(weights.values())
    return {
        stat: (weight / total) * 100
        for stat, weight in weights.items()
    }
```

**Ejemplo:**
```python
weights = {"AP": 10.0, "Fire_Mastery": 9.0, "HP": 4.0}
# Total = 23.0

normalized = {
    "AP": 43.48%,           # (10/23) * 100
    "Fire_Mastery": 39.13%, # (9/23) * 100
    "HP": 17.39%            # (4/23) * 100
}
```

---

## 💡 Tips para Usuarios

1. **Empezar con el Rol Primario**: Cada clase tiene un rol recomendado
2. **Personalizar después**: Los presets son puntos de partida, ajusta según tu estilo
3. **Combinar con Preferencias de Elementos**: Los presets incluyen orden de elementos recomendado
4. **Probar Diferentes Roles**: Una misma clase puede tener múltiples roles viables

---

**Creado para:** Wakfu Builder Assistant  
**Versión:** 1.0.0  
**Última actualización:** Noviembre 2024

