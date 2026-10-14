#!/usr/bin/env python3
"""worker_sincronizacion.py

Worker en segundo plano para el contenedor Docker de Nexo.
Ejecuta ciclos periódicos de sincronización contra la API de Halcón
y persiste existencias y pedidos pendientes en SQLite de forma atómica.
"""

from __future__ import annotations

import logging
import os
import sqlite3
import sys
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s [WORKER] %(message)s")

API_BASE_URL = os.environ.get("API_BASE_URL", "http://127.0.0.1:8000")
CLIENT_ID = os.environ.get("CLIENT_ID", "nexo-demo")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET", "secreto-de-practica")
DB_PATH = os.environ.get("DB_PATH", "halcon.db")
INTERVALO_SEG = int(os.environ.get("INTERVALO_SYNC_SEG", "30"))


def asegurar_base_datos(db_path: str) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
    con = sqlite3.connect(db_path)
    with con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS inventario_sincronizado (
                sku TEXT NOT NULL,
                almacen TEXT NOT NULL,
                cantidad INTEGER NOT NULL,
                actualizado TEXT NOT NULL,
                sincronizado_el TEXT DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY(sku, almacen)
            );
        """)
    con.close()


def ciclo_sincronizacion() -> None:
    from cliente_resiliente import ClienteHalconResiliente

    cliente = ClienteHalconResiliente(
        base_url=API_BASE_URL,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        max_reintentos=4,
    )

    logging.info("--- Iniciando ciclo de sincronización ---")
    try:
        inventario = cliente.paginar_coleccion("/inventario", por_pagina=50)
        logging.info("Recibidos %d registros desde %s", len(inventario), API_BASE_URL)

        con = sqlite3.connect(DB_PATH)
        with con:
            sql = """
            INSERT INTO inventario_sincronizado (sku, almacen, cantidad, actualizado, sincronizado_el)
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(sku, almacen) DO UPDATE SET
                cantidad=excluded.cantidad,
                actualizado=excluded.actualizado,
                sincronizado_el=CURRENT_TIMESTAMP;
            """
            lote = [(i["sku"], i["almacen"], i["cantidad"], i["actualizado"]) for i in inventario]
            con.executemany(sql, lote)
        con.close()

        logging.info("✅ Sincronización completada. %d registros actualizados en BD.", len(lote))
    except Exception as e:
        logging.error("❌ Falla en el ciclo de sincronización: %s", e)


def main() -> None:
    logging.info("Iniciando Worker de Sincronización Nexo...")
    logging.info("Destino BD: %s | Intervalo: %d segundos", DB_PATH, INTERVALO_SEG)

    asegurar_base_datos(DB_PATH)

    while True:
        ciclo_sincronizacion()
        logging.info("Esperando %d segundos hasta el próximo ciclo...\n", INTERVALO_SEG)
        time.sleep(INTERVALO_SEG)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.info("Worker detenido cordialmente.")
        sys.exit(0)
