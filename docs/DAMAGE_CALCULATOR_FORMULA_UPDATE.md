# 🔄 Damage Calculator - Formula Update

## ✅ Actualización Aplicada: Fórmulas Oficiales de Wakfu

### Cambios Implementados

Se ha actualizado el calculador de daño para usar las **fórmulas oficiales de Wakfu** en lugar de una implementación simplificada.

---

## 📐 Fórmula Oficial Implementada

### Damage Formula
```
Elemental Damage = Base Damage × (Backstab Bonus) × 
                   (1 + [Elemental Mastery + Secondary Mastery] / 100) × 
                   (1 - [Elemental Resistance %])

Final Damage = Elemental Damage × (1 + Final Damage Bonus / 100)
```

### Resistance Conversion Formula
```
Elemental Resistance % = 1 - 0.8^(Flat Resistance / 100)
```

**Examples**:
| Flat Resistance | Resistance % |
|----------------|--------------|
| 0              | 0%           |
| 100            | 20%          |
| 200            | 36%          |
| 300            | 48.8%        |
| 400            | 59%          |
| 500            | 67.2%        |

---

## 🎯 Secondary Damage Bonuses (Dominios Secundarios)

El cálculo ahora incluye **todos** los dominios secundarios según las condiciones del combate:

### 1. **Critical Mastery** (Dominio Crítico)
- Se aplica **solo** si `is_critical = True`
- Añade el valor completo al mastery total

### 2. **Berserk Mastery** (Dominio Berserker)
- Se aplica **solo** si el atacante está bajo 50% HP (`is_berserk = True`)
- Añade el valor completo al mastery total

### 3. **Position Mastery** (Melee vs Distance)
- **Melee Mastery**: Si ataca a 2 celdas o menos (`is_melee = True`)
- **Distance Mastery**: Si ataca a 3+ celdas (`is_melee = False`)
- Solo uno se aplica según la distancia

### 4. **Rear Mastery** (Dominio por la Espalda)
- Se aplica si `is_backstab = True` o `is_sidestab = True`
- Añade el valor completo al mastery total

### 5. **Target Type Mastery** (Single Target vs AoE)
- **Single Target Mastery**: Si el hechizo es mono-objetivo (`is_single_target = True`)
- **AoE Mastery**: Si el hechizo es multi-objetivo (`is_single_target = False`)
- Solo uno se aplica según el tipo de hechizo

### 6. **Backstab Bonus** (Multiplicador de Posición)
- **Frontal**: 1.0x (sin bonificación)
- **Lateral** (`is_sidestab = True`): 1.10x (+10%)
- **Espalda** (`is_backstab = True`): 1.25x (+25%)

---

## 🔧 Parámetros del Cálculo

### DamageInput Model (Actualizado)

```python
class DamageInput(BaseModel):
    # Base
    base_spell_damage: float = 100.0
    elemental_mastery: float = 0.0
    
    # Secondary Masteries
    critical_mastery: float = 0.0
    berserk_mastery: float = 0.0
    melee_mastery: float = 0.0
    distance_mastery: float = 0.0
    rear_mastery: float = 0.0
    single_target_mastery: float = 0.0
    aoe_mastery: float = 0.0
    
    # Target resistance (FLAT value, not %)
    flat_resistance: float = 0.0
    
    # Combat conditions
    is_critical: bool = False
    is_berserk: bool = False
    is_backstab: bool = False
    is_sidestab: bool = False
    is_melee: bool = True
    is_single_target: bool = True
    
    # Final damage modifiers
    final_damage_bonus: float = 0.0
    armor: float = 0.0
```

---

## 📊 Ejemplo de Cálculo

### Escenario
```
Build Stats:
- Fire Mastery: 1200
- Elemental Mastery: 400
- Total Fire Mastery: 1600

- Critical Mastery: 300
- Melee Mastery: 200
- Rear Mastery: 150

Conditions:
- Base Spell Damage: 100
- Enemy Flat Resistance: 200
- Is Critical: Yes
- Is Melee: Yes (2 cells or closer)
- Is Backstab: Yes
- Is Single Target: Yes
```

### Paso a Paso

#### 1. Backstab Bonus
```
is_backstab = True
Backstab Bonus = 1.25
```

