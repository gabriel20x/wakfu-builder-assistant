# 🔍 Metodología de Debugging para Stats de Wakfu

**Propósito:** Documentar el proceso sistemático para investigar y corregir problemas de mapeo de stats en el sistema Wakfu Builder.

**Caso de uso:** Esta metodología se aplicó exitosamente el 2025-11-04 para corregir 4 problemas de stats.

---

## 📋 Contexto del Sistema

### Arquitectura de Stats
```
Datos del Juego (JSON) → Worker (Normalización) → Database (PostgreSQL) → API (Solver) → Frontend
     ↓                          ↓                       ↓
  Action IDs              Mapeo a Stats          Almacenamiento JSON
  (ej: 175, 192)          (ej: Dodge, WP)        stats::jsonb
```

### Archivos Clave
- **Worker:** `worker/fetch_and_load.py` - Normaliza datos del juego a stats
- **Solver:** `api/app/services/solver.py` - Genera builds óptimos
- **Database:** PostgreSQL con columna `stats` (JSON) y `raw_data` (JSON original)
- **Game Data:** `wakfu_data/gamedata_1.90.1.43/items.json`

---

## 🎯 Proceso de Debugging (Paso a Paso)

### Paso 1: Identificar la Discrepancia

**Entrada del usuario:**
- Screenshots del juego mostrando stats de items
- JSON de builds generados mostrando stats diferentes

**Acción:**
1. Comparar stats del screenshot vs stats en el build JSON
2. Identificar qué stats están mal/faltantes
3. Listar items específicos afectados con sus `item_id`

**Ejemplo real:**
```
Screenshot muestra: "Peinado Ror - 80 Esquiva"
Build JSON muestra: "Berserk_Mastery: 70"
→ Problema identificado: Dodge vs Berserk
```

---

### Paso 2: Investigar en la Base de Datos

#### 2.1 Verificar Stats Actuales en DB

```bash
docker-compose exec db psql -U wakfu -d wakfu_builder -c "
SELECT item_id, name_es, slot, level, rarity, stats
FROM items
WHERE item_id = <ITEM_ID_DEL_USUARIO>
  OR name_es ILIKE '%<NOMBRE_DEL_ITEM>%';
"
```

**Output esperado:**
- Stats actuales almacenados en la DB
- Confirma si el problema está en DB o solo en el solver

#### 2.2 Revisar Raw Data (equipEffects)

```bash
docker-compose exec db psql -U wakfu -d wakfu_builder -c "
SELECT item_id, name_es, 
       raw_data::jsonb->'definition'->'equipEffects' as effects
FROM items
WHERE item_id = <ITEM_ID>;
"
```

**Buscar en el output:**
- **Action IDs** (ej: `"actionId": 175`)
- **Params** (valores, ej: `"params": [70.0, 0.0]`)

**Ejemplo real:**
```json
{"actionId": 175, "params": [70.0, 0.0]}
→ Action ID 175 con valor 70
```

---

### Paso 3: Investigar el Mapeo en Worker

#### 3.1 Buscar Action ID en el Código

```bash
grep -n "175" worker/fetch_and_load.py
```

**O en código:**
```python
# Buscar en stat_map (líneas ~140-230)
stat_map = {
    175: "Dodge_or_Berserk",  # ← Encontrado
    ...
}
```

#### 3.2 Verificar Lógica Contextual

```bash
grep -A 15 "Dodge_or_Berserk" worker/fetch_and_load.py
```

**Buscar:**
- Thresholds (ej: `if stat_value < 50`)
- Condiciones de slot (ej: `if slot == "HEAD"`)
- Lógica de conversión

**Ejemplo real:**
```python
if stat_value < 50:  # ← Threshold muy bajo!
    stat_name = "Dodge"
else:
    stat_name = "Berserk_Mastery"
```

---

### Paso 4: Identificar el Patrón

#### Patrones Comunes en Wakfu

**A. Stats Contextuales (dependen de valor/slot):**
- Action ID 175: Dodge (< threshold) vs Berserk_Mastery (>= threshold)
- Action ID 1055: Armor_Given (≤ 50) vs Berserk_Mastery (> 50)
- Action ID 160: Range (armas) vs Elemental_Resistance (armaduras)

**B. Penalties (valor positivo → stat negativo):**
- Action ID 21: HP_Penalty → -HP
- Action ID 57: MP_Penalty → -MP
- Action ID 192: WP_Penalty → -WP
- Action ID 174: Lock_Penalty → -Lock
- Action ID 176: Dodge_Penalty → -Dodge

