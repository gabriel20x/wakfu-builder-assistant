# Guía de Fragmentos de Reliquia

## Descripción

En Wakfu, las reliquias pueden obtenerse de **dos formas diferentes**:

1. **Drop Directo**: El item completo dropea directamente de un boss/mob con cierto % de probabilidad
2. **Fragmentos**: Coleccionar 100 fragmentos del item y intercambiarlos por la reliquia completa

Este sistema te permite documentar ambas formas de obtención para cada reliquia.

## Ejemplos del Juego

### Fragmento de Ortiz

**Reliquia**: Ortiz (item completo)
**Fragmento**: Fragmento de Ortiz
**Fragmentos Requeridos**: 100

**Fuentes de Drop del Fragmento**:
- Gwan Visiw Wabbit: **8.122%**
- Mimic fragmentado: **5%**
- Pekewabbit: **0.812%**
- Awelito wabbit: **0.812%**
- Wabbit: **0.812%**
- Wabbit wodo: **0.812%**

### Fragmento de Poup Korn

**Reliquia**: Poup Korn (item completo)
**Fragmento**: Fragmento de Poup Korn
**Fragmentos Requeridos**: 100

**Fuentes de Drop del Fragmento**:
- Mimic fragmentado: **5%**

### Fragmento de Pastosa

**Reliquia**: Pastosa (item completo)
**Fragmento**: Fragmento de Pastosa
**Fragmentos Requeridos**: 100

**Fuentes de Drop del Fragmento**:
- Sombrero Mágiko: **10%**
- Maltrahzero: **1%**
- Malapiel: **1%**
- Malcac: **1%**
- Malajeta: **1%**
- Mimic fragmentado: **5%**

## Cómo Agregar Metadata de Fragmentos

### Paso 1: Buscar la Reliquia

1. Ve a la pestaña "⚙️ Metadatos de Items"
2. Busca el item de reliquia por nombre (ej: "Ortiz", "Poup Korn", "Pastosa")
3. Click en el item para abrir el editor

### Paso 2: Completar Información Básica (Opcional)

Si el item también se puede obtener por drop directo:
- **Drop Rate (%)**: Porcentaje de drop directo del item completo
- **Source Notes**: Notas sobre el drop directo

### Paso 3: Activar Sección de Fragmentos

Para items de rareza **Legendario (5), Reliquia (6), o Épico (7)**, aparecerá automáticamente la sección:

**🔮 Fragmentos de Reliquia**

1. Marcar el checkbox: **"¿Se puede obtener con fragmentos?"**

### Paso 4: Completar Información del Fragmento

Una vez marcado el checkbox, aparecen los campos:

#### a) ID del Fragmento
- El item_id del fragmento en la base de datos
- Ejemplo: Si "Fragmento de Ortiz" tiene ID 12345, poner 12345
- **Cómo encontrarlo**: Busca el fragmento en el admin, aparecerá su ID

#### b) Nombre del Fragmento
- Nombre descriptivo del fragmento
- Ejemplo: "Fragmento de Ortiz"

#### c) Fragmentos Requeridos
- Cantidad de fragmentos necesarios para intercambiar
- **Normalmente siempre es 100**
- Dejar en 100 a menos que sea diferente

#### d) Fuentes de Drop de Fragmentos
Click en **"+ Agregar Fuente"** para cada mob/boss que dropea el fragmento:

Para cada fuente, completar:
- **Nombre de la fuente**: Nombre del mob/boss (ej: "Gwan Visiw Wabbit")
- **Drop Rate (%)**: Porcentaje de drop (ej: 8.122)

Puedes agregar múltiples fuentes. Para eliminar una fuente, click en la **✕** roja.

### Paso 5: Guardar

Click en **"Guardar"** para guardar la metadata.

## Ejemplo Completo: Ortiz

```json
{
  "item_id": 26100,
  "name": "Ortiz",
  "relic_fragment_info": {
    "can_obtain_via_fragments": true,
    "fragment_item_id": 26099,
    "fragment_name": "Fragmento de Ortiz",
    "fragments_required": 100,
    "fragment_drop_sources": [
      {
        "source_name": "Gwan Visiw Wabbit",
        "drop_rate_percent": 8.122
      },
      {
        "source_name": "Mimic fragmentado",
        "drop_rate_percent": 5.0
      },
      {
        "source_name": "Pekewabbit",
        "drop_rate_percent": 0.812
      },
      {
        "source_name": "Awelito wabbit",
        "drop_rate_percent": 0.812
      },
      {
        "source_name": "Wabbit",
        "drop_rate_percent": 0.812
      },
      {
        "source_name": "Wabbit wodo",
        "drop_rate_percent": 0.812
      }
    ]
  },
  "added_by": "Tu nombre"
}
```