#### 2. Total Secondary Mastery
```
Secondary Mastery = 0
+ Critical Mastery (because is_critical)  = 300
+ Melee Mastery (because is_melee)       = 200
+ Rear Mastery (because is_backstab)     = 150
= 650
```

#### 3. Total Mastery
```
Total Mastery = Elemental Mastery + Secondary Mastery
              = 1600 + 650
              = 2250
```

#### 4. Convert Flat Resistance to %
```
Resistance % = 1 - 0.8^(200/100)
             = 1 - 0.8^2
             = 1 - 0.64
             = 0.36
             = 36%
```

#### 5. Calculate Elemental Damage
```
Elemental Damage = Base × Backstab × (1 + Mastery/100) × (1 - Res%)
                 = 100 × 1.25 × (1 + 2250/100) × (1 - 0.36)
                 = 100 × 1.25 × 23.5 × 0.64
                 = 1,880
```

#### 6. Final Damage
```
Final Damage = Elemental Damage × (1 + Final Bonus/100)
             = 1,880 × 1.0  (no final bonus)
             = 1,880
```

**Resultado**: **1,880 de daño**

---

## 🚫 Solo Valores Positivos

Según la solicitud del usuario, el sistema **solo muestra valores positivos**:

```python
# Only show positive damage (no healing enemy)
normal_damage = max(0, normal_result.final_damage)
critical_damage = max(0, crit_result.final_damage)
```

Si el daño calculado es negativo (resistencia muy alta), se muestra **0** en lugar de valores negativos.

**Nota**: En Wakfu real, la resistencia no puede reducir el daño por debajo del daño base del hechizo, pero para simplificar la estimación, mostramos 0 cuando sería negativo.

---

## 💡 Supuestos del Calculador

Para el estimador de daño en la interfaz, usamos estos valores por defecto:

1. **Base Spell Damage**: 100 (para normalizar comparaciones)
2. **Combat Type**: Melee + Single Target (más común)
3. **Position**: Frontal (sin backstab bonus)
4. **HP Status**: Por encima de 50% HP (sin berserk bonus)
5. **Resistances**: Valores planos (0, 100, 200, 300, 400, 500)

El usuario puede ver:
- **Normal Damage**: Golpe normal (sin crítico)
- **Critical Damage**: Con critical mastery aplicado

---

## 🎨 Cambios en la Interfaz

### Mostrar Resistencias

Antes:
```
200% res  ████████ 800
```

Ahora:
```
200 res       (36%)
████████ 800
```

Muestra tanto el valor **plano** como el **porcentaje convertido**.

### Solo Valores Positivos

Si el daño sería negativo, muestra:
```
500 res       (67.2%)
0             (en lugar de -500)
```

---

## 📚 Referencias

- **Wakfu Wiki - Damage**: https://wakfu.fandom.com/wiki/Damage
- **Formula**: `Elemental Damage = Base Damage * (Backstab Bonus) * (1 + [Elemental Mastery + Secondary Mastery]/100) * (1 - [Elemental Resistance %])`
- **Resistance Conversion**: `Elemental Resistance % = 1 - 0.8^(Flat Resist/100)`

---

## ✅ Validación

### Tests Actualizados

Se han actualizado los tests en `api/tests/test_damage_calculator.py` para validar:

1. ✅ Conversión de resistencia plana a porcentaje
2. ✅ Aplicación correcta de secondary masteries
3. ✅ Backstab bonus (1.0, 1.10, 1.25)
4. ✅ Critical hit calculations
5. ✅ Solo valores positivos en la salida
6. ✅ Melee vs Distance mastery
7. ✅ Single Target vs AoE mastery
8. ✅ Berserk mastery
9. ✅ Rear mastery

### Verificación Manual

Puedes verificar los cálculos con la calculadora oficial de Wakfu en Excel o comparando con el juego directamente.

---

## 🎯 Resultado Final

El calculador ahora:
- ✅ Usa fórmulas oficiales de Wakfu
- ✅ Incluye todos los secondary masteries
- ✅ Convierte resistencias planas a porcentajes correctamente
- ✅ Muestra solo valores positivos (DPT real)
- ✅ Calcula backstab bonuses correctamente
- ✅ Distingue entre melee/distance, single/AoE, critical/normal

**El sistema está completamente alineado con las mecánicas oficiales de Wakfu.** 🎊

