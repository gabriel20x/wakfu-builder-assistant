# 🎨 Frontend Rarity Migration Guide - v1.7

**Date:** 2025-11-03  
**Impact:** CRITICAL - Frontend no muestra rarities correctamente  
**Affected Files:** `frontend/src/composables/useStats.js`, `frontend/src/components/ItemCard.vue`

---

## 🔴 Problema Detectado

El frontend **NO está mostrando las rarities correctamente** porque el backend cambió el mapeo de rarity IDs, pero el frontend sigue usando el mapeo antiguo.

### Estado Actual del Frontend (❌ INCORRECTO):

```javascript
// frontend/src/composables/useStats.js - LÍNEAS 110-134
export const RARITY_COLORS = {
  0: '#808080',     // Sin rareza - Gris
  1: '#808080',     // Común - Gris
  2: '#9E9E9E',     // Inusual - Gris claro       ❌ INCORRECTO
  3: '#4CAF50',     // Raro - Verde
  4: '#FF9800',     // Mítico - Naranja           ❌ INCORRECTO
  5: '#E91E63',     // Reliquia - Fucsia/Rosa     ❌ INCORRECTO
  6: '#4FC3F7',     // Recuerdo - Celeste         ❌ INCORRECTO
  7: '#FFD700',     // Legendario - Dorado        ❌ INCORRECTO
}

export const RARITY_NAMES = {
  0: 'Común',
  1: 'Común',
  2: 'Inusual',      // ❌ NO EXISTE en equipment
  3: 'Raro',
  4: 'Mítico',       // ❌ INCORRECTO - Es Legendario
  5: 'Reliquia',     // ❌ INCORRECTO - Puede ser Legendario también
  6: 'Recuerdo',     // ⚠️ PARCIALMENTE CORRECTO
  7: 'Legendario',   // ❌ INCORRECTO - Es Épico
}
```

---

## ✅ Mapeo Correcto (Backend v1.7)

El backend ahora devuelve estos valores de `rarity`:

| `rarity` (API) | Nombre Correcto | Color Sugerido | Descripción |
|----------------|-----------------|----------------|-------------|
| **1** | Común | `#808080` (Gris) | Items comunes |
| **3** | Raro | `#4CAF50` (Verde) | Equipment skips rarity 2 |
| **4** | Mítico | `#FF9800` (Naranja) | Items míticos |
| **5** | Legendario | `#FFD700` (Dorado) | ⚠️ ERA "Reliquia" antes |
| **6** | Reliquia/Recuerdo | `#E91E63` (Fucsia) | Ver flags `is_relic` |
| **7** | Épico | `#D946EF` (Púrpura) | Items épicos |

### ⚠️ Casos Especiales:

#### Rarity 6 - Depende de Flags:
- **Si `is_relic = true`:** Es una **Reliquia verdadera** (98 items, varios niveles)
- **Si `is_relic = false`:** Es un **Recuerdo** (104 items, todos nivel 200)

#### Épicos (rarity 7):
- **Siempre tienen `is_epic = true`**
- Color distintivo: `#D946EF` (Púrpura)

---

## 🔧 Cambios Necesarios en el Frontend

### 1. Actualizar `useStats.js` - RARITY_COLORS

```javascript
// frontend/src/composables/useStats.js
export const RARITY_COLORS = {
  0: '#808080',     // Sin rareza - Gris
  1: '#808080',     // Común - Gris
  // 2: REMOVED - No existe en equipment
  3: '#4CAF50',     // Raro - Verde
  4: '#FF9800',     // Mítico - Naranja
  5: '#FFD700',     // Legendario - Dorado ✅ CAMBIADO
  6: '#E91E63',     // Reliquia/Recuerdo - Fucsia (ver flags)
  7: '#D946EF',     // Épico - Púrpura ✅ CAMBIADO
}
```

### 2. Actualizar `useStats.js` - RARITY_NAMES

```javascript
// frontend/src/composables/useStats.js
export const RARITY_NAMES = {
  0: 'Común',
  1: 'Común',
  // 2: REMOVED - No existe en equipment
  3: 'Raro',
  4: 'Mítico',
  5: 'Legendario',  // ✅ CAMBIADO (era "Reliquia")
  6: 'Reliquia',    // ⚠️ Default, se sobrescribe con flags
  7: 'Épico',       // ✅ CAMBIADO (era "Legendario")
}
```

### 3. Actualizar lógica de `ItemCard.vue` (YA CORRECTO ✅)

