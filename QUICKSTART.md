# 🚀 Inicio Rápido - Wakfu Builder Assistant

## Para Usuarios de Windows

### Opción 1: Scripts Automáticos

1. **Instala los requisitos**:
   - Node.js 18+ desde [nodejs.org](https://nodejs.org/)
   - Python 3.10+ desde [python.org](https://www.python.org/)
   - PostgreSQL 13+ desde [postgresql.org](https://www.postgresql.org/)

2. **Inicia el Backend**:
   - Doble clic en `start-backend.bat`
   - Espera a que el servidor inicie en http://localhost:8000

3. **Inicia el Frontend** (en otra ventana):
   - Doble clic en `start-frontend.bat`
   - Espera a que el servidor inicie en http://localhost:5173

4. **¡Listo!** Abre tu navegador en http://localhost:5173

### Opción 2: Con Docker

```bash
# Solo necesitas Docker Desktop instalado
docker-compose up -d

# Espera unos segundos y accede a:
# http://localhost:5173
```

## Para Usuarios de Linux/Mac

### Opción 1: Scripts Automáticos

```bash
# Terminal 1 - Backend
chmod +x start-backend.sh
./start-backend.sh

# Terminal 2 - Frontend
chmod +x start-frontend.sh
./start-frontend.sh
```

### Opción 2: Con Docker

```bash
docker-compose up -d
```

## ⚡ Uso Rápido

1. **Abre la aplicación** en http://localhost:5173

2. **Configura tu personaje**:
   ```
   Nivel Máximo: 230 (ajusta según tu nivel)
   ```

3. **Ajusta prioridades de stats**:
   ```
   HP:                1.0 ⭐
   AP:                2.5 ⭐⭐⭐
   MP:                2.0 ⭐⭐
   Critical_Hit:      1.5 ⭐⭐
   Distance_Mastery:  2.0 ⭐⭐
   ```

4. **Genera builds** con el botón "Generar Builds"

5. **Revisa resultados** en las 3 pestañas:
   - **Fácil**: Items fáciles de conseguir
   - **Medio**: Balance entre stats y dificultad
   - **Difícil**: Mejores stats, más difícil de conseguir

## 📊 Interpretación de Resultados

### Dificultad de Items
- 🟢 **0-3**: Muy fácil (drops comunes, tienda)
- 🟡 **3-6**: Medio (craft, dungeons normales)
- 🔴 **6-10**: Difícil (epics, relics, ultimate bosses)

### Stats Totales
Cada build muestra:
- Total de stats principales (HP, AP, MP, WP)
- Total de maestrías elementales
- Total de stats de combate
- Dificultad total del build

### Items Recomendados
Cada card muestra:
- Nombre e imagen del item
- Nivel y slot del equipo
- Todos los stats que otorga
- Fuente de obtención (drop, craft, quest)
- Dificultad individual

## 🎯 Tips para Mejores Builds

1. **Prioriza lo que más usas**:
   - ¿Daño a distancia? → Distance_Mastery alto
   - ¿Tank? → HP y resistencias altos
   - ¿Soporte? → Healing_Mastery alto

2. **AP y MP son valiosos**:
   - Son stats difíciles de conseguir
   - Usa prioridad 2.5+ si los necesitas

3. **Balanceo de Dificultad**:
   - **Build Fácil**: Para empezar rápido
   - **Build Medio**: Para progresar
   - **Build Difícil**: End-game objetivo

4. **Items Épicos/Reliquias**:
   - El sistema limita a 1 de cada
   - Son automáticamente los más potentes

## 🔧 Solución de Problemas

### El backend no inicia
```bash
# Verifica que PostgreSQL esté corriendo
# Windows: Servicios → PostgreSQL
# Linux: sudo systemctl status postgresql

# Verifica que la base de datos existe
psql -U postgres
CREATE DATABASE wakfu_builder;
```

### El frontend muestra error de conexión
```bash
# Verifica que el backend esté corriendo en puerto 8000
# Abre http://localhost:8000/health en tu navegador
# Debería mostrar: {"status": "healthy"}
```

### No se muestran items en los resultados
```bash
# Asegúrate de que los datos del juego estén cargados
# Revisa que existe: wakfu_data/gamedata_1.90.1.43/
```

## 📚 Más Información

- Ver [README.md](README.md) para documentación completa
- Ver [frontend/README.md](frontend/README.md) para docs del frontend
- Ver [api/README.md](api/README.md) para docs del backend (si existe)

## 🆘 ¿Necesitas Ayuda?

1. Revisa la [documentación de la API](http://localhost:8000/docs)
2. Abre un issue en GitHub
3. Contacta al equipo de desarrollo

¡Disfruta creando builds optimizados! 🎮✨