**C. Multi-param (requieren procesamiento especial):**
- Action ID 1068: Multi_Element_Mastery (params[0] = valor, params[2] = num elementos)
- Action ID 1069: Random_Elemental_Resistance (similar)

**Cómo identificar el patrón:**
1. Ver el valor en params (positivo/negativo)
2. Ver si hay múltiples params
3. Comparar con items similares en screenshots
4. Buscar patrones en el código existente

---

### Paso 5: Verificar con Múltiples Rarezas

**Importante:** Un item puede tener múltiples rarezas con diferentes valores

```bash
docker-compose exec db psql -U wakfu -d wakfu_builder -c "
SELECT item_id, name_es, level, rarity, 
       stats::jsonb->'<STAT_NAME>' as stat_value,
       raw_data::jsonb->'definition'->'equipEffects'->0->'effect'->'definition'->'actionId' as first_action
FROM items
WHERE name_es ILIKE '%<NOMBRE_BASE>%'
ORDER BY level, rarity;
"
```

**Buscar:**
- ¿Todas las rarezas tienen el mismo Action ID?
- ¿Los valores escalan con la rareza?
- ¿Hay cambios de signo entre rarezas?

**Ejemplo real:**
```
Anillo pinxudo:
- Raro (rarity 3): Action 192, params [1.0] → WP: -1
- Mítico (rarity 4): Action 192, params [1.0] → WP: -1
- Legendario (rarity 5): Action 192, params [1.0] → WP: -1

→ Todas las rarezas tienen el mismo pattern
```

---

### Paso 6: Aplicar el Fix

#### 6.1 Actualizar worker/fetch_and_load.py

**Para nuevo Action ID:**
```python
stat_map = {
    57: "MP_Penalty",  # ← Agregar nuevo mapeo
    ...
}
```

**Para penalty nuevo:**
```python
elif stat_name == "MP_Penalty":
    stat_name = "MP"
    stat_value = -stat_value
```

**Para stat contextual:**
```python
elif stat_name == "Dodge_or_Berserk":
    if slot in ["FIRST_WEAPON", "HEAD", "SHOULDERS", "SECOND_WEAPON"]:
        if stat_value < 250:  # ← Ajustar threshold
            stat_name = "Dodge"
        else:
            stat_name = "Berserk_Mastery"
```

#### 6.2 Reconstruir Worker (Importante: sin cache!)

```bash
# SIEMPRE usar --no-cache para asegurar que use código nuevo
docker-compose build --no-cache worker
```

#### 6.3 Limpiar y Recargar Datos

```bash
# Borrar registro de versión para forzar recarga
docker-compose exec db psql -U wakfu -d wakfu_builder -c \
  "DELETE FROM gamedata_versions WHERE version_string = '1.90.1.43';"

# Iniciar worker (se detendrá solo cuando termine)
docker-compose up -d worker

# Ver progreso (opcional)
docker-compose logs -f worker
```

#### 6.4 Reiniciar API

```bash
# Reiniciar API para limpiar cache
docker-compose restart api
```

---

### Paso 7: Verificar el Fix

#### 7.1 Verificar en Database

```bash
docker-compose exec db psql -U wakfu -d wakfu_builder -c "
SELECT item_id, name_es, slot, rarity,
       stats::jsonb->'<STAT_CORREGIDO>' as new_stat,
       stats::jsonb->'<STAT_ANTERIOR>' as old_stat
FROM items
WHERE item_id IN (<ITEM_IDS_AFECTADOS>)
ORDER BY item_id;
"
```

**Verificar:**
- ✅ Nuevo stat aparece con valor correcto
- ✅ Stat anterior ya no aparece (es null)

#### 7.2 Generar Build de Prueba

```bash
curl -X POST http://localhost:8000/build/solve \
  -H "Content-Type: application/json" \
  -d '{
    "level_max": 170,
    "stat_weights": {
      "HP": 4,
      "<STAT_CORREGIDO>": 10
    }
  }'
```

**Verificar en respuesta JSON:**
- ✅ Items tienen el stat corregido
- ✅ total_stats suma correctamente
- ✅ Stat anterior no aparece o es 0

---

## 🛠️ Comandos Útiles

### Explorar Database

