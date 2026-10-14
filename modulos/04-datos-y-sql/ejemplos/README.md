# Ejemplos del Módulo 04: Datos y SQL

Archivos SQL y scripts ejecutables en Python nativo (`sqlite3`) para modelar y consultar la base de datos de Distribuidora Halcón.

---

## 📂 Archivos disponibles

| Archivo | Descripción | Cómo usarlo |
|---------|-------------|-------------|
| [`esquema.sql`](esquema.sql) | Definición DDL de las tablas: `almacenes`, `productos`, `inventario`, `tiendas` y `pedidos`. | `sqlite3 halcon.db < esquema.sql` |
| [`cargar_datos_sqlite.py`](cargar_datos_sqlite.py) | Script ETL que lee `inventario_erp.csv`, normaliza los datos y los carga con `executemany` en `halcon.db`. | `python cargar_datos_sqlite.py` |
| [`consultas_operativas.py`](consultas_operativas.py) | Script que ejecuta consultas SQL con `INNER JOIN`, agregaciones y CTEs y muestra reportes formateados en terminal. | `python consultas_operativas.py` |

---

## 🚀 Cómo ejecutarlos

Desde la raíz del repositorio:

```bash
# 1. Cargar el esquema y los datos en SQLite
python modulos/04-datos-y-sql/ejemplos/cargar_datos_sqlite.py

# 2. Ejecutar las consultas de reporte operativo
python modulos/04-datos-y-sql/ejemplos/consultas_operativas.py
```
