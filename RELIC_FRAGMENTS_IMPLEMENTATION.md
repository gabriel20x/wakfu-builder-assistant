# Implementación de Sistema de Fragmentos de Reliquia

## Resumen

Se ha implementado un sistema completo para documentar la mecánica de fragmentos de reliquia en Wakfu, donde los jugadores pueden obtener items de reliquia reuniendo 100 fragmentos que dropean de diferentes mobs/bosses.

## Cambios Implementados

### 1. Estructura de Datos (item_metadata.json)

```json
{
  "version": "1.1.0",
  "description": "... includes relic fragments ...",
  "items": {
    "item_id": {
      // Campos existentes...
      "relic_fragment_info": {
        "can_obtain_via_fragments": false,
        "fragment_item_id": null,
        "fragment_name": "",
        "fragments_required": 100,
        "fragment_drop_sources": [
          {
            "source_name": "Mob Name",
            "drop_rate_percent": 5.0
          }
        ]
      },
      "drop_sources": []
    }
  }
}
```

### 2. Backend API (api/app/routers/item_metadata.py)

#### Nuevos Modelos Pydantic:

```python
class RelicFragmentInfo(BaseModel):
    can_obtain_via_fragments: bool = False
    fragment_item_id: Optional[int] = None
    fragment_name: Optional[str] = ""
    fragments_required: int = 100
    fragment_drop_sources: Optional[list] = []

class DropSource(BaseModel):
    source_name: str
    drop_rate_percent: Optional[float] = None
    notes: Optional[str] = ""
```

#### Actualización de ItemMetadata:
- Agregado campo `relic_fragment_info`
- Agregado campo `drop_sources`
- Extendido `corrected_source_type` para incluir "fragments"

#### Nuevas Estadísticas:
- `items_with_relic_fragments`: Cuenta items con info de fragmentos

### 3. Frontend (components/ItemMetadataAdmin.vue)

#### Nuevos Componentes UI:

**Sección de Fragmentos de Reliquia**:
- Solo visible para items con rareza ≥ 5 (Legendario, Reliquia, Épico)
- Checkbox para activar/desactivar funcionalidad de fragmentos
- Campos para:
  - ID del fragmento
  - Nombre del fragmento
  - Cantidad de fragmentos requeridos (default: 100)
  - Lista dinámica de fuentes de drop

**Lista de Fuentes de Drop**:
- Agregar múltiples fuentes con botón **"+ Agregar Fuente"**
- Cada fuente tiene:
  - Nombre del mob/boss
  - Drop rate en porcentaje
- Botón para eliminar fuentes (✕)
- Grid responsive

**Estadística Destacada**:
- Nueva card en el dashboard con degradado rosado/dorado
- Muestra cantidad de items con información de fragmentos

#### Nuevas Funciones:

```javascript
addFragmentSource() // Agrega nueva fuente de drop
removeFragmentSource(index) // Elimina fuente por índice
```

#### Actualización de editForm:
```javascript
relic_fragment_info: {
  can_obtain_via_fragments: false,
  fragment_item_id: null,
  fragment_name: '',
  fragments_required: 100,
  fragment_drop_sources: []
}
```

### 4. Traducciones (composables/useI18n.js)

#### Español:
- `metadata.relicFragmentTitle`: "🔮 Fragmentos de Reliquia"
- `metadata.canObtainViaFragments`: "¿Se puede obtener con fragmentos?"
- `metadata.fragmentItemId`: "ID del Fragmento"
- `metadata.fragmentName`: "Nombre del Fragmento"
- `metadata.fragmentsRequired`: "Fragmentos Requeridos"
- `metadata.fragmentDropSources`: "Fuentes de Drop de Fragmentos"
- `metadata.sourceName`: "Nombre de la fuente"
- `metadata.addSource`: "Agregar Fuente"
- `metadata.withRelicFragments`: "Con Info de Fragmentos"

