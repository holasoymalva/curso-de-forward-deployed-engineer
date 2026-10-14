# Lección 04: Consumir APIs desde Python sin dependencias

> **Nivel:** 🟢 Principiante · **Duración estimada:** 30 min

---

## Situación

Necesitas consultar el catálogo de productos de Distribuidora Halcón desde un script en Python para conciliarlo con la exportación del ERP. En tu entorno local podrías instalar la popular librería `requests`, pero en el servidor de pruebas del cliente no tienes acceso a internet para descargar paquetes de PyPI y no hay `pip` configurado.

Un FDE versátil domina el módulo nativo **`urllib.request`** de la biblioteca estándar de Python: sabe cómo enviar headers, serializar JSON, capturar errores HTTP y procesar respuestas sin instalar una sola librería externa.

---

## Conceptos clave

### 1. Consumo básico con `urllib.request`

Para realizar una petición `GET` básica y decodificar el JSON de respuesta:

```python
import json
import urllib.request

url = "http://127.0.0.1:8000/salud"

with urllib.request.urlopen(url) as respuesta:
    codigo = respuesta.status
    cuerpo_bytes = respuesta.read()
    datos = json.loads(cuerpo_bytes.decode("utf-8"))

print(f"Estado HTTP: {codigo}")
print(f"Respuesta:   {datos}")
```

---

### 2. Peticiones POST y autenticación con encabezados

Cuando necesitas enviar un método distinto a GET, agregar encabezados personalizados (como `Authorization`) o enviar un cuerpo en JSON, se utiliza la clase `urllib.request.Request`:

```python
import json
import urllib.request

url_token = "http://127.0.0.1:8000/auth/token"
payload = {
    "client_id": "nexo-demo",
    "client_secret": "secreto-de-practica"
}

# 1. Convertir diccionario a bytes codificados en UTF-8
cuerpo_bytes = json.dumps(payload).encode("utf-8")

# 2. Configurar la petición con headers explícitos
peticion = urllib.request.Request(
    url=url_token,
    data=cuerpo_bytes,
    headers={"Content-Type": "application/json"},
    method="POST"
)

# 3. Enviar y recibir respuesta
with urllib.request.urlopen(peticion) as respuesta:
    datos = json.loads(respuesta.read().decode("utf-8"))
    token = datos["access_token"]
    print("Token obtenido:", token)
```

---

### 3. Manejo de excepciones con `urllib.error.HTTPError`

A diferencia de librerías de terceros que a veces requieren configurar explícitamente el lanzamiento de errores, `urllib.request.urlopen` lanza automáticamente una excepción `urllib.error.HTTPError` ante cualquier código 4xx o 5xx:

```python
import urllib.error
import urllib.request

peticion_protegida = urllib.request.Request(
    url="http://127.0.0.1:8000/pedidos",
    headers={"Authorization": "Bearer token_falso"}
)

try:
    with urllib.request.urlopen(peticion_protegida) as resp:
        print("Éxito:", resp.status)
except urllib.error.HTTPError as error:
    codigo = error.code
    cuerpo_error = error.read().decode("utf-8")
    print(f"⚠️ Error HTTP capturado: {codigo}")
    print(f"Detalle del servidor: {cuerpo_error}")
except urllib.error.URLError as error_red:
    print(f"❌ Falla de conexión a la red: {error_red.reason}")
```

---

### 4. ¿Y qué hay de la librería `requests`?

En entornos donde sí puedes instalar librerías externas, `requests` ofrece una sintaxis mucho más compacta y cómoda:

```python
# Equivalente usando la librería 'requests' (requiere pip install requests)
import requests

resp = requests.post(
    "http://127.0.0.1:8000/auth/token",
    json={"client_id": "nexo-demo", "client_secret": "secreto-de-practica"}
)
if resp.ok:
    token = resp.json()["access_token"]
```

> **Criterio de ingeniería:** Usa `requests` cuando el entorno del cliente lo permita libremente. Domina `urllib` para cuando te enfrentes a entornos restringidos sin acceso a PyPI.

---

## Errores comunes

- **Olvidar codificar a bytes el cuerpo en `urllib`:** Pasar un string (`data='{"clave": 1}'`) a `Request(data=...)` en lugar de bytes (`.encode("utf-8")`) arroja `TypeError: POST data should be bytes`.
- **No leer el cuerpo de un `HTTPError`:** Cuando ocurre un 422, muchos desarrolladores solo ven el número del error y no leen `error.read()`, perdiéndose el mensaje exacto donde la API explica qué campo falló.
- **No configurar un tiempo de espera (*timeout*):** Si la red se congela o el servidor no responde, `urlopen` sin `timeout` puede quedarse esperando indefinidamente, congelando tu proceso nocturno. Usa siempre `timeout=10`.

---

## En el día a día de un FDE

Construir una pequeña clase cliente en Python con 3 métodos (`obtener_token`, `consultar_pedidos`, `crear_pedido`) te servirá de base reutilizable para todos los scripts y pruebas de la cuenta de Halcón.

---

## Resumen

- `urllib.request` y `urllib.error` permiten consumir cualquier API web sin instalar librerías de terceros.
- Con `urllib.request.Request` defines método, headers y body en bytes.
- Captura `urllib.error.HTTPError` para leer códigos de estado 4xx/5xx y el mensaje JSON retornado.
- Incluye siempre un parámetro `timeout` para evitar procesos colgados.

---

## Preguntas de repaso

1. ¿Por qué el argumento `data` en `urllib.request.Request` debe ser de tipo `bytes` y cómo se convierte un string JSON a bytes?
2. ¿Cómo obtienes el cuerpo de error en JSON cuando se dispara una excepción `urllib.error.HTTPError`?
3. ¿Qué beneficio operativo tiene definir un `timeout` explícito en llamadas de red?

---

⬅️ [Lección anterior: Principios REST](03-principios-rest-y-diseno-de-apis.md) | 📦 [Módulo](../README.md) | [Ir a Ejemplos del módulo](01-como-funciona-la-web-y-http.md) ➡️
