# Estructura Simplificada de Metadatos

## 📦 Resumen de Cambios

El formulario ahora está **mucho más simple y conciso**, enfocado solo en lo esencial:

### ✅ Lo que se MANTIENE:
- **Checkboxes booleanos** para cada método de obtención
- **Listas simples de %** para drops y fragmentos
- **Notas generales** para información adicional

### ❌ Lo que se ELIMINÓ:
- Nombres de mobs/bosses individuales (solo % de drop)
- IDs y nombres de fragmentos específicos
- IDs y nombres de monedas de crupier
- Nombres de quests y retos específicos
- Campo "Corrección de Origen" (ahora automático)
- Campos "Is Obtainable" y "Difficulty Override" de la interfaz (aún en JSON)

## 🎯 Nueva Estructura

### Formulario Visual:

```
┌─────────────────────────────────────┐
│ INFORMACIÓN BÁSICA                  │
│ • ID del Item: 25975               │
│ • Nombre: Actibotas                 │
│ • Origen Actual: drop               │
├─────────────────────────────────────┤
│ 📦 MÉTODOS DE OBTENCIÓN             │
│                                     │
│ ☑️ 💀 Drop de Mobs/Bosses           │
│    [2.5] %  [✕]                    │
│    [+ Agregar %]                    │
│                                     │
│ ☑️ 🔨 Receta / Crafteo              │
│                                     │
│ ☐ 🔮 Fragmentos de Reliquia         │
│                                     │
│ ☐ 💰 Crupier (Monedas)              │
│                                     │
│ ☐ 🏆 Recompensa de Reto             │
│                                     │
│ ☐ 📜 Misión / Quest                 │
│                                     │
│ ☐ ➕ Otro Método                     │
├─────────────────────────────────────┤
│ 📝 NOTAS GENERALES                  │
│ [Texto libre con detalles...]       │
├─────────────────────────────────────┤
│ [Guardar] [Eliminar] [Cancelar]    │
└─────────────────────────────────────┘
```

### Estructura JSON:

```json
{
  "item_id": 25975,
  "name": "Actibotas",
  "acquisition_methods": {
    "drop": {
      "enabled": true,
      "drop_rates": [2.5, 0.5]
    },
    "recipe": {
      "enabled": true
    },
    "fragments": {
      "enabled": false,
      "fragment_rates": []
    },
    "crupier": {
      "enabled": false
    },
    "challenge_reward": {
      "enabled": false
    },
    "quest": {
      "enabled": false
    },
    "other": {
      "enabled": false
    }
  },
  "source_notes": "Se obtiene principalmente por drop de mobs en zona X, o puede craftearse con materiales raros.",
  "added_by": "Admin",
  "added_date": "2025-11-05T..."
}
```

## 📊 Ejemplos Prácticos

### Ejemplo 1: Item con Drop Simple
```json
{
  "item_id": 12345,
  "name": "Lumicetro",
  "acquisition_methods": {
    "drop": { "enabled": true, "drop_rates": [2.0] },
    "recipe": { "enabled": false },
    "fragments": { "enabled": false },
    "crupier": { "enabled": false },
    "challenge_reward": { "enabled": false },
    "quest": { "enabled": false },
    "other": { "enabled": false }
  },
  "source_notes": "Dropea del boss Nox con 2% de probabilidad"
}
```

### Ejemplo 2: Reliquia con Fragmentos
```json
{
  "item_id": 26100,
  "name": "Ortiz",
  "acquisition_methods": {
    "drop": { "enabled": true, "drop_rates": [0.5] },
    "recipe": { "enabled": false },
    "fragments": { 
      "enabled": true, 
      "fragment_rates": [8.122, 5.0, 0.812, 0.812, 0.812, 0.812]
    },
    "crupier": { "enabled": true },
    "challenge_reward": { "enabled": false },
    "quest": { "enabled": false },
    "other": { "enabled": false }
  },
  "source_notes": "Drop directo 0.5% de Nox boss. Fragmentos dropean de: Gwan Visiw Wabbit (8.122%), Mimic fragmentado (5%), varios wabbits (0.812%). También disponible en crupier especial con 200 fichas de Nox."
}
```

