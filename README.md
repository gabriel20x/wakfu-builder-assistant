# 🎮 Wakfu Builder Assistant

**Genera builds optimizados de equipamiento para Wakfu automáticamente**

Una aplicación web que te ayuda a crear las mejores combinaciones de equipamiento para tu personaje en Wakfu, considerando qué tan difícil es conseguir cada item.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Status](https://img.shields.io/badge/status-active-success)

---

## 📖 ¿Qué hace esta aplicación?

Esta herramienta te ayuda a:
- ✨ **Generar builds automáticamente** - Ya no tienes que buscar item por item
- 🎯 **Optimizar tus stats** - Elige qué stats son importantes para ti
- 📊 **Ver 3 opciones diferentes** - Fácil, Medio y Difícil de conseguir
- 🔍 **Comparar equipamiento** - Ve todos los items de cada build en un solo lugar
- 📱 **Usar desde cualquier dispositivo** - Funciona en PC, tablet y móvil

---

## 🚀 Empezar a Usar (Para Principiantes)

### ¿Qué necesito instalar?

Solo necesitas instalar **2 programas gratuitos**:

1. **Docker Desktop** - Es como una "caja mágica" que ejecuta la aplicación
   - 📥 Descargar: [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)
   - 💻 Disponible para: Windows, Mac, Linux

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
