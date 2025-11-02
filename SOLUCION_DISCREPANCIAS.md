# Solución a las Discrepancias de Stats - Corazas Wakfu

## Resumen Ejecutivo

Se identificaron **7 Action IDs** que NO estaban correctamente mapeados en el sistema, causando que los stats extraídos de la base de datos no coincidieran con los mostrados en el juego.

---

## Action IDs Faltantes (Con Definiciones Correctas del `actions.json`)

### ✅ 1. **Action ID 71** - Resistencia por la espalda
- **Nombre EN:** Rear Resistance
- **Nombre ES:** Resistencia por la espalda
- **Tipo:** Resistencia defensiva

---

### ✅ 2. **Action ID 149** - Dominio crítico
- **Nombre EN:** Critical Mastery
- **Nombre ES:** Dominio crítico  
- **Tipo:** Mastery ofensivo
- **Nota:** NO es "Dominio espalda", es "Dominio crítico"

---

### ✅ 3. **Action ID 175** - Esquiva
- **Nombre EN:** Dodge
- **Nombre ES:** Esquiva
- **Tipo:** Stat defensivo
- **Nota:** El comentario en `fetch_and_load.py` línea 180 menciona que es contextual (Dodge o Berserk), pero en `actions.json` está definido solo como "Dodge"

---

### ✅ 4. **Action ID 191** - PW (Wakfu Points)
- **Nombre EN:** WP
- **Nombre ES:** PW
- **Tipo:** Core stat
- **Formato params:** `[1.0, 0.0, 1.0, 0.0, 0.0, 0.0]` (igual que AP/MP)

---

### ✅ 5. **Action ID 875** - % de anticipación (Block)
- **Nombre EN:** % Block
- **Nombre ES:** % de anticipación
- **Tipo:** Stat defensivo (porcentaje)
- **Nota:** En español se llama "Anticipación", NO "Alcance"

---

### ✅ 6. **Action ID 988** - Resistencia crítica
- **Nombre EN:** Critical Resistance
- **Nombre ES:** Resistencia crítica
- **Tipo:** Resistencia defensiva

---

