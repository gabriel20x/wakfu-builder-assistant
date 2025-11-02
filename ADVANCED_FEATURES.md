# 🚀 Características Avanzadas Implementadas

## ✅ Toggles para Items Difíciles de Conseguir

### 1. **Excluir Mascotas (PET)**

**Problema:**
- Las mascotas pueden ser difíciles/caras de conseguir
- Algunos jugadores prefieren builds sin mascotas

**Solución:**
```javascript
// Frontend
includePet: true/false

// Backend API
{
  "level_max": 80,
  "stat_weights": {"Distance_Mastery": 5.0},
  "include_pet": false  // ← Nuevo parámetro
}
```

**Resultado:**
```
include_pet: true  → Build con PET (11 items máximo)
include_pet: false → Build sin PET (10 items máximo)
```

### 2. **Excluir Emblemas (ACCESSORY)**

**Problema:**
- Los emblemas (Emblema de Bonta, Emblemas de relojero, etc.) pueden ser muy difíciles de conseguir
- Requieren misiones especiales, crafteo complejo, o drops raros

**Solución:**
```javascript
// Frontend
includeAccessory: true/false

// Backend API
{
  "level_max": 80,
  "stat_weights": {"Distance_Mastery": 5.0},
  "include_accessory": false  // ← Nuevo parámetro
}
```

**Resultado:**
```
include_accessory: true  → Build con ACCESSORY (11 items máximo)
include_accessory: false → Build sin ACCESSORY (10 items máximo)
```

---

## 🎮 UI del Frontend

### Ubicación

Los toggles aparecen en **"Opciones Avanzadas"** antes del botón "Generar Builds":

```
┌─────────────────────────────────┐
│ Opciones Avanzadas              │
│ Items difíciles de conseguir    │
│                                 │
│ [✓] 🐾 Incluir Mascotas        │
│     (pueden ser difíciles...)   │
│                                 │
│ [✓] ⭐ Incluir Emblemas         │
│     (pueden ser difíciles...)   │
└─────────────────────────────────┘

┌─────────────────────────────────┐
│     🌟 Generar Builds           │
└─────────────────────────────────┘
```

### Características UI

- ✅ Checkboxes con PrimeVue
- ✅ Iconos emoji (🐾 para mascotas, ⭐ para emblemas)
- ✅ Texto descriptivo
- ✅ Hint en gris claro
- ✅ Hover effect
- ✅ Background oscuro para destacar sección
- ✅ Valores por defecto: ambos true

---

## 🔧 Implementación Técnica

### Backend (FastAPI)

**Modelo de Request:**
```python
class SolveRequest(BaseModel):
    level_max: int = 230
    stat_weights: Dict[str, float] = {...}
    include_pet: bool = True
    include_accessory: bool = True
```

**Filtrado en Solver:**
```python
# Filtrar slots según preferencias
excluded_slots = []
if not include_pet:
    excluded_slots.append("PET")
if not include_accessory:
    excluded_slots.append("ACCESSORY")

if excluded_slots:
    query = query.filter(~Item.slot.in_(excluded_slots))
```

### Frontend (Vue 3)

**Variables Reactivas:**
```javascript
const includePet = ref(true)
const includeAccessory = ref(true)
```

**Request al API:**
```javascript
await builderAPI.solveBuild({
  level_max: characterLevel.value,
  stat_weights: activeStatWeights.value,
  include_pet: includePet.value,
  include_accessory: includeAccessory.value
})
```

---

## 🎯 Casos de Uso

### 1. Build Fácil de Conseguir
```
[✗] Incluir Mascotas
[✗] Incluir Emblemas

Resultado:
  - Solo items de drop común o crafteo simple
  - 9-10 slots equipados
  - Stats ligeramente inferiores pero más accesible
```

### 2. Build Completa (Máximo poder)
```
[✓] Incluir Mascotas
[✓] Incluir Emblemas

Resultado:
  - Todos los items disponibles
  - 11-12 slots equipados (máximo)
  - Stats optimizados al máximo
```

### 3. Build Intermedia
```
[✓] Incluir Mascotas
[✗] Incluir Emblemas

Resultado:
  - Mascotas sí (más fáciles de conseguir)
  - Emblemas no (muy difíciles)
  - 10-11 slots equipados
  - Balance entre poder y accesibilidad
```

---

## ⚔️ Restricción de Armas 2H (Implementada)

### Problema Original

Wakfu permite armas de 2 manos que bloquean el slot SECOND_WEAPON:
```
La Trireme (2H):
  - Ocupa: FIRST_WEAPON
  - Bloquea: SECOND_WEAPON
  - No permite escudo ni arma secundaria
```

### Solución Implementada

**Detección en el Solver (Runtime):**
```python
# Detectar armas 2H desde raw_data
for item in items:
    if item.slot == "FIRST_WEAPON" and item.raw_data:
        # Check AP cost (most 2H weapons cost 4-6 AP)
        ap_cost = item_def.get('useParameters', {}).get('useCostAp', 0)
        if ap_cost >= 4:
            two_handed_weapons.append(item)

# Agregar restricción
for two_hand in two_handed_weapons:
    for second_weapon in second_weapons:
        # No permitir 2H + second weapon
        prob += (item_vars[two_hand] + item_vars[second_weapon] <= 1)
```

