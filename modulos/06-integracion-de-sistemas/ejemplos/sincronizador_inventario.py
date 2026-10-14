#!/usr/bin/env python3
"""sincronizador_inventario.py

Proceso de sincronización incremental que consulta el endpoint /inventario
de la API de Halcón utilizando el ClienteHalconResiliente y persiste
los cambios de existencias de manera atómica en SQLite.
"""

from __future__ import annotations

import logging
import os
import sqlite3
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MOD4_DIR = os.path.join(os.path.dirname(BASE_DIR), "04-datos-y-sql", "ejemplos")
DB_PATH = os.path.join(MOD4_DIR, "halcon.db")

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


def sincronizar_inventario_api_a_db() -> int:
    from cliente_resiliente import ClienteHalconResiliente

    if not os.path.exists(DB_PATH):
        logging.error("No se encontró la base de datos en %s. Inicialízala en el Módulo 04.", DB_PATH)
        return 1

    cliente = ClienteHalconResiliente()
    logging.info("Iniciando sincronización incremental de inventario desde API...")

    # Recuperar todo el inventario con paginación resiliente
    try:
        registros_api = cliente.paginar_coleccion("/inventario", por_pagina=50)
    except Exception as e:
        logging.critical("Falla al recuperar inventario de la API: %s", e)
        return 1

    logging.info("Se recuperaron %d registros de existencias desde la API.", len(registros_api))

    conexion = sqlite3.connect(DB_PATH)
    lote_actualizacion = [
        (r["sku"], r["almacen"], r["cantidad"], r["actualizado"])
        for r in registros_api
    ]

    sql = """
    INSERT INTO inventario (sku, almacen_codigo, cantidad, fecha_actualizacion)
    VALUES (?, ?, ?, ?)
    ON CONFLICT(sku, almacen_codigo) DO UPDATE SET
        cantidad = excluded.cantidad,
        fecha_actualizacion = excluded.fecha_actualizacion;
    """

    with conexion:
        conexion.executemany(sql, lote_actualizacion)

    logging.info("✅ Sincronización exitosa: %d registros persistidos en SQLite.", len(lote_actualizacion))
    conexion.close()
    return 0


if __name__ == "__main__":
    sys.exit(sincronizar_inventario_api_a_db())
