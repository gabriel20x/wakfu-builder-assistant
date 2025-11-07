# 🎮 Wakfu Builder Assistant

Bienvenido/a a Wakfu Builder Assistant — una aplicación que genera builds óptimos de equipamiento para Wakfu y te ayuda a elegir los mejores items teniendo en cuenta disponibilidad, rareza y preferencias de stats.

Este README ha sido reorganizado para alguien sin conocimientos de programación: pasos claros para ejecutar la aplicación localmente, descripción de módulos principales, mantenimiento básico y notas sobre archivos antiguos que se han limpiado del árbol principal.

Estado del repositorio
- Artículos principales: API (FastAPI), Frontend (Vue 3), Worker (Python), PostgreSQL (Docker)
- Contenedores y configuración: `docker-compose.yml`
- Changelogs: conservados en `docs/changelogs/`

## 1) Ejecutar la aplicación localmente (para NO programadores)

Requisitos mínimos (fáciles):
- Windows/Mac/Linux
- Docker Desktop instalado y funcionando

Pasos (rápidos):

1. Abre Docker Desktop y asegúrate de que esté corriendo.
2. Abre la carpeta del proyecto (por ejemplo, usando el Explorador de archivos).
3. Ejecuta el archivo de comandos según tu sistema:

    - Windows (PowerShell):

       .\deploy.ps1

       Nota: el script `deploy.ps1` guía el proceso y también puede usarse para desplegar. Si prefieres usar Docker manualmente, continúa con el siguiente paso.

    - Alternativa (todas las plataformas) — usando Docker Compose:

       1) Abre una terminal (PowerShell en Windows).
       2) Sitúate en la carpeta del proyecto (la que contiene `docker-compose.yml`).
       3) Ejecuta:

            docker compose up -d --build

       4) Espera a que los contenedores inicien. Verás servicios para `db`, `api`, `frontend` y `worker`.

4. Una vez arriba:

    - Frontend (interfaz web): http://localhost:5173
    - API (documentación OpenAPI/Swagger): http://localhost:8000/docs

5. Para parar los servicios:

    docker compose down

Consejos para principiantes:
- Si Windows te pide permisos, acepta los permisos para Docker.
- Si algún servicio demora en iniciarse (por ejemplo la base de datos), espera 1–2 minutos y vuelve a cargar las URLs.

## 2) Qué hace cada módulo (resumen para no programadores)

He aquí una guía con los módulos principales y su responsabilidad, para entender la arquitectura sin ver código.

- API (carpeta `api/`)
   - Qué: Un servicio web que expone la funcionalidad del generador de builds y la API para el frontend.
   - Funcionalidades: endpoints REST para buscar items, generar builds, administrar metadatos de items, y documentación interactiva (Swagger).
   - Para ver: abre `http://localhost:8000/docs` cuando el proyecto esté corriendo.

- Frontend (carpeta `frontend/`)
   - Qué: Interfaz visual construida con Vue 3.
   - Funcionalidades: generador de builds, visualización del inventario, panel de administración de metadatos y control de items ignorados.
   - Para ver: abre `http://localhost:5173`.

- Worker (carpeta `worker/`)
   - Qué: scripts que procesan y normalizan los datos del juego (JSON), calculan dificultades y cargan items en la base de datos.
   - Funcionalidades: mapeo de Action IDs a stats, sincronización de metadatos, actualizaciones de gfx_id, y recalculación de dificultades.

- Base de datos y migraciones (`migrations/`, `docker-compose.yml`)
   - Qué: PostgreSQL usado para almacenar items, metadatos y caches.
   - Migraciones: SQL para cambios de esquema (por ejemplo `add_gfx_id.sql`).

- Datos del juego (`wakfu_data/`)
   - Qué: Contiene `item_metadata.json`, dumps del gamedata y scripts auxiliares. El worker usa estos archivos para poblar la DB.

- Documentación (`docs/`)
   - Qué: manuales, guías de despliegue, análisis de discrepancias y changelogs.
   - Importante: los changelogs se mantienen en `docs/changelogs/`.

## 3) Qué se hizo con archivos antiguos y tests

Se han limpiado algunos artefactos de verificación y reportes antiguos del árbol principal para que el proyecto sea más sencillo de entender. Esos archivos quedaron documentados en `ARCHIVE/ARCHIVE_SUMMARY.md` (nuevo) en lugar de estar mezclados en la raíz. Los changelogs permanecen en `docs/changelogs/`.

