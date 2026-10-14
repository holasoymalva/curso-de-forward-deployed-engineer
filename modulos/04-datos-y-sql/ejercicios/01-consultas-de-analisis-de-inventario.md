# Ejercicio 01: Consultas de análisis operativo de inventario

> **Nivel:** 🟢 Principiante · **Tiempo estimado:** 40 min

---

## Contexto

Laura Garza (Operaciones) te solicita tres consultas SQL específicas para su reunión semanal con la junta directiva de Distribuidora Halcón:

1. **Consulta A (Detección de productos huérfanos):** Quiere saber qué productos existen en el catálogo maestro (`productos`) pero **no tienen ningún registro de inventario** en el almacén de Guadalajara (`GDL`).
2. **Consulta B (Resumen por categoría):** Necesita saber, para cada categoría (`abarrotes`, `bebidas`, `limpieza`), el total de piezas en stock sumando todos los almacenes, el precio promedio de los productos de esa categoría y el producto más caro de cada una.
3. **Consulta C (Top 3 productos más valiosos en Monterrey):** Cuáles son los 3 productos con mayor valor económico retenido en el almacén de Monterrey (`cantidad * precio`).

---

## Lo que tienes que hacer

Escribe un script SQL llamado `consultas_ejercicio_01.sql` con las tres consultas solicitadas, asegurando que:
- Usen nombres de alias claros (`AS ...`).
- Apliquen `LEFT JOIN` para la consulta de productos huérfanos.
- Utilicen funciones de agregación (`SUM`, `AVG`, `MAX`, `ROUND`) y `GROUP BY`.

---

## Criterios de aceptación

- [ ] Las consultas se ejecutan sin error sobre `halcon.db`.
- [ ] La Consulta A devuelve los productos sin existencias en GDL usando `LEFT JOIN` y `WHERE ... IS NULL`.
- [ ] La Consulta B agrupa por categoría y redondea los promedios a 2 decimales.
- [ ] La Consulta C calcula el valor monetario (`cantidad * precio`) ordenado de mayor a menor con límite 3.

---

🔑 [Ver solución](soluciones/01-consultas-de-analisis-de-inventario.sql)
