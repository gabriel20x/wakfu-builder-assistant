# 📋 Sistema de Presets por Clase - Wakfu Builder Assistant

**Versión:** 1.7.0  
**Fecha:** 2025-11-03  
**Fuente:** Guías comunitarias y tutoriales oficiales de Wakfu

---

## 📚 Índice

1. [Resumen Ejecutivo](#resumen-ejecutivo)
2. [Arquitectura del Sistema](#arquitectura-del-sistema)
3. [Clases Disponibles](#clases-disponibles)
4. [Cómo Usar los Presets](#cómo-usar-los-presets)
5. [Guía de Ponderación de Stats](#guía-de-ponderación-de-stats)
6. [Detalles por Clase](#detalles-por-clase)

---

## 🎯 Resumen Ejecutivo

El sistema de presets permite a los usuarios autoconfigurar builds optimizados basados en:
- **9 Clases** completamente configuradas
- **19 Roles/Builds** diferentes
- **Ponderación 0-10** para stats (0 = ignorado, 10 = máxima prioridad)
- **Preferencias elementales** por build
- **Notas de gameplay** extraídas de guías expertas

### Clases Implementadas

| Clase | Roles Disponibles | Status |
|-------|-------------------|--------|
| **Cra** | 2 (DPS Explosivo, Farm) | ✅ Completo |
| **Sacrieur** | 3 (Berserker, Enflammé, Tank) | ✅ Completo |
| **Eniripsa** | 3 (Healer, Poison, Support) | ✅ Completo |
| **Feca** | 1 (Tank) | ✅ Básico |
| **Osamodas** | 1 (Support) | ✅ Básico |
| **Ouginak** | 1 (DPS Melé) | ✅ Básico |
| **Pandawa** | 2 (Tank, DPS) | ✅ Básico |
| **Steamer** | 1 (DPS Híbrido) | ✅ Básico |

---

## 🏗️ Arquitectura del Sistema

### Flujo de Datos

```
┌─────────────────────────────────────┐
│  frontend/public/class-presets.json │
│  (Archivo JSON estático)            │
└──────────────┬──────────────────────┘
               │
               │ fetch('/class-presets.json')
               ↓
┌─────────────────────────────────────┐
│  ClassPresetSelector.vue            │
│  - Carga clases y roles             │
│  - Muestra preview de stats         │
│  - Emite evento 'preset-applied'    │
└──────────────┬──────────────────────┘
               │
               │ emit('preset-applied', {...})
               ↓
┌─────────────────────────────────────┐
│  BuildGenerator.vue                 │
│  - Recibe preset                    │
│  - Aplica weights a stat groups     │
│  - Configura element preferences    │
└─────────────────────────────────────┘
```

### Estructura del JSON

```json
{
  "classes": [
    {
      "id": "cra",
      "name": "Cra (Arquero)",
      "description": "...",
      "primary_role": "dps_distance",
      "roles": [
        {
          "id": "dps_distance_explo",
          "name": "DPS Distancia (Explosivo)",
          "description": "...",
          "is_primary": true,
          "level_range": [20, 245],
          "elements": ["Fire", "Earth"],
          "stat_priorities": {
            "Distance_Mastery": 10.0,
            "Critical_Hit": 9.0,
            "AP": 10.0,
            "HP": 4.0
          },
          "recommended_passives": [...],
          "recommended_stats_distribution": {...},
          "gameplay_notes": [...]
        }
      ]
    }
  ],
  "role_templates": {...}
}
```

---

## 🎮 Cómo Usar los Presets

### Desde la UI

1. **Abrir BuildGenerator.vue**
2. **Sección "Quick Start - Presets por Clase"**
3. **Seleccionar Clase** (ej: Cra)
4. **Seleccionar Rol** (auto-selecciona el primario)
5. **Ver Preview** (top 6 stats con valores)
6. **Aplicar Preset** → Autoconfiguración completa

### Resultado al Aplicar

El preset configura automáticamente:
- ✅ **Stat Weights** (0-10) para todos los stats relevantes
- ✅ **Damage Preferences** (orden de elementos para maestrías)
- ✅ **Resistance Preferences** (todas por defecto)
- ✅ **Notificación** con nombre de clase y rol aplicado

---

## 📊 Guía de Ponderación de Stats

### Escala 0-10

| Valor | Significado | Uso |
|-------|-------------|-----|
| **0** | Ignorado | Stats irrelevantes para el build |
| **3-4** | Secundario | Stats útiles pero no críticos |
| **5-6** | Medio | Stats importantes |
| **7-8** | Alto | Stats muy importantes |
| **9-10** | Crítico | Stats absolutamente esenciales |

### Ejemplos por Arquetipo

#### DPS Distancia (Cra Explosivo)
```json
{
  "Distance_Mastery": 10.0,  // CORE stat
  "AP": 10.0,                // CORE para combos
  "Critical_Hit": 9.0,       // Muy importante
  "Critical_Mastery": 8.0,   // Alto
  "Fire_Mastery": 7.0,       // Elemento principal
  "Dodge": 7.0,              // Supervivencia
  "Range": 6.0,              // Útil
  "HP": 4.0,                 // Secundario
  "Elemental_Resistance": 5.0 // Medio
}
```

#### Berserker (Sacrieur)
```json
{
  "HP": 10.0,                      // CRÍTICO (base para armor)
  "Fire_Resistance": 10.0,         // CRÍTICO (supervivencia a 20% HP)
  "Water_Resistance": 10.0,        // CRÍTICO
  "Earth_Resistance": 10.0,        // CRÍTICO
  "Air_Resistance": 10.0,          // CRÍTICO
  "AP": 10.0,                      // CORE para combos
  "Elemental_Mastery": 9.0,        // Muy importante
  "Berserk_Mastery": 9.0,          // Muy importante
  "Armor_Received": 8.0,           // Alto
  "Melee_Mastery": 8.0,            // Alto
  "Rear_Mastery": 8.0,             // Alto (tapar espalda)
  "MP": 7.0,                       // Importante para mobility
  "Critical_Hit": 6.0              // Medio
}
```

#### Healer (Eniripsa)
```json
{
  "Healing_Mastery": 10.0,    // CORE
  "AP": 10.0,                 // CORE para combos
  "Heals_Performed": 9.0,     // Muy importante
  "WP": 8.0,                  // Alto (sorts cuestan WP)
  "HP": 8.0,                  // Alto (>80% HP = +3 WP/turn)
  "Elemental_Mastery": 8.0,   // Para Contre Nature
  "MP": 7.0,                  // Importante
  "Dodge": 6.0,               // Medio
  "Elemental_Resistance": 6.0, // Medio
  "Damage_Inflicted": 6.0     // Para mode offensivo
}
```

---

## 🎓 Detalles por Clase

### 1. Cra (Arquero) 🏹

#### DPS Distancia (Explosivo) - PRIMARY
**Nivel:** 20-245  
**Elementos:** Fire, Earth  
**Estrategia:** Mantener distancia >3 casillas para +50% daños

**Stats Core (10):**
- Distance_Mastery: 10.0
- AP: 10.0

**Stats Muy Importantes (9):**
- Critical_Hit: 9.0

**Stats Altos (7-8):**
- Critical_Mastery: 8.0
- Fire_Mastery: 7.0
- Earth_Mastery: 7.0
- Dodge: 7.0

**Gameplay Notes:**
- **Insaissable:** Bonus +30%/+40%/+50% daños al acabar turno >3 casillas
- **Precisión:** Acumular con sorts 2-4 PA, consumir con Tir Précis
- **Flèche Explosive:** Requiere 90 Precisión
- **Affûtage:** Cada 100 = 1 Pointe Affûtée + 1 balise gratis
- **Pointe Affûtée:** Stackeable 40%/80%/120% boost al próximo sort

**Passives Recomendados:**
1. **Esprit Affûté** (CORE): +5 Affûtage por sort Tir Précis
2. **Mobilité**: +1 PM al usar sorts de movimiento
3. **Evasion**: +Esquiva

---

### 2. Sacrieur ⚔️

#### DPS Melé (Berserker) - PRIMARY
**Nivel:** 20-70 (post-70 cambia gameplay)  
**Elementos:** All (multi-element)  
**Estrategia:** Jugar a 20% HP para máxima Furia (+50% daños)

**Stats CRÍTICOS (10):**
- HP: 10.0 (BASE PARA TODO)
- Fire_Resistance: 10.0
- Water_Resistance: 10.0
- Earth_Resistance: 10.0
- Air_Resistance: 10.0
- AP: 10.0

**Stats Muy Importantes (9):**
- Elemental_Mastery: 9.0
- Berserk_Mastery: 9.0

**Stats Altos (8):**
- Melee_Mastery: 8.0
- Rear_Mastery: 8.0
- Armor_Received: 8.0

**Gameplay Notes - MECÁNICAS CORE:**

1. **Jauge de Fureur:**
   - A 20% HP = +50% daños en TODOS los sorts
   - Mecánica central de la clase

2. **HP System:**
   - Base: 200% nivel
   - **Con Sang Tatoué:** 1000% nivel (MANDATORY)
   - Armor máximo = 50% de tus HP
   - **Por eso HP es el stat #1**

3. **Resistencias = Supervivencia:**
   - Con 20% HP, cada hit puede matarte
   - **Refus de la Mort:** +50 resistances al <20% HP
   - 5 puntos major = +25 en todas las resistencias

4. **Armor Generation:**
   - **Armure Sanguine:** % HP en armor
   - **Refus de la Mort:** +20% HP max en armor al <20%
   - Armor % HP >> Armor fijo (por eso HP crítico)

5. **Combo Estándar T1:**
   ```
   1. Punition (fija HP a 20%, +50% daños)
   2. Cent% (infliges 1% más → procuras <20%)
   3. → Refus de la Mort activo (+50 resist, armor)
   4. Armure Sanguine (recuperar armor)
   5. Fracas (daño + armor)
   ```

6. **Tapar Espalda:**
   - +25% daños finales en melé
   - **Mobility tools:** Assaut, Attirance, Transposition

7. **WP Regen:**
   - Recibir ≥1 daño de enemigo
   - Perder ≥20% HP con sorts propios

**Passives Recomendados:**
1. **Sang Tatoué** (MANDATORY): +800% nivel en HP
2. **Refus de la Mort** (CORE): +50 resist + armor al <20% HP
3. **Mobilité**: +1 PM por movimiento (Assaut/Transpos/Démence)

---

### 3. Eniripsa 💚

#### Healer (Principal) - PRIMARY
**Nivel:** 20-245  
**Elementos:** Fire, Water  
**Estrategia:** Alternar mode soin (stack Propagateur) y Contre Nature (daño)

**Stats Core (10):**
- Healing_Mastery: 10.0
- AP: 10.0

**Stats Muy Importantes (9):**
- Heals_Performed: 9.0

**Stats Altos (8):**
- HP: 8.0 (>80% = +3 WP/turn)
- Elemental_Mastery: 8.0 (para Contre Nature)
- WP: 8.0

**Gameplay Notes - MECÁNICAS CORE:**

1. **Propagateur:**
   - +Daño acumulado por cada soin realizado
   - Stack en mode soin, consume en mode daño
   - **Soin Unique:** Primer soin monocible duplicado → doble Propagateur

2. **Contre Nature (2 WP):**
   - Convierte: Bonus Soin Réalisé → Daños Infligidos
   - Convierte: Maestría Soin → Maestría Elemental
   - Pierdes -10% Grâce por turno (no ganas)

3. **Grâce:**
   - +10% Soin Réalisé por turno (max 50%)
   - Usar Contre Nature para convertir en +daños

4. **WP Economy:**
   - Base: +1 WP/turn
   - **Si >80% HP:** +3 WP/turn (CRITICAL)
   - Por eso HP = 8.0

5. **Combo Propagateur:**
   ```
   T1: Mot Soignant (3 PA)
   → Soin Unique trigger: 2x soin
   → 2x Propagateur stack
   → Sort de daño: consume Propagateur
   ```

6. **Tools Clave:**
   - **Fiole Infectée:** Vol de vie 100% → funciona bajo Contre Nature
   - **Super Lapino:** Transpos + soin 539 HP → NO afectado por malus
   - **Défazage (1 PA):** INVULNERABILIDAD total 1 turno
   - **Explosion:** Marca que genera Propagateur al matar

7. **Estrategia:**
   - Turno soin: Stack Propagateur sin Contre Nature
   - Turno daño: Contre Nature + consume Propagateur
   - Mantener >80% HP para +3 WP

**Passives Recomendados:**
1. **Soin Unique** (CORE): Primer soin monocible duplicado
2. **Super Lapino**: Lapino mejorado con transpos
3. **Marquage Précis**: Ganar Propagateur al trigger marcas

---

## 🔧 Mantenimiento y Actualización

### Agregar Nueva Clase

1. **Editar** `frontend/public/class-presets.json`
2. **Agregar objeto** en `classes[]`:
```json
{
  "id": "nueva_clase",
  "name": "Nueva Clase",
  "description": "...",
  "primary_role": "rol_principal",
  "roles": [...]
}
```
3. **Definir roles** con `stat_priorities` en escala 0-10
4. **Incluir:**
   - `elements`: Array de elementos principales
   - `gameplay_notes`: Mecánicas clave
   - `recommended_passives`: Passives esenciales

### Modificar Ponderaciones

**IMPORTANTE:** Los valores deben estar en rango **0-10**

```javascript
// ❌ INCORRECTO
"Distance_Mastery": 5.0

// ✅ CORRECTO (escalado a 0-10)
"Distance_Mastery": 10.0
```

Para cambiar valores:
1. Editar `class-presets.json`
2. Guardar (hot-reload automático en dev)
3. Refresh del navegador

---

## 📈 Estadísticas del Sistema

```
Total Clases:          9
Total Roles:           19
Roles PRIMARY:         9
Roles Secundarios:     10

Stats Únicos Usados:   30+
Rango de Valores:      0-10
Paso Mínimo:           0.5

Cobertura:
- DPS Distancia:       22% (2 clases con variantes)
- DPS Melé:            33% (3 clases con variantes)
- Tank:                22% (2 clases)
- Healer/Support:      22% (2 clases)
```

---

## 🎯 Próximos Pasos

### Pendiente de Implementación

- [ ] **Más Builds por Clase:** Ej. Cra Terre, Sacrieur Armure Brûlante completo
- [ ] **Clases Faltantes:** Iop, Eliotrope, Huppermage, etc.
- [ ] **Level-Specific Presets:** Variantes para early/mid/endgame
- [ ] **Import/Export:** Guardar presets custom del usuario
- [ ] **Community Presets:** Sistema de voting para builds

### Mejoras UX

- [ ] **Tooltip ampliado:** Mostrar gameplay notes en hover
- [ ] **Comparación:** Comparar 2 presets lado a lado
- [ ] **Búsqueda:** Filtrar presets por elemento o nivel

---

**Status:** ✅ Production Ready v1.7  
**Última Actualización:** 2025-11-03  
**Mantenedor:** Lixnard


