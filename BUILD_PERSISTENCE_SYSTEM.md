# Sistema de Persistencia de Builds

## 🎯 Características Implementadas

### 1. ✅ Persistencia Automática de Build Activa

La build actualmente generada **se guarda automáticamente** en localStorage:
- Al generar un nuevo build
- Al cambiar de pestaña
- Persiste al recargar la página

**Incluye**:
- Los 5 builds (easy, medium, hard_epic, hard_relic, full)
- Configuración completa (nivel, stats, preferencias)
- Timestamp de creación

### 2. 📜 Historial de Builds (Max 10)

Mantiene historial de las **últimas 10 builds generadas**:
- Auto-guardado al generar
- Ordenado por fecha (más recientes primero)
- Muestra nivel y stats principales
- Click para cargar cualquier build del historial

### 3. ⭐ Builds Guardadas por Usuario (Max 20)

El usuario puede **guardar builds con nombre personalizado**:
- Botón "💾 Guardar Build" en el header
- Prompt para ingresar nombre
- Lista separada de historial
- Máximo 20 builds guardadas
- Puede eliminar builds guardadas

### 4. 🔄 Restauración Automática

Al abrir la aplicación o cambiar de pestaña:
- **Restaura la build activa** automáticamente
- **Restaura la configuración** (nivel, stats, preferencias)
- **Todo vuelve como estaba** antes de salir

### 5. 📊 Metadata en Builds

Cada item en la build muestra:
- **Tag verde "📊 Info"** si tiene metadata
- **Tooltip al hover** con drop rates y métodos
- **Botón ⚙️** para editar metadata directamente
- Click → Cambia a pestaña metadata con item preseleccionado

### 6. 📈 Estadísticas de Cobertura

En la pestaña de Metadata:
```
┌────────────────────────────────┐
│ Cobertura de Metadatos         │
│ 25 / 1,234 items               │
│ ████░░░░░░░░░░░░ 2.03%        │
└────────────────────────────────┘
```

## 🎨 Interfaz de Usuario

### Panel de Configuración:

```
┌──────────────────────────────────────┐
│ Configuración del Build              │
│ [🌟 Generar Builds] [💾 Guardar]    │
├──────────────────────────────────────┤
│ Nivel: 230                            │
│ Stats a priorizar...                  │
└──────────────────────────────────────┘
```

### Panel de Stats (Cuando hay build):

```
┌──────────────────────────────────────┐
│ Stats Totales                         │
├──────────────────────────────────────┤
│ [Stats detallados...]                 │
├──────────────────────────────────────┤
│ [Damage Estimator...]                 │
├──────────────────────────────────────┤
│ 🕐 Historial | ⭐ Guardadas           │
│                                       │
│ 05/11/25 17:30   Niv. 230    [📂]   │
│ HP, AP, Crítico                       │
│                                       │
│ 05/11/25 16:15   Niv. 215    [📂]   │
│ AP, MP, Daño Fuego                    │
└──────────────────────────────────────┘
```

### Cards de Items:

```
┌────────────────────┐
│ [⚙️]               │ ← Botón editar metadata
│ ┌───┐              │
│ │IMG│ Item Name    │
│ └───┘ Niv. 165     │
│ [Mítico] [📊 Info] │ ← Tag con metadata
└────────────────────┘
```

**Tooltip al hover sobre tag "📊 Info"**:
```
Drop: 8%, 2.5% | Crafteable | Fragmentos: 5%, 0.812%
```

## 💾 Estructura de Almacenamiento

### localStorage Keys:

- `wakfu_current_build` - Build activa
- `wakfu_current_config` - Configuración activa
- `wakfu_saved_builds` - Builds guardadas por usuario (max 20)
- `wakfu_build_history` - Historial automático (max 10)

### Estructura de Datos:

```json
{
  "builds": {
    "easy": { "items": [...], "total_stats": {...}, ... },
    "medium": { ... },
    "hard_epic": { ... },
    "hard_relic": { ... },
    "full": { ... }
  },
  "config": {
    "level_max": 230,
    "stat_weights": { "HP": 2.0, "AP": 3.0, ... },
    "include_pet": true,
    "include_accessory": true,
    "damage_preferences": ["Fire", "Water"],
    "resistance_preferences": ["Fire", "Water", "Earth", "Air"]
  },
  "timestamp": "2025-11-05T17:30:00.000Z"
}
```

### Build Guardada con Nombre:

```json
{
  "id": "1730835000000",
  "name": "Mi Build PvM Fuego Niv 230",
  "builds": { ... },
  "config": { ... },
  "timestamp": "2025-11-05T17:30:00.000Z"
}
```

## 🔄 Flujos de Trabajo

### Flujo 1: Generar y Persistir
```
1. Usuario configura stats
2. Click "Generar Builds"
3. ✅ Auto-guardado en localStorage
4. ✅ Agregado al historial
5. Usuario puede cambiar de pestaña
6. Al volver → Build restaurada automáticamente
```

### Flujo 2: Guardar con Nombre
```
1. Generar build
2. Click "💾 Guardar Build"
3. Ingresar nombre: "Mi Build PvM Fuego 230"
4. ✅ Guardada en lista de favoritos
5. Accesible en tab "⭐ Guardadas"
```

