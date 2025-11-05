# Guía de Métodos Múltiples de Obtención

## 📦 Descripción

El sistema ahora soporta **múltiples métodos de obtención simultáneos** para cada item. Un mismo item puede obtenerse de varias formas diferentes, y el sistema permite documentar todas ellas.

## 🎯 Métodos Disponibles

### 1. 💀 Drop de Mobs/Bosses
**Cuándo usar**: Item que dropea de mobs o bosses

**Campos**:
- **Drop Rate General (%)**: Porcentaje de drop principal
- **Fuentes de Drop**: Lista de mobs/bosses específicos con sus rates
  - Nombre del mob/boss
  - Drop rate %

**Ejemplo**:
```
✅ Drop de Mobs/Bosses
  Drop Rate: 2%
  Fuentes:
    • Nox: 2%
    • Sombrero Mágiko: 0.5%
```

### 2. 🔨 Receta / Crafteo
**Cuándo usar**: Item que se puede craftear

**Campos**:
- Checkbox simple (no requiere campos adicionales)

**Ejemplo**:
```
✅ Receta / Crafteo
  (Este item se obtiene mediante crafteo/receta)
```

### 3. 🔮 Fragmentos de Reliquia
**Cuándo usar**: Items de rareza Legendario/Reliquia/Épico que se pueden obtener con fragmentos

**Campos**:
- **ID del Fragmento**: Item ID del fragmento
- **Nombre del Fragmento**: Nombre descriptivo
- **Fragmentos Requeridos**: Cantidad (normalmente 100)
- **Fuentes de Drop de Fragmentos**: Lista de mobs que dropean el fragmento
  - Nombre del mob
  - Drop rate %

**Ejemplo**:
```
✅ Fragmentos de Reliquia
  Fragment ID: 26099
  Nombre: Fragmento de Ortiz
  Requeridos: 100
  Fuentes:
    • Gwan Visiw Wabbit: 8.122%
    • Mimic fragmentado: 5%
    • Pekewabbit: 0.812%
```

### 4. 💰 Crupier (Monedas)
**Cuándo usar**: Item que se canjea en un crupier con monedas especiales

**Campos**:
- **ID de la Moneda**: Item ID de la moneda de cambio
- **Nombre de la Moneda**: Nombre de la moneda (ej: "Ficha preciosa")
- **Cantidad de Monedas**: Cuántas monedas se necesitan
- **Notas**: Información adicional

**Ejemplo**:
```
✅ Crupier (Monedas)
  Moneda ID: 54321
  Nombre: Ficha preciosa
  Cantidad: 50
  Notas: Se canjea en cualquier crupier de mazmorras. 
         Las monedas se obtienen de retos de mazmorras.
```

### 5. 🏆 Recompensa de Reto
**Cuándo usar**: Item que se obtiene como recompensa de reto/challenge

**Campos**:
- **Tipo de Reto**: Descripción del tipo de reto
- **Notas**: Detalles sobre el reto

**Ejemplo**:
```
✅ Recompensa de Reto
  Tipo: Reto de mazmorra Wabbit
  Notas: Recompensa por completar todos los retos de la 
         mazmorra Wabbit en dificultad máxima.
```

### 6. 📜 Misión / Quest
**Cuándo usar**: Item que se obtiene de una misión/quest

**Campos**:
- **Nombre de la Misión**: Nombre de la quest
- **Notas**: Detalles sobre la misión

**Ejemplo**:
```
✅ Misión / Quest
  Nombre: La búsqueda del tesoro perdido
  Notas: Recompensa final de la cadena de misiones de la 
         isla de Otomai. Nivel 100+.
```

### 7. ➕ Otro Método
**Cuándo usar**: Cualquier otro método no cubierto por las categorías anteriores

**Campos**:
- **Nombre del Método**: Descripción breve del método
- **Notas**: Detalles completos

**Ejemplo**:
```
✅ Otro Método
  Método: Evento de aniversario
  Notas: Solo disponible durante el evento de aniversario de 
         Wakfu. Se obtiene completando las misiones especiales 
         del evento.
```

## 🔄 Ejemplo Completo: Item con Múltiples Métodos

**Ejemplo Real**: Un item de reliquia que se puede obtener de 3 formas diferentes

```
ITEM: Ortiz (Reliquia)

✅ Drop de Mobs/Bosses
   Drop Rate: 0.5%
   Fuentes:
     • Nox Boss: 0.5%

✅ Fragmentos de Reliquia
   Fragment ID: 26099
   Nombre: Fragmento de Ortiz
   Requeridos: 100
   Fuentes de fragmentos:
     • Gwan Visiw Wabbit: 8.122%
     • Mimic fragmentado: 5%
     • Pekewabbit: 0.812%
     • Awelito wabbit: 0.812%
     • Wabbit: 0.812%
     • Wabbit wodo: 0.812%

✅ Crupier (Monedas)
   Moneda ID: 54321
   Nombre: Ficha de Nox
   Cantidad: 200
   Notas: Se canjea en el crupier especial de Nox con 
          fichas obtenidas de derrotar al boss Nox.

Notas Generales: Múltiples formas de obtención. 
Los fragmentos son la opción más accesible para la 
mayoría de jugadores.
```

## 💡 Casos de Uso Comunes

### Caso 1: Item Solo por Drop
```
✅ Drop de Mobs/Bosses (SOLO)
   Drop Rate: 2%
   Fuentes:
     • Lumicetro: 2%
```

