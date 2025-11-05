# Reorganización Completa del Sistema de Scoring

**Fecha**: 2025-11-05  
**Motivo**: Corrección de duplicación de stats y reorganización según análisis del usuario

---

## 🎯 Problemas Identificados

### 1. **Duplicación de Stats**
Los stats solicitados por el usuario se contaban **DOS veces**:
- En `stat_score`: `Fire_Mastery × 7 (peso usuario) = 2,100 puntos`
- En `item_power`: `Fire_Mastery × 1.5 × 0.1 = 45 puntos`
- **Total**: 2,145 puntos por el MISMO stat ❌

### 2. **Falta de Normalización**
Los stats no se ajustaban según su rareza/frecuencia en items:
- AP (muy raro: 1-2 por item) contaba igual que HP (común: 100-500 por item)

### 3. **Stats Negativos Mal Manejados**
Las penalties por stats negativos no eran proporcionales al impacto

### 4. **Compensaciones Limitadas**
Solo se compensaba AP↔MP, sin considerar Range

---

## ✅ Solución Implementada

### 1. **Sistema de Normalización de Stats**

Todos los stats ahora se multiplican por un **factor de normalización** basado en su rareza:

```python
normalization_factors = {
    # Muy raros (1-2 por item)
    "AP": 100.0,
    "MP": 80.0,
    "Range": 60.0,
    
    # Raros (2-5 por item)
    "Critical_Hit": 20.0,
    "WP": 20.0,
    "Control": 10.0,
    "Block": 5.0,
    
    # Poco comunes (10-50)
    "Critical_Mastery": 2.0,
    "Dodge": 1.0,
    "Lock": 1.0,
    
    # Comunes (20-100)
    "Fire/Water/Earth/Air_Mastery": 1.0,
    "Melee/Distance/Rear/Healing/Berserk_Mastery": 1.0,
    
    # Resistencias (ajustadas según impacto)
    "Fire/Water/Earth/Air_Resistance": 1.2,
    "Elemental_Resistance": 1.5,  # Vale por 4 elementos
    "Critical_Resistance": 1.0,
    "Rear_Resistance": 1.0,
    
    # Extremadamente común (100-500)
    "HP": 0.1,
}
```

### 2. **Score para Stats Solicitados**

```python
if stat_name in stat_weights:
    # Usuario pidió este stat: peso × valor × factor_normalización
    stat_score += stat_value * user_weight * norm_factor
```

**Ejemplo**: Fire_Mastery = 122, user_weight = 7, norm_factor = 1.0
```python
score = 122 × 7 × 1.0 = 854 puntos
```

### 3. **Bonus para Stats NO Solicitados**

```python
if stat_name not in stat_weights:
    # NO lo pidió: pequeño bonus (10% del valor normalizado)
    # EXCEPTO: dominios elementales/secundarios (no contar si no se piden)
    excluded_from_bonus = {"Fire_Mastery", "Water_Mastery", "Earth_Mastery", "Air_Mastery",
                          "Melee_Mastery", "Distance_Mastery", "Rear_Mastery", 
                          "Healing_Mastery", "Berserk_Mastery", "Critical_Mastery"}
    
    if stat_name not in excluded_from_bonus:
        bonus_score += stat_value * norm_factor * 0.1
```

**Ejemplos**:
- HP = 210 (no solicitado): `210 × 0.1 × 0.1 = 2.1 puntos` ✅
- Dodge = 40 (no solicitado): `40 × 1.0 × 0.1 = 4.0 puntos` ✅

**Nota**: Solo dominios elementales y secundarios NO dan bonus si no se solicitan (valores moderados gracias al norm_factor)

### 4. **Penalties por Stats Negativos**

Penalties proporcionales al impacto del stat:

```python
if stat_value < 0:
    if stat_name in ["AP", "MP", "Range"]:
        # Stats críticos negativos: penalty extrema (50x)
        penalty += abs(value) × norm_factor × 50.0
    
    elif stat_name == "WP":
        # WP negativo: penalty severa escalada por nivel (30x)
        level_factor = min(level_max / 100.0, 2.0)
        penalty += abs(value) × norm_factor × level_factor × 30.0
    
    elif stat_name in ["Critical_Hit", "Control", "Block"]:
        # Stats importantes negativos: penalty alta (20x)
        penalty += abs(value) × norm_factor × 20.0
    
    else:
        # Otros stats negativos: penalty moderada (10x)
        penalty += abs(value) × norm_factor × 10.0
```

**Ejemplo**: WP = -1, norm_factor = 20, level = 155
```python
level_factor = 1.55
penalty = 1 × 20 × 1.55 × 30.0 = 930 puntos ❌
```

### 5. **Compensaciones Mejoradas**

Ahora incluye compensación por Range además de AP/MP:

#### Para BACK/NECK (esperan AP):
```python
if ap_value <= 0:
    base_penalty = AP_weight × 200
    
    # Compensación por MP (alta - 40% max)
    if mp_value > 0:
        compensation += min(mp_value × MP_weight × 0.5, base_penalty × 0.4)
    
    # Compensación por Range (menor - 20% max)
    if range_value > 0:
        compensation += min(range_value × Range_weight × 0.3, base_penalty × 0.2)
    
    penalty = base_penalty - compensation
```

#### Para CHEST/LEGS (esperan MP):
```python
if mp_value <= 0:
    base_penalty = MP_weight × 200
    
    # Compensación por AP (alta - 40% max)
    if ap_value > 0:
        compensation += min(ap_value × AP_weight × 0.5, base_penalty × 0.4)
    
    # Compensación por Range (menor - 20% max)  
    if range_value > 0:
        compensation += min(range_value × Range_weight × 0.3, base_penalty × 0.2)
    
    penalty = base_penalty - compensation
```

