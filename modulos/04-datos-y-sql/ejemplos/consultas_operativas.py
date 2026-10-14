#!/usr/bin/env python3
"""consultas_operativas.py

Demuestra la ejecución de consultas analíticas avanzadas
(JOINs, agrupaciones, CTEs) contra la base SQLite cargada.
"""

from __future__ import annotations

import os
import sqlite3
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "halcon.db")


def ejecutar_consultas() -> None:
    if not os.path.exists(DB_PATH):
        print(f"❌ Base de datos no encontrada en {DB_PATH}. Ejecuta primero cargar_datos_sqlite.py.", file=sys.stderr)
        sys.exit(1)

    conexion = sqlite3.connect(DB_PATH)
    conexion.row_factory = sqlite3.Row
    cursor = conexion.cursor()

    print("=" * 65)
    print("📊 1. REPORTE DE ALERTAS: PRODUCTOS CON STOCK <= MÍNIMO (INNER JOIN)")
    print("=" * 65)
    sql_alertas = """
    SELECT 
        p.sku,
        p.nombre,
        i.almacen_codigo AS almacen,
        i.cantidad AS stock_actual,
        p.stock_minimo,
        (p.stock_minimo - i.cantidad) AS deficit
    FROM productos p
    INNER JOIN inventario i ON p.sku = i.sku
    WHERE i.cantidad <= p.stock_minimo
    ORDER BY deficit DESC, i.almacen_codigo;
    """
    cursor.execute(sql_alertas)
    filas = cursor.fetchall()
    for f in filas:
        print(f" • [{f['almacen']}] {f['sku']} {f['nombre']:<20} | Stock: {f['stock_actual']:>3} (Mín: {f['stock_minimo']:>2}) | Déficit: -{f['deficit']}")

    print("\n" + "=" * 65)
    print("📈 2. RESUMEN DE INVENTARIO Y VALOR ESTIMADO POR ALMACÉN (CTE + GROUP BY)")
    print("=" * 65)
    sql_resumen = """
    WITH MetricasInventario AS (
        SELECT 
            i.almacen_codigo,
            COUNT(DISTINCT i.sku) AS skus_distintos,
            SUM(i.cantidad) AS piezas_totales,
            SUM(i.cantidad * p.precio) AS valor_monetario_total
        FROM inventario i
        INNER JOIN productos p ON i.sku = p.sku
        GROUP BY i.almacen_codigo
    )
    SELECT 
        a.codigo,
        a.nombre,
        a.ciudad,
        m.skus_distintos,
        m.piezas_totales,
        ROUND(m.valor_monetario_total, 2) AS valor_inventario
    FROM MetricasInventario m
    INNER JOIN almacenes a ON m.almacen_codigo = a.codigo
    ORDER BY m.valor_monetario_total DESC;
    """
    cursor.execute(sql_resumen)
    for f in cursor.fetchall():
        print(f" 🏢 {f['nombre']} ({f['ciudad']}):")
        print(f"    SKUs: {f['skus_distintos']} | Unidades: {f['piezas_totales']} | Valor estimado: ${f['valor_inventario']:,.2f}")

    conexion.close()


if __name__ == "__main__":
    ejecutar_consultas()
