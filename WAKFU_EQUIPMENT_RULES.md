# ⚔️ Reglas de Equipamiento de Wakfu (v1.90.x)

## 🎯 Reglas Obligatorias para el Solver

### 1. **Slots de Equipamiento**

Un personaje tiene las siguientes ranuras disponibles:

| Slot | Nombre | Cantidad | Notas |
|------|--------|----------|-------|
| `HEAD` | Casco | 1 | - |
| `SHOULDERS` | Hombreras | 1 | - |
| `NECK` | Amuleto | 1 | - |
| `CHEST` | Pechera | 1 | - |
| `LEFT_HAND` | Anillo izquierdo | 1 | No puede repetirse |
| `RIGHT_HAND` | Anillo derecho | 1 | No puede repetirse |
| `BELT` | Cinturón | 1 | - |
| `LEGS` | Botas | 1 | - |
| `BACK` | Capa | 1 | - |
| `FIRST_WEAPON` | Arma principal | 1 | Ver reglas de armas |
| `SECOND_WEAPON` | Arma secundaria | 1 | Ver reglas de armas |
| `PET` | Mascota | 1 | - |
| `MOUNT` | Montura | 1 | - |
| `ACCESSORY` | Emblema | 1 | - |
| `COSTUME` | Insignia/Traje | 1 | Solo cosmético |

**Total: 15 slots**

### 2. **Restricciones de Rareza** ⭐

#### Épicos
- ✅ **Solo 1 épico** por build
- Identificación: `is_epic = true` o `properties contains 21`
- Pueden coexistir con 1 reliquia

#### Reliquias
- ✅ **Solo 1 reliquia** por build
- Identificación: `rarity = 5` o `is_relic = true`
- Pueden coexistir con 1 épico

#### Otros
- Sin límite de comunes, raros, míticos o legendarios

### 3. **Reglas de Anillos** 💍

```python
# RESTRICCIONES:
1. Máximo 2 anillos (LEFT_HAND + RIGHT_HAND)
2. No pueden ser el mismo item_id
3. Algunos anillos épicos/reliquia ocupan AMBOS slots

# IMPLEMENTACIÓN:
if item.slot == "LEFT_HAND":
    # Verificar que no sea el mismo que RIGHT_HAND
    if right_hand_item and right_hand_item.item_id == item.item_id:
        # RECHAZAR
```

### 4. **Reglas de Armas** ⚔️

#### Armas de 1 Mano
- Ocupan solo `FIRST_WEAPON`
- Permiten usar `SECOND_WEAPON` (otra arma o escudo)

#### Armas de 2 Manos
- Ocupan `FIRST_WEAPON` **Y** `SECOND_WEAPON`
- No permiten escudo ni segunda arma
- Identificación: `disabledSlots contains SECOND_WEAPON`

```python
# RESTRICCIÓN:
if weapon_is_two_handed:
    SECOND_WEAPON slot = BLOQUEADO
```

### 5. **Restricción de Nivel** 📊

```python
item.level <= character.level
```

Simple: el personaje debe tener nivel igual o superior al del item.

### 6. **Sin Restricciones por Clase** 🚫

En la versión actual (1.90.x):
- ❌ NO hay restricciones por clase
- ❌ NO hay restricciones por características
- ❌ NO hay restricciones por profesión
- ✅ Cualquier clase puede usar cualquier item

### 7. **Restricciones NO Aplicables** (Obsoletas)

Estas ya no se aplican en versiones modernas:
- ~~Requisitos de características (Fuerza, Inteligencia)~~
- ~~Restricciones por clase~~
- ~~Requisitos de profesión~~
- ~~Requisitos de misión~~

## 🔧 Implementación en el Solver

### Restricciones Actuales (solver.py)

```python
# ✅ IMPLEMENTADO:
- 1 item por slot (excepto anillos)
- Max 1 épico
- Max 1 reliquia
- Level <= level_max

# ❌ FALTA IMPLEMENTAR:
- Anillos no pueden ser duplicados
- Armas de 2 manos bloquean SECOND_WEAPON
- Validación de slots ocupados por armas 2H
```

### Restricciones a Agregar

#### 1. Anillos Únicos
```python
# Constraint: Los dos anillos deben ser diferentes
for item1 in items_left_hand:
    for item2 in items_right_hand:
        if item1.item_id == item2.item_id:
            prob += (item_vars[item1] + item_vars[item2] <= 1)
```

#### 2. Armas de 2 Manos
```python
# Si arma es 2H, bloquear SECOND_WEAPON
for weapon in two_handed_weapons:
    for second_weapon in all_second_weapons:
        prob += (item_vars[weapon] + item_vars[second_weapon] <= 1)
```

## 📋 Checklist de Implementación

### Implementado ✅
- [x] 1 item por slot básico
- [x] Max 1 épico
- [x] Max 1 reliquia
- [x] Level filtering
- [x] Extracción de stats correcta

### Por Implementar ⚠️
- [ ] Anillos no duplicados
- [ ] Armas 2H bloquean segundo slot
- [ ] Detección de armas 2H desde raw_data
- [ ] Validación de slots inválidos

### Optimizaciones Futuras 💡
- [ ] Penalizar items de nivel muy bajo
- [ ] Bonus de sets (si aplica)
- [ ] Preferir items más fáciles en empate
- [ ] Llenar todas las ranuras posibles

## 🎯 Slots del Solver

### Actualmente en el Código
```python
SLOTS = [
    "HEAD", "SHOULDERS", "CHEST", "BACK", "BELT", "LEGS",
    "FIRST_WEAPON", "SECOND_WEAPON",
    "NECK", "LEFT_HAND", "RIGHT_HAND"
]
```

### Falta Agregar
```python
SLOTS = [
    # ... los actuales ...
    "PET",        # Mascota
    "MOUNT",      # Montura
    "ACCESSORY",  # Emblema
    # "COSTUME"   # Solo cosmético, opcional
]
```

## 📝 Notas para Desarrollo

1. **Raw Data Disponible**: Los items tienen `raw_data` con info completa de Wakfu
2. **Disabled Slots**: Verificar `disabledSlots` array para armas 2H
3. **Properties**: Array con flags como épico (ID 21)
4. **Item Type ID**: Puede usarse para validar tipo de arma

## 🚀 Prioridad de Implementación

1. **Alta**: Anillos no duplicados (rompe builds)
2. **Alta**: Armas 2H (rompe builds)
3. **Media**: Agregar PET, MOUNT, ACCESSORY slots
4. **Baja**: Optimizaciones de scoring

---

**Documentado**: 2025-11-01  
**Versión de Wakfu**: 1.90.x  
**Fuente**: Reglas oficiales del juego

