# 🧪 Guía de Pruebas - Wakfu Builder Assistant

## Pre-requisitos

Antes de comenzar las pruebas, asegúrate de que:

- ✅ El backend está corriendo en `http://localhost:8000`
- ✅ El frontend está corriendo en `http://localhost:5173`
- ✅ La base de datos PostgreSQL tiene datos cargados
- ✅ Puedes acceder a `http://localhost:8000/docs`

## 🎯 Casos de Prueba

### Test 1: Verificar que el Frontend Carga

**Objetivo**: Verificar que la aplicación frontend se carga correctamente

**Pasos**:
1. Abre el navegador
2. Navega a `http://localhost:5173`
3. Verifica que ves:
   - Header con título "Wakfu Builder Assistant"
   - Panel de configuración a la izquierda
   - Panel de resultados a la derecha
   - Mensaje "¿Listo para comenzar?"

**Resultado Esperado**: ✅ La página carga sin errores

---

### Test 2: Verificar Configuración de Nivel

**Objetivo**: Probar el input de nivel máximo

**Pasos**:
1. En el panel izquierdo, busca "Nivel Máximo"
2. Prueba el input numérico:
   - Escribe `150`
   - Usa los botones +/- 
3. Prueba el slider:
   - Arrastra a diferentes valores
   - Verifica que el número se actualiza

**Resultado Esperado**: ✅ Ambos controles funcionan y están sincronizados

---

### Test 3: Ajustar Prioridades de Stats

**Objetivo**: Verificar que se pueden ajustar los pesos de stats

**Pasos**:
1. Busca la sección "Prioridad de Stats"
2. Para cada stat:
   - Usa los botones +/- para ajustar
   - Verifica que el valor cambia
3. Intenta configurar:
   ```
   HP:                1.0
   AP:                3.0
   MP:                2.5
   Critical_Mastery:  2.0
   Distance_Mastery:  3.5
   ```

**Resultado Esperado**: ✅ Todos los valores se ajustan correctamente (0.0 - 5.0)

---

### Test 4: Generar Build Básico

**Objetivo**: Probar la generación de builds

**Pasos**:
1. Configura:
   ```
   Nivel: 230
   HP: 1.0
   AP: 2.5
   MP: 2.0
   Critical_Hit: 1.5
   ```
2. Haz clic en "Generar Builds"
3. Espera a que cargue (spinner debe aparecer)

**Resultado Esperado**: 
- ✅ Aparece spinner mientras carga
- ✅ Se muestran 3 pestañas (Fácil, Medio, Difícil)
- ✅ Cada pestaña tiene items
- ✅ Se muestra resumen de stats totales

---

### Test 5: Verificar Build Fácil

**Objetivo**: Revisar que el build fácil tiene items accesibles

**Pasos**:
1. Después de generar, haz clic en pestaña "Fácil"
2. Revisa:
   - Badge de dificultad total (debe ser verde o amarillo)
   - Stats totales mostrados
   - Items en la lista

3. Para cada item verifica:
   - Tiene imagen (o placeholder)
   - Muestra nombre y nivel
   - Muestra slot (Cabeza, Pecho, etc.)
   - Lista de stats visible
   - Indicador de dificultad individual

**Resultado Esperado**: 
- ✅ Dificultad total < 40
- ✅ Al menos 1 item visible
- ✅ Todos los items son drops comunes o craft simple

---

### Test 6: Comparar Builds

**Objetivo**: Verificar diferencias entre dificultades

**Pasos**:
1. Abre pestaña "Fácil" y anota:
   - Dificultad total
   - Total de HP
   - Total de AP
   
2. Abre pestaña "Medio" y compara

3. Abre pestaña "Difícil" y compara

**Resultado Esperado**:
- ✅ Build Difícil tiene mejores stats que Medio
- ✅ Build Medio tiene mejores stats que Fácil
- ✅ Dificultad aumenta: Fácil < Medio < Difícil

---

### Test 7: Priorización de Stats Específicos

**Objetivo**: Verificar que el sistema prioriza correctamente

**Pasos**:
1. Genera build con:
   ```
   Distance_Mastery: 5.0 (máximo)
   Todos los demás: 0.5 (mínimo)
   ```

2. Revisa el build "Difícil"

3. Suma el Distance_Mastery total

4. Genera otro build con:
   ```
   HP: 5.0 (máximo)
   Todos los demás: 0.5 (mínimo)
   ```

5. Compara los totales

