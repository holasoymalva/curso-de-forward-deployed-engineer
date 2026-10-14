# Ejercicios del Módulo 06: Integración de sistemas

Prácticas de ingeniería de integración avanzada: resiliencia ante errores de red, ciclo de vida de tokens, idempotencia y seguridad de webhooks.

---

## 📋 Lista de ejercicios

| # | Ejercicio | Nivel | Tiempo estimado | Enfoque |
|---|-----------|-------|-----------------|---------|
| 01 | [Cliente con renovación y reintentos ante fallas](01-cliente-con-renovacion-y-reintentos.md) | 🟡 | 45 min | Backoff exponencial, captura de 503/429 y manejo de `Retry-After`. |
| 02 | [Validador de Webhooks con HMAC y almacenamiento idempotente](02-validador-de-webhooks-con-hmac.md) | 🟡 | 45 min | Verificación criptográfica con `hmac.compare_digest` y prevención de duplicados. |

---

## 💡 Instrucciones

1. Inicia la API simulada en una terminal dedicada con parámetros de falla para probar el Ejercicio 01:
   ```bash
   FALLAS=0.25 LIMITE_POR_MINUTO=12 python recursos/api-simulada/servidor.py
   ```
2. Consulta las soluciones completas en [`soluciones/`](soluciones/).
