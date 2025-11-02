# 🔧 Tareas de Implementación - HOMBRERAS (NUEVAS)

## 📋 Resumen Ejecutivo

**Nuevo análisis:** 19 hombreras (nivel 215-245)  
**Discrepancias detectadas:** 111  
**Nuevas tareas identificadas:** 2 CRÍTICAS  

**Reporte completo:** Ver `SHOULDERS_ANALYSIS.md`

---

## 🆕 TAREAS NUEVAS (Críticas - Específicas de SHOULDERS)

### 🔴 Tarea #6: Corregir Dodge → Berserk_Mastery en SHOULDERS (CRÍTICA)
**Archivo:** `worker/fetch_and_load.py`  
**Ubicación:** Donde se maneja Action ID 175 (líneas ~280-290)
**Prioridad:** 🔴 CRÍTICA

**Problema NUEVO:**
- En SHOULDERS, Dodge (incluso con valor ≤100) se extrae como Berserk_Mastery
- Afecta **9/19 hombreras (47%)**
- La lógica contextual actual no considera el SLOT

**Ejemplos de items afectados:**
| Item | Juego | DB (Actual) | Error |
|------|-------|-------------|-------|
| Hombreras crepusculares | 100 Dodge | 100 Berserk_Mastery | ❌ |
| Hombreras ajustables | 95 Dodge | 76 Berserk_Mastery extra | ❌ |
| Hombreras pehese | 152 Dodge | 125 Berserk_Mastery extra | ❌ |
| Las Cegatas ancestrales | 115 Dodge | 96 Berserk_Mastery extra | ❌ |
| Hombreras desperdiciadas | 115 Dodge | 115 Berserk_Mastery extra | ❌ |
| +4 items más... | | | ❌ |

**Causa:**
- Action ID 175 tiene lógica: `valor ≤100 = Dodge`, `valor >100 = Berserk`
- Pero en SHOULDERS, esta lógica falla
- Posiblemente porque en hombreras se usan umbrales diferentes

**Solución propuesta:**
```python
# En worker/fetch_and_load.py
# Buscar donde se maneja Action ID 175

# Lógica ACTUAL (líneas ~280-290):
elif action_id == 175:
    if value <= 100:
        stat_name = "Dodge"
    else:
        stat_name = "Berserk_Mastery"

# CAMBIAR A:
elif action_id == 175:
    if slot == "SHOULDERS":
        # En hombreras, diferentes umbrales
        # Todos los valores observados son Dodge
        if value <= 200:
            stat_name = "Dodge"
        else:
            stat_name = "Berserk_Mastery"
    else:
        # Lógica actual para otros slots
        if value <= 100:
            stat_name = "Dodge"
        else:
            stat_name = "Berserk_Mastery"
```

**Impacto esperado:**
- ✅ Corrige 9 hombreras (47% del slot)
- ✅ Elimina 9 Berserk_Mastery incorrectos
- ✅ Agrega 9 Dodge correctos

---

### 🟡 Tarea #7: Agregar SHOULDERS a range_slots
**Archivo:** `worker/fetch_and_load.py`  
**Ubicación:** Línea 256 (ya modificada)
**Prioridad:** 🟡 ALTA

