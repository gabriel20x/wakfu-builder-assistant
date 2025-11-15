# 🚀 Cómo Deployar en Render Correctamente

## ❌ Lo que NO debes hacer:
- No conectes servicios individuales
- No uses "New + Web Service" directamente

## ✅ Lo que DEBES hacer:

### Paso 1: Ir a Render Dashboard
https://dashboard.render.com

### Paso 2: Crear Blueprint (No Web Service individual)
1. Click en **"New +"**
2. Selecciona **"Blueprint"** (NO "Web Service")
3. Elige **"Public Git repository"**
4. Pega: `https://github.com/gabriel20x/wakfu-builder-assistant`
5. Click en **"Connect"**

### Paso 3: Render detectará `render.yaml`
- Render mostrará: "Blueprint detected: render.yaml"
- Verifica que muestre 4 servicios:
  - ✅ wakfu-db (PostgreSQL)
  - ✅ wakfu-api (Web service)
  - ✅ wakfu-frontend (Web service)
  - ✅ wakfu-worker (Background worker)

### Paso 4: Deploy
Click en **"Deploy Blueprint"**

---

## 🔧 Si ya creaste servicios individuales:

1. Ve a cada servicio en Render
2. Settings → Danger Zone → Delete Service
3. Comienza de nuevo desde Paso 1 (Usar Blueprint)

---

## 📋 Checklist Final:
- [ ] Usado "Blueprint" (no "Web Service individual")
- [ ] render.yaml fue detectado por Render
- [ ] Todos 4 servicios aparecen en la configuración
- [ ] Has confirmado el Deploy del Blueprint
- [ ] Esperar 5-10 minutos para que se construyan

---

## 🆘 Si sigue fallando:

Si Render muestra el mismo error incluso con Blueprint:

1. Abre el Release en GitHub: https://github.com/gabriel20x/wakfu-builder-assistant/releases
2. Verifica que esté el archivo `wakfu_data.tar.gz` descargable
3. Si NO está, créalo:
   - Ya lo comprimimos, está en tu carpeta: `wakfu_data.tar.gz`
   - Subirlo a un Release en GitHub

¿Dónde crease exactamente el Blueprint en Render? ¿Qué pasos seguiste?