### 6. **Score Final**

```python
item_score = (
    stat_score              # Stats solicitados × peso × norm_factor
    + power_bonus           # Stats NO solicitados × 0.1
    - negative_penalty      # Penalties por stats negativos
    - missing_stat_penalty  # Falta de AP/MP en slots esperados
    - lambda × difficulty   # Dificultad de farmeo
    + rarity_bonus          # Bonus por rareza (HARD builds)
    + slot_fill_bonus       # Incentivo para llenar slots
)
```

---

## 📊 Ejemplo Completo: Crabby vs Kimono

### User Weights:
- AP: 10, MP: 6
- Fire_Mastery: 7, Earth_Mastery: 7
- Melee_Mastery: 10, Critical_Mastery: 8
- Critical_Hit: 9, Lock: 6

### Crabby Breastplate (Legendario):
**Stats**: AP=1, HP=210, Lock=40, Dodge=40, Fire_Mastery=122, Earth_Mastery=122, Water_Res=69, Air_Res=69

**1. stat_score** (solicitados × peso × norm):
```python
AP: 1 × 10 × 100 = 1,000
Fire_Mastery: 122 × 7 × 1.0 = 854
Earth_Mastery: 122 × 7 × 1.0 = 854
Lock: 40 × 6 × 1.0 = 240
Total stat_score = 2,948
```

**2. power_bonus** (NO solicitados × 0.1):
```python
HP: 210 × 0.1 × 0.1 = 2.1
Dodge: 40 × 1.0 × 0.1 = 4.0
Water_Res: 69 × 1.2 × 0.1 = 8.28
Air_Res: 69 × 1.2 × 0.1 = 8.28
Total power_bonus = 22.66
```

**3. missing_stat_penalty**:
```python
MP faltante: base_penalty = 6 × 200 = 1,200
Compensación AP: min(1 × 10 × 0.5, 480) = 5.0
Net penalty = 1,200 - 5 = 1,195
```

**4. Score Final**:
```python
2,948 + 22.66 - 0 - 1,195 = 1,775.66 puntos
```

### Happy Sram Kimono (Epic):
**Stats**: AP=1, HP=362, Lock=50, Block=8, Fire/Earth/Air_Mastery=88, Elemental_Res=60

**1. stat_score**:
```python
AP: 1 × 10 × 100 = 1,000
Fire_Mastery: 88 × 7 × 1.0 = 616
Earth_Mastery: 88 × 7 × 1.0 = 616
Lock: 50 × 6 × 1.0 = 300
Total stat_score = 2,532
```

**2. power_bonus**:
```python
HP: 362 × 0.1 × 0.1 = 3.62
Block: 8 × 5.0 × 0.1 = 4.0
Elemental_Res: 60 × 1.5 × 0.1 = 9.0
Total power_bonus = 16.62
```
**Nota**: Air_Mastery NO se cuenta en bonus (dominio no solicitado)

**3. missing_stat_penalty**:
```python
MP faltante: base_penalty = 6 × 200 = 1,200
Compensación AP: min(1 × 10 × 0.5, 480) = 5.0
Net penalty = 1,200 - 5 = 1,195
```

**4. Score Final**:
```python
2,532 + 16.62 - 0 - 1,195 = 1,353.62 puntos
```

---

## 🏆 Resultado

**Crabby Breastplate**: 1,775.66 puntos ✅  
**Happy Sram Kimono**: 1,353.62 puntos ❌

**Crabby gana por 422.04 puntos** gracias a mejores stats base.

**Diferencias clave**:
- **Crabby tiene mayor bonus** (+6.04 puntos): Dodge + resistencias con factores ajustados
- **HP SÍ cuenta en bonus** pero con valores moderados gracias al `norm_factor = 0.1`
- **Resistencias elementales ahora valen más** (1.2x vs 0.8x anteriormente)
- **Air_Mastery del Kimono NO cuenta** (dominio no solicitado excluido)

---

## 📝 Cambios en Código

### Archivo: `api/app/services/solver.py`

| Líneas | Cambio |
|--------|--------|
| 253-352 | Sistema completo de normalización + scoring reorganizado |
| 317-335 | Penalties proporcionales por stats negativos |
| 362-393 | BACK/NECK penalties con compensación AP/MP/Range |
| 395-426 | CHEST/LEGS penalties con compensación MP/AP/Range |
| 428 | Eliminado código duplicado de WP penalty |
| 455-464 | Score final con todas las componentes |

---

## ✅ Checklist de Requerimientos Cumplidos

| # | Requerimiento | Status |
|---|---------------|--------|
| 1 | Stats solicitados pasan por normalización | ✅ |
| 2 | Critical_Hit: 20x, Range: 60x, Control: 10x, HP: 0.1x | ✅ |
| 3 | Stats no solicitados: bonus 10% (excepto masteries) | ✅ |
| 4 | Penalties AP faltante con compensación MP/Range | ✅ |
| 5 | Penalties MP faltante con compensación AP/Range | ✅ |
| 6 | Stats negativos con penalties proporcionales | ✅ |
| 7 | Otras anotaciones del código consideradas | ✅ |

---

## 🚀 Próximos Pasos

1. **Reiniciar API** para aplicar cambios
2. **Probar con payload nivel 155** 
3. **Verificar scores** son consistentes y sin duplicación
4. **Confirmar** que Crabby Breastplate gana sobre Kimono cuando ambos faltan MP

---

**Status**: ✅ **COMPLETADO - LISTO PARA TESTING**  
**Versión**: 2.0 - Sistema de Scoring Reorganizado  
**Fecha**: 2025-11-05

