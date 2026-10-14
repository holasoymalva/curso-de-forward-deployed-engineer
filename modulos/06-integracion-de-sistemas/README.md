# Módulo 06: Integración de sistemas

> **Nivel:** 🟡 Intermedio  
> **Duración aproximada:** 6 horas  
> **Prerrequisitos:** [Módulo 03: HTTP y APIs](../03-http-y-apis/README.md) y [Módulo 04: Datos y SQL](../04-datos-y-sql/README.md)  

---

## 🎯 ¿Por qué importa para un FDE?

En un entorno local de laboratorio, la red nunca falla, las peticiones tardan 2 milisegundos y los tokens no vencen. En el mundo corporativo real con clientes como Distribuidora Halcón:
- La conexión a internet se interrumpe justo a la mitad de un pedido.
- El servidor responde `503 Service Unavailable` porque está sobrecargado.
- El cliente tiene un *Rate Limit* de 60 peticiones por minuto y te arroja un `429 Too Many Requests`.
- Si reintentas a ciegas un pedido fallido sin una llave de **idempotencia**, apartas mercancía dos veces o cobras doble a la tienda.

Este módulo separa a los desarrolladores novatos de los Forward Deployed Engineers profesionales: aquí aprenderás a diseñar conectores de integración de grado de producción, resilientes a fallas de red, con renovación automática de tokens, reintentos con *backoff* exponencial e idempotencia estricta.

---

## ✅ Objetivos de aprendizaje

Al terminar este módulo podrás:

- Evaluar y seleccionar el patrón de integración adecuado: procesamiento por lotes (*batch*) vs. eventos en tiempo real (*webhooks / streaming*).
- Implementar clientes HTTP con gestión de ciclo de vida de tokens: detección proactiva de expiración y renovación transparente tras un código `401`.
- Diseñar mecanismos de reintentos robustos ante códigos `429` y `503` aplicando **backoff exponencial con jitter** y respetando el encabezado `Retry-After`.
- Garantizar la **idempotencia** de las mutaciones mediante encabezados `Idempotency-Key` para evitar transacciones o pedidos duplicados.
- Construir y asegurar receptores de **webhooks** mediante validación de firmas criptográficas HMAC con SHA-256.

---

## 📖 Lecciones

| # | Lección | Nivel | Duración |
|---|---------|-------|----------|
| 01 | [Patrones de integración: Batch vs. Tiempo Real](lecciones/01-patrones-de-integracion-batch-vs-streaming.md) | 🟡 | 25 min |
| 02 | [Autenticación robusta y renovación de tokens](lecciones/02-autenticacion-robusta-y-renovacion-de-tokens.md) | 🟡 | 30 min |
| 03 | [Resiliencia: Backoff exponencial, jitter y rate limiting](lecciones/03-resiliencia-backoff-exponencial-y-rate-limiting.md) | 🟡 | 35 min |
| 04 | [Idempotencia: Cómo evitar duplicados en operaciones críticas](lecciones/04-idempotencia-y-evitar-duplicados.md) | 🟡 | 30 min |
| 05 | [Webhooks y validación de firmas criptográficas HMAC](lecciones/05-webhooks-y-firmas-criptograficas-hmac.md) | 🟡 | 30 min |

---

## 💻 Ejemplos

Herramientas y clientes de integración ejecutables con biblioteca estándar de Python:
- Consulta [ejemplos/README.md](ejemplos/README.md).
  - [Cliente HTTP resiliente de producción (`cliente_resiliente.py`)](ejemplos/cliente_resiliente.py)
  - [Receptor de Webhooks con verificación HMAC (`servidor_webhook.py`)](ejemplos/servidor_webhook.py)
  - [Sincronizador incremental de inventario (`sincronizador_inventario.py`)](ejemplos/sincronizador_inventario.py)

---

## 🏋️ Ejercicios

Casos prácticos de integración contra la API simulada en condiciones hostiles:
- Consulta [ejercicios/README.md](ejercicios/README.md).
  - [Ejercicio 01: Cliente con renovación automática y reintentos ante fallas](ejercicios/01-cliente-con-renovacion-y-reintentos.md)
  - [Ejercicio 02: Validador de Webhooks con firma HMAC y almacenamiento idempotente](ejercicios/02-validador-de-webhooks-con-hmac.md)

---

## 🎥 Guion sugerido para video

1. **Gancho (1-2 min):** *"Arrancamos la API simulada con `FALLAS=0.3` (30 % de fallas aleatorias) y `LIMITE_POR_MINUTO=10`. Un script novato falla en la tercera petición y arroja un error feo. En esta lección ejecutaremos nuestro cliente resiliente: verás cómo captura el 503, espera pacientemente con jitter, renueva el token vencido y completa el 100 % de los pedidos sin una sola queja."*
2. **Concepto (5-8 min):** La fórmula de backoff exponencial $t = \min(t_{\max}, t_{\text{base}} \times 2^{\text{intento}}) \pm \text{jitter}$. El concepto de idempotencia en peticiones POST.
3. **Demo (6-8 min):** Ejecutar `cliente_resiliente.py` en vivo mostrando los logs detallados de reintentos y cabeceras de idempotencia.
4. **Cierre (1-2 min):** Resumen de por qué estos patrones son obligatorios en cualquier conector empresarial y presentación del reto del Ejercicio 01.

---

## 📚 Para profundizar

- [Enterprise Integration Patterns (Hohpe & Woolf)](../../recursos/lecturas.md#🌐-http-apis-y-arquitectura-de-integración).
- [Designing Data-Intensive Applications (Martin Kleppmann)](../../recursos/lecturas.md#🌐-http-apis-y-arquitectura-de-integración).

---

⬅️ [Módulo 05: Descubrimiento con clientes](../05-descubrimiento-con-clientes/README.md) | 🏠 [Índice](../../README.md) | [Módulo 07: Despliegue y cloud](../07-despliegue-y-cloud/README.md) ➡️
