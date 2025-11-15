# 🚀 Instrucciones de Deployment a Render

## Paso 1: Crear Release en GitHub (Manual)

El archivo `wakfu_data.tar.gz` (4.5MB) está listo en la raíz del proyecto.

### Opción A: Usando la interfaz web de GitHub (RECOMENDADO)

1. Ve a: https://github.com/gabriel20x/wakfu-builder-assistant/releases
2. Click en **"Draft a new release"**
3. **Tag version**: `v1.0.0-gamedata`
4. **Release title**: `Wakfu Game Data v1.0.0`
5. **Description**: 
   ```
   Complete wakfu_data folder with gamedata, item metadata, and processed data.
   Use this for production deployments on Render.
   ```
6. **Assets**: Arrastra y suelta `wakfu_data.tar.gz`
7. Click en **"Publish release"**

### Opción B: Usando GitHub CLI

```bash
cd c:\Users\Lixnard\WebstormProjects\wakfu-builder-assistant
gh auth login  # Autenticarse si es necesario
gh release create v1.0.0-gamedata wakfu_data.tar.gz --title "Wakfu Game Data v1.0.0" --notes "Complete wakfu_data folder"
```

---

## Paso 2: Verificar que los Dockerfiles estén actualizados

Los Dockerfiles ya han sido actualizados para descargar automáticamente `wakfu_data` desde GitHub Releases.

✅ `api/Dockerfile.prod` - Descarga datos en el build
✅ `worker/Dockerfile` - Descarga datos en el build

---

## Paso 3: Deployar en Render

1. Ve a: https://render.com
2. Si no tienes cuenta, regístrate (usa GitHub)
3. En el Dashboard, click en **"New +"** → **"Blueprint"**
4. Selecciona **"Public Git Repository"**
5. Pega: `https://github.com/gabriel20x/wakfu-builder-assistant`
6. Click en **"Connect"**
7. Render detectará automáticamente `render.yaml`
8. Review la configuración y click en **"Deploy"**

### Servicios que se crearán:
- 🗄️ **wakfu-db** (PostgreSQL)
- 🔌 **wakfu-api** (FastAPI)
- 🎨 **wakfu-frontend** (Vue 3)
- 🔄 **wakfu-worker** (Background tasks)

---

## Paso 4: Esperar y verificar

⏱️ **Tiempo estimado**: 5-10 minutos

Una vez deployado:
- Frontend: `https://wakfu-frontend.onrender.com`
- API Docs: `https://wakfu-api.onrender.com/docs`

---

## 🔧 Solución de problemas

### Los contenedores no tienen datos
- ✅ Verifica que el Release `v1.0.0-gamedata` exista en GitHub
- ✅ Confirma que `wakfu_data.tar.gz` está en el Release

### Error al descargar gamedata
- ✅ El URL en Dockerfiles está correcto
- ✅ GitHub no está bloqueado

### Render dice "Invalid Dockerfile"
- ✅ Los Dockerfiles están válidos (ya verificados)
- ✅ Trigger un redeploy manual en Render

---

## 📝 Notas importantes

1. **Free tier de Render**: La BD caduca después de 90 días. Upgrade o recrea.
2. **Primer deploy es más lento**: Los contenedores descargan ~100MB de datos.
3. **Worker debe completar**: Espera a que el worker procese los datos antes de usar la app.

---

## ✅ Resumen de cambios realizados

- ✅ Comprimida toda `wakfu_data/` en `wakfu_data.tar.gz` (4.5MB)
- ✅ Actualizado `api/Dockerfile.prod` para descargar datos
- ✅ Actualizado `worker/Dockerfile` para descargar datos
- ✅ Cambios pusheados a GitHub (`main` branch)
- ✅ `render.yaml` lista para deployment

**Siguiente paso**: Crear el Release en GitHub y deployar en Render 🚀