```bash
# Ver todas las tablas
docker-compose exec db psql -U wakfu -d wakfu_builder -c "\dt"

# Ver estructura de tabla items
docker-compose exec db psql -U wakfu -d wakfu_builder -c "\d items"

# Contar items por slot
docker-compose exec db psql -U wakfu -d wakfu_builder -c "
SELECT slot, COUNT(*) FROM items GROUP BY slot ORDER BY slot;
"

# Buscar items por nombre
docker-compose exec db psql -U wakfu -d wakfu_builder -c "
SELECT item_id, name_es, slot, level, rarity 
FROM items 
WHERE name_es ILIKE '%<BÚSQUEDA>%' 
LIMIT 10;
"

# Ver stats de un item específico
docker-compose exec db psql -U wakfu -d wakfu_builder -c "
SELECT item_id, name_es, stats 
FROM items 
WHERE item_id = <ITEM_ID>;
"

# Ver raw_data (equipEffects con Action IDs)
docker-compose exec db psql -U wakfu -d wakfu_builder -c "
SELECT raw_data::jsonb->'definition'->'equipEffects' 
FROM items 
WHERE item_id = <ITEM_ID>;
"
```

### Analizar Action IDs

```bash
# Ver todos los Action IDs únicos en la DB
docker-compose exec db psql -U wakfu -d wakfu_builder -c "
SELECT DISTINCT 
  effects->>'actionId' as action_id,
  COUNT(*) as count
FROM items,
  jsonb_array_elements(raw_data::jsonb->'definition'->'equipEffects') as effects
WHERE jsonb_typeof(raw_data::jsonb->'definition'->'equipEffects') = 'array'
GROUP BY effects->>'actionId'
ORDER BY action_id::int;
"
```

### Debugging Worker

```bash
# Ver logs del worker
docker-compose logs worker

# Ver solo últimas líneas
docker-compose logs --tail=50 worker

# Seguir logs en tiempo real
docker-compose logs -f worker

# Ver si worker está corriendo
docker-compose ps worker
```

---

## 🧩 Checklist de Debugging

Cuando un usuario reporte un problema de stats:

- [ ] **1. Obtener evidencia**
  - [ ] Screenshots del juego con stats correctos
  - [ ] JSON del build mostrando stats incorrectos
  - [ ] Item IDs específicos afectados

- [ ] **2. Investigar en DB**
  - [ ] Consultar stats actuales del item
  - [ ] Revisar raw_data para ver Action IDs
  - [ ] Verificar múltiples rarezas del mismo item

- [ ] **3. Analizar Worker**
  - [ ] Buscar Action ID en stat_map
  - [ ] Revisar lógica contextual (if/else)
  - [ ] Identificar patrón (contextual, penalty, multi-param)

- [ ] **4. Comparar con Otros Items**
  - [ ] Buscar items similares en screenshots
  - [ ] Ver si otros items tienen el mismo Action ID
  - [ ] Identificar el patrón correcto

- [ ] **5. Aplicar Fix**
  - [ ] Actualizar stat_map en worker/fetch_and_load.py
  - [ ] Agregar lógica contextual si es necesario
  - [ ] Agregar handling de penalty si aplica

- [ ] **6. Rebuild & Reload**
  - [ ] `docker-compose build --no-cache worker`
  - [ ] Borrar gamedata_versions
  - [ ] Iniciar worker para recargar
  - [ ] Reiniciar API

- [ ] **7. Verificar**
  - [ ] Consultar DB para ver stats corregidos
  - [ ] Generar build de prueba
  - [ ] Comparar con screenshot original

- [ ] **8. Documentar**
  - [ ] Crear/actualizar documentación
  - [ ] Agregar al SUMMARY.md
  - [ ] Limpiar archivos temporales

---

## 💡 Prompt para Agente AI

### Prompt Inicial
```
Tengo un problema con los stats de items en mi sistema Wakfu Builder.

[Usuario proporciona screenshots e items JSON]

El item "<NOMBRE>" muestra "<STAT_CORRECTO>" en el juego, 
pero en mi build aparece como "<STAT_INCORRECTO>".

Por favor:
1. Investiga qué Action ID tiene ese item
2. Verifica el mapeo en worker/fetch_and_load.py
3. Identifica el patrón (contextual, penalty, etc.)
4. Aplica el fix necesario
5. Reconstruye el worker y recarga los datos
6. Verifica que el fix funcione
```

### Información de Contexto para el Agente

**Arquitectura:**
- Worker en Docker: `worker/fetch_and_load.py`
- API en Docker: `api/app/services/solver.py`
- DB PostgreSQL: tabla `items` con columnas `stats` (JSON) y `raw_data` (JSON)
- Game data: `wakfu_data/gamedata_1.90.1.43/items.json`

**Comandos importantes:**
- Rebuild worker: `docker-compose build --no-cache worker`
- Limpiar DB: `DELETE FROM gamedata_versions WHERE version_string = '1.90.1.43';`
- Iniciar worker: `docker-compose up -d worker`
- Reiniciar API: `docker-compose restart api`

