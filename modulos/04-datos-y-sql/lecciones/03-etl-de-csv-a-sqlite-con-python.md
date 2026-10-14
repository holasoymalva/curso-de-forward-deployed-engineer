# Lección 03: ETL: De CSV a SQLite con Python nativo

> **Nivel:** 🟢 Principiante · **Duración estimada:** 30 min

---

## Situación

Cada noche a las 3:30 AM, el archivo `inventario_erp.csv` se descarga en el servidor. Tu tarea como FDE es automatizar un proceso que:
1. Extraiga (*Extract*) los registros crudos del archivo.
2. Transforme (*Transform*) y sanitice los datos corruptos usando las funciones defensivas de Python del Módulo 02.
3. Cargue (*Load*) los datos limpios en una base de datos relacional SQLite de forma atómica y segura mediante transacciones.

Este proceso es un pipeline **ETL** (*Extract, Transform, Load*), la columna vertebral de la ingeniería de datos y la integración de sistemas.

---

## Conceptos clave

### 1. El módulo `sqlite3` de la biblioteca estándar

Python incluye de fábrica el motor de base de datos relacional más utilizado del planeta: **SQLite**. No necesitas instalar Docker, ni PostgreSQL, ni configurar puertos o contraseñas de red. Todo vive en un único archivo en disco (ej. `halcon.db`).

```python
import sqlite3

# Abrir conexión a un archivo local (se crea si no existe)
conexion = sqlite3.connect("halcon.db")

# Habilitar soporte para llaves foráneas en SQLite
conexion.execute("PRAGMA foreign_keys = ON;")

cursor = conexion.cursor()
```

---

### 2. Consultas parametrizadas: ¡Nunca concatenes cadenas!

El riesgo de seguridad número uno en bases de datos es la **Inyección SQL** (*SQL Injection*). Ocurre cuando concatenas variables directamente en el texto de la consulta:

❌ **Vulnerable a hackeo o errores con comillas:**
```python
sku = "HAL-1001"
# Si sku contiene comillas como "HAL-1001'; DROP TABLE productos;--" destruirás la base de datos
cursor.execute(f"INSERT INTO productos (sku) VALUES ('{sku}');")
```

✅ **Seguro con parámetros (marcador `?`):**
```python
cursor.execute(
    "INSERT INTO productos (sku, nombre, precio) VALUES (?, ?, ?);",
    ("HAL-1001", "Arroz chico", 18.50)
)
```

SQLite escapa los valores automáticamente en binario, haciendo imposible la inyección de código malicioso.

---

### 3. Carga masiva eficiente con `executemany` y Transacciones

Insertar 10,000 filas una por una haciendo `commit()` en cada ciclo es increíblemente lento porque el disco debe confirmar cada escritura individualmente.

El método `executemany()` inserta un lote completo de registros dentro de una sola transacción atómica:

```python
lote_productos = [
    ("HAL-1001", "Arroz chico", "abarrotes", 18.50, 20),
    ("HAL-1002", "Arroz mediano", "abarrotes", 32.90, 20),
    ("HAL-1003", "Arroz grande", "abarrotes", 58.00, 20),
]

# Inserción idempotente: Si el producto ya existe, actualiza el precio
sql = """
INSERT INTO productos (sku, nombre, categoria, precio, stock_minimo)
VALUES (?, ?, ?, ?, ?)
ON CONFLICT(sku) DO UPDATE SET
    precio = excluded.precio,
    nombre = excluded.nombre;
"""

cursor.executemany(sql, lote_productos)
conexion.commit() # Confirmar cambios en disco
```

---

### 4. Lectura de resultados con `row_factory`

Por defecto, SQLite devuelve cada fila como una tupla anónima (`('HAL-1001', 120)`). Para acceder a los campos por su nombre de columna como si fuera un diccionario:

```python
conexion.row_factory = sqlite3.Row

cursor = conexion.cursor()
cursor.execute("SELECT sku, cantidad FROM inventario WHERE almacen_codigo = 'MTY'")

for fila in cursor.fetchall():
    print(fila["sku"], fila["cantidad"])  # ¡Acceso limpio por nombre!
```

---

## Errores comunes

- **Olvidar ejecutar `conexion.commit()`:** Modificas datos, el script termina sin errores pero al abrir la base de datos... ¡está vacía! Si no llamas a `.commit()`, los cambios se descartan automáticamente al cerrar la conexión.
- **Dejar conexiones abiertas:** No cerrar la conexión (`conexion.close()`) o no usar un manejador de contexto `with sqlite3.connect(...) as conexion:`.
- **Bloqueo de base de datos (*Database is locked*):** En SQLite, si un proceso abre una transacción de escritura y nunca hace commit ni rollback, otros procesos no podrán escribir en la base de datos.

---

## En el día a día de un FDE

Un script ETL en Python + SQLite de 80 líneas programado con `executemany` puede procesar un millón de registros en menos de 3 segundos sin consumir más de 30 MB de RAM. Es la solución perfecta para microservicios de sincronización local en servidores de clientes.

---

## Resumen

- SQLite está integrado de forma nativa en Python a través del módulo `sqlite3`.
- Usa siempre consultas parametrizadas con marcadores de posición (`?`) para evitar inyecciones SQL.
- `executemany()` combinado con transacciones optimiza el rendimiento en varios órdenes de magnitud.
- Configura `conexion.row_factory = sqlite3.Row` para leer resultados como diccionarios.

---

## Preguntas de repaso

1. ¿Por qué es peligroso usar f-strings de Python para construir consultas SQL?
2. ¿Qué ocurre con los cambios realizados en una base de datos SQLite si el script termina antes de invocar `conexion.commit()`?
3. ¿Cuál es la ventaja de rendimiento de usar `executemany()` frente a ejecutar `execute()` en un ciclo `for`?

---

⬅️ [Lección anterior: Consultas esenciales](02-consultas-sql-esenciales.md) | 📦 [Módulo](../README.md) | [Siguiente lección: Consultas avanzadas y Joins](04-consultas-avanzadas-joins-y-agrupaciones.md) ➡️
