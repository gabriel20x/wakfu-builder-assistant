# Wakfu Builder Assistant - Frontend

Una Single Page Application (SPA) construida con Vue 3 para generar builds optimizados de equipamiento en Wakfu.

## Características

- 🎮 Generación de builds con 3 niveles de dificultad (Fácil, Medio, Difícil)
- 📊 Sistema de priorización de stats personalizable
- 🎨 Interfaz moderna con PrimeVue
- 🔍 Visualización detallada de items y stats
- 📱 Diseño responsivo

## Requisitos

- Node.js 18+ 
- npm o yarn
- Backend API corriendo en `http://localhost:8000`

## Instalación

```bash
# Instalar dependencias
npm install

# Iniciar servidor de desarrollo
npm run dev

# Build para producción
npm run build

# Vista previa del build
npm run preview
```

## Estructura del Proyecto

```
frontend/
├── src/
│   ├── components/          # Componentes Vue
│   │   ├── BuildGenerator.vue   # Componente principal
│   │   ├── BuildResult.vue      # Muestra resultados de builds
│   │   ├── ItemCard.vue         # Card de item individual
│   │   └── ItemStatList.vue     # Lista de stats de item
│   ├── composables/         # Composables y utilidades
│   │   └── useStats.js          # Definiciones de stats y constantes
│   ├── services/            # Servicios de API
│   │   └── api.js               # Cliente API
│   ├── assets/              # Assets estáticos
│   │   └── styles/
│   │       └── main.scss        # Estilos globales
│   ├── App.vue              # Componente raíz
│   └── main.js              # Punto de entrada
├── index.html
├── vite.config.js
└── package.json
```

## Configuración de la API

La aplicación se conecta al backend a través de un proxy configurado en `vite.config.js`:

```javascript
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:8000',
      changeOrigin: true,
    },
  },
}
```

## Uso

1. **Configurar el nivel máximo del personaje** (1-245)
2. **Ajustar las prioridades de stats** (0.0 - 5.0)
   - Valores más altos = mayor prioridad
   - Los stats más priorizados tendrán más peso en la optimización
3. **Generar builds** haciendo clic en el botón
4. **Ver resultados** en las 3 pestañas (Fácil, Medio, Difícil)

### Stats Disponibles

- **HP**: Puntos de Vida
- **AP**: Puntos de Acción  
- **MP**: Puntos de Movimiento
- **WP**: Puntos de Wakfu
- **Critical_Hit**: Golpe Crítico
- **Critical_Mastery**: Dominio Crítico
- **Distance_Mastery**: Dominio Distancia
- **Melee_Mastery**: Dominio de Melé
- **Water/Fire/Earth/Air_Mastery**: Maestrías Elementales

## Personalización

### Agregar nuevos stats

Edita `src/composables/useStats.js`:

```javascript
export const STAT_NAMES = {
  // ... stats existentes
  NEW_STAT: { label: 'Nuevo Stat', icon: 'icon.png' }
}
```

### Cambiar pesos por defecto

Edita `DEFAULT_STAT_WEIGHTS` en `src/composables/useStats.js`:

```javascript
export const DEFAULT_STAT_WEIGHTS = {
  HP: 1.0,
  AP: 2.5,
  // ...
}
```

## Tecnologías

- **Vue 3** - Framework progresivo
- **Vite** - Build tool y dev server
- **PrimeVue** - Biblioteca de componentes UI
- **Axios** - Cliente HTTP
- **SASS** - Preprocesador CSS

## Desarrollo

El proyecto usa Vite con Hot Module Replacement (HMR) para desarrollo rápido.

```bash
npm run dev
```

La aplicación estará disponible en `http://localhost:5173`

## Producción

Para crear un build optimizado:

```bash
npm run build
```

Los archivos optimizados se generarán en el directorio `dist/`

## API Endpoints Utilizados

- `POST /build/solve` - Genera builds optimizados
- `GET /build/history` - Obtiene historial de builds
- `GET /items` - Lista items con filtros
- `GET /items/{id}` - Obtiene detalles de un item

## Licencia

MIT