**Verificación:**
- Query DB: `docker-compose exec db psql -U wakfu -d wakfu_builder -c "..."`
- Ver raw_data para Action IDs
- Generar build de prueba con curl

**Patrones comunes:**
- Stats contextuales: dependen de valor o slot
- Penalties: valor positivo en datos → stat negativo
- Multi-param: requieren params[2] o params[3]

---

## 🔍 Casos Reales Resueltos (2025-11-04)

### Caso 1: Dodge vs Berserk_Mastery

**Síntomas:**
- Peinado Ror (HEAD): Build muestra Berserk_Mastery: 70
- Screenshot muestra: 80 Esquiva (Dodge)

**Investigación:**
```bash
# 1. Ver raw_data
→ Action ID 175, params: [70.0]

# 2. Ver mapeo en worker
→ 175: "Dodge_or_Berserk"
→ Threshold: if stat_value < 50 → Dodge, else → Berserk

# 3. Problema identificado
→ Threshold muy bajo (Dodge puede llegar a 170+)
```

**Fix aplicado:**
```python
# Antes
if stat_value < 50:
    stat_name = "Dodge"

# Después
if slot in ["FIRST_WEAPON", "HEAD", "SHOULDERS", "SECOND_WEAPON"]:
    if stat_value < 250:
        stat_name = "Dodge"
```

**Impacto:** +180 a +350 puntos de Dodge por build

---

### Caso 2: Prospecting vs -WP

**Síntomas:**
- Anillo pinxudo: Build muestra Prospecting: 1
- Screenshot muestra: -1 PM máx. (WP negativo)

**Investigación:**
```bash
# 1. Ver raw_data
→ Action ID 192, params: [1.0]

# 2. Ver mapeo
→ 192: "Prospecting"

# 3. Insight del usuario
→ "Podría ser WP_Penalty, como otros penalties"
```

**Fix aplicado:**
```python
# Antes
192: "Prospecting"

# Después
192: "WP_Penalty"  # Sigue patrón de penalties

elif stat_name == "WP_Penalty":
    stat_name = "WP"
    stat_value = -stat_value  # 1.0 → -1
```

**Lección:** Escuchar insights del usuario que conoce los patrones del juego

---

### Caso 3: MP Penalty Missing

**Síntomas:**
- Sello fulgurante: Build no muestra -MP
- Screenshot muestra: -1 PM máx.

**Investigación:**
```bash
# 1. Ver raw_data
→ Action ID 57, params: [1.0]

# 2. Ver mapeo
→ 57: (no existe en stat_map) ← Problema!
```

**Fix aplicado:**
```python
57: "MP_Penalty"  # Nueva entrada

elif stat_name == "MP_Penalty":
    stat_name = "MP"
    stat_value = -stat_value
```

**Lección:** Action IDs faltantes se descubren comparando raw_data con mapeo

---

### Caso 4: Sistema de 2 Anillos

**Síntomas:**
- Builds solo muestran 1 anillo
- Wakfu permite equipar 2

**Investigación:**
```bash
# 1. Ver slots en DB
→ LEFT_HAND: 847 items (todos anillos)
→ RIGHT_HAND: 0 items (no existe!)

# 2. Ver solver
→ Constraint: lpSum(vars_in_slot) <= 1 para LEFT_HAND
```

**Fix aplicado:**
```python
# Antes
prob += lpSum(vars_in_slot) <= 1, f"max_one_{slot}"

# Después
if slot == "LEFT_HAND":
    prob += lpSum(vars_in_slot) <= 2, f"max_two_rings"
else:
    prob += lpSum(vars_in_slot) <= 1, f"max_one_{slot}"
```

**Restricción adicional:**
```python
# Prevenir duplicados (mismo nombre base)
if ring1.item_id == ring2.item_id or name1 == name2:
    prob += (vars[ring1] + vars[ring2] <= 1)
```

**Lección:** Verificar estructura de datos real (no asumir RIGHT_HAND existe)

---

## 🎓 Lecciones Aprendidas

### 1. Siempre Verificar Raw Data
- No asumir que el mapeo actual es correcto
- Los Action IDs en raw_data son la fuente de verdad

### 2. Reconstruir Sin Cache
- Docker cachea layers → puede usar código viejo
- SIEMPRE usar `--no-cache` cuando actualizas worker

### 3. Escuchar al Usuario
- El usuario conoce el juego mejor que los datos
- Sus insights sobre patrones (ej: "podría ser penalty") son valiosos

