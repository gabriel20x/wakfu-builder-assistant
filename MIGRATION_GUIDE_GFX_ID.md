# Migración: Agregar soporte para gfx_id (Graphics ID)

## 📋 Resumen de Cambios

Se ha agregado soporte para almacenar y usar el `gfx_id` (Graphics ID) de los items, que permite mostrar las imágenes correctas de los items desde los assets de Wakfu.

### Cambios Realizados:

1. **Backend (API)**
   - ✅ Agregado campo `gfx_id` (Integer) al modelo `Item` en `api/app/db/models.py`

2. **Worker**
   - ✅ Agregado campo `gfx_id` al modelo `Item` en `worker/fetch_and_load.py`
   - ✅ Extracción automática de `gfx_id` desde `graphicParameters.gfxId` del JSON
   - ✅ El campo se guarda al cargar items en la base de datos

3. **Frontend**
   - ✅ Actualizado `ItemCard.vue` para usar `gfx_id` directamente
   - ✅ Sistema de fallback mejorado para imágenes:
     - 1º: Usa `gfx_id` si está disponible (más confiable)
     - 2º: Intenta extraer de `raw_data` si existe
     - 3º: Usa formato legacy como último recurso
   - ✅ Eliminado console.log que intentaba acceder a datos no estructurados

4. **Base de Datos**
   - ✅ Creada migración SQL: `api/migrations/add_gfx_id.sql`
   - ✅ Documentación en `api/migrations/README.md`

## 🚀 Cómo Aplicar los Cambios

### Opción 1: Reload Completo (RECOMENDADO)

Si puedes recargar todos los datos, esta es la forma más simple:

```bash
# 1. Detener los contenedores
docker-compose down

# 2. (Opcional) Limpiar la base de datos
docker volume rm wakfu-builder-assistant_postgres_data

# 3. Reiniciar con force reload
docker-compose up -d
```

El worker creará automáticamente el nuevo campo `gfx_id` y lo llenará con los datos correctos.

### Opción 2: Migración Sin Reload

Si NO quieres perder los datos existentes:

```bash
# 1. Aplicar la migración SQL
docker exec -i wakfu-builder-assistant-db-1 psql -U wakfu -d wakfu_builder < api/migrations/add_gfx_id.sql

# 2. Actualizar los servicios (sin tocar la DB)
docker-compose up -d --build api worker frontend

# 3. IMPORTANTE: Los items existentes tendrán gfx_id = NULL
#    Para llenarlos, necesitas ejecutar FORCE_RELOAD=true
```

### Opción 3: Update Script para Items Existentes

Si ya tienes datos y quieres extraer el `gfx_id` del campo `raw_data` sin recargar todo:

```python
# Script para actualizar items existentes (ejecutar en el worker o API)
from sqlalchemy import create_engine, text
import json

engine = create_engine("postgresql://wakfu:wakfu123@db:5432/wakfu_builder")

with engine.connect() as conn:
    result = conn.execute(text("SELECT item_id, raw_data FROM items WHERE gfx_id IS NULL"))
    
    for row in result:
        item_id = row[0]
        raw_data = row[1]
        
        if raw_data and 'definition' in raw_data:
            gfx_id = raw_data.get('definition', {}).get('item', {}).get('graphicParameters', {}).get('gfxId')
            
            if gfx_id:
                conn.execute(
                    text("UPDATE items SET gfx_id = :gfx_id WHERE item_id = :item_id"),
                    {"gfx_id": gfx_id, "item_id": item_id}
                )
                print(f"Updated item {item_id} with gfx_id {gfx_id}")
    
    conn.commit()
```

## 🔍 Verificación

Para verificar que todo funciona correctamente:

1. **Backend**: Verifica que el campo existe
   ```bash
   docker exec -i wakfu-builder-assistant-db-1 psql -U wakfu -d wakfu_builder -c "\d items"
   ```
   Deberías ver la columna `gfx_id` en la tabla.

2. **Frontend**: Abre la app y verifica que las imágenes de los items se cargan correctamente.

3. **Logs del Worker**: Verifica que no hay errores
   ```bash
   docker logs wakfu-builder-assistant-worker-1
   ```

## 📊 Estructura de Datos

### JSON Original (items.json)
```json
{
  "definition": {
    "item": {
      "id": 12345,
      "graphicParameters": {
        "gfxId": 42
      }
    }
  }
}
```

### Modelo de Base de Datos
```python
class Item:
    item_id: int          # 12345
    gfx_id: int           # 42 (extraído de graphicParameters.gfxId)
    raw_data: dict        # Todo el JSON original
```

### Frontend (ItemCard.vue)
```javascript
// URL de la imagen
`https://vertylo.github.io/wakassets/items/${props.item.gfx_id}.png`
```

## 🎯 Beneficios

1. **Imágenes Correctas**: Ahora se usan los IDs gráficos reales de Wakfu
2. **Rendimiento**: No se necesita parsear `raw_data` en el frontend
3. **Mantenibilidad**: Campo dedicado y documentado
4. **Compatibilidad**: Sistema de fallback para datos antiguos

## ⚠️ Notas Importantes

- Los items cargados ANTES de esta actualización tendrán `gfx_id = NULL`
- El frontend tiene fallbacks para manejar esto
- Se recomienda ejecutar `FORCE_RELOAD=true` una vez para poblar todos los `gfx_id`
- El campo `raw_data` aún se mantiene por si se necesitan otros datos en el futuro

## 🐛 Troubleshooting

### Las imágenes no se muestran

1. Verifica que `gfx_id` no es NULL:
   ```sql
   SELECT item_id, gfx_id FROM items LIMIT 10;
   ```

2. Verifica la URL en la consola del navegador

3. Verifica que wakassets está disponible:
   ```bash
   curl -I https://vertylo.github.io/wakassets/items/1.png
   ```

### El campo gfx_id es NULL para algunos items

Algunos items pueden no tener `graphicParameters.gfxId` en el JSON original. Esto es normal.

### Error al aplicar la migración

Si ya tienes el campo:
```sql
ALTER TABLE items DROP COLUMN IF EXISTS gfx_id;
```
Luego aplica la migración nuevamente.

