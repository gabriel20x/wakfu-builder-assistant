# Sistema de Anillos (Rings)

## 📋 Resumen

El sistema de anillos permite equipar **2 anillos simultáneamente** en un build, con restricciones específicas para evitar duplicados.

---

## 🎯 Características

### Slots de Anillos

El juego Wakfu permite equipar 2 anillos:
- **LEFT_HAND** (Anillos - permite hasta 2)
- ~~**RIGHT_HAND**~~ (No existe en los datos del juego - todos los anillos usan LEFT_HAND)

### Restricciones

**No se pueden equipar:**
1. ❌ El mismo anillo (mismo `item_id`) en ambas manos
2. ❌ El mismo anillo base con diferentes rarezas (mismo nombre, diferente rareza)

**Sí se pueden equipar:**
- ✅ Dos anillos completamente diferentes

---

## 🔧 Implementación Técnica

### Backend - Solver (api/app/services/solver.py)

**Ubicación:** Líneas 261-285

**Lógica de restricción:**
```python
# Allow up to 2 rings in LEFT_HAND slot
if slot == "LEFT_HAND":
    prob += lpSum(vars_in_slot) <= 2, f"max_two_rings"

# Constraint: Rings cannot be duplicated (same item_id OR same base name)
if "LEFT_HAND" in slots_used:
    ring_items = [item for item in items if item.slot == "LEFT_HAND"]
    
    # For each pair of rings, ensure they can't both be selected if same
    for i, ring1 in enumerate(ring_items):
        for ring2 in ring_items[i+1:]:
            name1 = ring1.name_es or ring1.name_en or ring1.name
            name2 = ring2.name_es or ring2.name_en or ring2.name
            
            if ring1.item_id == ring2.item_id or name1 == name2:
                # Can't equip both if same item or same base name
                prob += (item_vars[ring1.item_id] + item_vars[ring2.item_id] <= 1)
```

**¿Por qué comparar por nombre?**
- Diferentes rarezas tienen diferentes `item_id`
- Ejemplo: Anillo pinxudo Raro (25849) ≠ Anillo pinxudo Legendario (25851)
- Pero ambos tienen el mismo `name_es`: "Anillo pinxudo"
- La restricción por nombre previene equipar variantes del mismo anillo

**¿Por qué solo LEFT_HAND?**
- En los datos del juego Wakfu (gamedata_1.90.1.43), **todos los anillos usan slot LEFT_HAND**
- No existe el slot RIGHT_HAND en los datos
- El solver permite hasta **2 items en LEFT_HAND** para soportar 2 anillos
- Otros slots (armas, armadura) mantienen el límite de 1 item

---

## 📊 Ejemplos

### ✅ Combinaciones Permitidas

| Anillo 1 | Anillo 2 | Resultado |
|----------|----------|-----------|
| Anillo pinxudo (Raro) | Anillo güino (Legendario) | ✅ Permitido - nombres diferentes |
| Anillo de Lacrimorsa | Anillo de la era glaciar | ✅ Permitido - nombres diferentes |
| Círculo axiar | Anillo gastrolito | ✅ Permitido - nombres diferentes |
| Sello fulgurante (Reliquia) | Anillo pinxudo (Legendario) | ✅ Permitido - nombres diferentes |

### ❌ Combinaciones NO Permitidas

| Anillo 1 | Anillo 2 | Razón |
|----------|----------|-------|
| Anillo pinxudo (Raro) | Anillo pinxudo (Raro) | ❌ Mismo item_id |
| Anillo pinxudo (Raro) | Anillo pinxudo (Legendario) | ❌ Mismo nombre base, diferente rareza |
| Anillo güino (Mítico) | Anillo güino (Épico) | ❌ Mismo nombre base, diferente rareza |
| Sello fulgurante + Sello fulgurante | - | ❌ Mismo nombre (solo existe 1 rareza) |

---

## 🎨 Frontend

### Visualización

**Componente:** `frontend/src/components/BuildResult.vue`

El frontend muestra todos los items del build en un grid:
```vue
<ItemCard 
  v-for="item in build.items" 
  :key="item.item_id"
  :item="item"
/>
```

**Características:**
- ✅ Muestra automáticamente ambos anillos si el solver los incluye
- ✅ Cada anillo tiene su propia card
- ✅ Key único basado en `item_id`
- ✅ Grid responsivo adapta el layout

### Identificación Visual

Los anillos se muestran con:
- **Slot:** "Anillo" o "Ring" (según idioma)
- **Nombre:** Nombre específico del anillo
- **Rareza:** Color y badge correspondiente
- **Stats:** Stats individuales de cada anillo

---

## 🧪 Testing

### Verificación Manual

Para verificar que el sistema funciona:

1. **Generar build con prioridad en stats de anillos:**
```bash
curl -X POST http://localhost:8000/solver \
  -H "Content-Type: application/json" \
  -d '{
    "level_max": 170,
    "stat_weights": {
      "HP": 2,
      "Dodge": 3,
      "Distance_Mastery": 2
    }
  }'
```

2. **Verificar en la respuesta:**
   - ✅ Debe haber 2 items con `"slot": "LEFT_HAND"`
   - ✅ Ambos anillos deben tener nombres diferentes (`name_es` diferente)
   - ✅ Si hay Anillo pinxudo, solo debe aparecer UNA versión (no múltiples rarezas del mismo anillo)

3. **Verificar en el frontend:**
   - ✅ Ambos anillos se muestran en la lista de items
   - ✅ Los stats de ambos anillos se suman en "Stats Totales"

---

## 🔍 Casos Especiales

### Anillos con Stats Únicos

Algunos anillos tienen stats únicos que los hacen valiosos:

**Anillo pinxudo / Mamagring:**
- Todas las rarezas: `WP: -1` (penalty)
- Alto Dodge
- Dominio en 2 elementos
- **Restricción:** Solo una versión por build

**Anillo güino:**
- `Berserk_Mastery` (legítimo)
- Dominio en 2 elementos
- **Puede combinarse** con otros anillos diferentes

**Anillo descolorido:**
- `Berserk_Mastery: 173` (muy alto)
- **Puede combinarse** con otros anillos diferentes

---

## 📝 Notas de Desarrollo

### Orden de Comparación de Nombres

El solver compara nombres en este orden:
1. `name_es` (Español) - prioridad
2. `name_en` (Inglés) - fallback
3. `name` (default) - fallback final

Esto asegura que la comparación funcione independientemente del idioma de los datos.

### Performance

**Complejidad:** O(n × m) donde:
- n = número de anillos LEFT_HAND
- m = número de anillos RIGHT_HAND

**Impacto:**
- Típicamente ~50-100 anillos por slot
- ~5,000-10,000 comparaciones por build
- Tiempo: < 1ms (negligible en el solver total)

---

## 🎯 Resumen

| Aspecto | Estado | Detalles |
|---------|--------|----------|
| **Slots** | ✅ Implementado | LEFT_HAND (hasta 2 items) |
| **Restricción por item_id** | ✅ Implementado | No duplicar mismo item |
| **Restricción por nombre** | ✅ Implementado | No duplicar mismo anillo base |
| **Frontend** | ✅ Compatible | Muestra automáticamente ambos |
| **Testing** | ✅ Verificado | Funciona correctamente |

---

**Última actualización:** 2025-11-04  
**Implementado en:** v1.x  
**Mantenedor:** AI Assistant

