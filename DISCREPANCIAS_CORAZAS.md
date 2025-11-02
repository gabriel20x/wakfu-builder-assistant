# Discrepancias entre Imágenes y Base de Datos - Corazas Wakfu

## Resumen de Problemas Encontrados

Se encontraron **múltiples discrepancias** entre los stats mostrados en el juego (imágenes) y los stats extraídos de la base de datos. El problema principal es que **faltan mappings de Action IDs**.

---

## Action IDs Faltantes Identificados

### 1. **Action ID 1068** - "Dominio en N elementos"
- **Aparece en:** Ledmadura, Armadutería, Fulguraza, Coraza cúbica, Torso funesto, etc.
- **Parámetros:** `[valor, 0.0, num_elementos, 0.0]`
- **Descripción:** Dominio elemental múltiple. El 3er parámetro indica el número de elementos.

**Ejemplos:**
- Ledmadura: Action ID 1068 con params `[270.0, 0.0, 2.0, 0.0]` → **270 Dominio en 2 elementos**
- Armadutería: Action ID 1068 con params `[260.0, 0.0, 3.0, 0.0]` → **260 Dominio en 3 elementos**
- Fulguraza: Action ID 1068 con params `[202.0, 0.0, 3.0, 0.0]` → **202 Dominio en 3 elementos**

---

### 2. **Action ID 175** - "Esquiva" o "Dodge/Berserk contextual"
- **Aparece en:** Ledmadura, Túnica somera, Coraza de Seraflix, Coraza del maestro jefe, Coraza cúbica, Coraza estelar
- **Parámetros:** `[valor, 0.0]`
- **Descripción:** Parece ser Esquiva (Dodge) en la mayoría de los casos.

**Ejemplos:**
- Ledmadura: Action ID 175 con params `[135.0, 0.0]` → **135 Esquiva**
- Túnica somera: Action ID 175 con params `[90.0, 0.0]` → **90 Esquiva**
- Coraza de Seraflix: Action ID 175 con params `[100.0, 0.0]` → **100 Esquiva**

**NOTA:** En el archivo `worker/fetch_and_load.py` línea 180, dice que 175 es contextual: "Dodge (valores bajos) o Berserk (valores altos)"

---

### 3. **Action ID 149** - Probablemente "Dominio espalda" o "Dominio crítico"
- **Aparece en:** Coraza de Zulnara, Torso funesto
- **Parámetros:** `[valor, 0.0]`

**Ejemplos:**
- Coraza de Zulnara: Action ID 149 con params `[293.0, 0.0]` → Se muestra como "293 Dominio espalda" en imagen
- Torso funesto: Action ID 149 con params `[246.0, 0.0]` → Se muestra como "246 Dominio crítico" en imagen

**PROBLEMA:** El mismo Action ID 149 se interpreta diferente en distintos items. Probablemente es contextual.

---

### 4. **Action ID 71** - "Resistencia crítica" o "Resistencia espalda"
- **Aparece en:** Coraza del Corazón Ardiente ancestal
- **Parámetros:** `[10.0, 0.0]`
- **Imagen muestra:** "10 Resistencia por la espalda"

---

### 5. **Action ID 191** - Desconocido
- **Aparece en:** Coraza del maestro jefe
- **Parámetros:** `[1.0, 0.0, 1.0, 0.0, 0.0, 0.0]` (formato similar a AP/MP/WP)
- **No se muestra en imagen**, podría ser un stat oculto o pasivo.

---

### 6. **Action ID 875** - "Range or Block" → Interpretado como "Anticipación" o "Bloqueo"
- **Aparece en:** Túnica somera, Coraza de Seraflix, Armadutería, Corazón Ardiente
- **Parámetros:** `[valor, 0.0]`

**Ejemplos:**
- Corazón Ardiente: Action ID 875 con params `[6.0, 0.0]` → Imagen muestra "6% de anticipación"
- Armadutería: Action ID 875 con params `[6.0, 0.0]` → Imagen muestra "6% de anticipación"
- Coraza de Seraflix: Action ID 875 con params `[7.0, 0.0]` → Imagen muestra "7 Alcance"

**PROBLEMA:** El mismo Action ID se interpreta como "Anticipación" o "Alcance" dependiendo del contexto.

---

### 7. **Action ID 988** - "Block" → "Resistencia crítica" o "Bloqueo"
- **Aparece en:** Corazón Ardiente ancestal
- **Parámetros:** `[10.0, 0.0]`
- **Imagen muestra:** "10 Resistencia crítica"

---

## Discrepancias Específicas por Item

### **Coraza loca**
| Stat | Imagen | Base de Datos |
|------|--------|---------------|
| Berserk_Mastery | 460 | 0 (pero hay Melee_Mastery: 460) |
| Elemental_Resistance | 50 | 0 (pero hay Critical_Hit: 50) |

