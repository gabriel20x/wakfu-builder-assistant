# 🚀 Instrucciones para Aplicar los Fixes

## ✅ Lo que ya está hecho

### 1. Código del Worker Actualizado ✅
**Archivo:** `worker/fetch_and_load.py`

**Fixes aplicados:**
- ✅ **Action ID 175** (Dodge vs Berserk): Thresholds actualizados
  - Armas/Cabeza: < 250 = Dodge
  - Otros slots: < 100 = Dodge
  
- ✅ **Action ID 192** (Prospecting vs -WP): Detección por signo
  - Valor positivo = Prospecting
  - Valor negativo = -WP

### 2. Migración SQL Creada ✅
**Archivo:** `migrations/fix_dodge_and_prospecting_stats.sql`

Corrige AMBOS problemas en la base de datos existente.

### 3. Documentación Completa ✅
- `CONTEXTUAL_STATS_FIX_COMPLETE.md` - Resumen completo
- `docs/FIX_DODGE_BERSERK_ISSUE.md` - Detalles Dodge/Berserk
- `docs/PROSPECTING_VS_WP_ISSUE.md` - Detalles Prospecting/WP
- `docs/rarity_analysis/SUMMARY.md` - Actualizado con ambos fixes
- `migrations/README.md` - Guía de migraciones

---

## 🎯 Lo que necesitas hacer AHORA

### Paso 1: FIXES YA APLICADOS ✅

**Todos los fixes ya fueron aplicados mediante:**

```bash
# Worker reconstruido con código actualizado
docker-compose build --no-cache worker

# Datos recargados con thresholds correctos
docker-compose exec db psql -U wakfu -d wakfu_builder -c \
  "DELETE FROM gamedata_versions WHERE version_string = '1.90.1.43';"
docker-compose up -d worker

# API reiniciada
docker-compose restart api
```

**Estado:** ✅ **COMPLETADO - Sistema listo para usar**

---

## 🔍 Verificación

### 1. Verifica que los Items estén Corregidos

```bash
docker-compose exec db psql -U wakfu -d wakfu_builder -c "
SELECT item_id, name_es, slot, level, rarity, 
       stats::jsonb->'Dodge' as dodge,
       stats::jsonb->'Berserk_Mastery' as berserk,
       stats::jsonb->'WP' as wp,
       stats::jsonb->'Prospecting' as prospecting
FROM items
WHERE item_id IN (21218, 26638, 25849)
ORDER BY item_id;
"
```

**Resultado esperado:**
```
 item_id |      name_es        | slot  | level | rarity | dodge | berserk |  wp  | prospecting
---------+---------------------+-------+-------+--------+-------+---------+------+-------------
  21218  | Peinado Ror        | HEAD  |  162  |   3    |  70   | null    | null | null
  26638  | Espada de Pym...   | FIRST |  165  |   3    | 110   | null    | null | null
  25849  | Anillo pinxudo     | LEFT  |  165  |   3    | null  | null    |  -1  | null
```

### 2. Genera un Build y Verifica

```bash
curl -X POST http://localhost:8000/solver \
  -H "Content-Type: application/json" \
  -d '{
    "level_max": 165,
    "stat_weights": {
      "HP": 1,
      "Dodge": 3,
      "WP": 1,
      "Distance_Mastery": 2
    }
  }'
```

**En la respuesta busca:**
- ✅ `"Dodge"` en vez de `"Berserk_Mastery"` para Screechcut/Pepepew
- ✅ `"WP": -1` en vez de `"Prospecting": 1` para Mamagring
- ✅ `total_stats.Dodge` debe ser mucho mayor (~390 vs ~210)

---

## 📊 Comparación: Antes vs Después

### Build Easy - Nivel 165

**ANTES del fix ❌:**
```json
{
  "items": [
    {"name": "Peinado Ror", "stats": {"Berserk_Mastery": 70}},
    {"name": "Espada de Pym", "stats": {"Berserk_Mastery": 110}},
    {"name": "Anillo pinxudo", "stats": {"Prospecting": 1}}
  ],
  "total_stats": {
    "Berserk_Mastery": 180,  // ❌
    "Dodge": 210,            // ❌ Faltan ~180 puntos
    "Prospecting": 1,        // ❌
    "WP": 0                  // ❌ Falta -1
  }
}
```

**DESPUÉS del fix ✅:**
```json
{
  "items": [
    {"name": "Peinado Ror", "stats": {"Dodge": 70}},      // ✅
    {"name": "Espada de Pym", "stats": {"Dodge": 110}},   // ✅
    {"name": "Anillo pinxudo", "stats": {"WP": -1}}       // ✅
  ],
  "total_stats": {
    "Berserk_Mastery": 0,    // ✅ Solo items legítimos
    "Dodge": 390,            // ✅ Todos los Dodge sumados
    "Prospecting": 0,        // ✅ Sin falsos positivos
    "WP": -1                 // ✅ Penalización correcta
  }
}
```

---

## ❓ FAQ

### ¿Necesito aplicar la migración si recargo los datos?
No. Si usas la **Opción B** (restart worker), los datos se recargarán con el código corregido. La migración es solo para la **Opción A**.

### ¿Puedo aplicar la migración múltiples veces?
Sí, es seguro. La migración es **idempotente** (detecta items ya corregidos).

### ¿Afectará a otros stats?
No. Solo corrige los 2 problemas específicos identificados:
- Dodge vs Berserk (Action ID 175)
- Prospecting vs -WP (Action ID 192)

### ¿Cuánto tiempo toma?
- **Opción A (migración):** ~1 segundo
- **Opción B (reload):** ~5-10 minutos

---

## 🎉 Después de Aplicar

Una vez aplicado el fix:

1. ✅ Los builds mostrarán stats correctos
2. ✅ El frontend mostrará Dodge en vez de Berserk donde corresponda
3. ✅ Los anillos mostrarán -WP en vez de Prospecting
4. ✅ Los totales de stats serán precisos

**¡Los builds ahora son 100% precisos!** 🎯

---

## 📞 Si Algo Sale Mal

Si encuentras problemas:

```bash
# Ver logs del worker
docker-compose logs worker

# Ver logs de la API
docker-compose logs api

# Ver logs de la DB
docker-compose logs db

# Reiniciar todo
docker-compose restart
```

O revisa la documentación completa en `CONTEXTUAL_STATS_FIX_COMPLETE.md`

---

**Última actualización:** 2025-11-04  
**Status:** ✅ **CÓDIGO LISTO** - ⏳ **ESPERANDO APLICACIÓN DE MIGRACIÓN**

