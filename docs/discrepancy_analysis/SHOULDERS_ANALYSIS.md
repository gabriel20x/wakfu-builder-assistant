# 🔍 Análisis de Hombreras (SHOULDERS)

## 📋 Resumen Ejecutivo
**Fecha:** 2025-11-02  
**Items Analizados:** 19 hombreras (18 nivel 245 + 1 nivel 215)  
**Discrepancias Detectadas:** 111  
**Items Afectados:** 19 (100%)  

---

## 🚨 Hallazgos CRÍTICOS Nuevos

### 🔴 **PROBLEMA #1: Dodge se extrae como Berserk_Mastery**
**Afecta:** 9/19 items (47%)

| Item | Juego | DB |
|------|-------|-----|
| Hombreras crepusculares | 100 Dodge | 100 Berserk ❌ |
| Hombreras ajustables | 95 Dodge | 76 Berserk extra ❌ |
| Hombreras pehese | 152 Dodge | 125 Berserk extra ❌ |
| Las Cegatas ancestrales | 115 Dodge | 96 Berserk extra ❌ |
| Hombreras desperdiciadas | 115 Dodge | 115 Berserk extra ❌ |
| Hombreras del clan | 80 Dodge | 80 Berserk extra ❌ |
| Hombreras de Gabhortom | 115 Dodge | FALTA ❌ |
| Hombreras de botones | 140 Dodge | 130 Berserk extra ❌ |
| Homblelas Empeladol | 103 Dodge | 84 Berserk extra ❌ |
| Las Influenciables | 90 Dodge | 90 Berserk extra ❌ |

**Causa probable:**
- Action ID 175 tiene lógica: valor ≤100 = Dodge, >100 = Berserk
- Pero en SHOULDERS slot, Dodge también se convierte en Berserk incluso con valores ≤100
- **Lógica contextual incorrecta por SLOT**

**Solución:**
```python
# En worker/fetch_and_load.py
# La lógica de Action ID 175 debe considerar el SLOT

if action_id == 175:
    # En SHOULDERS, siempre es Dodge si valor <= 200
    # En otros slots, valor <= 100 = Dodge, > 100 = Berserk
    if slot == "SHOULDERS":
        if value <= 200:
            stat_name = "Dodge"
        else:
            stat_name = "Berserk_Mastery"
    else:
        # Lógica actual
        if value <= 100:
            stat_name = "Dodge"
        else:
            stat_name = "Berserk_Mastery"
```

---

### 🔴 **PROBLEMA #2: Critical_Hit negativo → Indirect_Damage**
**Afecta:** 1 item

| Item | Juego | DB |
|------|-------|-----|
| Electrombreras | -10% Critical_Hit | FALTA ❌ + 10% Indirect_Damage extra |

**Causa probable:**
- Critical_Hit negativo (penalty) no se maneja correctamente
- Se convierte en Indirect_Damage positivo

**Solución:**
```python
# Manejar penalties negativos correctamente
# Verificar si el valor es negativo y preservar el signo
```

---

## ✅ Patrones Confirmados (Iguales que Amuletos)

### 1. **Rear_Mastery → Lock**
**Afecta:** 3 items (16%)
- Hombreras crepusculares: Rear=782 → Lock=782
- Hombreras pehese: Rear=380 → Lock=310 (¡diferente!)
- Las Cegatas: Rear=372 → Lock=325 (¡diferente!)

### 2. **Armor_Given → Heals_Received**
**Afecta:** 4 items (21%)
- Hombreras desperdiciadas: 6% → Heals_Received
- Hombreras del clan: 10% → Heals_Received
- Hombreras de botones: 10% → Heals_Received (extra: 6%)
- Hombreras de Lacrimorsa: 5% → Heals_Received

**Confirmado:** Action ID 39 necesita lógica contextual

### 3. **Healing_Mastery → Armor_Received**
**Afecta:** 1 item (5%)
- Las Influenciables: 274 Healing → 274 Armor_Received

### 4. **Elemental_Resistance Genérica Faltante**
**Afecta:** 14 items (74%)

### 5. **Range Faltante**
**Afecta:** 2 items (11%)
- Las Cronógrafas
- Hombreras de Imagori

**Confirmado:** SHOULDERS no está en weapon_slots

---

