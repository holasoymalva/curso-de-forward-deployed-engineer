# Ejemplos del Módulo 06: Integración de sistemas

Herramientas y clientes de integración de grado de producción construidos exclusivamente con la **biblioteca estándar de Python**.

---

## 📂 Archivos disponibles

| Script | Descripción | Cómo ejecutarlo |
|--------|-------------|-----------------|
| [`cliente_resiliente.py`](cliente_resiliente.py) | Cliente HTTP avanzado que maneja ciclo de vida completo de tokens Bearer, reintentos con backoff exponencial y jitter ante 429/503, paginación completa y cabecera de idempotencia en `POST`. | `python cliente_resiliente.py` |
| [`servidor_webhook.py`](servidor_webhook.py) | Servidor HTTP mínimo con `http.server` que escucha en `/webhook`, valida firmas HMAC-SHA256 en tiempo constante y rechaza peticiones no autorizadas. | `python servidor_webhook.py` |
| [`sincronizador_inventario.py`](sincronizador_inventario.py) | Script de sincronización incremental que consulta existencias de la API y las actualiza de forma transaccional e idempotente en SQLite. | `python sincronizador_inventario.py` |

---

## 🚀 Cómo probar en condiciones hostiles

Para poner a prueba la resiliencia del cliente, inicia la API simulada forzando fallas aleatorias del 20 % y un rate limit bajo:

```bash
# En una terminal independiente:
FALLAS=0.2 LIMITE_POR_MINUTO=10 python recursos/api-simulada/servidor.py

# En tu terminal de trabajo:
python modulos/06-integracion-de-sistemas/ejemplos/cliente_resiliente.py
```
