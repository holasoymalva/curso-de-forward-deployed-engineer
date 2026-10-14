# Lección 02: Logging estructurado en JSON y contexto operativo

> **Nivel:** 🟡 Intermedio · **Duración estimada:** 25 min

---

## Situación

Abres el archivo de logs de un conector en el servidor de Halcón y encuentras 40,000 líneas que se ven así:

```text
Iniciando proceso...
Procesando pedido 101
Error en pedido
Fallo de red
Reintentando
Listo
```

¿Qué pedido falló? ¿A qué hora exacta? ¿Qué código HTTP devolvió el servidor? ¿Cuánto tiempo tardó la llamada? ¿Con qué tienda estaba relacionado?

Ese formato de texto desordenado es prácticamente inútil para depurar incidentes a escala. La industria moderna resolvió esto adoptando el **Logging Estructurado en formato JSON**.

---

## Conceptos clave

### 1. ¿Qué es el Logging Estructurado?

En lugar de emitir texto plano arbitrario, cada mensaje de log se emite como un **objeto JSON en una sola línea** (*JSON Lines / jsonl*) con campos clave-valor estandarizados:

```json
{
  "timestamp": "2026-10-14T03:22:15.120Z",
  "nivel": "ERROR",
  "mensaje": "Falla al crear pedido en API de Halcón",
  "cliente_id": "halcon-mty",
  "solicitud_id": "req-9b1deb4d-3b7d",
  "endpoint": "/pedidos",
  "metodo": "POST",
  "codigo_http": 503,
  "intento": 3,
  "duracion_ms": 1420.5,
  "tienda": "Tienda Doña Mary",
  "error_detalle": "Service Unavailable: conexión rechazada por backend"
}
```

#### Ventajas inmediatas:
- **Indexable y filtrable automáticamente:** Herramientas como Datadog, Grafana Loki, AWS CloudWatch o un simple script de Python pueden filtrar en un milisegundo: *"Muéstrame todos los logs donde `codigo_http == 503` y `tienda == 'Tienda Doña Mary'`"*.
- **Trazabilidad de extremo a extremo:** El campo `solicitud_id` permite rastrear el viaje completo de una petición a través de múltiples microservicios.

---

### 2. Los niveles estándar de severidad

| Nivel | Cuándo usarlo | Ejemplo en Nexo |
|-------|---------------|-----------------|
| **`DEBUG`** | Diagnóstico detallado útil únicamente durante el desarrollo local. | Payload binario en bytes antes de enviarse por el socket. |
| **`INFO`** | Hitos operativos normales del ciclo de vida del sistema. | *"Inicio de sincronización"*, *"Token renovado"*, *"150 pedidos procesados"*. |
| **`WARNING`** | Eventos inesperados que el sistema pudo manejar o reintentar sin fallar. | *"Respuesta 503 transitoria; reintentando con backoff"*, *"SKU duplicado omitido"*. |
| **`ERROR`** | Falla que impidió procesar una operación puntual pero el sistema sigue vivo. | *"No se pudo procesar el pedido #105 por error de validación 422"*. |
| **`CRITICAL`** | Falla catastrófica que detiene por completo la aplicación. | *"No se puede conectar a la base de datos local SQLite. Proceso abortado."* |

---

### 3. Implementación nativa de un formateador JSON en Python

No necesitas librerías externas para emitir logs en JSON:

```python
import json
import logging
from datetime import datetime

class FormateadorJSON(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "nivel": record.levelname,
            "modulo": record.module,
            "mensaje": record.getMessage(),
        }
        # Agregar campos de contexto si existen en 'extra'
        if hasattr(record, "contexto") and isinstance(record.contexto, dict):
            log_entry.update(record.contexto)
            
        if record.exc_info:
            log_entry["traceback"] = self.formatException(record.exc_info)
            
        return json.dumps(log_entry, ensure_ascii=False)
```

---

## Errores comunes

- **Filtrar secretos y contraseñas en los logs:** Registrar objetos completos que contienen `client_secret` o tokens Bearer sin censurar. Los logs suelen almacenarse en texto plano y pueden ser leídos por múltiples personas.
- **Registrar múltiples líneas dentro de un solo log:** Si emites un traceback con saltos de línea sin formatear en JSON, las herramientas de observabilidad interpretarán cada línea del traceback como un evento independiente y desordenado.
- **Usar niveles incorrectos:** Enviar mensajes normales como `ERROR` (lo que dispara falsas alarmas al equipo de guardia) o esconder errores críticos bajo el nivel `INFO`.

---

## En el día a día de un FDE

Cuando Roberto Treviño te pregunte qué pasó durante la noche, no le mandas un texto vago: abres la terminal, filtras los logs estructurados con `analizar_logs.py` y le entregas una tabla con el conteo exacto de códigos HTTP, latencias promedio y causas de reintento.

---

## Resumen

- El logging estructurado en JSON transforma los logs en datos analizables por máquinas y humanos.
- Campos como `solicitud_id`, `duracion_ms` y `codigo_http` permiten correlacionar eventos rápidamente.
- Usa los niveles de severidad de forma consistente (`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`).
- Nunca registres credenciales ni información confidencial en los logs.

---

## Preguntas de repaso

1. ¿Qué ventajas ofrece el logging estructurado en JSON frente a mensajes de texto plano tradicionales?
2. ¿Qué información aporta el campo `solicitud_id` (*request_id*) al diagnosticar un problema?
3. ¿Cuál es la diferencia entre el nivel `WARNING` y el nivel `ERROR`?

---

⬅️ [Lección anterior: Método de debugging](01-metodo-sistematico-de-debugging.md) | 📦 [Módulo](../README.md) | [Siguiente lección: Observabilidad y SLOs](03-observabilidad-metricas-trazas-y-slos.md) ➡️