## 📊 Estadísticas Completas

### Resumen
- **Total Discrepancias:** 111
- **Stats Faltantes:** 37 (33.3%)
- **Valores Diferentes:** 55 (49.5%)
- **Stats Extra en DB:** 19 (17.1%)

### Desglose de Stats Faltantes
| Stat | Ocurrencias | % Items |
|------|-------------|---------|
| Elemental_Resistance | 14 | 74% |
| Dodge | 9 | 47% 🚨 |
| Armor_Given | 4 | 21% |
| Rear_Mastery | 3 | 16% |
| Range | 2 | 11% |
| Healing_Mastery | 1 | 5% |
| Critical_Hit (negativo) | 1 | 5% 🚨 |
| WP (negativo) | 1 | 5% |

### Stats Extra en DB (No en Juego)
| Stat | Ocurrencias | Causa |
|------|-------------|-------|
| Berserk_Mastery | 9 | ← Dodge mal mapeado 🚨 |
| Lock | 3 | ← Rear_Mastery mal mapeado |
| Heals_Received | 4 | ← Armor_Given mal mapeado |
| Armor_Received | 1 | ← Healing_Mastery mal mapeado |
| Indirect_Damage | 1 | ← Critical_Hit negativo? |
| Prospecting | 1 | ← WP negativo? |

---

## 🎯 Priorización de Correcciones

### 🔴 CRÍTICAS (Nuevas en Hombreras)
1. **Dodge → Berserk_Mastery** (47% hombreras)
   - Lógica contextual de Action ID 175 por SLOT
2. **Critical_Hit negativo** (1 item pero puede afectar más)
   - Manejar penalties negativos

### 🔴 CRÍTICAS (Confirmadas en Múltiples Slots)
3. **Armor_Given → Heals_Received** (21% hombreras, 10% amuletos)
4. **Elemental_Resistance genérica** (74% hombreras, 71% amuletos)
5. **Healing_Mastery → Armor_Received** (5% hombreras, 5% amuletos)

### 🟡 ALTAS
6. **Rear_Mastery → Lock** (16% hombreras, 14% amuletos)
7. **Range faltante** (11% hombreras, 48% amuletos)

---

## 📋 Tareas de Implementación

### Tarea #1: Corregir Dodge en SHOULDERS (NUEVA - CRÍTICA)
```python
# En worker/fetch_and_load.py, modificar Action ID 175

if action_id == 175:
    if slot == "SHOULDERS":
        # En hombreras, umbrales diferentes
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

**Impacto:** 9 items corregidos (47% hombreras)

### Tarea #2: Agregar SHOULDERS a weapon_slots (Range)
```python
weapon_slots = ["FIRST_WEAPON", "SECOND_WEAPON", "HEAD", "NECK", "SHOULDERS"]
```

**Impacto:** 2 items corregidos

### Tarea #3: Manejar Critical_Hit Negativo (NUEVA)
```python
# Preservar el signo negativo en penalties
# Evitar que se convierta en otro stat
```

**Impacto:** 1 item corregido (pero importante para penalties)

### Tareas #4-6: Ya Identificadas en Amuletos
- Action ID 39 contextual (Armor_Given)
- Healing_Mastery mapping
- Rear_Mastery vs Lock

---

## 📈 Comparación: Amuletos vs Hombreras

| Problema | Amuletos | Hombreras | Total |
|----------|----------|-----------|-------|
| Elemental_Resistance faltante | 71% | 74% | 72% 🚨 |
| Dodge → Berserk | 0% | 47% | 24% 🆕 |
| Range faltante | 48% | 11% | 30% |
| Armor_Given → Heals | 10% | 21% | 15% |
| Rear → Lock | 14% | 16% | 15% |
| Healing → Armor | 5% | 5% | 5% |

**Conclusión:** Los problemas son SISTÉMICOS, afectan múltiples slots

---

## 🔗 Referencias

- **Análisis completo de amuletos:** `DISCREPANCY_REPORT.md`
- **Script de análisis:** `analyze_shoulders.py`
- **Archivo a modificar:** `worker/fetch_and_load.py`

---

**Creado:** 2025-11-02  
**Estado:** ✅ Análisis Completo  
**Siguiente:** Agregar 2 tareas nuevas a IMPLEMENTATION_TASKS.md