## Visualización en el Admin

Cuando editas una reliquia que ya tiene metadata de fragmentos:

1. La sección **🔮 Fragmentos de Reliquia** aparecerá destacada
2. El checkbox estará marcado
3. Se mostrarán todos los campos completados
4. Puedes agregar más fuentes o editar las existentes

## Estadísticas

En el panel de estadísticas del admin, verás:

- **Con Info de Fragmentos**: Número de reliquias con información de fragmentos
  - Esta card tiene un degradado rosado/dorado especial para destacar

## Búsqueda de Fragmentos

### Encontrar el ID del Fragmento

1. Busca el fragmento por nombre (ej: "Fragmento de Ortiz")
2. Click en el fragmento para abrir el editor
3. En "ID del Item" verás el ID (ej: 26099)
4. Copia ese ID
5. Vuelve a buscar el item principal (la reliquia)
6. Pega el ID en el campo "ID del Fragmento"

### Encontrar las Fuentes de Drop

Las fuentes de drop se pueden encontrar:

1. **Wiki de Wakfu**: https://www.wakfu.com/
2. **Zenith Wakfu**: Base de datos de la comunidad
3. **Experiencia de jugadores**: Contribuciones de la comunidad
4. **Game data scraping**: A veces incluido en los JSON

## Tipos de Corrección de Origen

Para items que se obtienen principalmente por fragmentos:

- **Corrección de Origen**: Dejar como está o poner "fragments"
- Esto ayuda al sistema a entender que la forma principal es por fragmentos

## Notas Importantes

### ¿Cuándo usar la sección de fragmentos?

- **SÍ**: Para todas las reliquias (rareza 6) que tengan sistema de fragmentos
- **SÍ**: Para legendarios (rareza 5) que tengan sistema de fragmentos
- **SÍ**: Para épicos (rareza 7) que tengan sistema de fragmentos
- **NO**: Para items que NO tienen sistema de fragmentos

### Drop Directo + Fragmentos

Algunos items se pueden obtener de **ambas formas**:

1. **Drop directo** del boss completo (muy raro, ej: 0.5%)
2. **Fragmentos** (más común, farmeable)

En este caso:
- Completa el campo **"Drop Rate (%)"** con el rate del drop directo
- Completa la sección de **fragmentos** con toda la información
- En **"Source Notes"** puedes explicar ambas opciones

Ejemplo:
```
Drop Rate: 0.5%
Source Notes: "Se obtiene con 0.5% del Nox boss, o reuniendo 100 fragmentos que dropean de varios wabbits"
```

## Beneficios para los Jugadores

Con esta información completa, los jugadores podrán:

1. **Planificar farming**: Saber qué mobs farmear para los fragmentos
2. **Calcular probabilidades**: Entender cuánto tiempo tomará conseguir el item
3. **Comparar opciones**: ¿Vale la pena farmear fragmentos o intentar el drop directo?
4. **Optimizar rutas**: Farmear múltiples fragmentos en una zona

## Futuras Mejoras

Posibles mejoras al sistema:

- Calculadora de probabilidades (cuántos kills necesitas)
- Comparador de eficiencia (fragmentos vs drop directo)
- Mapa interactivo de ubicaciones de mobs
- Tracker de progreso de fragmentos
- Integración con inventario del jugador

## Preguntas Frecuentes

**P: ¿Todos los items tienen fragmentos?**
R: No, solo algunas reliquias, legendarios y épicos tienen sistema de fragmentos.

**P: ¿Los fragmentos siempre son 100?**
R: Generalmente sí, pero puede variar según el item.

**P: ¿Puedo dejar campos vacíos?**
R: Sí, pero es recomendable completar todo lo que sepas.

**P: ¿Cómo sé si un item tiene fragmentos?**
R: Busca en la wiki de Wakfu o pregunta en la comunidad.

**P: ¿Qué pasa si agrego información incorrecta?**
R: Puedes editarla o eliminarla en cualquier momento.

## Contribución a la Comunidad

Si completas esta información:

1. Estarás ayudando a toda la comunidad
2. La información quedará guardada para futuros usuarios
3. Se puede compartir el archivo JSON con otros proyectos
4. Es fácil actualizar si cambia algún drop rate

¡Gracias por contribuir al sistema de metadata de Wakfu Builder Assistant!