### Ejemplo 3: Item Crafteable + Drop de Materiales
```json
{
  "item_id": 54321,
  "name": "Amuleto de Zora",
  "acquisition_methods": {
    "drop": { "enabled": false },
    "recipe": { "enabled": true },
    "fragments": { "enabled": false },
    "crupier": { "enabled": false },
    "challenge_reward": { "enabled": false },
    "quest": { "enabled": false },
    "other": { "enabled": false }
  },
  "source_notes": "Se craftea en Joyería. Los materiales dropean de mobs en la zona Wabbit."
}
```

### Ejemplo 4: Item de Crupier + Reto
```json
{
  "item_id": 99999,
  "name": "Ficha preciosa",
  "acquisition_methods": {
    "drop": { "enabled": false },
    "recipe": { "enabled": false },
    "fragments": { "enabled": false },
    "crupier": { "enabled": true },
    "challenge_reward": { "enabled": true },
    "quest": { "enabled": false },
    "other": { "enabled": false }
  },
  "source_notes": "Se obtiene completando retos de mazmorras. Se puede canjear en cualquier crupier de mazmorra (Blop, Viticulista, Zombbit, etc.)"
}
```

## 💡 Filosofía del Diseño

### Solo lo Esencial:
- **Booleanos** para indicar SI/NO se puede obtener por cada método
- **Listas de %** para datos numéricos (drop rates)
- **Notas generales** para contexto y detalles específicos

### Información Detallada en Notas:
En lugar de campos específicos, usa las notas para documentar:
- Nombres de mobs/bosses
- Nombres de monedas y cantidades
- Nombres de quests
- Tipos de retos
- Cualquier detalle relevante

### Corrección de Origen Automática:
El worker determina el `source_type` basándose en los métodos habilitados:
1. **recipe** habilitado → source_type = "recipe"
2. **fragments** habilitado → source_type = "drop"
3. **drop** habilitado → source_type = "drop"
4. **crupier/challenge/quest** habilitado → source_type = "special"

## 🎨 UI Minimalista

### Formulario Compacto:
- Cada método ocupa una línea
- Solo se expanden los que necesitan datos extra (drop, fragments)
- Cards compactas con hover effect
- Diseño responsive

### Interacción Rápida:
- Checkbox → marcar método
- Si tiene % → aparece lista inline
- Click + → agregar otro %
- Click ✕ → eliminar %
- Todo en una vista compacta

## 📝 Guía Rápida de Uso

### Para un Item con Drop:
1. Marca ☑️ Drop
2. Agrega los % (ej: 2.5, 0.5)
3. En notas escribe de qué mobs
4. Guardar

### Para una Reliquia con Fragmentos:
1. Marca ☑️ Fragmentos
2. Agrega los % de fragmentos (ej: 8.122, 5.0, 0.812...)
3. En notas escribe qué mobs dropean fragmentos
4. Guardar

### Para Item de Crupier:
1. Marca ☑️ Crupier
2. En notas escribe qué moneda y cuántas
3. Guardar

### Para Item con Múltiples Métodos:
1. Marca todos los checkboxes aplicables
2. Completa % donde corresponda
3. En notas explica cada método
4. Guardar

## ✅ Ventajas

1. **Más rápido de completar** - Menos campos
2. **Menos errores** - Estructura más simple
3. **Más flexible** - Notas para detalles
4. **Más mantenible** - Código más limpio
5. **Más escalable** - Fácil agregar nuevos métodos

## 🚀 Siguiente Nivel

Con esta base simple, en el futuro se puede:
- Agregar parseo automático de notas
- Extraer drop rates de la wiki
- Generar reportes de métodos más comunes
- Crear herramientas de análisis

Pero por ahora: **simple, funcional, y efectivo**. 🎯