**Resultado Esperado**:
- ✅ Primer build maximiza Distance_Mastery
- ✅ Segundo build maximiza HP
- ✅ El stat priorizado es claramente mayor

---

### Test 8: Manejo de Errores

**Objetivo**: Verificar manejo de errores

**Pasos**:
1. Detén el backend (Ctrl+C)
2. En el frontend, intenta generar un build
3. Observa qué pasa

**Resultado Esperado**:
- ✅ Aparece mensaje de error
- ✅ Toast notification muestra el error
- ✅ La aplicación no se rompe
- ✅ Puedes intentar de nuevo

---

### Test 9: Items con Tags Especiales

**Objetivo**: Verificar que items épicos/reliquias se muestran correctamente

**Pasos**:
1. Genera un build "Difícil"
2. Busca items con tags:
   - "Épico" (rojo)
   - "Reliquia" (cyan)
   - "Gema" (morado)

3. Verifica que máximo hay:
   - 1 item épico
   - 1 item reliquia

**Resultado Esperado**:
- ✅ Tags se muestran con colores correctos
- ✅ Restricciones de cantidad se respetan

---

### Test 10: Responsive Design

**Objetivo**: Verificar que funciona en diferentes tamaños

**Pasos**:
1. Abre DevTools (F12)
2. Usa el modo responsive
3. Prueba en:
   - Desktop (1920x1080)
   - Tablet (768x1024)
   - Mobile (375x667)

**Resultado Esperado**:
- ✅ En desktop: 2 columnas (config + results)
- ✅ En tablet/mobile: 1 columna apilada
- ✅ Todo el contenido es accesible
- ✅ No hay scroll horizontal

---

### Test 11: Performance

**Objetivo**: Verificar tiempos de respuesta

**Pasos**:
1. Abre DevTools → Network
2. Genera un build
3. Observa el tiempo de la petición a `/build/solve`

**Resultado Esperado**:
- ✅ Request completa en < 5 segundos
- ✅ No hay memory leaks (verificar en Performance)
- ✅ UI se mantiene responsive

---

### Test 12: Verificar Stats Totales

**Objetivo**: Confirmar que los cálculos son correctos

**Pasos**:
1. Genera un build
2. En el build "Fácil", anota el total de HP mostrado
3. Suma manualmente los HP de cada item individual
4. Compara

**Resultado Esperado**:
- ✅ Total mostrado = suma de items
- ✅ Todos los stats son coherentes

---

## 🔍 Tests de Integración API

### Verificar Endpoints Directamente

```bash
# Health check
curl http://localhost:8000/health

# Generate build
curl -X POST http://localhost:8000/build/solve \
  -H "Content-Type: application/json" \
  -d '{
    "level_max": 230,
    "stat_weights": {
      "HP": 1.0,
      "AP": 2.5,
      "MP": 2.0
    }
  }'

# Get items
curl http://localhost:8000/items?level_max=230&limit=10

# Build history
curl http://localhost:8000/build/history?limit=5
```

**Resultado Esperado**:
- ✅ Todos los endpoints responden 200 OK
- ✅ JSON válido en respuestas

---

## 🐛 Checklist de Bugs Comunes

- [ ] Imágenes no cargan → Verificar URLs de WakfuAssets
- [ ] CORS error → Verificar config.py tiene puerto 5173
- [ ] No se generan builds → Verificar base de datos tiene datos
- [ ] Stats en 0 → Verificar cálculos en backend
- [ ] UI se rompe → Verificar console para JS errors

---

## 📊 Métricas de Éxito

Para considerar el testing completo:

- ✅ 12/12 tests pasan
- ✅ 0 errores en consola del navegador
- ✅ Tiempo de respuesta < 5s
- ✅ UI funciona en mobile y desktop
- ✅ Todos los endpoints responden correctamente

---

## 🆘 Si algo Falla

1. **Revisar logs del backend**:
   ```bash
   # Ver logs si estás usando Docker
   docker logs wakfu_api
   ```

2. **Revisar consola del navegador**:
   - F12 → Console
   - Buscar errores en rojo

3. **Verificar Network**:
   - F12 → Network
   - Ver si las requests fallan

4. **Limpiar y reiniciar**:
   ```bash
   # Frontend
   cd frontend
   rm -rf node_modules
   npm install
   npm run dev
   
   # Backend
   docker-compose down
   docker-compose up -d
   ```

---

**Happy Testing! 🧪✨**