**Problema:**
- Ya se agregó NECK a range_slots (Tarea #2 completada ✅)
- Pero SHOULDERS también tiene items con Range
- Afecta **2/19 hombreras (11%)**

**Items afectados:**
- Las Cronógrafas: 1 Alcance ❌
- Hombreras de Imagori: 1 Alcance ❌

**Solución propuesta:**
```python
# En worker/fetch_and_load.py, línea 256
# Código ACTUAL (ya modificado):
range_slots = ["FIRST_WEAPON", "SECOND_WEAPON", "HEAD", "NECK"]

# CAMBIAR A:
range_slots = ["FIRST_WEAPON", "SECOND_WEAPON", "HEAD", "NECK", "SHOULDERS"]
```

**Impacto esperado:**
- ✅ Corrige 2 hombreras adicionales
- ✅ Total Range corregidos: 10 amuletos + 2 hombreras = 12 items

---

## 🔍 TAREAS YA COMPLETADAS (Aplican también a Hombreras)

### ✅ Action ID 39: Armor_Given en NECK
**Estado:** IMPLEMENTADO ✅  
**Aplica a Hombreras:** SÍ

Pero necesita extensión:
```python
# Código ACTUAL (líneas 262-267):
elif stat_name == "Heals_Received_or_Armor_Given":
    if slot == "NECK":
        stat_name = "Armor_Given"
    else:
        stat_name = "Heals_Received"

# EXTENDER A:
elif stat_name == "Heals_Received_or_Armor_Given":
    if slot in ["NECK", "SHOULDERS"]:  # ← AGREGAR SHOULDERS
        stat_name = "Armor_Given"
    else:
        stat_name = "Heals_Received"
```

**Items de hombreras que se benefician:**
- Hombreras desperdiciadas: 6% Armor_Given
- Hombreras del clan de Bworkana: 10% Armor_Given
- Hombreras de botones: 10% Armor_Given
- Hombreras de Lacrimorsa: 5% Armor_Given

**Impacto adicional:** ✅ 4 hombreras corregidas

---

### ✅ Action ID 180: Rear_Mastery en NECK
**Estado:** IMPLEMENTADO ✅  
**Aplica a Hombreras:** PARCIALMENTE

**Problema en hombreras:**
- En NECK ya está corregido ✅
- Pero en SHOULDERS, algunos items tienen Rear_Mastery
- Necesita verificar si Action ID 180 en SHOULDERS también es Rear_Mastery

**Items de hombreras afectados:**
- Hombreras crepusculares: 782 Rear_Mastery → DB tiene Lock: 782
- Hombreras pehese: 380 Rear_Mastery → DB tiene Lock: 310 (diferente!)
- Las Cegatas: 372 Rear_Mastery → DB tiene Lock: 325 (diferente!)

**Posible extensión:**
```python
# Código ACTUAL:
elif stat_name == "Lock_or_Rear_Mastery":
    if slot == "NECK":
        stat_name = "Rear_Mastery"
    else:
        stat_name = "Lock"

# POSIBLE EXTENSIÓN (REQUIERE VERIFICACIÓN):
elif stat_name == "Lock_or_Rear_Mastery":
    if slot in ["NECK", "SHOULDERS"]:  # Verificar si aplica
        stat_name = "Rear_Mastery"
    else:
        stat_name = "Lock"
```

⚠️ **ADVERTENCIA:** Requiere verificación porque en hombreras sí hay Lock legítimo en otros items

---

## 🆕 PROBLEMA ADICIONAL DETECTADO

### 🔴 Critical_Hit Negativo → Indirect_Damage
**Archivo:** `worker/fetch_and_load.py`  
**Prioridad:** 🔴 CRÍTICA (aunque afecta 1 item)

**Item afectado:**
- Electrombreras: Juego=-10% Critical_Hit, DB=10% Indirect_Damage

**Problema:**
- Penalties negativos no se manejan correctamente
- El signo negativo se pierde
- Se convierte en otro stat (Indirect_Damage)

**Investigación requerida:**
1. Verificar cómo se parsean valores negativos
2. Identificar si es problema de Action ID o de parsing
3. Asegurar que penalties se preserven con signo negativo

**Impacto:**
- Afecta 1 hombrera conocida
- Potencialmente más items con penalties en otros slots

---

## 📊 Resultados Esperados

### Después de Implementar Tareas #6-7:
- **Discrepancias adicionales resueltas:** ~11/111 hombreras (10%)
- **Total acumulado:** 
  - Amuletos: 34/132 (25.8%)
  - Hombreras: 15/111 (13.5%)
  - **Total:** 49/243 (20.2%)

### Si se extienden las correcciones a SHOULDERS:
- **Armor_Given:** +4 items corregidos
- **Rear_Mastery:** +3 items (requiere verificación)
- **Total potencial:** ~22/111 hombreras (19.8%)

---

## ✅ Checklist de Implementación

### Tareas Nuevas (Hombreras)
- [ ] **Tarea #6:** Dodge → Berserk en SHOULDERS (CRÍTICA) 🔴
- [ ] **Tarea #7:** SHOULDERS en range_slots 🟡
- [ ] **Extensión:** Action ID 39 para SHOULDERS (Armor_Given)
- [ ] **Verificación:** Action ID 180 en SHOULDERS (Rear_Mastery)
- [ ] **Investigación:** Critical_Hit negativo

### Verificación
- [ ] Rebuild worker
- [ ] Recargar DB
- [ ] Re-ejecutar `analyze_shoulders.py`
- [ ] Comparar resultados antes/después
- [ ] Documentar mejoras

---

## 📁 Archivos de Referencia

- **Reporte completo:** `SHOULDERS_ANALYSIS.md`
- **Script de análisis:** `analyze_shoulders.py`
- **Tareas de amuletos:** `IMPLEMENTATION_TASKS.md` (4/5 completadas ✅)
- **Archivo a modificar:** `worker/fetch_and_load.py`

---

## 🎯 Próximos Pasos

1. **Implementar Tarea #6** (Dodge en SHOULDERS) - CRÍTICA
2. **Implementar Tarea #7** (Range en SHOULDERS) - ALTA
3. **Extender Action ID 39** a SHOULDERS
4. **Verificar Action ID 180** en SHOULDERS
5. **Rebuild y verificar** con `analyze_shoulders.py`

---

**Creado por:** Agente Detector de Discrepancias  
**Para:** Agente Actualizador de Worker  
**Fecha:** 2025-11-02  
**Estado:** 🆕 PENDIENTE - 2 tareas críticas nuevas  
**Prioridad:** 🔴 ALTA (47% hombreras afectadas por Tarea #6)

