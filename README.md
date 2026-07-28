# 🎮 Wakfu Builder Assistant

Aplicación web que genera builds óptimos de equipamiento para **Wakfu**, eligiendo los mejores items según disponibilidad, rareza y tus preferencias de stats.

> **⚡ Arquitectura 2026:** la aplicación ahora es **100% estática** — todo corre en tu navegador. No hay backend, ni base de datos, ni Docker. El solver de optimización (MILP) se ejecuta localmente con HiGHS compilado a WebAssembly, los datos del juego se sirven como JSON estático, y tus builds guardados viven en el localStorage de tu navegador.

**Datos del juego:** parche **1.92.1.59** (datos de comunidad — drops de monstruos y mazmorras — del 1.90.1.43).

---

## 🚀 Ejecutar en local

Requisitos: [Node.js](https://nodejs.org) 18+ (con `yarn` o `npm`).

```bash
git clone https://github.com/gabriel20x/wakfu-builder-assistant.git
cd wakfu-builder-assistant/frontend
yarn install
yarn dev
```

Abre **http://localhost:5173** — eso es todo. No hay servicios adicionales que levantar.

### Build de producción

```bash
cd frontend
yarn build      # genera frontend/dist/
yarn preview    # sirve el build en http://localhost:4173
```

### Tests

Los módulos portados de Python (solver, calculadora de daño, presets) tienen suites de paridad verificadas contra el comportamiento del backend original:

```bash
cd frontend
node tests/solver.test.mjs    # 1628 aserciones (incluye integración con items.json real)
node tests/damage.test.mjs
node tests/presets.test.mjs
```

---

## 🧠 Cómo funciona (arquitectura)

```
wakfu_data/gamedata_<versión>/     ← JSON crudos del CDN de Ankama
        │
        ▼  scripts/build_static_data.py  (se corre 1 vez por parche)
frontend/public/data/items.json    ← 7920 items procesados (stats, drops, dificultad)
        │
        ▼  en el navegador
frontend/src/lib/solver/           ← solver MILP (HiGHS WASM, en un Web Worker)
frontend/src/lib/damage/           ← calculadora de daño
frontend/src/lib/presets/          ← presets por clase/rol
frontend/src/services/api.js       ← fachada local (misma interfaz que la vieja API REST)
localStorage                       ← builds guardados y ediciones de metadatos
```

- **Solver:** genera 5 builds por petición (Fácil / Medio / Difícil-Épico / Difícil-Reliquia / Completo) en menos de 1 segundo, respetando restricciones de slots, anillos duplicados, armas a 2 manos y límites de épicos/reliquias.
- **Metadatos manuales:** las ediciones desde la pestaña "Metadatos de Items" se guardan en localStorage como overlay sobre los datos embebidos (exportables a JSON).

---

## 🔄 Actualizar a un nuevo parche de Wakfu

Cuando Ankama publique un parche nuevo:

```bash
# 1. Consulta la versión actual del gamedata
#    https://wakfu.cdn.ankama.com/gamedata/config.json

# 2. Descarga los JSON del CDN (ejemplo con 1.93.x.x)
mkdir wakfu_data/gamedata_<NUEVA_VERSION>
# descarga items.json, actions.json, equipmentItemTypes.json, recipes.json,
# recipeResults.json, recipeIngredients.json, harvestLoots.json,
# collectibleResources.json, itemTypes.json, itemProperties.json, states.json
# desde https://wakfu.cdn.ankama.com/gamedata/<NUEVA_VERSION>/<archivo>.json

# 3. Regenera los datos estáticos
python scripts/build_static_data.py --version <NUEVA_VERSION>

# 4. Verifica y publica
cd frontend && yarn build
git add . && git commit -m "gamedata <NUEVA_VERSION>" && git push
```

> **Nota:** los datos de comunidad (drops de monstruos, mazmorras) provienen de scrapeos que no se pueden regenerar automáticamente. Los items nuevos del parche aparecerán sin fuentes de drop hasta que se actualice esa información (`--community-version` controla qué carpeta de datos de comunidad se usa).

---

## 🌐 Deploy en Vercel

El repo incluye `vercel.json` en la raíz, así que el deploy es directo:

1. Sube el código a GitHub (`git push`).
2. Crea una cuenta en [vercel.com](https://vercel.com) (gratis, entra con GitHub).
3. **Add New → Project** → importa `wakfu-builder-assistant` → **Deploy**.
4. Listo: tu app queda en `https://<tu-proyecto>.vercel.app` y se redeploya sola con cada push.

No hay variables de entorno, bases de datos ni servicios que configurar.

---

## 🎯 Cómo usar la aplicación

La pantalla del generador tiene **3 columnas**: configuración (izquierda), items recomendados (centro) y stats totales (derecha).

1. **Configura tu build**: nivel del personaje, clase y rol (Quick Start autoconfigura los pesos), stats prioritarios y preferencias de elementos.
2. **Genera**: pulsa "Generar Builds" y obtendrás **5 pestañas**:
   - 🟢 **Fácil** — solo items accesibles (raros)
   - 🟡 **Medio** — míticos + 1 legendario + 1 épico/reliquia
   - 🔴 **Difícil (Épico)** — máximos legendarios + 1 épico
   - 🔵 **Difícil (Reliquia)** — máximos legendarios + 1 reliquia
   - ⭐ **Completo** — lo mejor posible (épico + reliquia)
3. **Explora**: cada item muestra stats, rareza, dificultad y fuentes de drop; puedes ignorar items, ver alternativas y guardar builds con nombre (pestaña "Mis Builds").

---

## ❓ Preguntas frecuentes

- **¿Es gratis?** Sí, 100% gratis y open source (MIT).
- **¿Necesito cuenta?** No.
- **¿Funciona offline?** En local sí; la versión web requiere conexión solo para cargar la página e imágenes.
- **¿Puedo confiar en las builds?** El algoritmo optimiza matemáticamente la combinación según tus pesos. Verifica en el juego antes de invertir recursos.
- **¿Dónde se guardan mis builds?** En el localStorage de tu navegador (no hay servidor). Si limpias los datos del navegador, se pierden.

---

## 📁 Estructura del proyecto

```
wakfu-builder-assistant/
├── frontend/                  → La app completa (Vue 3 + Vite)
│   ├── public/data/           → Datos del juego procesados (generados)
│   ├── src/lib/solver/        → Solver MILP portado a JS (HiGHS WASM)
│   ├── src/lib/damage/        → Calculadora de daño portada a JS
│   ├── src/lib/presets/       → Presets de clases portados a JS
│   ├── src/services/          → Fachada API local + dataStore (localStorage)
│   ├── src/workers/           → Web Worker del solver
│   └── tests/                 → Suites de paridad vs Python
├── scripts/build_static_data.py  → Pipeline: gamedata crudo → JSON estático
├── wakfu_data/                → Datos crudos del CDN + datos de comunidad
├── vercel.json                → Config de deploy
│
└── (legacy, ya no se usa en producción)
    ├── api/                   → Antiguo backend FastAPI + solver PuLP
    ├── worker/                → Antiguo ETL a PostgreSQL
    ├── docker-compose.yml     → Antiguo entorno Docker
    └── render.yaml            → Antiguo blueprint de Render
```

Las carpetas legacy se conservan como referencia (el solver Python sigue siendo el "oráculo" contra el que se validó el port), pero no participan en la app.

---

## 🤝 Contribuir

1. Haz fork del proyecto
2. Crea una rama: `git checkout -b mi-mejora`
3. Haz tus cambios y commit
4. Abre un Pull Request

También puedes ayudar reportando bugs o sugiriendo mejoras en [GitHub Issues](https://github.com/gabriel20x/wakfu-builder-assistant/issues).

---

## 📄 Licencia

MIT License — usa, modifica y comparte libremente.

## 🙏 Agradecimientos

- 🎮 **Ankama Games** — por crear Wakfu y publicar su gamedata
- 🖼️ **vertylo/wakassets** y **tmktahu/WakfuAssets** — por los iconos e imágenes
- 👥 **Comunidad de Wakfu** — por los datos de drops, feedback y testing

---

**Hecho con ❤️ para la comunidad de Wakfu**

**Versión:** 2.0.0 (estática) | **Última actualización:** Julio 2026