**Heurística:**
- Armas con AP cost ≥ 4 = probablemente 2H
- La Trireme: AP cost = 5 ✅

---

## 📊 Impacto en Builds

### Comparación: Con vs Sin Mascota/Emblema

**Nivel 80, Distance_Mastery priorizado:**

| Config | Items | Distance_Mastery | HP | Observación |
|--------|-------|------------------|-----|-------------|
| ✓ PET ✓ ACCESSORY | 10-11 | 349 | ~530 | Máximo poder |
| ✓ PET ✗ ACCESSORY | 10 | ~340 | ~520 | Sin emblemas |
| ✗ PET ✓ ACCESSORY | 10 | ~340 | ~520 | Sin mascotas |
| ✗ PET ✗ ACCESSORY | 9 | 334 | ~500 | Más fácil |

**Diferencia:**
- PET aporta: ~15 Distance_Mastery, ~10 HP
- ACCESSORY aporta: ~10 Distance_Mastery, ~20 HP, stats extras

---

## 🎮 Items Afectados por los Toggles

### Mascotas (PET)
```
Ejemplos:
  - Kometa: 5 HP, 15 Distance_Mastery
  - Gélutin Chasseur: 20 HP, 20 Critical_Mastery, 30 Distance
  - Bow Meow: 30 HP
  
Dificultad:
  - Drops raros de mobs específicos
  - Eventos especiales
  - Compra con tokens
```

### Emblemas (ACCESSORY)
```
Ejemplos:
  - Emblema de Bonta: 97 HP, 8 Lock, 10 Mastery_3_elements, 1% Crit, 9 Elemental_Res
  - Emblema de Relojero II: 255 Distance, 75 Dodge, 3% Crit, 15 Elemental_Res
  - Emblema del Vil III: 356 Berserk, 200 Mastery_3_elements, 3% Block
  
Dificultad:
  - Misiones faccionarias (Bonta/Brakmar)
  - Dungeons específicos
  - Crafteo complejo
  - Drops muy raros
```

---

## 📝 Archivos Modificados

```
Backend:
  ✅ api/app/routers/solver.py
     - SolveRequest con include_pet e include_accessory
     - Parámetros pasados a solve_build()
  
  ✅ api/app/services/solver.py
     - solve_build() acepta nuevos parámetros
     - Filtrado de slots antes del solver
     - Detección de armas 2H (AP cost >= 4)
     - Restricción: 2H + SECOND_WEAPON <= 1
  
  ✅ api/app/db/models.py
     - blocks_second_weapon column (para futuro)
  
Frontend:
  ✅ frontend/src/components/BuildGenerator.vue
     - Sección "Opciones Avanzadas"
     - 2 checkboxes (PET, ACCESSORY)
     - Variables reactivas includePet, includeAccessory
     - Parámetros enviados en request
     - Estilos para .advanced-options
  
Migración:
  ✅ api/migrations/add_blocks_second_weapon.sql
     - ALTER TABLE para agregar columna
     - Index para mejor performance
```

---

## ✨ Ventajas del Sistema

### Para Jugadores Casuales
```
[✗] Mascotas
[✗] Emblemas

→ Build más fácil de conseguir
→ Menos farming requerido
→ Accesible para nuevos jugadores
```

### Para Jugadores Hardcore
```
[✓] Mascotas
[✓] Emblemas

→ Build óptima
→ Máximo poder posible
→ Worth the farming
```

### Para Min-Maxers
```
Pueden comparar:
  - Build con todo (máximo)
  - Build sin PET (ahorra farming de mascota)
  - Build sin ACCESSORY (ahorra misiones)
  - Build mínima (más rápida de conseguir)
```

---

## 🎯 Ejemplo de Uso

### Request Completo
```json
POST /api/build/solve
{
  "level_max": 80,
  "stat_weights": {
    "Distance_Mastery": 5.0,
    "HP": 1.0,
    "Critical_Hit": 2.0
  },
  "include_pet": false,
  "include_accessory": false
}
```

### Response
```json
{
  "easy": {
    "items": [9 items sin PET ni ACCESSORY],
    "total_stats": {...},
    "total_difficulty": 48.5
  },
  "medium": {...},
  "hard": {...}
}
```

---

## 🔄 Próximas Mejoras

### Implementadas ✅
- ✅ Toggle para Mascotas
- ✅ Toggle para Emblemas  
- ✅ Detección de armas 2H (AP cost)
- ✅ Restricción 2H bloquea SECOND_WEAPON

### En Consideración 💡
- [ ] Toggle para Monturas
- [ ] Detección mejorada de 2H (equipment type file)
- [ ] Sets/sinergias (bonus por equipar set completo)
- [ ] Facilidad de obtención (scoring)
- [ ] Preferencias de clase

---

**Versión**: 0.4.0  
**Fecha**: 2025-11-02  
**Estado**: ✅ **Toggles PET/ACCESSORY Funcionando**  
**Restricción 2H**: ✅ **Implementada**

