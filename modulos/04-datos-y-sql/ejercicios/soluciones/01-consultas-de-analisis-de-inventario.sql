-- ==============================================================================
-- 01-consultas-de-analisis-de-inventario.sql
-- Solución al Ejercicio 01 del Módulo 04.
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- CONSULTA A: Productos en catálogo que NO tienen inventario registrado en GDL
-- Usa LEFT JOIN y filtra donde la clave de la tabla derecha es NULL
-- ------------------------------------------------------------------------------
SELECT 
    p.sku,
    p.nombre,
    p.categoria,
    p.precio
FROM productos p
LEFT JOIN inventario i 
    ON p.sku = i.sku AND i.almacen_codigo = 'GDL'
WHERE i.id IS NULL
ORDER BY p.categoria, p.sku;


-- ------------------------------------------------------------------------------
-- CONSULTA B: Resumen analítico por categoría de producto
-- Total de piezas, precio promedio y precio máximo por categoría
-- ------------------------------------------------------------------------------
SELECT 
    p.categoria,
    COUNT(DISTINCT p.sku) AS total_skus,
    COALESCE(SUM(i.cantidad), 0) AS unidades_en_stock,
    ROUND(AVG(p.precio), 2) AS precio_promedio,
    ROUND(MAX(p.precio), 2) AS precio_maximo
FROM productos p
LEFT JOIN inventario i ON p.sku = i.sku
GROUP BY p.categoria
ORDER BY unidades_en_stock DESC;


-- ------------------------------------------------------------------------------
-- CONSULTA C: Top 3 productos con mayor valor económico en Monterrey
-- Valor económico = existencias físicas * precio unitario
-- ------------------------------------------------------------------------------
SELECT 
    p.sku,
    p.nombre,
    p.categoria,
    i.cantidad AS unidades,
    p.precio AS precio_unitario,
    ROUND(i.cantidad * p.precio, 2) AS valor_total_inventario
FROM inventario i
INNER JOIN productos p ON i.sku = p.sku
WHERE i.almacen_codigo = 'MTY'
ORDER BY valor_total_inventario DESC
LIMIT 3;