Archivos removidos del raíz o carpeta principal (su contenido está documentado en `ARCHIVE/ARCHIVE_SUMMARY.md`):
- `verify_improvements.py` (script de verificación)
- Tests antiguos en `api/tests/` (archivados en la lista)
- Reportes de sesión/resúmenes (varios `RESUMEN_*.md`, `FINAL_*.md`, `FIXES_*.md`, etc.)

Si prefieres que esos archivos se restauren o se copien dentro de una carpeta `archive/` con su contenido original completo, dime y lo hago.

## 4) Cómo mantener y actualizar datos (operaciones comunes)

- Volver a cargar gamedata completo (worker):

   1) Asegúrate de que la DB esté corriendo y accesible.
   2) Ejecuta el worker que importa los datos (puede hacerse via `docker compose restart worker` o mediante el comando que se haya documentado en `worker/`).

- Aplicar migraciones SQL:

   - Si usas el contenedor del DB: docker compose exec db psql -U wakfu -d wakfu_builder -f /migrations/add_gfx_id.sql

## 5) Despliegue en la nube (opciones rápidas)

- Render.com: se provee `render.yaml` para un blueprint con servicios (db, api, frontend, worker). Recomendado para usuarios sin conocimientos infra.
- Railway / Fly.io: opciones alternativas (más avanzadas).

## 6) Seguridad y notas finales

- No incluyas credenciales sensibles en repositorios públicos.
- Variables de entorno críticas: `DATABASE_URL`, `VITE_API_URL`, `GAMEDATA_PATH`, `CORS_ORIGINS`.

## 7) Soporte y próximos pasos

- ¿Quieres que restauraré algunos reportes y tests antes de borrarlos? (Recomendado: mantener tests en un branch `archive/tests` si no los quieres ejecutar ahora.)
- Puedo también generar un `README_deploy_quick.md` con capturas/screenshot si quieres una guía tipo "paso a paso con imágenes" para un público totalmente no técnico.

---

Gracias — si quieres que haga una copia del README en inglés, o que empaque una versión PDF para enviar a otros, dímelo y lo preparo.


