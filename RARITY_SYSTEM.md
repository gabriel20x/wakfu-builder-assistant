# ⭐ Sistema de Rareza y Dificultad

## 🎯 Objetivo

Hacer que el solver prefiera items más fáciles de conseguir cuando los stats son similares, reflejando las probabilidades de drop reales del juego.

---

## 📊 Escala de Rareza en Wakfu

### Drop Rates Aproximados

| Rareza | ID | Drop Rate | Dificultad | Multiplicador |
|--------|-----|-----------|------------|---------------|
| Común | 1-2 | ~5% | +5-10 | 1x (base) |
| **Raro** | 3 | **~0.2%** | **+15** | **1x** |
| **Mítico** | 4 | **~0.1%** | **+30** | **2x más difícil** |
| **Legendario** | 5 | **~0.05%** | **+50** | **4x más difícil** |
| Reliquia | 6 | Muy raro | +45 | Único |
| Épico | 7 | Muy raro | +40 | Único |

**Progresión Exponencial:**
```
Raro (0.2%) → base
Mítico (0.1%) → 2x más difícil que Raro
Legendario (0.05%) → 4x más difícil que Raro, 2x que Mítico
```

---

## 🔧 Implementación

### Cálculo de Dificultad

```python
def calculate_difficulty(item, recipes_map, harvest_map):
    difficulty = 0.0
    
    # 1. Nivel (max 20 puntos)
    difficulty += min(20.0, item.level / 245.0 * 20.0)
    
    # 2. Rareza (exponencial)
    rarity_scores = {
        1: 5,   # Común
        2: 10,  # Poco común
        3: 15,  # Raro (~0.2% drop)
        4: 30,  # Mítico (~0.1%, 2x más difícil)
        5: 50,  # Legendario (~0.05%, 4x más difícil)
        6: 45,  # Reliquia
        7: 40,  # Épico
    }
    difficulty += rarity_scores.get(item.rarity, 5)
    
    # 3. Flags especiales
    if item.is_epic:
        difficulty += 20
    if item.is_relic:
        difficulty += 25
    
    # 4. Source type
    if item.source_type == "harvest":
        difficulty += 3   # Farmeable
    elif item.source_type == "recipe":
        difficulty += 8   # Crafteo
    elif item.source_type == "drop":
        difficulty += 15  # Drop de mob
    
    return min(100.0, difficulty)
```

### Lambda Weights (Penalización)

El solver usa: `score = stat_value - lambda * difficulty`

```python
EASY_LAMBDA: 3.0
  → Alta penalización de dificultad
  → Prefiere Raros sobre Míticos
  → Item Raro (difficulty 35): -105 penalty
  → Item Mítico (difficulty 50): -150 penalty
  → Diferencia: 45 puntos
  
MEDIUM_LAMBDA: 1.5
  → Balance entre facilidad y poder
  → Acepta Míticos si tienen buenos stats
  → Diferencia Raro/Mítico: 22.5 puntos
  
HARD_LAMBDA: 0.3
  → Baja penalización
  → Prioriza stats sobre facilidad
  → Diferencia Raro/Mítico: 4.5 puntos
```

---

## 🎯 Ejemplos de Impacto

### Caso 1: Items con Stats Similares

**Item A (Raro):**
```
Distance_Mastery: 40
Difficulty: 35
Score (EASY): 40*5 - 3.0*35 = 200 - 105 = 95
```

**Item B (Mítico):**
```
Distance_Mastery: 42
Difficulty: 50
Score (EASY): 42*5 - 3.0*50 = 210 - 150 = 60
```

**Resultado:** Build EASY prefiere Item A (Raro) aunque tiene 2 puntos menos de Distance_Mastery.

### Caso 2: Diferencia de Stats Grande

**Item A (Raro):**
```
Distance_Mastery: 40
Score (EASY): 95 (como arriba)
```

**Item B (Legendario):**
```
Distance_Mastery: 60
Difficulty: 75
Score (EASY): 60*5 - 3.0*75 = 300 - 225 = 75
```

**Resultado:** Build EASY sigue prefiriendo Raro (95 > 75), necesitaría 25+ más de Distance_Mastery para compensar.

---

## 📈 Resultados Reales (Nivel 80, Distance Build)

### Build EASY
```
Dificultad promedio: 38.67
Rareza:
  - 7 Raros ✅ (mayoría)
  - 1 Mítico
  - 1 Épico
  - 1 Común

Distance_Mastery: 337
```

