# Wakfu Builder Assistant

Una aplicación web completa para generar builds optimizados de equipamiento en Wakfu, considerando la dificultad de obtención de cada item.

## 🎮 Características

- **Generación de Builds Inteligente**: Crea 3 tipos de builds (Fácil, Medio, Difícil) basados en tus prioridades de stats
- **Sistema de Dificultad**: Considera la dificultad de obtención de cada item
- **Optimización Personalizada**: Ajusta el peso de cada stat según tu estilo de juego
- **Interfaz Moderna**: UI responsive y atractiva con Vue 3 y PrimeVue
- **Base de Datos Completa**: Integración con datos oficiales de Wakfu

## 📋 Requisitos

### Backend (API)
- Python 3.10+
- PostgreSQL 13+
- Docker (opcional pero recomendado)

### Frontend
- Node.js 18+
- npm o yarn

## 🚀 Instalación Rápida

### Opción 1: Con Docker (Recomendado)

```bash
# Clonar el repositorio
git clone <repo-url>
cd wakfu-builder-assistant

# Iniciar con docker-compose
docker-compose up -d

# La aplicación estará disponible en:
# Frontend: http://localhost:5173
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Opción 2: Manual

#### 1. Backend Setup

```bash
cd api

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tu configuración

# Iniciar servidor
uvicorn app.main:app --reload
```

#### 2. Frontend Setup

```bash
cd frontend

# Instalar dependencias
npm install

# Iniciar servidor de desarrollo
npm run dev
```

## 📁 Estructura del Proyecto

```
wakfu-builder-assistant/
├── api/                      # Backend (FastAPI)
│   ├── app/
│   │   ├── core/            # Configuración
│   │   ├── db/              # Modelos y database
│   │   ├── routers/         # Endpoints de API
│   │   ├── services/        # Lógica de negocio
│   │   └── main.py          # Punto de entrada
│   ├── tests/               # Tests unitarios
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/                # Frontend (Vue 3)
│   ├── src/
│   │   ├── components/      # Componentes Vue
│   │   ├── composables/     # Composables
│   │   ├── services/        # Servicios API
│   │   ├── assets/          # Assets estáticos
│   │   ├── App.vue
│   │   └── main.js
│   ├── index.html
│   ├── vite.config.js
│   └── package.json
│
├── wakfu_data/              # Datos del juego
│   └── gamedata_1.90.1.43/
│
├── docker-compose.yml
└── README.md
```

## 🔧 Configuración

### Variables de Entorno (Backend)

Crea un archivo `.env` en el directorio `api/`:

```env
DATABASE_URL=postgresql://wakfu:wakfu123@localhost:5432/wakfu_builder
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
GAMEDATA_PATH=../wakfu_data/gamedata_1.90.1.43

# Solver parameters
MAX_EPIC_ITEMS=1
MAX_RELIC_ITEMS=1

# Difficulty thresholds
EASY_DIFFICULTY_MAX=40.0
MEDIUM_DIFFICULTY_MAX=70.0
HARD_DIFFICULTY_MAX=100.0
```

## 📖 Uso

1. **Accede al frontend** en `http://localhost:5173`

2. **Configura tu build**:
   - Selecciona el nivel máximo de tu personaje (1-245)
   - Ajusta las prioridades de stats (0.0 - 5.0)
     - 0.0 = No importante
     - 2.5 = Importante
     - 5.0 = Muy importante

3. **Genera builds** haciendo clic en "Generar Builds"

4. **Revisa los resultados** en las 3 pestañas:
   - **Fácil**: Items más accesibles
   - **Medio**: Balance entre stats y dificultad
   - **Difícil**: Máxima optimización de stats

## 🎯 Stats Disponibles

### Stats Principales
- **HP** (Puntos de Vida)
- **AP** (Puntos de Acción)
- **MP** (Puntos de Movimiento)
- **WP** (Puntos de Wakfu)

### Maestrías Elementales
- Agua, Aire, Tierra, Fuego

### Maestrías Especiales
- Dominio Crítico
- Dominio Espalda
- Dominio de Melé
- Dominio Distancia
- Dominio Cura
- Dominio Berserker

### Otros Stats
- Golpe Crítico
- Anticipación (Block)
- Iniciativa
- Esquiva
- Placaje (Lock)
- Y más...

## 🔌 API Endpoints

### Build Solver
```
POST /build/solve
```
Genera 3 builds optimizados basados en stat weights y nivel máximo.

### Items
```
GET /items                 # Lista items con filtros
GET /items/{item_id}      # Obtiene detalles de un item
POST /items/{item_id}/difficulty  # Actualiza dificultad manual
```

### Game Data
```
GET /gamedata/items       # Obtiene items del gamedata
GET /gamedata/stats       # Información de stats
```

Ver documentación completa en: `http://localhost:8000/docs`

## 🧪 Testing

### Backend
```bash
cd api
pytest
```

### Frontend
```bash
cd frontend
npm run test
```

## 🛠️ Desarrollo

### Ejecutar en modo desarrollo

```bash
# Terminal 1 - Backend
cd api
source venv/bin/activate
uvicorn app.main:app --reload

# Terminal 2 - Frontend
cd frontend
npm run dev
```

### Build para producción

```bash
# Frontend
cd frontend
npm run build

# Los archivos optimizados estarán en frontend/dist/
```

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Notas Técnicas

### Sistema de Dificultad

El sistema calcula la dificultad de obtención de cada item basándose en:
- **Drop items**: Nivel del monstruo + ajuste manual
- **Craft items**: Rareza y nivel del item
- **Quest items**: Dificultad fija media
- **Shop items**: Dificultad baja

### Algoritmo de Optimización

El solver usa una función objetivo que balancea:
- Maximización de stats priorizados
- Minimización de dificultad de obtención
- Restricciones de slots y rareza (máx 1 épico, máx 1 reliquia)

## 📄 Licencia

MIT License - ver archivo LICENSE para más detalles

## 🙏 Agradecimientos

- Datos del juego cortesía de Wakfu
- Iconos e imágenes de [WakfuAssets](https://github.com/tmktahu/WakfuAssets)
- Comunidad de Wakfu por feedback y testing

## 🐛 Reportar Bugs

Si encuentras un bug, por favor abre un issue en GitHub con:
- Descripción del problema
- Pasos para reproducir
- Comportamiento esperado vs actual
- Screenshots si es posible

## 💬 Soporte

¿Tienes preguntas? Abre un issue o contacta a través de [Discord/Email]