### Flujo 3: Cargar Build Anterior
```
1. Click en tab "🕐 Historial" o "⭐ Guardadas"
2. Ver lista de builds
3. Click en 📂 de una build
4. ✅ Build cargada
5. ✅ Configuración restaurada
6. ✅ Stats aplicados
7. ✅ Items mostrados
```

### Flujo 4: Editar Metadata desde Build
```
1. Ver build generada
2. Notar item sin metadata
3. Click en ⚙️ en la card
4. ✅ Cambia a pestaña Metadata
5. ✅ Item preseleccionado
6. Agregar metadata
7. Guardar
8. Volver a Builder
9. ✅ Build sigue ahí (persistida)
10. Regenerar → metadata visible
```

## 🎮 Casos de Uso

### Caso 1: Jugador con Múltiples Personajes
```
Build 1: "Iop Fuego Niv 230" ⭐ Guardada
Build 2: "Cra Agua Niv 215" ⭐ Guardada
Build 3: "Osa Tank Niv 200" ⭐ Guardada

Puede cambiar entre ellas fácilmente.
```

### Caso 2: Experimentar con Variantes
```
Genera build base
↓
Guarda como "Base Fuego"
↓
Modifica stats (más crítico)
↓
Genera nueva
↓
Compara con historial
↓
Guarda mejor versión como "Fuego Crítico Final"
```

### Caso 3: Documentar Items Mientras Genera
```
Genera build
↓
Ve item sin metadata
↓
Click ⚙️
↓
Agrega metadata
↓
Vuelve a Builder
↓
Build sigue ahí ✅
↓
Completa metadata de todos los items
```

## 🔧 Componentes Creados/Modificados

### Nuevos Archivos:

1. **`frontend/src/composables/useBuildPersistence.js`**
   - Maneja todo el localStorage
   - Funciones de guardar/cargar
   - Gestión de historial y guardados

2. **`frontend/src/components/BuildHistory.vue`**
   - Lista visual de historial/guardados
   - Tabs para cambiar entre vistas
   - Botones de cargar/eliminar

### Archivos Modificados:

1. **`frontend/src/components/BuildGenerator.vue`**
   - Integra useBuildPersistence
   - Restaura builds al montar
   - Botón "Guardar Build"
   - Función loadBuild
   - Componente BuildHistory agregado

2. **`frontend/src/App.vue`**
   - Maneja evento edit-metadata
   - Pasa item preseleccionado a Metadata

3. **`frontend/src/components/ItemCard.vue`**
   - Botón ⚙️ para editar
   - Tag 📊 con metadata
   - Tooltip con información

4. **`frontend/src/components/ItemMetadataAdmin.vue`**
   - Acepta prop preselectedItem
   - Auto-selecciona item al montar
   - Barra de progreso con total

5. **`api/app/services/solver.py`**
   - Carga metadata desde JSON
   - Incluye metadata en cada item del build

6. **`api/app/routers/item_metadata.py`**
   - Endpoint `/stats` mejorado
   - Cuenta total de items en juego
   - Calcula porcentaje de cobertura

## 🚀 Cómo Usar

### Guardar una Build:

1. Genera una build con tus stats preferidos
2. Click en **"💾 Guardar Build"** (aparece cuando hay build)
3. Ingresa un nombre descriptivo: `"Iop Fuego PvM Niv 230"`
4. La build se guarda en **⭐ Guardadas**

### Cargar una Build Guardada:

1. En el panel de Stats, ve a la sección de historial
2. Click en tab **"⭐ Guardadas"**
3. Click en el icono **📂** de la build que quieras
4. Todo se restaura automáticamente

### Ver Historial:

1. Tab **"🕐 Historial"**
2. Ve las últimas 10 builds generadas
3. Click **📂** para cargar cualquiera

### Editar Metadata de un Item:

1. En cualquier build, click en **⚙️** en la card del item
2. Se abre automáticamente la pestaña de Metadata
3. El item ya está seleccionado y listo para editar
4. Agrega métodos y porcentajes
5. Guarda
6. Vuelve al Builder → tu build sigue ahí ✅

## 📱 Responsive

Todo funciona perfectamente en mobile:
- Historial scrolleable
- Botones táctiles
- Layout adaptable

## 🔒 Seguridad y Límites

- **Max 10** builds en historial (las más antiguas se eliminan)
- **Max 20** builds guardadas
- Datos solo en localStorage (privado del navegador)
- No se envía nada al servidor
- Cada usuario tiene sus propias builds

## 🎯 Beneficios

1. **Nunca pierdas tu progreso** - Auto-guardado continuo
2. **Experimenta libremente** - Guarda variantes y compara
3. **Multi-personaje** - Builds diferentes con nombres
4. **Workflow fluido** - Edita metadata sin perder build
5. **Historial útil** - Vuelve a builds anteriores
6. **Zero friction** - Todo automático

## ✅ ¡Listo para Usar!

El sistema está completamente funcional. Solo:

1. **Recarga la página** (F5)
2. **Genera una build**
3. **Cambia de pestaña** → Build se mantiene
4. **Vuelve** → Build sigue ahí
5. **Guarda con nombre** → Accesible siempre
6. **Edita metadata** → Build no se pierde

¡Todo funciona a la perfección! 🚀