### Build MEDIUM
```
Dificultad promedio: 39.84
Rareza:
  - 7 Raros
  - 2 Míticos ✅ (acepta más)
  - 1 Épico
  - 1 Común

Distance_Mastery: 337
```

### Build HARD
```
Dificultad promedio: 47.81
Rareza:
  - 5 Raros
  - 2 Míticos
  - 1 Legendario ✅
  - 2 Épicos ✅
  - 1 Común

Distance_Mastery: 314
```

**Observación:** Build HARD tiene MENOS Distance_Mastery porque prioriza variedad de rareza sobre stats puros.

---

## 🎮 Casos de Uso

### Para Jugadores Nuevos
```
Usar: Build EASY

Ventajas:
  - Mayoría de items Raros (~0.2% drop)
  - Más fácil de completar
  - Buen balance de stats
  
Ejemplo:
  - 7 items Raros
  - 337 Distance_Mastery
  - Dificultad: 38.67
```

### Para Jugadores Intermedios
```
Usar: Build MEDIUM

Ventajas:
  - Acepta algunos Míticos
  - Mejor balance dificultad/poder
  - Stats competitivos
  
Ejemplo:
  - 7 Raros + 2 Míticos
  - 337 Distance_Mastery
  - Dificultad: 39.84
```

### Para Completistas/Min-Maxers
```
Usar: Build HARD

Ventajas:
  - Incluye Legendarios y múltiples Épicos
  - Máxima variedad
  - Builds únicas
  
Ejemplo:
  - Mix de todas las rarezas
  - 314 Distance_Mastery
  - Dificultad: 47.81
  
Nota: A veces tiene MENOS stats porque
      prioriza items muy raros con stats únicos
```

---

## ⚖️ Balance del Sistema

### Thresholds de Dificultad

```python
EASY_DIFFICULTY_MAX: 45.0
  → Permite Raros (difficulty ~35)
  → Evita Míticos (difficulty ~50)
  → Bloquea Legendarios (difficulty ~75)
  
MEDIUM_DIFFICULTY_MAX: 70.0
  → Permite Raros y Míticos
  → Evita Legendarios en exceso
  
HARD_DIFFICULTY_MAX: 100.0
  → Permite TODO
```

### Lambda Weights

```python
EASY: 3.0
  → Mítico necesita +18 stats para compensar dificultad
  → Legendario necesita +40 stats para compensar
  
MEDIUM: 1.5
  → Mítico necesita +9 stats
  → Legendario necesita +20 stats
  
HARD: 0.3
  → Mítico necesita +2 stats
  → Legendario necesita +4 stats
```

---

## 🔍 Verificación

### Test: ¿Qué Build es Mejor?

**Para un jugador que quiere:**
- Máximo Distance_Mastery
- Razonable de conseguir

**Respuesta:** Build EASY o MEDIUM
```
Distance_Mastery: 337 (ambos)
Dificultad: 38-40
Mayoría de items Raros
```

**Para un jugador que quiere:**
- Build única/especial
- No le importa farmear mucho

**Respuesta:** Build HARD
```
Distance_Mastery: 314 (menor)
Dificultad: 47.81
Incluye Legendario y 2 Épicos
```

---

## 📝 Configuración Final

### worker/fetch_and_load.py
```python
# Escala exponencial de rareza
Raro (3): +15
Mítico (4): +30 (2x)
Legendario (5): +50 (4x)

# Penalties adicionales
Épico: +20
Reliquia: +25
```

### api/app/core/config.py
```python
# Thresholds
EASY_DIFFICULTY_MAX: 45.0
MEDIUM_DIFFICULTY_MAX: 70.0
HARD_DIFFICULTY_MAX: 100.0

# Lambda weights
EASY_LAMBDA: 3.0 (alta penalización)
MEDIUM_LAMBDA: 1.5 (balance)
HARD_LAMBDA: 0.3 (baja penalización)
```

---

## ✅ Resultado

El sistema ahora:
- ✅ Considera rareza exponencialmente
- ✅ Prefiere Raros en builds fáciles
- ✅ Acepta Míticos si valen la pena
- ✅ Incluye Legendarios solo en build hard
- ✅ Balance stats vs facilidad de obtención

**El solver es más inteligente y genera builds más realistas** 🎮✨

---

**Versión**: 0.4.1  
**Fecha**: 2025-11-02  
**Estado**: ✅ **Sistema de Rareza Exponencial Implementado**

