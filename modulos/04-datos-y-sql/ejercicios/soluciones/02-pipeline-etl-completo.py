#!/usr/bin/env python3
"""02-pipeline-etl-completo.py - Solución al Ejercicio 02 del Módulo 04."""

from __future__ import annotations

import csv
import json
import logging
import os
import sqlite3
import sys
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MOD_DIR = os.path.dirname(os.path.dirname(BASE_DIR))
REPO_ROOT = os.path.dirname(os.path.dirname(MOD_DIR))

DB_PATH = os.path.join(MOD_DIR, "ejemplos", "halcon.db")
CSV_PATH = os.path.join(REPO_ROOT, "recursos", "caso-de-estudio", "datos", "inventario_erp.csv")


def asegurar_tabla_auditoria(conexion: sqlite3.Connection) -> None:
    sql = """
    CREATE TABLE IF NOT EXISTS auditoria_rechazos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha_proceso TEXT NOT NULL,
        numero_linea INTEGER NOT NULL,
        sku_crudo TEXT,
        motivo TEXT NOT NULL,
        contenido_crudo TEXT NOT NULL
    );
    """
    conexion.execute(sql)
    conexion.commit()


def ejecutar_etl_con_auditoria(ruta_csv: str, ruta_db: str) -> None:
    if not os.path.exists(ruta_csv):
        logging.error("No se encontró el archivo CSV: %s", ruta_csv)
        sys.exit(1)

    # Reusar funciones de limpieza del Módulo 02
    sys.path.insert(0, os.path.join(REPO_ROOT, "modulos", "02-python-para-fde", "ejemplos"))
    from limpiar_inventario import normalizar_sku, normalizar_precio, normalizar_cantidad, normalizar_fecha, ALMACENES_VALIDOS

    conexion = sqlite3.connect(ruta_db)
    asegurar_tabla_auditoria(conexion)

    productos_validos: dict[str, tuple] = {}
    inventario_valido: dict[tuple[str, str], tuple] = {}
    rechazos: list[tuple] = []
    fecha_ahora = datetime.now().isoformat()

    logging.info("Procesando ETL con auditoría desde: %s", ruta_csv)

    with open(ruta_csv, mode="r", encoding="utf-8") as f:
        lector = csv.DictReader(f)
        for num_linea, fila in enumerate(lector, start=2):
            motivos = []
            sku_crudo = fila.get("sku", "")

            sku = normalizar_sku(sku_crudo)
            if not sku.startswith("HAL-"):
                motivos.append("SKU inválido")

            almacen = fila.get("almacen", "").strip().upper()
            if almacen not in ALMACENES_VALIDOS:
                motivos.append(f"Almacén '{almacen}' fuera de catálogo")

            try:
                precio = normalizar_precio(fila.get("precio", ""))
            except Exception as e:
                motivos.append(f"Precio inválido: {e}")
                precio = 0.0

            try:
                cantidad = normalizar_cantidad(fila.get("cantidad", ""))
            except Exception as e:
                motivos.append(f"Cantidad inválida: {e}")
                cantidad = 0

            try:
                fecha = normalizar_fecha(fila.get("fecha_actualizacion", ""))
            except Exception as e:
                motivos.append(f"Fecha inválida: {e}")
                fecha = ""

            if motivos:
                rechazos.append((
                    fecha_ahora,
                    num_linea,
                    sku_crudo,
                    "; ".join(motivos),
                    json.dumps(fila, ensure_ascii=False)
                ))
            else:
                productos_validos[sku] = (sku, fila.get("nombre", "").strip(), fila.get("categoria", "").strip().lower(), precio, 20)
                inventario_valido[(sku, almacen)] = (sku, almacen, cantidad, fecha)

    # Inserción atómica en base de datos
    with conexion:
        # 1. Catálogo
        conexion.executemany("""
            INSERT INTO productos (sku, nombre, categoria, precio, stock_minimo)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(sku) DO UPDATE SET precio=excluded.precio, nombre=excluded.nombre;
        """, list(productos_validos.values()))

        # 2. Inventario
        conexion.executemany("""
            INSERT INTO inventario (sku, almacen_codigo, cantidad, fecha_actualizacion)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(sku, almacen_codigo) DO UPDATE SET cantidad=excluded.cantidad, fecha_actualizacion=excluded.fecha_actualizacion;
        """, list(inventario_valido.values()))

        # 3. Auditoría de rechazos
        conexion.executemany("""
            INSERT INTO auditoria_rechazos (fecha_proceso, numero_linea, sku_crudo, motivo, contenido_crudo)
            VALUES (?, ?, ?, ?, ?);
        """, rechazos)

    logging.info("✅ Pipeline completado con éxito:")
    logging.info("   • Productos cargados/actualizados: %d", len(productos_validos))
    logging.info("   • Registros de inventario:         %d", len(inventario_valido))
    logging.info("   • Anomalías guardadas en auditoría: %d", len(rechazos))

    conexion.close()


if __name__ == "__main__":
    ejecutar_etl_con_auditoria(CSV_PATH, DB_PATH)
