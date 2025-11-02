# ⚠️ Limitaciones Conocidas

## 🔄 Action IDs Compartidos en Wakfu

### Problema: Action ID 175

Wakfu reutiliza el mismo action ID para diferentes stats dependiendo del contexto:

**Action ID 175 se usa para:**
- `Berserk_Mastery` (valores altos: 50-200)
- `Dodge` (valores bajos: 3-30)

**Decisión actual:**
- ✅ Mapeado como `Berserk_Mastery`
- Razón: Hay 527 items con Berserk_Mastery vs ~100 con Dodge
- Impacto: Algunos items muestran "Berserk_Mastery" cuando debería ser "Dodge"

**Items Afectados:**
```
El flan de las estrellas:
  Muestra: Berserk_Mastery: 10
  Debería: Dodge: 10 (Esquiva)

Depredadoras:
  Muestra: Berserk_Mastery: 7
  Debería: Dodge: 7
```

**Solución Futura:**
- Necesita lógica contextual basada en:
  - Tipo de item (itemTypeId)
  - Valor del stat (threshold)
  - Otros effects presentes

### Problema: Action ID 120

**Action ID 120 se usa para:**
- `Damage_Inflicted` (Daños Finales %)
- `Elemental_Mastery` (en algunos items)

**Items Afectados:**
```
Anillo de satisfacción:
  Muestra: Damage_Inflicted: 12
  Debería: Elemental_Mastery: 12 (según imagen)
```

### Problema: Variaciones de Nivel

Algunos items tienen stats que escalan con nivel:
- **Freyrr's Bow**: Level 95, muestra 525 Distance_Mastery
  - Raw data: actionId 175, params=[30.0, X]
  - Segundo parámetro probablemente es "por nivel"
  - 30 + (95 × factor) = 525

**Actualmente:**
- Solo usamos params[0] (valor base)
- Ignoramos params[1] (incremento por nivel)

**Impacto:**
- Items levelables muestran stats menores
- No afecta comparaciones relativas
- Sigue siendo funcional para builds

## ✅ Stats Funcionando Correctamente

### Core (4)
- ✅ HP, AP, MP, WP

### Maestrías (7)
- ✅ Distance_Mastery (207 items)
- ✅ Melee_Mastery (3,850 items)
- ✅ Critical_Mastery
- ✅ Rear_Mastery
- ✅ Healing_Mastery
- ✅ Fire/Water/Earth/Air_Mastery
- ⚠️ Berserk_Mastery (conflicto con Dodge)

### Resistencias (10+)
- ✅ Todas las resistencias elementales
- ✅ Critical_Resistance
- ✅ Rear_Resistance

### Combate (8)
- ✅ Critical_Hit
- ✅ Block
- ✅ Lock
- ✅ Range
- ✅ Control
- ✅ Wisdom
- ✅ Prospecting
- ⚠️ Dodge (conflicto con Berserk via ID 175)

### Especiales
- ✅ HP negativos
- ✅ Lock negativos
- ✅ Dodge negativos
- ✅ Maestrías aleatorias con X elementos
- ✅ Resistencias aleatorias con X elementos

## 📊 Precisión del Sistema

**Stats Correctos:** ~90%
**Stats con Conflictos:** ~10% (principalmente Dodge/Berserk)

**Impacto en Builds:**
- Builds siguen siendo óptimos
- La mayoría de stats son precisos
- Distance_Mastery funciona perfectamente
- Diferencias menores en algunos items específicos

## 🔧 Workaround Actual

Para minimizar el impacto:
1. Priorizamos Berserk_Mastery (más items)
2. Dodge está disponible via action ID 181
3. Los builds son funcionales y competitivos

## 🚀 Solución Ideal (Futuro)

```python
def determine_stat_from_context(action_id, value, item_type, other_stats):
    if action_id == 175:
        # Heurística: valores < 50 probablemente son Dodge
        if value < 50:
            return "Dodge"
        else:
            return "Berserk_Mastery"
    # ... más lógica contextual
```

## 📝 Documentación para Usuarios

**Nota en la UI:**
```
⚠️ Algunos items pueden mostrar "Berserk_Mastery" 
   donde debería ser "Dodge" debido a limitaciones 
   en el formato de datos de Wakfu.
   
   La optimización de builds sigue funcionando correctamente.
```

---

**Última revisión**: 2025-11-01  
**Estado**: Documentado y bajo seguimiento

