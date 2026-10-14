# Datos de ejemplo

Datos ficticios de Distribuidora Halcón. **Contienen errores intencionales** para practicar limpieza y validación.

| Archivo | Descripción | Errores incluidos |
|---------|-------------|-------------------|
| [`inventario_erp.csv`](inventario_erp.csv) | Exportación nocturna del ERP. | Filas duplicadas, fechas en varios formatos, cantidades negativas o vacías (`N/D`), SKU en minúsculas, almacén inválido (`XYZ`), mayúsculas inconsistentes, espacios extra, precio con coma decimal. |
| [`tiendas.csv`](tiendas.csv) | Catálogo de tiendas cliente. | Contiene datos personales simulados (nombre, teléfono, correo), teléfonos con formatos distintos, correos inválidos o vacíos y una tienda duplicada. |

> Todos los nombres, teléfonos y correos son inventados.
