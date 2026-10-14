# Lección 01: Estructuras de datos y funciones para automatización

> **Nivel:** 🟢 Principiante · **Duración estimada:** 25 min

---

## Situación

En el archivo nocturno de Distribuidora Halcón recibes 25 filas de inventario. Dos filas tienen exactamente el mismo SKU y almacén (`HAL-1004` en `MTY`), y un producto viene con el almacén inventado `XYZ`. Si intentas guardar esto a ciegas en una base de datos relacional con llaves únicas, la base de datos rechazará la carga y la sincronización se detendrá.

Para resolver esto en memoria antes de persistir nada, necesitas dominar las estructuras de datos fundamentales de Python: listas, diccionarios, conjuntos y tuplas.

---

## Conceptos clave

### 1. El repertorio de estructuras nativas

| Estructura | Sintaxis | Propiedad clave | Caso de uso típico para un FDE |
|------------|----------|-----------------|--------------------------------|
| **Lista (`list`)** | `[1, 2, 3]` | Ordenada, mutable, permite duplicados | Colección secuencial de registros o líneas de un pedido |
| **Diccionario (`dict`)** | `{"sku": "HAL-1001", "stock": 50}` | Clave-valor, búsquedas $O(1)$ ultra rápidas | Representar un registro con campos con nombre |
| **Conjunto (`set`)** | `{"MTY", "GDL", "CDMX"}` | Único, sin duplicados, membresía $O(1)$ | Validar catálogos válidos y deduplicar SKUs |
| **Tupla (`tuple`)** | `("HAL-1001", "MTY")` | Inmutable, hashable | Llaves compuestas (SKU + Almacén) en diccionarios |

---

### 2. Validación de catálogos con conjuntos (`set`)

Comprobar si un elemento está en una lista de 10,000 elementos tarda proporcionalmente al tamaño ($O(n)$). En un conjunto, la comprobación es prácticamente instantánea ($O(1)$):

```python
# Catálogo oficial de almacenes permitidos de Distribuidora Halcón
ALMACENES_VALIDOS = {"MTY", "GDL", "CDMX"}

almacen_recibido = "XYZ"

if almacen_recibido.upper() not in ALMACENES_VALIDOS:
    print(f"⚠️ Almacén desconocido detectado: {almacen_recibido}")
```

---

### 3. Diccionarios con llaves compuestas para deduplicar

Para detectar si una fila ya fue procesada hoy, puedes usar una tupla `(sku, almacen)` como clave de un diccionario:

```python
registros_unicos: dict[tuple[str, str], dict] = {}

fila_1 = {"sku": "HAL-1004", "almacen": "MTY", "cantidad": 15}
fila_2 = {"sku": "HAL-1004", "almacen": "MTY", "cantidad": 15}  # Duplicado

llave_compuesta = (fila_1["sku"], fila_1["almacen"])
registros_unicos[llave_compuesta] = fila_1

# Al procesar fila_2, sobreescribirá o ignorará limpiamente sin duplicar
```

---

### 4. Funciones pequeñas con anotaciones de tipo (*Type Hints*)

El código que escribes hoy para Halcón será leído dentro de seis meses por otro compañero o por ti mismo. Los type hints evitan sorpresas:

```python
from typing import Optional

def normalizar_sku(sku_crudo: str) -> str:
    """Elimina espacios accidentales y asegura mayúsculas consistentes."""
    return sku_crudo.strip().upper()

def convertir_cantidad(valor: str) -> Optional[int]:
    """Convierte texto a entero o retorna None si el valor está corrupto."""
    if not valor or valor.strip().upper() in {"N/D", "NA", "NULL"}:
        return None
    try:
        numero = int(valor.strip())
        return numero if numero >= 0 else None
    except ValueError:
        return None
```

---

## Ejemplo práctico interactivo

```python
# Prueba rápida de normalización
skus_sucios = [" HAL-1001 ", "hal-1002", "HAL-1003", " hal-1001 "]

skus_limpios = {normalizar_sku(s) for s in skus_sucios}
print(skus_limpios)
# Salida: {'HAL-1001', 'HAL-1002', 'HAL-1003'} (¡Espacios fuera y duplicados eliminados!)
```

---

## Errores comunes

- **Modificar una lista mientras estás iterando sobre ella:** Puede provocar que elementos se salten de forma silenciosa.
- **Usar tipos mutables como llaves de un diccionario:** Intentar usar una lista como clave (`{[1, 2]: "valor"}`) arroja un `TypeError: unhashable type: 'list'`. Usa una tupla (`{(1, 2): "valor"}`).
- **Asumir que los datos numéricos siempre son enteros:** En el CSV de Halcón, los precios vienen como `"76,50"`. Si ejecutas `float("76,50")` directamente, Python arrojará `ValueError`.

---

## En el día a día de un FDE

Construir funciones puras y reutilizables para transformar datos es el 70 % del trabajo técnico inicial de un FDE. Cuanto más modulares sean tus funciones, más fácil será probarlas y moverlas al core de tu empresa cuando se vuelvan estándar.

---

## Resumen

- Las estructuras nativas de Python (`set`, `dict`, `list`, `tuple`) ofrecen rendimiento óptimo para limpiar datos en memoria.
- Usa `set` para validaciones de pertenencia rápidas frente a catálogos oficiales.
- Aplica type hints para documentar claramente qué espera y qué entrega cada función.

---

## Preguntas de repaso

1. ¿Por qué es más eficiente buscar un SKU en un `set` que en una `list` cuando hay miles de productos?
2. ¿Qué ventaja ofrece usar una tupla `(sku, almacen)` como clave en lugar de concatenar cadenas tipo `sku + "_" + almacen`?
3. Si recibes la cadena `"N/D"`, ¿qué debería retornar una función de conversión numérica segura?

---

📦 [Volver al módulo](../README.md) | [Siguiente lección: Archivos CSV y JSON](02-archivos-csv-y-json.md) ➡️