### 4. Verificar Múltiples Rarezas
- Un fix debe funcionar para TODAS las rarezas del item
- Verificar raro, mítico, legendario, reliquia, épico

### 5. Documentar Todo
- Futuros problemas similares se resuelven más rápido
- La documentación ayuda a entrenar nuevos agentes/desarrolladores

---

## 📝 Template de Documentación

Cuando se corrige un problema, crear:

```markdown
# Fix: <NOMBRE_DEL_PROBLEMA>

## Problema
- Item: <NOMBRE>
- Síntoma: Muestra <STAT_INCORRECTO> en vez de <STAT_CORRECTO>

## Investigación
- Action ID: <ID>
- Params: <VALORES>
- Mapeo anterior: <MAPEO_VIEJO>

## Solución
- Nuevo mapeo: <MAPEO_NUEVO>
- Threshold/lógica: <DETALLES>

## Impacto
- Build easy: +<DIFERENCIA>
- Build hard: +<DIFERENCIA>

## Verificación
```sql
<QUERY_VERIFICACION>
```

## Archivos modificados
- worker/fetch_and_load.py: líneas <X-Y>
```

---

## 🚀 Comandos de Referencia Rápida

### Ciclo completo de fix:

```bash
# 1. Investigar
docker-compose exec db psql -U wakfu -d wakfu_builder -c "
SELECT raw_data::jsonb->'definition'->'equipEffects' 
FROM items WHERE item_id = <ID>;
"

# 2. Actualizar código
# Editar worker/fetch_and_load.py o api/app/services/solver.py

# 3. Aplicar fix
docker-compose build --no-cache worker
docker-compose exec db psql -U wakfu -d wakfu_builder -c \
  "DELETE FROM gamedata_versions WHERE version_string = '1.90.1.43';"
docker-compose up -d worker

# 4. Esperar carga (ver logs)
docker-compose logs -f worker
# Ctrl+C cuando veas "Game data loading complete!"

# 5. Reiniciar API
docker-compose restart api

# 6. Verificar
docker-compose exec db psql -U wakfu -d wakfu_builder -c "
SELECT item_id, name_es, stats 
FROM items 
WHERE item_id IN (<IDS>);
"
```

---

## 📚 Recursos Adicionales

### Documentación del Proyecto
- `docs/RING_SYSTEM.md` - Sistema de anillos
- `docs/FIX_DODGE_BERSERK_ISSUE.md` - Caso Dodge/Berserk
- `docs/PROSPECTING_VS_WP_ISSUE.md` - Caso Prospecting/WP
- `TODOS_LOS_FIXES_APLICADOS.md` - Resumen de todos los fixes

### Worker Code Reference
- **Stat map:** `worker/fetch_and_load.py` líneas 139-229
- **Contextual logic:** `worker/fetch_and_load.py` líneas 253-330
- **Penalties handling:** `worker/fetch_and_load.py` líneas 316-329

### Solver Code Reference
- **Constraints:** `api/app/services/solver.py` líneas 240-310
- **Ring system:** `api/app/services/solver.py` líneas 261-285

---

## ⚠️ Precauciones

### NO hacer:
- ❌ Rebuild worker sin `--no-cache` → puede usar código viejo
- ❌ Olvidar borrar gamedata_versions → worker no recargará
- ❌ Olvidar reiniciar API → puede servir datos cacheados
- ❌ Asumir que RIGHT_HAND existe → verificar con query primero

### SÍ hacer:
- ✅ Verificar raw_data antes de asumir
- ✅ Probar con múltiples rarezas
- ✅ Comparar con screenshots del usuario
- ✅ Documentar el proceso y la solución
- ✅ Limpiar archivos temporales al finalizar

---

## 🎯 Resumen Ejecutivo

**Para debugging de stats en Wakfu Builder:**

1. **Comparar:** Screenshot vs Build JSON
2. **Investigar:** raw_data → Action IDs
3. **Analizar:** Worker code → stat_map
4. **Identificar:** Patrón (contextual, penalty, missing)
5. **Fix:** Actualizar mapeo/lógica
6. **Rebuild:** `--no-cache` + borrar version + reload
7. **Verificar:** DB query + build test
8. **Documentar:** Para futuros casos

**Tiempo típico:** 30-60 minutos por problema (incluyendo investigación y verificación)

---

**Creado:** 2025-11-04  
**Basado en:** 4 casos reales resueltos  
**Autor:** AI Assistant (documentando proceso)  
**Uso:** Template para futuros debugging sessions

