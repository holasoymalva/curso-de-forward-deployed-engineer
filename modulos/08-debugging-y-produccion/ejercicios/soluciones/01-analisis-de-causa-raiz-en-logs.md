# Solución al Ejercicio 01: Análisis de causa raíz en logs de producción

## 📊 Tarea 1: Respuestas a la inspección forense

1. **Hora de inicio y primer error:**
   * **Inicio del proceso:** `2026-10-14T02:00:00Z` con el lote `batch_001`.
   * **Primer error registrado:** Ocurrió a las `2026-10-14T03:00:15Z` en el lote `batch_081`.
2. **Primer código HTTP y mensaje de error:**
   * Código: `HTTP 401 Unauthorized`.
   * Mensaje del servidor: `"Token has expired at 2026-10-14T03:00:00Z"`.
3. **Cambio posterior de error a HTTP 429:**
   * A partir de las `03:00:20Z`, el conector comenzó a recibir `HTTP 429 Too Many Requests`.
   * **Razón:** El script cliente entró en un bucle cerrado de reintentos rápidos (reintentando cada 1-2 segundos sin renovar el token), lo que disparó la protección de *rate limiting* del servidor de la API.
4. **Lotes procesados con éxito:**
   * Se procesaron exactamente **80 lotes** (`batch_001` a `batch_080`) correspondientes a 8,000 registros antes de la falla.
5. **Latencia promedio:**
   * Lotes exitosos: ~420 ms por lote.
   * Lotes con error 401/429: ~45 ms (rechazo inmediato por el middleware de seguridad).

---

## 🔍 Tarea 2: Diagrama de los 5 Porqués (Root Cause Analysis)

```text
1. ¿Por qué se detuvo la sincronización y saltaron alertas de rate limiting (429)?
   └── Porque el cliente inundó el endpoint con más de 40 peticiones por minuto.

2. ¿Por qué el cliente inundó el endpoint en un bucle cerrado?
   └── Porque la función de reintento reaccionó a un fallo continuo sin aplicar backoff exponencial ni jitter.

3. ¿Por qué fallaban continuamente las peticiones en primer lugar?
   └── Porque el servidor devolvía 401 Unauthorized de forma sostenida.

4. ¿Por qué el servidor devolvía 401 si las credenciales iniciales eran correctas?
   └── Porque el token Bearer emitido al inicio tenía un tiempo de vida (TTL) de 3,600 segundos (1 hora) y expiró a las 03:00:00Z.

5. ¿Por qué el conector no renovó el token al expirar? (Causa Raíz)
   └── Porque el diseño del conector asumía erróneamente que la corrida completa tardaría menos de 30 minutos y no implementó un interceptor para detectar el código 401 y refrescar el token de sesión.
```

---

## ✉️ Tarea 3: Comunicado de incidente a las 03:30 AM

```markdown
Para: Laura Garza <laura.garza@distribuidorahalcon.com>, Roberto Treviño <roberto.trevino@distribuidorahalcon.com>
De: Guardias de Integración Nexo <soporte-fde@nexo-ai.internal>
Asunto: [ACTUALIZACIÓN SEV-1] Incidente en sincronización nocturna de Almacén Monterrey

Estimados Laura y Roberto,

Les escribo para informarles de manera proactiva que a las 03:15 AM nuestros sistemas de monitoreo detectaron una interrupción en el conector de sincronización de inventario nocturno para el Almacén de Monterrey.

Estado actual del diagnóstico:
- Se procesaron exitosamente los primeros 8,000 registros de catálogo (lotes 1 al 80).
- La causa de la detención está identificada: una expiración de la sesión de autenticación durante la corrida provocó el rechazo de los lotes restantes.
- No hay pérdida de datos ni inconsistencias en la base de datos central de Nexo ni en su ERP.

Acciones en curso:
- Nuestro equipo ya preparó la actualización para refrescar las credenciales de conexión de forma automática y estamos listos para reanudar la carga a partir del lote 81.
- El tiempo estimado para finalizar el procesamiento completo de Monterrey es de 35 minutos una vez reanudado.

Compromiso de entrega:
El inventario estará al 100% conciliado antes de las 05:00 AM, garantizando que sus sucursales operen con normalidad al abrir al público a las 07:00 AM.

Les enviaré una nueva actualización a las 04:15 AM o en cuanto el lote final quede confirmado.

Quedo a su entera disposición en esta línea y en el canal de Slack habitual.

Atentamente,
Equipo de Forward Deployed Engineering — Nexo AI
```
