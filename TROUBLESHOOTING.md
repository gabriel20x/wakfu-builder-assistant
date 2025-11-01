# 🔧 Guía de Solución de Problemas

## Error: "Port 5432 is already allocated"

**Problema**: Ya tienes PostgreSQL corriendo localmente en el puerto 5432.

**Solución Aplicada**: El `docker-compose.yml` ahora usa el puerto **5433** externamente.

```yaml
ports:
  - "5433:5432"  # Host:Container
```

### Conexiones a la Base de Datos

- **Desde el contenedor API**: `db:5432` (ya configurado) ✅
- **Desde tu máquina local**: `localhost:5433`

### Si quieres conectarte manualmente:

```bash
# Con psql desde tu máquina
psql -h localhost -p 5433 -U wakfu -d wakfu_builder

# Con pgAdmin o similar:
Host: localhost
Port: 5433
User: wakfu
Password: wakfu123
Database: wakfu_builder
```

## Error: "Cannot connect to API"

**Síntomas**: El frontend no puede conectarse al backend.

**Soluciones**:

1. **Verifica que el backend esté corriendo**:
   ```bash
   curl http://localhost:8000/health
   # Debe responder: {"status": "healthy"}
   ```

2. **Verifica los logs**:
   ```bash
   docker logs wakfu_api
   ```

3. **Revisa CORS**: Asegúrate de que `api/app/core/config.py` incluye:
   ```python
   CORS_ORIGINS = "http://localhost:3000,http://localhost:5173"
   ```

## Error: "Module not found" en Frontend

**Síntomas**: Error al importar módulos en Vue.

**Solución**:
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

## Error: Database Connection Failed

**Síntomas**: El API no puede conectarse a PostgreSQL.

**Soluciones**:

1. **Espera a que PostgreSQL esté listo**:
   ```bash
   # Verifica el health check
   docker-compose ps
   # wakfu_db debe mostrar "healthy"
   ```

2. **Reconstruye los contenedores**:
   ```bash
   docker-compose down -v
   docker-compose up -d
   ```

## Error: "No items found" en resultados

**Síntomas**: Los builds no muestran items.

**Posibles causas**:

1. **Base de datos vacía**: No se han cargado los datos del juego
   ```bash
   # Verifica que existe la carpeta
   ls wakfu_data/gamedata_1.90.1.43/
   ```

2. **Nivel demasiado bajo**: Intenta con nivel 230

3. **Stats muy restrictivos**: Reduce las prioridades

## Error: Images not loading

**Síntomas**: Las imágenes de items no cargan.

**Causa**: WakfuAssets no tiene esa imagen específica.

**Solución**: Ya implementado, muestra placeholder automáticamente. Si quieres cambiar el placeholder:

```javascript
// En ItemCard.vue
const onImageError = (event) => {
  event.target.src = 'TU_IMAGEN_AQUI'
}
```

## Frontend no compila

**Error común**: `Cannot find module 'primevue'`

**Solución**:
```bash
cd frontend
npm install primevue primeicons
npm run dev
```

## Docker: "Cannot start service"

**Síntomas**: Docker-compose falla al iniciar.

**Soluciones**:

1. **Limpia todo**:
   ```bash
   docker-compose down -v
   docker system prune -a
   docker-compose up -d
   ```

2. **Verifica Docker está corriendo**:
   ```bash
   docker ps
   ```

3. **Revisa logs específicos**:
   ```bash
   docker logs wakfu_db
   docker logs wakfu_api
   docker logs wakfu_frontend
   ```

## Slow Build Generation

**Síntomas**: Toma más de 10 segundos generar builds.

**Soluciones**:

1. **Reduce el límite de items**: Modifica `api/app/services/solver.py`

2. **Verifica índices en DB**:
   ```sql
   CREATE INDEX idx_items_level ON items(level);
   CREATE INDEX idx_items_slot ON items(slot);
   ```

3. **Aumenta recursos de Docker**:
   - Docker Desktop → Settings → Resources
   - Aumenta CPU y RAM

## CORS Errors en Producción

**Síntomas**: Frontend en producción no puede llamar al API.

**Solución**: Actualiza `CORS_ORIGINS` en `.env`:
```env
CORS_ORIGINS=https://tu-dominio.com,http://localhost:5173
```

## Hot Reload no funciona (Frontend)

**Síntomas**: Los cambios en Vue no se reflejan.

**Solución**:
```bash
# Detén el servidor
# Limpia caché
rm -rf node_modules/.vite
npm run dev
```

## TypeScript Errors (si los hay)

**Nota**: Este proyecto usa JavaScript puro, no TypeScript. Si ves errores de tipos:

```bash
# En frontend/
touch jsconfig.json
```

Contenido:
```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

## Comandos Útiles de Diagnóstico

```bash
# Ver todos los contenedores
docker-compose ps

# Ver logs en tiempo real
docker-compose logs -f

# Reiniciar un servicio específico
docker-compose restart api

# Entrar a un contenedor
docker exec -it wakfu_api /bin/sh

# Ver uso de recursos
docker stats

# Limpiar todo Docker
docker system prune -a --volumes
```

## Verificar Conectividad

```bash
# Desde el contenedor API, conectar a DB
docker exec -it wakfu_api /bin/sh
ping db

# Desde tu máquina, conectar a API
curl http://localhost:8000/docs

# Desde tu máquina, conectar a Frontend
curl http://localhost:5173
```

## ¿Aún tienes problemas?

1. **Revisa los logs completos**:
   ```bash
   docker-compose logs > logs.txt
   ```

2. **Verifica las variables de entorno**:
   ```bash
   docker-compose config
   ```

3. **Abre un issue en GitHub** con:
   - Descripción del error
   - Output de `docker-compose logs`
   - Sistema operativo
   - Versión de Docker

---

**Última actualización**: 2025-01-01

