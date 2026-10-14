# Solución al Ejercicio 02: CLI de auditoría y detección de anomalías

Código completo del script `auditar_inventario.py`:

```python
#!/usr/bin/env python3
"""auditar_inventario.py - Solución al Ejercicio 02."""

from __future__ import annotations

import argparse
import csv
import json
import logging
import os
import sys

ALMACENES_VALIDOS = {"MTY", "GDL", "CDMX"}


def auditar_archivo(ruta_csv: str, max_errores: int, ruta_reporte: str | None) -> int:
    if not os.path.exists(ruta_csv):
        logging.error("El archivo no existe: %s", ruta_csv)
        return 1

    errores_encontrados = []
    total_filas = 0

    with open(ruta_csv, mode="r", encoding="utf-8") as f:
        lector = csv.DictReader(f)
        for num_linea, fila in enumerate(lector, start=2):
            total_filas += 1
            fallas = []

            # 1. Regla SKU
            sku = fila.get("sku", "").strip().upper()
            if not sku.startswith("HAL-"):
                fallas.append("SKU no comienza con 'HAL-'")

            # 2. Regla Almacén
            almacen = fila.get("almacen", "").strip().upper()
            if almacen not in ALMACENES_VALIDOS:
                fallas.append(f"Almacén '{almacen}' fuera de catálogo {ALMACENES_VALIDOS}")

            # 3. Regla Cantidad
            try:
                cant = int(fila.get("cantidad", ""))
                if cant < 0:
                    fallas.append(f"Cantidad negativa ({cant})")
            except (ValueError, TypeError):
                fallas.append("Cantidad no es un entero válido")

            # 4. Regla Precio
            try:
                precio_limpio = fila.get("precio", "").replace(",", ".").replace('"', "").strip()
                precio = float(precio_limpio)
                if precio <= 0:
                    fallas.append(f"Precio menor o igual a cero ({precio})")
            except (ValueError, TypeError):
                fallas.append("Precio no es numérico")

            if fallas:
                errores_encontrados.append({
                    "linea": num_linea,
                    "sku": sku,
                    "fallas": fallas,
                    "fila_cruda": fila
                })

    logging.info("Auditoría terminada: %d filas inspeccionadas, %d errores encontrados.", total_filas, len(errores_encontrados))

    if ruta_reporte:
        with open(ruta_reporte, mode="w", encoding="utf-8") as f:
            json.dump({
                "archivo_auditado": ruta_csv,
                "total_filas": total_filas,
                "total_errores": len(errores_encontrados),
                "detalles": errores_encontrados
            }, f, indent=2, ensure_ascii=False)
        logging.info("Reporte detallado guardado en: %s", ruta_reporte)

    if len(errores_encontrados) > max_errores:
        logging.error("❌ Auditoría FALLIDA: %d errores superan el máximo tolerable de %d.", len(errores_encontrados), max_errores)
        return 1

    logging.info("✅ Auditoría APROBADA: Errores dentro del umbral permitido.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Auditor de calidad de datos para archivos de inventario.")
    parser.add_argument("archivo", help="Ruta al archivo CSV de inventario a auditar")
    parser.add_argument("--max-errores", type=int, default=0, help="Máximo número de errores permitidos (default: 0)")
    parser.add_argument("--salida-reporte", help="Ruta opcional para guardar el informe en JSON")
    parser.add_argument("-v", "--verbose", action="store_true", help="Mostrar logs detallados")

    args = parser.parse_args()
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

    return auditar_archivo(args.archivo, args.max_errores, args.salida_reporte)


if __name__ == "__main__":
    sys.exit(main())
```