**Problema:** La imagen muestra "460 Dominio berserker" y "50 Resistencia elemental", pero en DB aparece como "Melee_Mastery" y "Critical_Hit".

---

### **Ledmadura**
| Stat | Imagen | Base de Datos | Action ID |
|------|--------|---------------|-----------|
| Dodge | 135 | 0 | 175 |
| Dominio_2_elementos | 270 | 0 | 1068 (params[2] = 2) |

**Problema:** No se mapean correctamente los Action IDs 175 y 1068.

---

### **Coraza de Zulnara**
| Stat | Imagen | Base de Datos | Action ID |
|------|--------|---------------|-----------|
| Rear_Mastery | 293 | 293 (pero como "Lock") | 180 + 149 |

**Problema:** El Action ID 180 es "Lock" (Placaje), pero Action ID 149 con el mismo valor (293) podría ser "Rear Mastery" (Dominio espalda). Ambos suman al mismo valor.

---

### **Coraza del Corazón Ardiente ancestal**
| Stat | Imagen | Base de Datos | Action ID |
|------|--------|---------------|-----------|
| Anticipación | 6% | 0 (Range_or_Block: 6) | 875 |
| Dominio_3_elementos | 256 | 0 | 1068 (params[2] = 3) |
| Resistencia elemental | 50 | 0 (Critical_Hit: 50) | 80 |
| Resistencia crítica | 10 | 0 (Block: 10) | 988 |
| Resistencia espalda | 10 | 0 | 71 |

**Problema Múltiple:**
- Action ID 875 se muestra como "6% de anticipación" pero en DB es "Range_or_Block"
- Action ID 1068 no está mapeado
- Action ID 80 se muestra como "Resistencia elemental" pero en DB es "Critical_Hit"
- Action ID 988 se muestra como "Resistencia crítica"
- Action ID 71 no está mapeado

---

### **Armadutería**
| Stat | Imagen | Base de Datos | Action ID |
|------|--------|---------------|-----------|
| Anticipación | 6% | 0 (Range_or_Block: 6) | 875 |
| Dominio_3_elementos | 260 | 0 | 1068 (params[2] = 3) |
| Armadura dada | 10% | 0 (Heals_Received: 10) | 39 |

**Problema:**
- Action ID 39 se interpreta como "Heals_Received" pero imagen muestra "10% de armadura dada"
- Igual que Corazón Ardiente, el Action ID 875 es "Anticipación" pero se mapea como "Range_or_Block"

---

### **Torso funesto**
| Stat | Imagen | Base de Datos | Action ID |
|------|--------|---------------|-----------|
| Dominio_2_elementos | 246 | 0 | 1068 (params[2] = 2) |
| Dominio crítico | 246 | 0 | 149 |

**Problema:** Action ID 149 aquí es "Dominio crítico", pero en Coraza de Zulnara parecía ser "Dominio espalda".

---

## Conclusiones y Recomendaciones

### Problemas Principales:

1. **Action IDs contextuales:** Algunos Action IDs cambian su significado según el item o sus valores:
   - Action ID 149: ¿Dominio espalda o Dominio crítico?
   - Action ID 875: ¿Anticipación, Alcance o Bloqueo?
   - Action ID 80: ¿Critical Hit o Resistencia elemental?
   - Action ID 39: ¿Heals Received o Armadura dada?

2. **Action IDs faltantes:** Varios Action IDs no están en el mapping:
   - Action ID 1068: Dominio en N elementos
   - Action ID 175: Esquiva/Dodge
   - Action ID 71: Resistencia espalda
   - Action ID 191: Desconocido

3. **Interpretación incorrecta de stats:** El juego puede aplicar lógica adicional para mostrar stats que no está reflejada en el simple mapeo de Action IDs.

### Soluciones Propuestas:

1. **Añadir Action IDs faltantes al mapping en `worker/fetch_and_load.py`:**
   ```python
   1068: "Multi_Element_Mastery",  # Params[2] = número de elementos
   175: "Dodge",  # Esquiva (contextual con Berserk)
   149: "Critical_Mastery_or_Rear_Mastery",  # Contextual
   71: "Rear_Resistance",
   191: "Unknown_Passive",
   ```

2. **Implementar lógica contextual:** Algunos stats necesitan interpretación basada en:
   - El tipo de equipo (arma vs armadura)
   - El valor del stat (bajo vs alto para Action ID 175)
   - La presencia de otros stats relacionados

3. **Revisar el archivo `actions.json`:** Este archivo podría tener información adicional sobre cómo interpretar cada Action ID.

---

## Archivo para Investigación

Sería útil revisar: `wakfu_data/gamedata_1.90.1.43/actions.json` para entender mejor la definición de cada Action ID y sus parámetros.

---

**Fecha del análisis:** 2025-11-02  
**Versión del juego:** Wakfu 1.90.1.43

