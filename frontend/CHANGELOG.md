# Changelog - Wakfu Builder Assistant Frontend

## [0.2.0] - 2025-11-01

### ✨ Nuevas Características

#### 🌍 Sistema Multiidioma
- Selector de idioma en el header (Español, English, Français)
- Idioma predeterminado: Español
- Persistencia en localStorage
- Nombres de items en 3 idiomas desde la base de datos

#### 📊 Extracción Completa de Stats
- **40+ tipos de stats** extraídos correctamente
- **Maestrías con X elementos**: "12 Maestría (2 elementos)"
- **Valores negativos**: -50 Lock, -50 Dodge se muestran correctamente
- **Resistencias elementales**: Fire, Water, Earth, Air Resistance
- **Stats especiales**: Kit Skill, Armor Given/Received, etc.

### 🐛 Correcciones

#### Backend/Worker
- Mapeo completo de 50+ action IDs de Wakfu
- Manejo de penalties (stats negativos)
- Extracción de maestrías/resistencias aleatorias con múltiples elementos
- Nombres de items en múltiples idiomas
- Filtrado de efectos especiales (estados, mecánicas especiales)

#### Frontend
- Proxy Vite actualizado para Docker (wakfu_api:8000)
- Composable useLanguage para manejo de idiomas
- Labels de stats actualizados en español
- Formato correcto de valores negativos en ItemStatList

### 🔧 Mejoras Técnicas

- Base de datos con columnas multiidioma (name_es, name_en, name_fr)
- Modelo Item actualizado para soportar 3 idiomas
- API response incluye nombres en todos los idiomas
- Frontend solicita idioma preferido

### 📦 Nuevos Archivos

```
frontend/src/composables/useLanguage.js  - Sistema de idiomas
frontend/CHANGELOG.md                     - Este archivo
```

### ⚙️ Archivos Modificados

```
worker/fetch_and_load.py      - 50+ action IDs, multiidioma, penalties
api/app/db/models.py           - Columnas multiidioma
api/app/routers/items.py       - Response con idiomas
frontend/vite.config.js        - Proxy para Docker
frontend/src/composables/useStats.js  - 40+ stats con labels
frontend/src/App.vue           - Selector de idioma
frontend/src/components/ItemCard.vue  - Uso de idiomas
```

## [0.1.0] - 2025-11-01

### 🎉 Lanzamiento Inicial

- SPA con Vue 3 + Vite + PrimeVue
- Generador de builds con 3 niveles de dificultad
- Sistema de priorización de stats personalizable
- Visualización de items con cards estilo WakForge
- Integración completa con backend FastAPI
- Docker support completo
- Sistema de stats básico (12 stats iniciales)

---

## Stats Soportados

### Core (4)
HP, AP, MP, WP

### Maestrías Elementales (5 + variantes)
- Fire/Water/Earth/Air_Mastery
- Elemental_Mastery
- Elemental_Mastery_1/2/3/4_elements

### Maestrías Posicionales (6)
- Critical/Rear/Melee/Distance/Healing/Berserk_Mastery

### Resistencias Elementales (5 + variantes)
- Fire/Water/Earth/Air_Resistance
- Elemental_Resistance
- Elemental_Resistance_1/2/3/4_elements

### Resistencias Especiales (2)
- Critical/Rear_Resistance

### Stats de Combate (10)
- Critical_Hit, Block, Initiative, Dodge, Lock
- Wisdom, Prospecting, Range, Control, Force_Of_Will

### Stats Porcentuales (6)
- Damage_Inflicted, Heals_Performed, Heals_Received
- Armor_Given, Armor_Received, Indirect_Damage

### Otros (2)
- Kit_Skill, Resistance

**Total: 50+ stats diferentes**

---

## Próximas Versiones

### Planeado para 0.3.0
- [ ] Filtros avanzados de items
- [ ] Exportar/Importar builds
- [ ] Comparador de builds lado a lado
- [ ] Historial de búsquedas
- [ ] Sistema de favoritos

### Planeado para 0.4.0
- [ ] Modo análisis (importar build actual)
- [ ] Calculadora de daño
- [ ] Recomendaciones por clase
- [ ] Tooltips detallados con info de enciclopedia
- [ ] Tutorial interactivo

---

**Mantenido por**: Equipo Wakfu Builder  
**Licencia**: MIT