```javascript
// frontend/src/components/ItemCard.vue - LÍNEAS 69-91
const rarityColor = computed(() => {
  // ✅ Épicos: Prioridad máxima
  if (props.item.is_epic) {
    return '#D946EF' // Épico - Púrpura
  }
  // ✅ Reliquias: Prioridad sobre rarity genérico
  if (props.item.is_relic) {
    return '#E91E63' // Reliquia - Fucsia
  }
  // ✅ Caso general: Usar RARITY_COLORS
  return getRarityColor(props.item.rarity)
})

const rarityName = computed(() => {
  // ✅ Épicos
  if (props.item.is_epic) {
    return 'Épico'
  }
  // ✅ Reliquias (prioridad sobre rarity)
  if (props.item.is_relic) {
    return 'Reliquia'
  }
  // ⚠️ NECESITA ACTUALIZACIÓN: getRarityName debe devolver nombres correctos
  return getRarityName(props.item.rarity)
})
```

**ItemCard.vue está CORRECTO** ✅ porque usa flags `is_epic` y `is_relic` primero.

---

## 📊 Ejemplos de Items y Cómo se Mostrarán

### Ejemplo 1: Legendario "La punzante" (lvl 125)
```json
{
  "item_id": 23145,
  "name_es": "La punzante",
  "rarity": 5,           // ← Legendario (ANTES era Reliquia)
  "is_epic": false,
  "is_relic": false
}
```
**Frontend debe mostrar:**
- Color: `#FFD700` (Dorado)
- Nombre: "Legendario"

### Ejemplo 2: Reliquia "La Pastosa" (lvl 110)
```json
{
  "item_id": 26502,
  "name_es": "La Pastosa",
  "rarity": 6,           // ← Rarity 6
  "is_epic": false,
  "is_relic": true       // ← FLAG CRÍTICO
}
```
**Frontend debe mostrar:**
- Color: `#E91E63` (Fucsia)
- Nombre: "Reliquia"
- Tag: "⚡ Única"

### Ejemplo 3: Recuerdo "Yugotillas" (lvl 200)
```json
{
  "item_id": 24120,
  "name_es": "Yugotillas",
  "rarity": 6,           // ← Rarity 6
  "is_epic": false,
  "is_relic": false      // ← NO es Reliquia verdadera
}
```
**Frontend debe mostrar:**
- Color: `#E91E63` (Fucsia) - Mismo que Reliquia
- Nombre: "Recuerdo" (opcional: mostrar distinción visual)
- Sin tag "⚡ Única"

### Ejemplo 4: Épico "Casco de Hazieff" (lvl 110)
```json
{
  "item_id": 16074,
  "name_es": "Casco de Hazieff",
  "rarity": 7,           // ← Épico
  "is_epic": true,       // ← FLAG CRÍTICO
  "is_relic": false
}
```
**Frontend debe mostrar:**
- Color: `#D946EF` (Púrpura)
- Nombre: "Épico"
- Tag: "⚡ Única"

---

## 🎯 Resumen de Cambios CRÍTICOS

| Campo | Valor Antiguo | Valor Nuevo | Impacto |
|-------|---------------|-------------|---------|
| `RARITY_COLORS[5]` | `#E91E63` (Reliquia) | `#FFD700` (Legendario) | ⚠️ CRÍTICO |
| `RARITY_COLORS[7]` | `#FFD700` (Legendario) | `#D946EF` (Épico) | ⚠️ CRÍTICO |
| `RARITY_NAMES[5]` | "Reliquia" | "Legendario" | ⚠️ CRÍTICO |
| `RARITY_NAMES[7]` | "Legendario" | "Épico" | ⚠️ CRÍTICO |
| `RARITY_NAMES[2]` | "Inusual" | ❌ ELIMINAR | No existe |

---

## 🚀 Plan de Implementación

### Paso 1: Actualizar `useStats.js`
```javascript
export const RARITY_COLORS = {
  0: '#808080',
  1: '#808080',
  3: '#4CAF50',
  4: '#FF9800',
  5: '#FFD700',  // ✅ Legendario (era Reliquia)
  6: '#E91E63',  // Reliquia/Recuerdo
  7: '#D946EF',  // ✅ Épico (era Legendario)
}

export const RARITY_NAMES = {
  0: 'Común',
  1: 'Común',
  3: 'Raro',
  4: 'Mítico',
  5: 'Legendario',  // ✅ CAMBIADO
  6: 'Reliquia',    // ⚠️ Ver flags
  7: 'Épico',       // ✅ CAMBIADO
}
```

