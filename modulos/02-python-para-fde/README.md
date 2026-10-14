# Módulo 02: Python para FDE

> **Nivel:** 🟢 Principiante  
> **Duración aproximada:** 6 horas  
> **Prerrequisitos:** [Módulo 01: Herramientas esenciales](../01-herramientas-esenciales/README.md)  

---

## 🎯 ¿Por qué importa para un FDE?

En el mundo real de las empresas, los datos nunca vienen limpios ni en APIs listas. Vienen en exportaciones nocturnas de ERPs de hace décadas, archivos CSV con fechas en formatos mezclados, SKUs con espacios accidentales y números con comas en lugar de puntos decimales.

Python es el lenguaje por excelencia del Forward Deployed Engineer porque te permite escribir en minutos scripts de automatización confiables, robustos y fáciles de auditar. Aprenderás a escribir código defensivo que no truene ante datos corruptos y que reporte con claridad qué filas pudieron procesarse y cuáles requieren atención.

---

## ✅ Objetivos de aprendizaje

Al terminar este módulo podrás:

- Manipular estructuras de datos nativas (`dict`, `list`, `set`, `tuple`) y aplicar type hints para código legible.
- Leer, sanitizar y escribir archivos CSV y JSON usando únicamente la biblioteca estándar (`csv`, `json`).
- Implementar validaciones rigurosas y manejo de excepciones (`try/except/finally`) para crear scripts tolerantes a fallos.
- Construir herramientas de línea de comandos profesionales con `argparse` y sustituir `print` por logging estructurado con el módulo `logging`.
- Procesar el archivo real con errores de Distribuidora Halcón (`inventario_erp.csv`) y generar reportes de stock bajo.

---

## 📖 Lecciones

| # | Lección | Nivel | Duración |
|---|---------|-------|----------|
| 01 | [Estructuras de datos y funciones para automatización](lecciones/01-fundamentos-y-estructuras-de-datos.md) | 🟢 | 25 min |
| 02 | [Manipulación de archivos: CSV y JSON en la práctica](lecciones/02-archivos-csv-y-json.md) | 🟢 | 30 min |
| 03 | [Manejo defensivo de errores y validación de datos](lecciones/03-manejo-de-errores-y-validaciones.md) | 🟢 | 30 min |
| 04 | [Herramientas CLI con argparse y logging profesional](lecciones/04-cli-con-argparse-y-logging.md) | 🟢 | 25 min |

---

## 💻 Ejemplos

Scripts listos para ejecutar que procesan los datos del caso de estudio:
- Consulta [ejemplos/README.md](ejemplos/README.md).
  - [Limpiador y normalizador de inventario (`limpiar_inventario.py`)](ejemplos/limpiar_inventario.py)
  - [Generador de reporte de stock bajo en JSON (`generar_reporte_stock.py`)](ejemplos/generar_reporte_stock.py)

---

## 🏋️ Ejercicios

Casos prácticos de programación con soluciones en Python:
- Consulta [ejercicios/README.md](ejercicios/README.md).
  - [Ejercicio 01: Normalizador de catálogo de tiendas con PII](ejercicios/01-normalizador-de-csv.md)
  - [Ejercicio 02: CLI de auditoría y detección de anomalías de inventario](ejercicios/02-cli-de-auditoria-de-inventario.md)

---

## 🎥 Guion sugerido para video

1. **Gancho (1-2 min):** *"Mariana de Distribuidora Halcón pasa 3 horas diarias en Excel arreglando fechas como '01/10/2026' y '4 oct 2026', borrando duplicados y eliminando espacios en blanco. Si le entregas un script de Python que hace todo eso en 0.2 segundos, te ganas un aliado para toda la vida del proyecto."*
2. **Concepto (5-8 min):** Uso del módulo `csv.DictReader` vs listas simples; por qué usar diccionarios y conjuntos (`set`) para deduplicar eficientemente en memoria.
3. **Demo (6-8 min):** Ejecutar `limpiar_inventario.py` en vivo mostrando cómo detecta los 6 errores del CSV y genera el JSON limpio.
4. **Cierre (1-2 min):** La diferencia entre `print()` y `logging.info()`, y presentación del reto del Ejercicio 01.

---

## 📚 Para profundizar

- [Tutorial oficial de Python (Docs oficiales)](../../recursos/lecturas.md#💻-herramientas-unix-y-git).
- [Módulo 04: Datos y SQL](../04-datos-y-sql/README.md).

---

⬅️ [Módulo 01: Herramientas esenciales](../01-herramientas-esenciales/README.md) | 🏠 [Índice](../../README.md) | [Módulo 03: HTTP y APIs](../03-http-y-apis/README.md) ➡️
