# API simulada de Distribuidora Halcón

Servidor local que imita la API interna del cliente del [caso de estudio](../caso-de-estudio/README.md). Usa **solo la biblioteca estándar de Python**, así que no hay que instalar nada.

## Iniciar el servidor

```bash
python recursos/api-simulada/servidor.py
```

Variables de entorno opcionales:

| Variable | Default | Descripción |
|----------|---------|-------------|
| `PUERTO` | `8000` | Puerto donde escucha el servidor. |
| `FALLAS` | `0` | Probabilidad (0 a 1) de responder `503` al azar. Útil para practicar reintentos. |
| `LIMITE_POR_MINUTO` | `60` | Peticiones permitidas por token por minuto antes de responder `429`. |
| `DURACION_TOKEN_SEG` | `300` | Vigencia del token de acceso. |

Ejemplo con condiciones "hostiles":

```bash
FALLAS=0.2 LIMITE_POR_MINUTO=10 DURACION_TOKEN_SEG=30 python recursos/api-simulada/servidor.py
```

## Credenciales de práctica

```text
client_id:     nexo-demo
client_secret: secreto-de-practica
```

## Endpoints

| Método | Ruta | Auth | Descripción |
|--------|------|------|-------------|
| `GET` | `/salud` | No | Verifica que el servidor esté arriba. |
| `POST` | `/auth/token` | No | Obtiene un token Bearer. Cuerpo: `{"client_id": "...", "client_secret": "..."}` |
| `GET` | `/productos` | Sí | Lista paginada. Filtros: `categoria`, `pagina`, `por_pagina` (máx. 100). |
| `GET` | `/productos/{sku}` | Sí | Detalle de un producto. |
| `GET` | `/inventario` | Sí | Inventario por almacén. Filtros: `almacen` (`MTY`, `GDL`, `CDMX`), `pagina`, `por_pagina`. |
| `GET` | `/pedidos` | Sí | Lista paginada. Filtros: `estado`, `almacen`, `pagina`, `por_pagina`. |
| `GET` | `/pedidos/{id}` | Sí | Detalle de un pedido. |
| `POST` | `/pedidos` | Sí | Crea un pedido. Acepta el encabezado `Idempotency-Key`. |

### Formato de respuestas paginadas

```json
{
  "datos": [ ... ],
  "pagina": 1,
  "por_pagina": 20,
  "total": 250,
  "siguiente_pagina": 2
}
```

### Códigos de error que puedes encontrar

| Código | Significado |
|--------|-------------|
| `400` | Solicitud mal formada o JSON inválido. |
| `401` | Token ausente, inválido o expirado. |
| `404` | Recurso o ruta no encontrada. |
| `422` | Error de validación al crear un pedido. |
| `429` | Límite de peticiones excedido (revisa el encabezado `Retry-After`). |
| `503` | Falla temporal simulada. |

## Prueba rápida con `curl`

```bash
# 1. Obtener token
curl -s -X POST http://127.0.0.1:8000/auth/token \
  -H "Content-Type: application/json" \
  -d '{"client_id":"nexo-demo","client_secret":"secreto-de-practica"}'

# 2. Usar el token (reemplaza TU_TOKEN)
curl -s "http://127.0.0.1:8000/pedidos?estado=pendiente&por_pagina=5" \
  -H "Authorization: Bearer TU_TOKEN"

# 3. Crear un pedido de forma idempotente
curl -s -X POST http://127.0.0.1:8000/pedidos \
  -H "Authorization: Bearer TU_TOKEN" \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: pedido-tienda-0001-a" \
  -d '{"tienda":"Tienda 0001","almacen":"MTY","lineas":[{"sku":"HAL-1001","cantidad":5}]}'
```

> Los datos se generan de forma determinista al iniciar, y los pedidos creados se pierden al detener el servidor.