### Caso 2: Item Crafteable con Materiales que Dropean
```
✅ Receta / Crafteo
✅ Drop de Mobs/Bosses (para los materiales)
   Notas: Los materiales para craftear se obtienen por drop.
```

### Caso 3: Item de Reto + Crupier
```
✅ Recompensa de Reto
   Tipo: Reto semanal de mazmorra
   Notas: Al completar otorga 5 fichas.

✅ Crupier (Monedas)
   Moneda: Ficha semanal
   Cantidad: 50
   Notas: Alternativa al reto, se pueden acumular fichas 
          durante varias semanas.
```

### Caso 4: Item de Evento Temporal
```
✅ Otro Método
   Método: Evento de Halloween
   Notas: Solo disponible durante octubre. Se obtiene 
          completando la quest especial del evento "Trick or Treat".

✅ Crupier (Monedas)
   Moneda: Caramelo encantado
   Cantidad: 100
   Notas: Los caramelos se obtienen durante el evento.
```

### Caso 5: Reliquia - Todas las Opciones
```
✅ Drop de Mobs/Bosses
✅ Fragmentos de Reliquia
✅ Crupier (Monedas)
✅ Recompensa de Reto

(Forma más completa de documentar una reliquia)
```

## 🎨 Interfaz de Usuario

### Checkbox por Método
Cada método tiene su propio checkbox. Al marcarlo, aparecen los campos relevantes.

### Cards Expandibles
Los métodos aparecen como cards que se expanden al marcar el checkbox:
- Header con icono + nombre del método
- Detalles expandibles con campos específicos
- Hover effect para mejor UX

### Organización
1. **Drop**: 💀 (skull)
2. **Recipe**: 🔨 (hammer)
3. **Fragments**: 🔮 (crystal ball) - solo para reliquias
4. **Crupier**: 💰 (money bag)
5. **Challenge**: 🏆 (trophy)
6. **Quest**: 📜 (scroll)
7. **Other**: ➕ (plus)

## 📊 Estructura de Datos (JSON)

```json
{
  "item_id": 26100,
  "name": "Ortiz",
  "acquisition_methods": {
    "drop": {
      "enabled": true,
      "drop_rate_percent": 0.5,
      "drop_sources": [
        {
          "source_name": "Nox Boss",
          "drop_rate_percent": 0.5
        }
      ]
    },
    "recipe": {
      "enabled": false
    },
    "fragments": {
      "enabled": true,
      "fragment_item_id": 26099,
      "fragment_name": "Fragmento de Ortiz",
      "fragments_required": 100,
      "fragment_drop_sources": [
        {
          "source_name": "Gwan Visiw Wabbit",
          "drop_rate_percent": 8.122
        }
      ]
    },
    "crupier": {
      "enabled": true,
      "currency_item_id": 54321,
      "currency_name": "Ficha de Nox",
      "currency_amount": 200,
      "notes": "Se canjea en el crupier especial..."
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
  "is_obtainable": true,
  "source_notes": "Múltiples formas de obtención disponibles.",
  "added_by": "Admin",
  "added_date": "2025-11-05T..."
}
```

## ✅ Beneficios del Sistema

### Para Administradores:
1. **Documentación completa**: Todas las formas de obtener un item en un solo lugar
2. **Flexibilidad**: Agregar/quitar métodos fácilmente
3. **Organización**: Estructura clara por tipo de método
4. **Validación**: Solo campos relevantes por método

### Para Jugadores:
1. **Información completa**: Saber todas las opciones disponibles
2. **Comparación**: Elegir el método más conveniente
3. **Planificación**: Decidir la ruta óptima de farming
4. **Transparencia**: Ver probabilidades reales

## 🔍 Búsqueda y Filtrado (Futuro)

Posibles mejoras:
- Filtrar items por método de obtención
- Buscar items disponibles en crupier X
- Listar items de evento temporal
- Calcular eficiencia (tiempo/probabilidad)

## 📝 Notas Importantes

### No Especificar Crupiers Individuales
Como mencionaste: "No hace falta indicar cual cuprier"
- Usar campo "Notas" para aclarar si es necesario
- Enfocarse en la moneda requerida

### No Especificar Retos Individuales
Como mencionaste: "No hace falta indicar cual reto"
- Usar campo "Tipo de Reto" para categorizar
- Usar "Notas" para detalles si son relevantes

### Monedas de Crupier
- Ejemplo de tu imagen: **Ficha preciosa**
- Documentar ID, nombre y cantidad requerida
- Las monedas mismas son items que se pueden buscar

## 🚀 Migración de Datos Antiguos

El sistema mantiene **backward compatibility**:
- Campos antiguos (`drop_rate_percent`, `is_craftable`, etc.) se mantienen
- La nueva estructura (`acquisition_methods`) es opcional
- Los datos antiguos siguen funcionando

## 📚 Ejemplos Adicionales

### Item de Mazmorra
```
✅ Drop de Mobs/Bosses
✅ Crupier (Monedas)
✅ Recompensa de Reto

(Típico de items de mazmorra)
```

### Item de Quest Única
```
✅ Misión / Quest

(Solo se obtiene una vez de una quest específica)
```

### Item de Crafteo con Materiales Raros
```
✅ Receta / Crafteo
✅ Drop de Mobs/Bosses (mencionar que son los materiales)

Notas: Requiere materiales raros que solo dropean 
de bosses específicos.
```

---

## 🎮 ¡Listo para Usar!

El sistema está completo y listo para documentar **todas** las formas de obtener items en Wakfu. Marca los métodos aplicables, completa los campos relevantes, y guarda. ¡Así de simple!