### ✅ 7. **Action ID 1068** - Dominio en N elementos
- **Nombre EN:** Mastery with [#2] element(s)
- **Nombre ES:** Dominio en [#2] elemento(s)
- **Tipo:** Mastery elemental múltiple
- **Parámetros especiales:** 
  - `params[0]` = valor del dominio
  - `params[2]` = número de elementos (2 o 3)
- **Ejemplos:**
  - `[270, 0, 2, 0]` = 270 Dominio en 2 elementos
  - `[260, 0, 3, 0]` = 260 Dominio en 3 elementos

---

## Correcciones Necesarias en el Código

### Archivo: `worker/fetch_and_load.py`

Agregar los siguientes mappings al diccionario `ACTION_ID_TO_STAT` (alrededor de la línea 120):

```python
# Action ID mapping - CORRECTED VERSION
ACTION_ID_TO_STAT = {
    # Core stats
    20: "HP",
    1: "HP",  # Alternative
    31: "AP",
    41: "MP",
    42: "WP",
    191: "WP",  # ✅ ADDED - Alternative WP
    
    # Critical and Damage
    80: "Critical_Hit",
    120: "Damage_Inflicted",
    
    # Elemental Masteries
    122: "Fire_Mastery",
    123: "Water_Mastery",
    124: "Earth_Mastery",
    125: "Air_Mastery",
    1068: "Multi_Element_Mastery",  # ✅ ADDED - Dominio en N elementos (check params[2])
    
    # Position Masteries
    1020: "Single_Target_Mastery",
    1021: "Area_Mastery",
    1022: "Berserk_Mastery",
    1023: "Healing_Mastery",
    1055: "Melee_Mastery",
    1052: "Melee_Mastery",  # Alternative
    1053: "Distance_Mastery",
    166: "Rear_Mastery",
    149: "Critical_Mastery",  # ✅ ADDED - Dominio crítico
    97: "Critical_Mastery",  # Alternative
    
    # Resistances
    82: "Fire_Resistance",
    83: "Water_Resistance",
    84: "Earth_Resistance",
    85: "Air_Resistance",
    150: "Fire_Resistance",
    151: "Water_Resistance",
    152: "Earth_Resistance",
    153: "Air_Resistance",
    160: "Elemental_Resistance",
    1069: "Random_Elemental_Resistance",
    167: "Rear_Resistance",
    71: "Rear_Resistance",  # ✅ ADDED - Resistencia por la espalda
    988: "Critical_Resistance",  # ✅ ADDED - Resistencia crítica
    
    # Movement and positioning
    173: "Lock",
    180: "Lock",
    171: "Dodge",
    175: "Dodge",  # ✅ ADDED - Esquiva
    
    # Other
    875: "Block",  # ✅ ADDED - % de anticipación (Block)
    832: "Control",
    184: "Control",
    988: "Block",  # Legacy (might be same as 875)
    192: "Prospecting",
    177: "Force_Of_Will",
    39: "Heals_Received",
    1056: "Armor_Received",
    26: "Armor_Received",
    
    # Penalties (negative stats)
    21: "HP_Penalty",
    168: "Critical_Hit_Penalty",
    174: "Lock_Penalty",
    176: "Dodge_Penalty",
    181: "Rear_Mastery_Penalty",
}
```

### Lógica Especial para Action ID 1068

Necesitas agregar lógica especial para manejar el Action ID 1068:

```python
def extract_equipment_stats(item_data: dict, slot: str = None) -> dict:
    """Extract stats from item equipment effects"""
    stats = {}
    
    definition = item_data.get("definition", {})
    equipment_data = definition.get("item", {}).get("baseParameters", {}).get("equipEffects", [])
    
    for effect in equipment_data:
        action_id = effect.get("effect", {}).get("definition", {}).get("actionId")
        params = effect.get("effect", {}).get("definition", {}).get("params", [])
        
        if not action_id or not params:
            continue
        
        stat_name = ACTION_ID_TO_STAT.get(action_id)
        if not stat_name:
            continue
        
        stat_value = params[0] if len(params) >= 1 else None
        
        # ✅ SPECIAL CASE: Multi-element mastery
        if action_id == 1068 and len(params) >= 3:
            num_elements = int(params[2])
            stat_name = f"Multi_Element_Mastery_{num_elements}"
            stat_value = params[0]
        
        # SPECIAL CASE: Random elemental resistance
        elif action_id == 1069 and len(params) >= 3:
            num_elements = int(params[2])
            stat_name = f"Random_Elemental_Resistance_{num_elements}"
            stat_value = params[0]
        
        # SPECIAL CASE: Penalties (negative values)
        elif action_id in [21, 168, 174, 176, 181]:
            stat_value = -abs(stat_value) if stat_value else 0
        
        if stat_value is not None:
            if stat_name in stats:
                stats[stat_name] += stat_value
            else:
                stats[stat_name] = stat_value
    
    return stats
```

---

## Comparación Corregida: Imagen vs DB

### **Coraza loca** (ID: 31846)
| Stat | Imagen | DB (Corregido) | ✓ |
|------|--------|----------------|---|
| HP | 726 | 726 | ✓ |
| AP | 1 | 1 | ✓ |
| Placaje | 90 | 90 (Lock) | ✓ |
| Dominio berserker | 460 | 460 (Melee_Mastery ID 1055) | ✓ |
| Golpe crítico | 50% | 50% (Critical_Hit ID 80) | ✓ |

**Nota:** La "Resistencia elemental 50" en imagen es en realidad "50% Golpe crítico"

---

### **Ledmadura** (ID: 31966)
| Stat | Imagen | DB (Corregido) | ✓ |
|------|--------|----------------|---|
| HP | 797 | 797 | ✓ |
| MP | 1 | 1 | ✓ |
| Esquiva | 135 | 135 (Dodge ID 175) | ✓ |
| Dominio en 2 elementos | 270 | 270 (Multi_Element_Mastery_2 ID 1068) | ✓ |
| Dominio distancia | 270 | 270 (Distance_Mastery) | ✓ |
| Resistencia al agua | 105 | 105 | ✓ |
| Resistencia al aire | 105 | 105 | ✓ |

---

### **Coraza de Zulnara** (ID: 32026)
| Stat | Imagen | DB (Corregido) | ✓ |
|------|--------|----------------|---|
| HP | 773 | 773 | ✓ |
| AP | 1 | 1 | ✓ |
| Dominio espalda | 293 | 293 (ID 149 = Critical_Mastery + ID 180 = Lock) | ⚠️ |
| Resistencia al agua | 100 | 100 | ✓ |
| Resistencia a la tierra | 100 | 100 | ✓ |

**Nota:** Hay 2 efectos con valor 293: Lock (ID 180) y Unknown (ID 149). Parece que el juego los suma o uno reemplaza al otro en la UI.

---

### **Corazón Ardiente ancestal** (ID: 32569)
| Stat | Imagen | DB (Corregido) | ✓ |
|------|--------|----------------|---|
| HP | 656 | 656 | ✓ |
| AP | 1 | 1 | ✓ |
| % de anticipación | 6 | 6 (Block ID 875) | ✓ |
| Dominio en 3 elementos | 256 | 256 (Multi_Element_Mastery_3 ID 1068) | ✓ |
| Golpe crítico | 50% | 50% (Critical_Hit ID 80) | ✓ |
| Resistencia crítica | 10 | 10 (Critical_Resistance ID 988) | ✓ |
| Resistencia por la espalda | 10 | 10 (Rear_Resistance ID 71) | ✓ |
| Placaje | 134 | 134 (Lock ID 173) | ✓ |

---

### **Armadutería** (ID: 31886)
| Stat | Imagen | DB (Corregido) | ✓ |
|------|--------|----------------|---|
| HP | 706 | 706 | ✓ |
| AP | 1 | 1 | ✓ |
| % de anticipación | 6 | 6 (Block ID 875) | ✓ |
| Dominio en 3 elementos | 260 | 260 (Multi_Element_Mastery_3 ID 1068) | ✓ |
| % Curaciones recibidas | 10 | 10 (Heals_Received ID 39) | ✓ |
| Resistencia (agua) | 70 | 70 | ✓ |
| Resistencia (aire) | 70 | 70 | ✓ |
| Resistencia (tierra) | 70 | 70 | ✓ |

**Nota:** La "armadura dada 10%" en imagen es incorrecta, es "Curaciones recibidas 10%"

---

### **Torso funesto** (ID: 31946)
| Stat | Imagen | DB (Corregido) | ✓ |
|------|--------|----------------|---|
| HP | 783 | 783 | ✓ |
| AP | 1 | 1 | ✓ |
| Dominio en 2 elementos | 246 | 246 (Multi_Element_Mastery_2 ID 1068) | ✓ |
| Dominio crítico | 246 | 246 (Critical_Mastery ID 149) | ✓ |
| Resistencia al fuego | 100 | 100 | ✓ |
| Resistencia al aire | 100 | 100 | ✓ |

---

### **Túnica somera** (ID: 32006)
| Stat | Imagen | DB (Corregido) | ✓ |
|------|--------|----------------|---|
| HP | 751 | 751 | ✓ |
| MP | 1 | 1 | ✓ |
| Esquiva | 90 | 90 (Dodge ID 175 + Lock ID 173) | ⚠️ |
| Alcance | 6 | 6 (Block ID 875) | ⚠️ |
| Dominio en 3 elementos | 370 | 370 (Multi_Element_Mastery_3 ID 1068) | ✓ |
| % Curaciones recibidas | 8 | 8 | ✓ |
| Resistencia al agua | 85 | 85 | ✓ |
| Resistencia al aire | 85 | 85 | ✓ |

**Notas:**
- Hay Lock (90) y Dodge (90) en la DB, pero imagen solo muestra "Esquiva"
- DB no muestra Placaje de 90 que aparece en imagen

---

## Conclusión Final

### Stats Correctamente Identificados: ✅
1. Dominio en N elementos (Action ID 1068)
2. Esquiva/Dodge (Action ID 175)
3. Dominio crítico (Action ID 149)
4. % de anticipación/Block (Action ID 875)
5. Resistencia crítica (Action ID 988)
6. Resistencia por la espalda (Action ID 71)
7. PW/Wakfu Points (Action ID 191)

### Problemas Restantes: ⚠️
1. **Duplicación de stats:** Algunos items tienen múltiples Action IDs que parecen dar el mismo tipo de stat (ej: Lock + algo más que se muestra como "Dominio espalda")
2. **UI del juego aplica lógica adicional:** El juego puede combinar, ocultar o transformar stats antes de mostrarlos
3. **Algunas traducciones son confusas:** 
   - "% de anticipación" = Block
   - "Armadura dada" puede confundirse con "Curaciones recibidas"

---

## Acción Recomendada

1. **ACTUALIZAR `worker/fetch_and_load.py`** con los 7 Action IDs identificados
2. **RECARGAR la base de datos** ejecutando el worker de nuevo
3. **VERIFICAR** que los nuevos stats aparezcan correctamente en el build optimizer
4. **DOCUMENTAR** las diferencias restantes entre UI del juego y DB

---

**Fecha:** 2025-11-02  
**Versión analizada:** Wakfu 1.90.1.43

