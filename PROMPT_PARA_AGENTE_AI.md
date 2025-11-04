# 🤖 Prompt para Agente AI - Debugging de Stats en Wakfu Builder

**Uso:** Copia este prompt al iniciar un nuevo chat cuando necesites investigar problemas de stats.

---

## 📋 PROMPT PARA COPIAR

```
Soy desarrollador del proyecto Wakfu Builder Assistant. Necesito tu ayuda para investigar y corregir problemas con stats de items.

CONTEXTO DEL SISTEMA:
- Proyecto: Wakfu Builder (generador de builds óptimos para el juego Wakfu)
- Stack: Python FastAPI (backend), Vue 3 (frontend), PostgreSQL (database)
- Docker: worker, api, db, frontend (4 contenedores)
- Worker: Normaliza datos del juego (JSON) → Database
- Solver: Linear Programming para generar builds óptimos

ARQUITECTURA DE STATS:
1. Game Data (items.json) → tiene "equipEffects" con Action IDs
2. Worker (fetch_and_load.py) → mapea Action IDs a nombres de stats
3. Database (items table) → guarda stats como JSON + raw_data original
4. Solver (solver.py) → genera builds usando stats de la DB
5. Frontend → muestra builds generados

ARCHIVOS CLAVE:
- worker/fetch_and_load.py (líneas 139-330): Mapeo de Action IDs a stats
- api/app/services/solver.py (líneas 200-310): Constraints del solver
- Database: tabla items con columnas stats (JSON) y raw_data (JSON)

PROBLEMA REPORTADO:
[Aquí describes el problema con screenshots o JSON]

Ejemplo:
"El item 'Peinado Ror' muestra 'Berserk_Mastery: 70' en mi build, 
pero en el juego muestra '80 Esquiva'. Item ID: 21218"

PROCESO QUE DEBES SEGUIR:

1. INVESTIGAR EN DATABASE:
   - Query stats actuales del item
   - Query raw_data para ver Action IDs y params
   - Verificar múltiples rarezas del mismo item

2. ANALIZAR WORKER CODE:
   - Buscar Action ID en stat_map (worker/fetch_and_load.py)
   - Revisar lógica contextual (thresholds, conditions)
   - Identificar el patrón: ¿contextual? ¿penalty? ¿missing?

3. IDENTIFICAR EL PATRÓN:
   - Stats contextuales: dependen de valor o slot
     Ej: Action 175 → Dodge (< threshold) vs Berserk (>= threshold)
   
   - Penalties: valor positivo en raw_data → stat negativo en DB
     Ej: Action 192 → params [1.0] → WP: -1
     Ej: Action 57 → params [1.0] → MP: -1
   
   - Multi-param: requieren procesamiento especial
     Ej: Action 1068 → params[0] = valor, params[2] = num elementos

4. APLICAR FIX:
   - Actualizar stat_map si es nuevo Action ID
   - Ajustar threshold si es contextual
   - Agregar penalty handling si aplica
   - Modificar solver.py si es problema de constraints

5. REBUILD Y RELOAD (MUY IMPORTANTE):
   ```bash
   # SIEMPRE sin cache
   docker-compose build --no-cache worker
   
   # Limpiar versión para forzar recarga
   docker-compose exec db psql -U wakfu -d wakfu_builder -c \
     "DELETE FROM gamedata_versions WHERE version_string = '1.90.1.43';"
   
   # Iniciar worker
   docker-compose up -d worker
   
   # Ver progreso
   docker-compose logs -f worker
   
   # Reiniciar API
   docker-compose restart api
   ```

6. VERIFICAR:
   - Query DB para confirmar stats corregidos
   - Generar build de prueba
   - Comparar con screenshot original

7. DOCUMENTAR:
   - Crear/actualizar documentación en docs/
   - Actualizar SUMMARY.md
   - Limpiar archivos temporales

IMPORTANTE:
- Usa SIEMPRE '--no-cache' al rebuilder worker
- Borra gamedata_versions antes de reload
- Reinicia API después de reload
- Verifica en DB antes de declarar "fix completo"
- Escucha insights del usuario sobre patrones del juego

COMANDOS ÚTILES:
```bash
# Ver raw_data de un item
docker-compose exec db psql -U wakfu -d wakfu_builder -c "
SELECT raw_data::jsonb->'definition'->'equipEffects' 
FROM items WHERE item_id = <ID>;
"

# Ver stats actuales
docker-compose exec db psql -U wakfu -d wakfu_builder -c "
SELECT item_id, name_es, stats FROM items WHERE item_id = <ID>;
"

# Buscar items por nombre
docker-compose exec db psql -U wakfu -d wakfu_builder -c "
SELECT item_id, name_es, level, rarity FROM items 
WHERE name_es ILIKE '%<nombre>%';
"

# Ver logs del worker
docker-compose logs --tail=20 worker
```

Por favor, sigue este proceso sistemático para investigar y corregir el problema.
```

---

## 📋 Ejemplos de Problemas Comunes

