#!/usr/bin/env python3
"""generar_reporte_stock.py

Herramienta de línea de comandos (CLI) con argparse y logging que lee
el inventario limpio y genera alertas para productos que están
por debajo del umbral de stock de seguridad.
"""

from __future__ import annotations

import argparse
import csv
import json
import logging
import os
import sys
from datetime import datetime


def configurar_cli() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Genera reporte y alertas de stock bajo para Distribuidora Halcón."
    )
    parser.add_argument(
        "-i", "--entrada",
        type=str,
        default=os.path.join(os.path.dirname(__file__), "inventario_limpio.csv"),
        help="Ruta al archivo CSV de inventario limpio (default: inventario_limpio.csv)",
    )
    parser.add_argument(
        "-o", "--salida",
        type=str,
        default=os.path.join(os.path.dirname(__file__), "alerta_stock_bajo.json"),
        help="Ruta donde se escribirá el reporte JSON de alertas",
    )
    parser.add_argument(
        "-u", "--umbral",
        type=int,
        default=25,
        help="Umbral de unidades para considerar stock en riesgo (default: 25)",
    )
    parser.add_argument(
        "-a", "--almacen",
        type=str,
        choices=["MTY", "GDL", "CDMX", "TODOS"],
        default="TODOS",
        help="Filtrar alertas por almacén específico (default: TODOS)",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Activar registro detallado (DEBUG)",
    )
    return parser.parse_args()


def generar_alertas(
    ruta_entrada: str, ruta_salida: str, umbral: int, almacen_filtro: str
) -> int:
    if not os.path.exists(ruta_entrada):
        logging.error("El archivo '%s' no existe. Ejecuta primero limpiar_inventario.py.", ruta_entrada)
        return 1

    logging.info("Analizando inventario desde: %s (Umbral de riesgo: %d unidades)", ruta_entrada, umbral)

    alertas = []
    total_revisados = 0

    with open(ruta_entrada, mode="r", encoding="utf-8") as f:
        lector = csv.DictReader(f)
        for fila in lector:
            total_revisados += 1
            almacen = fila.get("almacen", "").upper()

            if almacen_filtro != "TODOS" and almacen != almacen_filtro:
                continue

            try:
                cantidad = int(fila.get("cantidad", 0))
            except ValueError:
                cantidad = 0

            if cantidad <= umbral:
                nivel_urgencia = "CRÍTICO" if cantidad == 0 else "ALTO" if cantidad <= 10 else "MEDIO"
                alerta = {
                    "sku": fila.get("sku"),
                    "nombre": fila.get("nombre"),
                    "categoria": fila.get("categoria"),
                    "almacen": almacen,
                    "cantidad_actual": cantidad,
                    "urgencia": nivel_urgencia,
                    "fecha_actualizacion": fila.get("fecha_actualizacion"),
                }
                alertas.append(alerta)
                logging.warning(
                    "⚠️  [%s] %s (%s) en %s con solo %d unidades.",
                    nivel_urgencia, alerta["nombre"], alerta["sku"], almacen, cantidad
                )

    reporte = {
        "generado_el": datetime.now().isoformat(),
        "umbral_configurado": umbral,
        "filtro_almacen": almacen_filtro,
        "total_productos_analizados": total_revisados,
        "total_alertas_detectadas": len(alertas),
        "alertas": alertas,
    }

    with open(ruta_salida, mode="w", encoding="utf-8") as f:
        json.dump(reporte, f, indent=2, ensure_ascii=False)

    logging.info(
        "✅ Reporte generado exitosamente con %d alertas en: %s",
        len(alertas), ruta_salida
    )
    return 0


def main() -> int:
    args = configurar_cli()
    nivel_log = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=nivel_log, format="%(asctime)s [%(levelname)s] %(message)s")

    return generar_alertas(args.entrada, args.salida, args.umbral, args.almacen)


if __name__ == "__main__":
    sys.exit(main())
