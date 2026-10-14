# Ejercicio 01: Cliente con renovación y reintentos ante fallas

> **Nivel:** 🟡 Intermedio · **Tiempo estimado:** 45 min

---

## Contexto

El servidor de pedidos de Distribuidora Halcón presenta inestabilidad periódica: durante las horas pico responde con códigos de error `503 Service Unavailable` de forma intermitente y aplica un límite estricto de peticiones por minuto devolviendo `429 Too Many Requests` con la cabecera `Retry-After`. Además, sus tokens expiran cada 5 minutos (o 30 segundos si se prueba con `DURACION_TOKEN_SEG=30`).

---

## Lo que tienes que hacer

Escribe un script en Python llamado `cliente_robusto.py` que implemente una función `consultar_con_resiliencia(url: str, token_manager) -> dict`:

1. **Gestión de Token:** Renovar automáticamente el token si expiró o si la API responde con un código `401 Unauthorized`.
2. **Estrategia de Reintentos:**
   - Si la API responde con `503` o falla la conexión de red, reintentar hasta 4 veces aplicando backoff exponencial: espera base de 1 segundo multiplicada por $2^{\text{intento}-1}$ más un jitter aleatorio de 0.1 a 0.4 segundos.
   - Si la API responde con `429`, extraer el valor entero de la cabecera `Retry-After` y esperar ese tiempo exacto antes de reintentar.
   - Si la API responde con `404` o `422`, abortar inmediatamente sin reintentar e imprimir el detalle del error.
3. Probar la función haciendo 10 consultas consecutivas contra el endpoint `/pedidos` con la API simulada ejecutándose en modo hostil (`FALLAS=0.25`).

---

## Criterios de aceptación

- [ ] Soporta fallas simuladas 503 sin abortar el proceso.
- [ ] Respeta el encabezado `Retry-After` ante un código 429.
- [ ] Renueva el token de forma transparente si expira.
- [ ] No reintenta ante errores no recuperables (404, 422).

---

🔑 [Ver solución](soluciones/01-cliente-con-renovacion-y-reintentos.py)