### Template 1: Stat Contextual con Threshold Incorrecto

```
PROBLEMA: El item "X" muestra "StatA: valor" en el build, 
pero en el screenshot del juego muestra "StatB: valor".

INVESTIGACIÓN:
1. Ver raw_data → Action ID <N>, params [<valor>]
2. Ver worker → Action <N>: "StatA_or_StatB"
3. Ver threshold → if stat_value < <THRESHOLD_ACTUAL>
4. Comparar con screenshots → valores reales van hasta <VALOR_MAX>

FIX:
- Actualizar threshold de <VIEJO> a <NUEVO>
- Justificar basándose en valores reales del juego

ARCHIVOS:
- worker/fetch_and_load.py: línea del Action ID + líneas de lógica contextual
```

### Template 2: Penalty Faltante

```
PROBLEMA: El item "X" no muestra penalty de stat Y, 
pero en el screenshot muestra "-1 Y máx."

INVESTIGACIÓN:
1. Ver raw_data → Action ID <N>, params [1.0] (valor positivo)
2. Ver worker → Action <N>: "StatY" o no mapeado
3. Comparar con otros penalties → Pattern: valor positivo → stat negativo

FIX:
- Cambiar mapeo: <N>: "Y_Penalty"
- Agregar handling: stat_name = "Y"; stat_value = -stat_value

ARCHIVOS:
- worker/fetch_and_load.py: stat_map + penalties section
```

### Template 3: Constraint del Solver

```
PROBLEMA: Builds no muestran <COMPORTAMIENTO_ESPERADO>
(ej: 2 anillos, items específicos, etc.)

INVESTIGACIÓN:
1. Ver solver.py → Constraints section
2. Identificar constraint relevante
3. Ver datos en DB → estructura real de slots/items

FIX:
- Actualizar constraint para permitir <COMPORTAMIENTO>
- Agregar restricciones anti-abuse si es necesario

ARCHIVOS:
- api/app/services/solver.py: constraints section
```

---

## 🎯 Checklist de Uso del Prompt

Antes de usar este prompt con un agente AI:

- [ ] Recopilar screenshots del juego mostrando stats correctos
- [ ] Obtener JSON del build mostrando stats incorrectos
- [ ] Identificar item_ids específicos afectados
- [ ] Describir claramente qué stat está mal y cuál debería ser
- [ ] Copiar el prompt completo al chat
- [ ] Proporcionar screenshots e información adicional
- [ ] Estar disponible para proporcionar insights sobre patrones del juego

---

## 💡 Tips para el Usuario

### Cómo Ayudar al Agente

**Proporciona:**
- ✅ Screenshots claros del juego mostrando stats
- ✅ Item IDs si los conoces
- ✅ JSON completo del build generado
- ✅ Nombre exacto de los items (en español)

**Insights valiosos:**
- ✅ "Este stat podría ser un penalty como otros"
- ✅ "En el juego este item tiene valor negativo"
- ✅ "Todos los anillos usan el mismo slot"
- ✅ "Este stat solo aparece en ciertos slots"

**Evita:**
- ❌ "Arregla el sistema" (muy genérico)
- ❌ Solo screenshots sin contexto
- ❌ Asumir que el agente conoce todas las mecánicas de Wakfu

---

## 🔧 Casos de Uso

### Caso 1: Nuevo Problema de Stats
```
[Copiar PROMPT PARA COPIAR completo]

PROBLEMA REPORTADO:
Item "Anillo nuevo X" muestra "StatA: 50" pero debería mostrar "StatB: 50"
Item ID: 12345
Screenshot: [adjuntar]
Build JSON: {"stats": {"StatA": 50}}
```

### Caso 2: Problema de Solver (Constraints)
```
[Copiar PROMPT PARA COPIAR completo]

PROBLEMA REPORTADO:
Las builds no están incluyendo <tipo de item> aunque debería ser posible.
Ejemplo: Solo 1 anillo cuando debería permitir 2.
Build JSON: [adjuntar]
```

### Caso 3: Múltiples Stats Incorrectos
```
[Copiar PROMPT PARA COPIAR completo]

PROBLEMAS REPORTADOS:
1. Item A: Stat1 incorrecto
2. Item B: Stat2 faltante
3. Item C: Stat3 con valor equivocado

Screenshots: [adjuntar todos]
Build JSON: [adjuntar]
```

---

## ✅ Verificación Final

Después de que el agente complete el fix, verifica:

- [ ] Stats corregidos en DB (query de verificación)
- [ ] Build generado muestra stats correctos
- [ ] Total_stats suma correctamente
- [ ] No hay regresiones (otros stats siguen bien)
- [ ] Documentación creada/actualizada
- [ ] Archivos temporales eliminados

---

**Última actualización:** 2025-11-04  
**Versión:** 1.0  
**Casos exitosos:** 4/4 (Dodge, WP, MP, Rings)  
**Efectividad:** 100% ✅

**Este prompt ha sido probado y funciona.** Úsalo con confianza! 🚀

