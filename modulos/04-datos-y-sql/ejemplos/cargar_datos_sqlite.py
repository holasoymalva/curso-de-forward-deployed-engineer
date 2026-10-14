#!/usr/bin/env python3
"""cargar_datos_sqlite.py

Pipeline ETL que inicializa el esquema SQLite y carga los datos limpios
de inventario_erp.csv y los almacenes oficiales de Distribuidora Halcón.
"""

from __future__ import annotations

import csv
import logging
import os
import sqlite3
import sys

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(BASE_DIR)))
DB_PATH = os.path.join(BASE_DIR, "halcon.db")
SQL_SCHEMA_PATH = os.path.join(BASE_DIR, "esquema.sql")
CSV_PATH = os.path.join(REPO_ROOT, "recursos", "caso-de-estudio", "datos", "inventario_erp.csv")


def inicializar_bd(conexion: sqlite3.Connection) -> None:
    logging.info("Inicializando esquema en base de datos: %s", DB_PATH)
    with open(SQL_SCHEMA_PATH, mode="r", encoding="utf-8") as f:
        script_sql = f.read()
    conexion.executescript(script_sql)

    # Insertar almacenes base si no existen
    almacenes_base = [
        ("MTY", "Almacén Regional Norte", "Monterrey", "Nuevo León"),
        ("GDL", "Almacén Regional Occidente", "Guadalajara", "Jalisco"),
        ("CDMX", "Centro de Distribución Valle de México", "Ciudad de México", "CDMX"),
    ]
    conexion.executemany(
        "INSERT OR IGNORE INTO almacenes (codigo, nombre, ciudad, estado) VALUES (?, ?, ?, ?);",
        almacenes_base,
    )
    conexion.commit()


def cargar_inventario_csv(conexion: sqlite3.Connection, ruta_csv: str) -> tuple[int, int]:
    # Importar el normalizador del módulo 02 para reusar código limpio
    sys.path.insert(0, os.path.join(REPO_ROOT, "modulos", "02-python-para-fde", "ejemplos"))
    try:
        from limpiar_inventario import normalizar_sku, normalizar_precio, normalizar_cantidad, normalizar_fecha, ALMACENES_VALIDOS
    except ImportError:
        logging.error("No se pudo importar limpiar_inventario.py")
        return 0, 0

    productos_map: dict[str, tuple[str, str, str, float, int]] = {}
    inventario_map: dict[tuple[str, str], tuple[str, str, int, str]] = {}
    errores = 0

    with open(ruta_csv, mode="r", encoding="utf-8") as f:
        lector = csv.DictReader(f)
        for fila in lector:
            try:
                sku = normalizar_sku(fila.get("sku", ""))
                almacen = fila.get("almacen", "").strip().upper()
                if not sku.startswith("HAL-") or almacen not in ALMACENES_VALIDOS:
                    errores += 1
                    continue

                precio = normalizar_precio(fila.get("precio", ""))
                cantidad = normalizar_cantidad(fila.get("cantidad", ""))
                fecha = normalizar_fecha(fila.get("fecha_actualizacion", ""))
                nombre = fila.get("nombre", "").strip()
                categoria = fila.get("categoria", "").strip().lower()

                # Catálogo
                productos_map[sku] = (sku, nombre, categoria, precio, 20)
                # Inventario
                inventario_map[(sku, almacen)] = (sku, almacen, cantidad, fecha)
            except Exception:
                errores += 1

    # Cargar Productos
    sql_prod = """
    INSERT INTO productos (sku, nombre, categoria, precio, stock_minimo)
    VALUES (?, ?, ?, ?, ?)
    ON CONFLICT(sku) DO UPDATE SET precio=excluded.precio, nombre=excluded.nombre;
    """
    conexion.executemany(sql_prod, list(productos_map.values()))

    # Cargar Inventario
    sql_inv = """
    INSERT INTO inventario (sku, almacen_codigo, cantidad, fecha_actualizacion)
    VALUES (?, ?, ?, ?)
    ON CONFLICT(sku, almacen_codigo) DO UPDATE SET cantidad=excluded.cantidad, fecha_actualizacion=excluded.fecha_actualizacion;
    """
    conexion.executemany(sql_inv, list(inventario_map.values()))
    conexion.commit()

    logging.info("✅ ETL Exitoso: %d productos y %d existencias cargadas a SQLite.", len(productos_map), len(inventario_map))
    if errores:
        logging.warning("⚠️ %d registros descartados por datos inválidos.", errores)

    return len(productos_map), len(inventario_map)


def main() -> None:
    conexion = sqlite3.connect(DB_PATH)
    try:
        inicializar_bd(conexion)
        cargar_inventario_csv(conexion, CSV_PATH)
    finally:
        conexion.close()


if __name__ == "__main__":
    main()
