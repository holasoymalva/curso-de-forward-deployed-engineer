# Ejercicio 02: Pipeline ETL completo con tabla de auditoría

> **Nivel:** 🟢 Principiante · **Tiempo estimado:** 50 min

---

## Contexto

Roberto Treviño (TI) te dice: *"No podemos permitir que los registros con errores se descarten en el aire sin dejar rastro en la base de datos. Si una fila del CSV viene corrupta o con un almacén inválido, necesitamos que quede guardada en una tabla relacional de auditoría llamada `auditoria_rechazos` para que mi equipo pueda investigar por qué el ERP exportó esa anomalía"*.

---

## Lo que tienes que hacer

Crea un script en Python llamado `etl_con_auditoria.py` que:

1. Cree una tabla adicional en SQLite llamada `auditoria_rechazos`:
   ```sql
   CREATE TABLE IF NOT EXISTS auditoria_rechazos (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       fecha_proceso TEXT NOT NULL,
       numero_linea INTEGER NOT NULL,
       sku_crudo TEXT,
       motivo TEXT NOT NULL,
       contenido_crudo TEXT NOT NULL
   );
   ```
2. Procese el archivo `recursos/caso-de-estudio/datos/inventario_erp.csv`.
3. Inserte los registros limpios en las tablas `productos` e `inventario`.
4. Inserte cada fila rechazada (por ejemplo, el almacén `XYZ` o la cantidad `N/D`) en la tabla `auditoria_rechazos`.
5. Ejecute todo el proceso dentro de una sola transacción segura con `conexion.commit()`.

---

## Criterios de aceptación

- [ ] La tabla `auditoria_rechazos` se crea automáticamente si no existe.
- [ ] Las filas con errores del CSV quedan registradas en `auditoria_rechazos` con su número de línea y motivo.
- [ ] Las filas válidas se cargan en `inventario` y `productos`.
- [ ] El script es completamente idempotente (puede ejecutarse múltiples veces sin duplicar registros).

---

🔑 [Ver solución](soluciones/02-pipeline-etl-completo.py)