#### English & Français:
- Traducciones completas en ambos idiomas

### 5. Estilos CSS

```css
.section-divider // Separador visual para sección de fragmentos
.checkbox-label // Estilo para checkbox activador
.fragment-details // Container con fondo destacado
.drop-sources-list // Lista de fuentes
.drop-source-item // Grid para cada fuente (nombre + rate + eliminar)
.btn-remove // Botón rojo circular para eliminar
.btn-add-source // Botón verde para agregar
.stat-card.relic-highlight // Card estadística con degradado especial
```

Responsive design incluido para mobile.

### 6. Documentación

**RELIC_FRAGMENTS_GUIDE.md**:
- Guía completa para usuarios
- Ejemplos prácticos con Ortiz, Poup Korn, Pastosa
- Paso a paso para agregar metadata
- FAQs
- Casos de uso

**RELIC_FRAGMENTS_IMPLEMENTATION.md** (este archivo):
- Documentación técnica
- Estructura de datos
- Cambios en código

## Flujo de Uso

```
1. Usuario busca reliquia (ej: "Ortiz")
   ↓
2. Click en el item
   ↓
3. Sistema detecta rarity ≥ 5
   → Muestra sección de fragmentos
   ↓
4. Usuario marca checkbox "¿Se puede obtener con fragmentos?"
   → Aparecen campos de fragmento
   ↓
5. Usuario completa:
   - ID del fragmento (ej: 26099)
   - Nombre (ej: "Fragmento de Ortiz")
   - Fragmentos requeridos (100)
   ↓
6. Usuario agrega fuentes de drop:
   - Gwan Visiw Wabbit: 8.122%
   - Mimic fragmentado: 5%
   - Pekewabbit: 0.812%
   - ... etc
   ↓
7. Click en "Guardar"
   → Metadata guardada en JSON
   ↓
8. Estadística "Con Info de Fragmentos" se actualiza
```

## Casos de Uso Soportados

### Caso 1: Solo Fragmentos
Item que **SOLO** se obtiene por fragmentos:
```json
{
  "item_id": 26100,
  "name": "Poup Korn",
  "relic_fragment_info": {
    "can_obtain_via_fragments": true,
    "fragment_item_id": 26099,
    "fragment_name": "Fragmento de Poup Korn",
    "fragments_required": 100,
    "fragment_drop_sources": [
      {"source_name": "Mimic fragmentado", "drop_rate_percent": 5.0}
    ]
  }
}
```

### Caso 2: Drop Directo + Fragmentos
Item que se puede obtener **por drop O por fragmentos**:
```json
{
  "item_id": 26100,
  "name": "Ortiz",
  "drop_rate_percent": 0.5,
  "source_notes": "Drop directo 0.5% de Nox boss, o 100 fragmentos",
  "relic_fragment_info": {
    "can_obtain_via_fragments": true,
    "fragment_item_id": 26099,
    "fragment_name": "Fragmento de Ortiz",
    "fragments_required": 100,
    "fragment_drop_sources": [
      {"source_name": "Gwan Visiw Wabbit", "drop_rate_percent": 8.122},
      {"source_name": "Mimic fragmentado", "drop_rate_percent": 5.0},
      // ... más fuentes
    ]
  }
}
```

### Caso 3: Múltiples Fuentes con Diferentes Rates
Item con fragmentos que dropean de muchos mobs:
```json
{
  "fragment_drop_sources": [
    {"source_name": "Sombrero Mágiko", "drop_rate_percent": 10.0},
    {"source_name": "Mimic fragmentado", "drop_rate_percent": 5.0},
    {"source_name": "Maltrahzero", "drop_rate_percent": 1.0},
    {"source_name": "Malapiel", "drop_rate_percent": 1.0},
    {"source_name": "Malcac", "drop_rate_percent": 1.0},
    {"source_name": "Malajeta", "drop_rate_percent": 1.0}
  ]
}
```

## Validaciones