2. **Git** - Para descargar el código de la aplicación
   - 📥 Descargar: [https://git-scm.com/downloads](https://git-scm.com/downloads)
   - 💻 Disponible para: Windows, Mac, Linux

> **💡 Nota para principiantes:** Instala estos programas haciendo doble clic en el instalador y siguiendo los pasos. Puedes dejar todas las opciones por defecto.

---

## 📝 Pasos para Instalar (¡Súper Fácil!)

### Paso 1: Descargar la Aplicación

1. Abre tu **Terminal** o **Símbolo del sistema**:
   - 🪟 **Windows**: Presiona `Win + R`, escribe `cmd` y da Enter
   - 🍎 **Mac**: Presiona `Cmd + Espacio`, escribe `Terminal` y da Enter
   - 🐧 **Linux**: Presiona `Ctrl + Alt + T`

2. Copia y pega este comando (da Enter después):
   ```bash
   git clone https://github.com/gabriel20x/wakfu-builder-assistant.git
   ```

3. Entra a la carpeta descargada:
   ```bash
   cd wakfu-builder-assistant
   ```

### Paso 2: Iniciar la Aplicación

1. Asegúrate de que **Docker Desktop esté abierto** (debe aparecer el icono en tu barra de tareas)

2. Copia y pega este comando:
   ```bash
   docker-compose up -d
   ```

3. **¡Espera 2-3 minutos!** ⏳ 
   - Docker está descargando e instalando todo lo necesario
   - La primera vez tarda un poco más

### Paso 3: ¡Usar la Aplicación! 🎉

1. **Abre tu navegador** (Chrome, Firefox, Edge, Safari, etc.)

2. **Ve a esta dirección**:
   ```
   http://localhost:5173
   ```

3. **¡Ya está!** Deberías ver la aplicación funcionando 🎮

---

## 🎯 Cómo Usar la Aplicación

### Pantalla Principal

La aplicación tiene **3 columnas**:

```
┌────────────────┬──────────────────┬────────────────┐
│   IZQUIERDA    │      CENTRO      │    DERECHA     │
│                │                  │                │
│  Configurar    │  Ver Items       │  Ver Stats     │
│  tu Build      │  Recomendados    │  Totales       │
│                │                  │                │
└────────────────┴──────────────────┴────────────────┘
```

### Paso 1: Configurar tu Build (Columna Izquierda)

1. **Selecciona el nivel de tu personaje**
   - Usa los botones rápidos (50, 100, 150, 200, 230, 245)
   - O ajusta manualmente con los botones +/-

2. **Elige tus preferencias de elementos**
   - Arrastra los elementos para ordenarlos
   - El primer elemento será tu prioridad principal
   - Ejemplo: Si eres Fuego, pon 🔥 Fuego arriba

3. **Marca los stats importantes para ti**
   - ✅ Marca solo los stats que usas
   - Ajusta la importancia con el número (1 = poco importante, 5 = muy importante)
   
   **Ejemplos:**
   - 🔥 DPS Distancia: Marca AP, PM, Dominio de fuego, Dominio distancia
   - 🛡️ Tank: Marca HP, Resistencias, Esquiva
   - 💚 Curandero: Marca AP, WP, Dominio cura

4. **Opciones avanzadas**
   - ✅ Incluir Mascotas (si quieres que considere mascotas)
   - ✅ Incluir Emblemas (si quieres que considere emblemas)

5. **Haz clic en "Generar Builds"** 🚀

### Paso 2: Ver los Resultados (Columna Centro)

Verás **3 pestañas** con diferentes builds:

- **🟢 Fácil**: Items más fáciles de conseguir (drops comunes, craft simple)
- **🟡 Medio**: Balance entre stats y dificultad (algunos items raros)
- **🔴 Difícil**: Máximos stats posibles (items muy difíciles de conseguir)

Cada build muestra:
- 📦 **Items recomendados** (cabeza, pecho, botas, arma, etc.)
- ⭐ **Rareza de cada item** (colores)
- 📊 **Stats que da cada item**
- 🎯 **Dificultad total del build**

### Paso 3: Ver Stats Totales (Columna Derecha)

Aquí ves el **resumen completo** de la build:
- 💚 HP, ⚡ AP, 🏃 PM, 💧 WP (stats principales)
- 🔥💧🌍💨 Dominios elementales
- 🛡️ Resistencias elementales
- ⚔️ Stats de combate (crítico, iniciativa, etc.)
- 📈 Stats secundarios

> **💡 Truco:** Cambia entre las pestañas (Fácil/Medio/Difícil) y verás cómo cambian los stats en tiempo real!

---

## ❓ Preguntas Frecuentes

### ¿Es gratis?
Sí, 100% gratis y de código abierto.

### ¿Necesito crear cuenta?
No, solo abres la página y empiezas a usar.

### ¿Funciona offline?
Sí, una vez que la descargaste, funciona sin internet.

### ¿Qué hago si algo no funciona?
Ve a la sección "Solucionar Problemas" más abajo 👇

### ¿Los datos están actualizados?
Esta versión usa datos del parche **1.90.1.43** de Wakfu.

### ¿Puedo confiar en las builds generadas?
Sí, el algoritmo calcula matemáticamente las mejores combinaciones. Sin embargo, siempre verifica en el juego antes de craftear/comprar.

---

## 🛑 Solucionar Problemas Comunes

### Problema: "Docker no está instalado"
**Solución:**
1. Instala Docker Desktop desde: https://www.docker.com/products/docker-desktop
2. Abre Docker Desktop (debe aparecer el icono de ballena en tu barra)
3. Espera que diga "Docker Desktop is running"
4. Intenta el comando `docker-compose up -d` de nuevo

### Problema: "No puedo abrir http://localhost:5173"
**Solución:**
1. Verifica que Docker Desktop esté corriendo
2. Espera 2-3 minutos después de ejecutar `docker-compose up -d`
3. Intenta con: `http://127.0.0.1:5173`
4. Si no funciona, ejecuta: `docker-compose restart frontend`

### Problema: "La página se ve en blanco"
**Solución:**
1. Presiona `Ctrl + F5` (o `Cmd + Shift + R` en Mac) para recargar
2. Limpia el caché del navegador
3. Intenta con otro navegador (Chrome, Firefox, etc.)

### Problema: "Sale error al generar builds"
**Solución:**
1. Verifica que la API esté funcionando: http://localhost:8000/docs
2. Si no carga, ejecuta: `docker-compose restart api`
3. Espera 1 minuto y vuelve a intentar

### Problema: "Quiero actualizar a la última versión"
**Solución:**
```bash
# 1. Para la aplicación
docker-compose down

# 2. Descarga los cambios nuevos
git pull

# 3. Vuelve a iniciar
docker-compose up -d --build
```

---

## 🛠️ Comandos Útiles

### Iniciar la aplicación
```bash
docker-compose up -d
```

### Detener la aplicación
```bash
docker-compose down
```

### Ver si está funcionando
```bash
docker-compose ps
```

### Ver los logs (para ver qué está pasando)
```bash
docker-compose logs -f
```

### Reiniciar todo (si algo falla)
```bash
docker-compose restart
```

### Eliminar todo y empezar de cero
```bash
docker-compose down -v
docker-compose up -d
```

---

## 🌐 ¿Quieres Poner la App en Internet? (Deploy)

Si quieres que otras personas puedan usar tu aplicación desde internet (sin tener que instalarla), puedes subirla **GRATIS** a servicios en la nube.

### Opción Más Fácil: Render.com (5 minutos)

1. **Crea una cuenta** en https://render.com (gratis)

2. **Sube tu código a GitHub**:
   ```bash
   # Si aún no lo has hecho
   git add .
   git commit -m "Mi build de Wakfu"
   git push
   ```

3. **En Render.com**:
   - Haz clic en "New +" → "Blueprint"
   - Conecta tu repositorio de GitHub
   - Render detectará todo automáticamente
   - Espera 10 minutos

4. **¡Listo!** Tu app estará en: `https://tu-app.onrender.com`

### Otras Opciones Gratuitas:

- **Railway.app** - Muy rápido, $5 créditos gratis/mes
- **Fly.io** - Mejor rendimiento, 3 apps gratis

**📖 Guías Completas:**
- [QUICK_DEPLOY.md](QUICK_DEPLOY.md) - Deploy en 5 minutos (paso a paso con capturas)
- [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) - Guía completa y detallada
- [START_HERE.md](START_HERE.md) - Guía de inicio desde cero

---

## 📊 Estructura del Proyecto (Para Curiosos)

```
wakfu-builder-assistant/
│
├── 🎨 frontend/              → La parte visual (Vue.js)
│   ├── src/
│   │   ├── components/       → Pantallas y botones
│   │   └── services/         → Comunicación con la API
│   └── package.json
│
├── 🔧 api/                   → El cerebro (FastAPI/Python)
│   ├── app/
│   │   ├── routers/          → Rutas de la API
│   │   └── services/         → Lógica del solver
│   └── requirements.txt
│
├── 📦 wakfu_data/            → Datos del juego Wakfu
│   └── gamedata_1.90.1.43/
│
├── 🐳 docker-compose.yml     → Configuración de Docker
└── 📖 README.md              → ¡Este archivo!
```

---

## 🎓 Recursos de Aprendizaje

¿Quieres aprender más sobre cómo funciona?

### Para Principiantes:
- [¿Qué es Docker?](https://docs.docker.com/get-started/) - Tutorial interactivo
- [Git Básico](https://git-scm.com/book/es/v2) - Libro gratis en español
- [Vue.js Curso](https://vuejs.org/tutorial/) - Tutorial oficial

### Documentación Técnica:
- **API Docs**: http://localhost:8000/docs (cuando la app esté corriendo)
- **START_HERE.md** - Explicación técnica completa
- **DEPLOYMENT_GUIDE.md** - Guía de deployment avanzada

---

## 🤝 ¿Quieres Contribuir?

¡Las contribuciones son bienvenidas! Aquí hay algunas formas de ayudar:

### Sin saber programar:
- 🐛 Reporta bugs (cosas que no funcionan)
- 💡 Sugiere nuevas características
- 📖 Mejora la documentación
- ⭐ Dale estrella al proyecto en GitHub

### Si sabes programar:
1. Haz fork del proyecto
2. Crea una rama: `git checkout -b mi-mejora`
3. Haz tus cambios y commit: `git commit -m 'Agrego nueva función'`
4. Push: `git push origin mi-mejora`
5. Abre un Pull Request

---

## 📞 Contacto y Soporte

### ¿Tienes problemas?
1. Revisa la sección "Solucionar Problemas" arriba ☝️
2. Busca en [GitHub Issues](https://github.com/gabriel20x/wakfu-builder-assistant/issues)
3. Abre un nuevo issue si no encuentras solución

### ¿Quieres reportar un bug?
Crea un issue con:
- 📝 Descripción del problema
- 🔢 Pasos para reproducirlo
- 🖼️ Capturas de pantalla (si es posible)
- 💻 Tu sistema operativo (Windows/Mac/Linux)

---

## 📄 Licencia

MIT License - Usa, modifica y comparte libremente.

---

## 🙏 Agradecimientos

- 🎮 **Ankama Games** - Por crear Wakfu
- 🖼️ **tmktahu/WakfuAssets** - Por los iconos y assets
- 💻 **Comunidad Open Source** - Por las herramientas usadas
- 👥 **Comunidad de Wakfu** - Por el feedback y testing

---

## 🌟 ¡Dale una Estrella!

Si te gusta este proyecto, ¡dale una ⭐ en GitHub! Ayuda a que más personas lo encuentren.

---

**Hecho con ❤️ para la comunidad de Wakfu**

**Versión:** 1.0.0 | **Última actualización:** Noviembre 2024
