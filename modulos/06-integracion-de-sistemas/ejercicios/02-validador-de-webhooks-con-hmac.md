# Ejercicio 02: Validador de Webhooks con HMAC y almacenamiento idempotente

> **Nivel:** 🟡 Intermedio · **Tiempo estimado:** 45 min

---

## Contexto

Roberto Treviño implementa un emisor de webhooks para alertar cuando un pedido se marca como `cancelado`. Para asegurar que Halcón no acepte peticiones fraudulentas, cada webhook se envía con la cabecera `X-Signature-SHA256` calculada con una clave secreta compartida (`mi-secreto-compartido-123`).

Además, para prevenir que un fallo de red provoque procesar la misma cancelación dos veces, cada evento contiene un campo `id_evento` único que debe registrarse de forma idempotente.

---

## Lo que tienes que hacer

Escribe un script en Python llamado `receptor_seguro.py` que:

1. Inicie un servidor HTTP local en el puerto `9080` escuchando peticiones `POST /eventos`.
2. Extraiga el cuerpo en **bytes crudos** y la cabecera `X-Signature-SHA256`.
3. Valide la firma calculando el HMAC-SHA256 con la clave secreta y comparando con `hmac.compare_digest`.
   - Si no coincide o falta: responder de inmediato con `401 Unauthorized` y JSON `{"error": "firma_invalida"}`.
4. Si la firma es válida:
   - Parsear el JSON y extraer el `id_evento`.
   - Mantener un conjunto en memoria `eventos_procesados = set()`.
   - Si el `id_evento` ya está en el conjunto, responder `200 OK` con `{"estado": "ya_procesado", "idempotente": True}` sin volver a ejecutar la acción.
   - Si es nuevo, agregarlo al conjunto y responder `201 Created`.

---

## Criterios de aceptación

- [ ] Rechaza peticiones sin firma o con firma incorrecta devolviendo HTTP 401.
- [ ] Acepta peticiones con firma válida devolviendo HTTP 201 en el primer envío.
- [ ] Si se envía el mismo evento por segunda vez con la misma firma, devuelve HTTP 200 reconociendo la idempotencia.
- [ ] Usa exclusivamente la biblioteca estándar de Python.

---

🔑 [Ver solución](soluciones/02-validador-de-webhooks-con-hmac.py)