### Frontend:
- Solo muestra sección para items con `rarity >= 5`
- Campos numéricos validados
- Lista de fuentes dinámica (agregar/eliminar)

### Backend:
- Pydantic valida estructura de datos
- Campos opcionales permiten flexibilidad
- Default de 100 fragmentos si no se especifica

## Beneficios

### Para Administradores:
1. **Interface intuitiva**: Sección claramente marcada con emoji 🔮
2. **Validación automática**: Solo aparece para reliquias/legendarios/épicos
3. **Gestión dinámica**: Agregar/quitar fuentes fácilmente
4. **Estadísticas**: Ver cuántos items tienen info completa

### Para Jugadores (futuro):
1. **Información completa**: Saber todas las formas de obtener un item
2. **Drop rates precisos**: Decidir qué mobs farmear
3. **Planificación**: Calcular tiempo estimado para conseguir item
4. **Comparación**: Drop directo vs fragmentos

## Próximos Pasos Sugeridos

### Mejoras Inmediatas:
1. **Auto-búsqueda de fragmentos**: Al escribir el nombre, buscar automáticamente el ID
2. **Validación de drop rates**: Sumar todos los rates y avisar si >100%
3. **Import/Export**: Importar lista de fuentes desde CSV

### Funcionalidades Avanzadas:
1. **Calculadora de farming**:
   - Input: Drop rate
   - Output: Kills promedio necesarios
   - Tiempo estimado

2. **Comparador de eficiencia**:
   - Drop directo vs fragmentos
   - ¿Qué opción es más rápida?

3. **Mapa interactivo**:
   - Mostrar ubicación de mobs que dropean fragmentos
   - Rutas de farming optimizadas

4. **Tracker de progreso**:
   - Registrar fragmentos actuales del jugador
   - Notificaciones de progreso

5. **Community data**:
   - Permitir que jugadores reporten drop rates
   - Validación comunitaria de datos

## Compatibilidad

- ✅ **Backward compatible**: Items sin fragmentos siguen funcionando
- ✅ **Optional fields**: Campos opcionales no rompen nada
- ✅ **Versioning**: Version 1.1.0 del schema
- ✅ **Multi-idioma**: ES, EN, FR completos

## Testing Manual Sugerido

1. **Buscar reliquia existente**
   - ✅ Verificar que aparece sección de fragmentos
   - ✅ Marcar checkbox y completar campos
   - ✅ Agregar múltiples fuentes
   - ✅ Eliminar una fuente
   - ✅ Guardar

2. **Buscar item común (rarity < 5)**
   - ✅ Verificar que NO aparece sección de fragmentos

3. **Editar item con fragmentos existentes**
   - ✅ Verificar que carga los datos correctamente
   - ✅ Modificar una fuente
   - ✅ Agregar nueva fuente
   - ✅ Guardar cambios

4. **Estadísticas**
   - ✅ Verificar que el contador de fragmentos aumenta
   - ✅ Verificar que la card tiene el estilo especial

5. **Responsive**
   - ✅ Probar en mobile
   - ✅ Verificar que grid de fuentes se adapta

## Archivos Modificados

```
✅ wakfu_data/item_metadata.json
✅ api/app/routers/item_metadata.py
✅ frontend/src/components/ItemMetadataAdmin.vue
✅ frontend/src/composables/useI18n.js
✅ RELIC_FRAGMENTS_GUIDE.md (nuevo)
✅ RELIC_FRAGMENTS_IMPLEMENTATION.md (nuevo)
```

## ¡Listo para Usar!

El sistema está completamente implementado y listo para documentar fragmentos de reliquia. Los usuarios pueden ahora:

1. Marcar qué items se obtienen por fragmentos
2. Documentar el ID y nombre del fragmento
3. Listar todas las fuentes de drop con sus rates
4. Ver estadísticas de cobertura

Todo con una interface intuitiva, validaciones, y soporte multi-idioma completo.

