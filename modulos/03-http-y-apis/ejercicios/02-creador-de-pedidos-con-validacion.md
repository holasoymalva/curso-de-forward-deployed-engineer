# Ejercicio 02: Creador de pedidos con validación de SKUs

> **Nivel:** 🟢 Principiante · **Tiempo estimado:** 45 min

---

## Contexto

El sistema de tiendas de Halcón necesita enviar pedidos nuevos a través del endpoint `POST /pedidos`. Sin embargo, a veces las tiendas envían productos inexistentes o cantidades negativas por error de dedo.

La API de Halcón responde con un código **`422 Unprocessable Entity`** cuando detecta errores de validación. Tu objetivo es construir una función robusta que intente enviar el pedido y, en caso de recibir un 422, capture el cuerpo JSON de la respuesta y muestre al usuario qué campos específicos debe corregir.

---

## Lo que tienes que hacer

Escribe un script en Python llamado `crear_pedido.py` que:

1. Obtenga el token Bearer en `/auth/token`.
2. Implemente la función `enviar_pedido(tienda: str, almacen: str, lineas: list[dict]) -> dict | None`:
   - Envíe una petición `POST` al endpoint `/pedidos` con encabezados `Content-Type: application/json` y `Authorization: Bearer <token>`.
3. **Maneje las respuestas:**
   - Si la respuesta es `201 Created`: Imprimir el ID del nuevo pedido generado y los datos confirmados.
   - Si la respuesta es `422 Unprocessable Entity`: Capturar la excepción `urllib.error.HTTPError`, decodificar el cuerpo JSON y mostrar en pantalla la lista exacta de errores reportados en `detalles`.
4. Pruebe dos casos en la función `main()`:
   - **Caso A (Exitoso):** Pedido válido para `"Tienda 0001"`, almacén `"MTY"` con SKU `"HAL-1001"` y cantidad `5`.
   - **Caso B (Fallido intencional):** Pedido con SKU desconocido `"HAL-9999"` y cantidad negativa `-2` para comprobar la captura del error 422.

---

## Criterios de aceptación

- [ ] El caso exitoso genera el pedido y muestra el ID devuelto por la API.
- [ ] El caso fallido no revienta con un traceback no controlado; captura el 422 e imprime los detalles de validación amigables.
- [ ] Usa exclusivamente la biblioteca estándar de Python.

---

🔑 [Ver solución](soluciones/02-creador-de-pedidos-con-validacion.py)