### Paso 2: (Opcional) Distinguir Recuerdos de Reliquias
```javascript
// Agregar función helper
export function getDisplayRarityName(item) {
  if (item.is_epic) return 'Épico'
  if (item.is_relic) return 'Reliquia'
  
  // Distinguir Recuerdos (rarity 6, pero NO is_relic)
  if (item.rarity === 6 && !item.is_relic) {
    return 'Recuerdo'
  }
  
  return RARITY_NAMES[item.rarity] || 'Unknown'
}
```

### Paso 3: Actualizar ItemCard.vue (si se implementa distinción Recuerdos)
```javascript
const rarityName = computed(() => {
  if (props.item.is_epic) return 'Épico'
  if (props.item.is_relic) return 'Reliquia'
  
  // ✅ Distinguir Recuerdos
  if (props.item.rarity === 6 && !props.item.is_relic) {
    return 'Recuerdo'
  }
  
  return getRarityName(props.item.rarity)
})
```

### Paso 4: Verificar colores en BuildGenerator
- Verificar que los 5 builds (easy, medium, hard_epic, hard_relic, full) se muestren correctamente
- Los items Legendarios deben ser **dorados**, no fucsias

---

## ✅ Tests de Verificación

### Test Visual 1: Legendarios
```
Buscar "La punzante" nivel 125:
- Color: DORADO (#FFD700) ✅
- Nombre: "Legendario" ✅
```

### Test Visual 2: Épicos
```
Buscar "Casco de Hazieff":
- Color: PÚRPURA (#D946EF) ✅
- Nombre: "Épico" ✅
- Tag: "⚡ Única" ✅
```

### Test Visual 3: Reliquias
```
Buscar "La Pastosa":
- Color: FUCSIA (#E91E63) ✅
- Nombre: "Reliquia" ✅
- Tag: "⚡ Única" ✅
```

### Test Visual 4: Recuerdos
```
Buscar "Yugotillas" nivel 200:
- Color: FUCSIA (#E91E63) ✅
- Nombre: "Recuerdo" (opcional) o "Reliquia"
- Sin tag "⚡ Única" ✅
```

---

## 📈 Impacto en los Builds

### Antes del fix (INCORRECTO):
```
MEDIUM build mostraba:
- Items "Legendario" (rarity 5) como FUCSIAS ❌
- Items "Épico" (rarity 7) como DORADOS ❌
```

### Después del fix (CORRECTO):
```
MEDIUM build muestra:
- Items Legendarios (rarity 5) como DORADOS ✅
- Sin Épicos ni Reliquias (correcto por constraints) ✅

HARD_EPIC build muestra:
- Items Legendarios como DORADOS ✅
- 1 Item Épico como PÚRPURA ✅

HARD_RELIC build muestra:
- Items Legendarios como DORADOS ✅
- 1 Item Reliquia como FUCSIA ✅
```

---

## 🔍 Debugging

### Cómo verificar si el frontend está actualizado:

1. **Inspeccionar item en consola:**
```javascript
// En DevTools console
console.log('Rarity:', item.rarity)
console.log('is_epic:', item.is_epic)
console.log('is_relic:', item.is_relic)
console.log('Color esperado:', getRarityColor(item.rarity))
```

2. **Verificar colores visualmente:**
- Legendarios (rarity 5): DORADO `#FFD700`
- Épicos (rarity 7): PÚRPURA `#D946EF`
- Reliquias (rarity 6 + is_relic): FUCSIA `#E91E63`

3. **Contar items por rarity en build:**
```javascript
// En BuildGenerator.vue
const countByRarity = (build) => {
  const counts = {}
  build.items.forEach(item => {
    counts[item.rarity] = (counts[item.rarity] || 0) + 1
  })
  return counts
}
```

---

## 🚨 PRIORIDAD: ALTA

**Este cambio es CRÍTICO** porque:
1. Los usuarios ven items Legendarios con color de Reliquia (confusión)
2. Los builds MEDIUM pueden mostrar items como "Épico" cuando son Legendarios
3. La jerarquía visual de rarities está invertida

**Tiempo estimado:** 15-30 minutos  
**Dificultad:** Baja (solo actualizar 2 objetos en useStats.js)

---

**Status:** ⚠️ PENDIENTE DE IMPLEMENTACIÓN  
**Blocker:** No - Backend funciona correctamente  
**Testing:** Verificar visualmente después de cambios


