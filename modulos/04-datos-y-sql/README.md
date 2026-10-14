# Módulo 04: Datos y SQL

> **Nivel:** 🟢 Principiante  
> **Duración aproximada:** 6 horas  
> **Prerrequisitos:** [Módulo 02: Python para FDE](../02-python-para-fde/README.md)  

---

## 🎯 ¿Por qué importa para un FDE?

Los archivos planos como CSV o JSON son excelentes para transportar información, pero pésimos para responder preguntas de negocio complejas como: *"¿Cuáles son los 5 productos con mayor riesgo de quiebre de stock en Monterrey?"* o *"¿Qué porcentaje de pedidos de esta semana incluyeron productos de limpieza?"*.

El lenguaje SQL (*Structured Query Language*) y las bases de datos relacionales son el estándar indiscutible para modelar, filtrar, unir y transformar datos con consistencia y velocidad. Aprenderás a diseñar esquemas limpios y a construir pipelines ETL (*Extract, Transform, Load*) usando SQLite y Python nativo, sin necesidad de instalar motores de bases de datos pesados.

---

## ✅ Objetivos de aprendizaje

Al terminar este módulo podrás:

- Diseñar esquemas relacionales con llaves primarias (`PRIMARY KEY`), llaves foráneas (`FOREIGN KEY`) y restricciones de integridad (`NOT NULL`, `CHECK`, `UNIQUE`).
- Escribir consultas SQL fundamentales: `SELECT`, `WHERE`, `ORDER BY`, `LIMIT` y funciones de agregación (`COUNT`, `SUM`, `AVG`).
- Combinar información de múltiples tablas usando `INNER JOIN` y `LEFT JOIN`.
- Agrupar datos y filtrar grupos mediante `GROUP BY` y `HAVING`.
- Construir un flujo ETL en Python que extraiga los datos de `inventario_erp.csv`, los normalice y los cargue en una base de datos SQLite persistente con consultas parametrizadas.

---

## 📖 Lecciones

| # | Lección | Nivel | Duración |
|---|---------|-------|----------|
| 01 | [Modelado relacional para integraciones de FDE](lecciones/01-modelado-relacional-para-integraciones.md) | 🟢 | 25 min |
| 02 | [Consultas SQL esenciales y agregaciones](lecciones/02-consultas-sql-esenciales.md) | 🟢 | 30 min |
| 03 | [ETL: De CSV a SQLite con Python nativo](lecciones/03-etl-de-csv-a-sqlite-con-python.md) | 🟢 | 30 min |
| 04 | [Consultas avanzadas: Joins y reportes operativos](lecciones/04-consultas-avanzadas-joins-y-agrupaciones.md) | 🟢 | 30 min |

---

## 💻 Ejemplos

Scripts y esquemas listos para ejecutar:
- Consulta [ejemplos/README.md](ejemplos/README.md).
  - [Esquema de base de datos (`esquema.sql`)](ejemplos/esquema.sql)
  - [Pipeline de carga ETL (`cargar_datos_sqlite.py`)](ejemplos/cargar_datos_sqlite.py)
  - [Consultas operativas ejecutables (`consultas_operativas.py`)](ejemplos/consultas_operativas.py)

---

## 🏋️ Ejercicios

Prácticas de diseño y análisis sobre los datos de Halcón:
- Consulta [ejercicios/README.md](ejercicios/README.md).
  - [Ejercicio 01: Consultas de análisis operativo de inventario](ejercicios/01-consultas-de-analisis-de-inventario.md)
  - [Ejercicio 02: Pipeline ETL completo con tabla de auditoría](ejercicios/02-pipeline-etl-completo.md)

---

## 🎥 Guion sugerido para video

1. **Gancho (1-2 min):** *"Mariana tarda 40 minutos en Excel haciendo tablas dinámicas y cruces con BUSCARV (VLOOKUP) para saber qué productos están en cero en CDMX. En SQL, esa misma pregunta se responde en 4 líneas y 2 milisegundos con un LEFT JOIN."*
2. **Concepto (5-8 min):** Modelado relacional: Productos vs. Almacenes vs. Existencias. Por qué separar catálogo de existencias.
3. **Demo (6-8 min):** Ejecutar `cargar_datos_sqlite.py` y correr consultas analíticas con `sqlite3` desde la terminal.
4. **Cierre (1-2 min):** La importancia de consultas parametrizadas contra inyecciones SQL y presentación del Ejercicio 01.

---

## 📚 Para profundizar

- [Documentación oficial de SQLite y sqlite3 en Python](../../recursos/lecturas.md#🗄️-datos-y-sql).
- [SQLBolt (Tutorial interactivo)](../../recursos/lecturas.md#🗄️-datos-y-sql).

---

⬅️ [Módulo 03: HTTP y APIs](../03-http-y-apis/README.md) | 🏠 [Índice](../../README.md) | [Módulo 05: Descubrimiento con clientes](../05-descubrimiento-con-clientes/README.md) ➡️
