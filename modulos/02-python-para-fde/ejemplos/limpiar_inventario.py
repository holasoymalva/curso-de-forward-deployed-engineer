#!/usr/bin/env python3
"""limpiar_inventario.py

Procesa la exportación nocturna del ERP de Distribuidora Halcón
(recursos/caso-de-estudio/datos/inventario_erp.csv), detecta anomalías,
normaliza campos y genera un archivo limpio y un reporte de errores.

Usa exclusivamente la biblioteca estándar de Python.
"""

from __future__ import annotations

import csv
import json
import logging
import os
import re
from datetime import datetime
from typing import Any

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

ALMACENES_VALIDOS = {"MTY", "GDL", "CDMX"}


def normalizar_sku(sku_raw: str) -> str:
    """Elimina espacios y convierte a mayúsculas consistentes."""
    return sku_raw.strip().upper()


def normalizar_precio(precio_raw: str) -> float:
    """Convierte cadenas como '76,50' o '18.50' a float válido."""
    limpio = precio_raw.strip().replace('"', "").replace("'", "").replace(",", ".")
    valor = float(limpio)
    if valor <= 0:
        raise ValueError(f"Precio inválido: {valor}")
    return round(valor, 2)


def normalizar_cantidad(cant_raw: str) -> int:
    """Valida y convierte la cantidad a un entero no negativo."""
    cant_str = cant_raw.strip()
    if not cant_str or cant_str.upper() in {"N/D", "NA", "NULL"}:
        raise ValueError("Cantidad no disponible o vacía")
    valor = int(cant_str)
    if valor < 0:
        raise ValueError(f"Cantidad negativa: {valor}")
    return valor


def normalizar_fecha(fecha_raw: str) -> str:
    """Normaliza formatos mixtos ('2026-10-01', '01/10/2026', '2026/10/03', '4 oct 2026') a ISO YYYY-MM-DD."""
    fecha_str = fecha_raw.strip().lower()
    
    # Manejar caso de texto en español como '4 oct 2026'
    meses = {"ene": 1, "feb": 2, "mar": 3, "abr": 4, "may": 5, "jun": 6,
             "jul": 7, "ago": 8, "sep": 9, "oct": 10, "nov": 11, "dic": 12}
    
    match_texto = re.match(r"(\d{1,2})\s+([a-z]{3})\s+(\d{4})", fecha_str)
    if match_texto:
        dia, mes_str, anio = match_texto.groups()
        mes_num = meses.get(mes_str)
        if mes_num:
            return f"{int(anio):04d}-{mes_num:02d}-{int(dia):02d}"

    formatos = ["%Y-%m-%d", "%d/%m/%Y", "%Y/%m/%d"]
    for fmt in formatos:
        try:
            return datetime.strptime(fecha_str, fmt).strftime("%Y-%m-%d")
        except ValueError:
            pass

    raise ValueError(f"Formato de fecha no reconocido: '{fecha_raw}'")


def procesar_archivo_inventario(
    ruta_entrada: str, ruta_salida_limpia: str, ruta_reporte_errores: str
) -> tuple[int, int]:
    """Lee el CSV sucio, sanitiza y separa válidos de rechazados."""
    if not os.path.exists(ruta_entrada):
        raise FileNotFoundError(f"No existe el archivo de entrada: {ruta_entrada}")

    registros_validos: dict[tuple[str, str], dict[str, Any]] = {}
    errores: list[dict[str, Any]] = []

    logging.info("Leyendo archivo de inventario: %s", ruta_entrada)

    with open(ruta_entrada, mode="r", encoding="utf-8") as f:
        lector = csv.DictReader(f)
        for num_linea, fila in enumerate(lector, start=2):
            fallas_fila = []

            # 1. Validar y normalizar SKU
            sku = normalizar_sku(fila.get("sku", ""))
            if not sku.startswith("HAL-"):
                fallas_fila.append(f"SKU inválido: '{fila.get('sku')}'")

            # 2. Validar Almacén
            almacen = fila.get("almacen", "").strip().upper()
            if almacen not in ALMACENES_VALIDOS:
                fallas_fila.append(f"Almacén desconocido: '{fila.get('almacen')}' (permitidos: {ALMACENES_VALIDOS})")

            # 3. Validar y normalizar Precio
            try:
                precio = normalizar_precio(fila.get("precio", ""))
            except Exception as e:
                fallas_fila.append(f"Error en precio: {e}")
                precio = 0.0

            # 4. Validar y normalizar Cantidad
            try:
                cantidad = normalizar_cantidad(fila.get("cantidad", ""))
            except Exception as e:
                fallas_fila.append(f"Error en cantidad: {e}")
                cantidad = 0

            # 5. Validar y normalizar Fecha
            try:
                fecha = normalizar_fecha(fila.get("fecha_actualizacion", ""))
            except Exception as e:
                fallas_fila.append(f"Error en fecha: {e}")
                fecha = ""

            nombre = fila.get("nombre", "").strip()
            categoria = fila.get("categoria", "").strip().lower()

            if fallas_fila:
                errores.append({
                    "linea": num_linea,
                    "sku_detectado": sku,
                    "motivos": fallas_fila,
                    "datos_crudos": fila,
                })
            else:
                llave = (sku, almacen)
                if llave in registros_validos:
                    logging.warning("Línea %d: Registro duplicado para %s en %s. Se conserva la versión más reciente.", num_linea, sku, almacen)
                registros_validos[llave] = {
                    "sku": sku,
                    "nombre": nombre,
                    "categoria": categoria,
                    "almacen": almacen,
                    "cantidad": cantidad,
                    "precio": precio,
                    "fecha_actualizacion": fecha,
                }

    # Escribir CSV limpio
    campos = ["sku", "nombre", "categoria", "almacen", "cantidad", "precio", "fecha_actualizacion"]
    with open(ruta_salida_limpia, mode="w", encoding="utf-8", newline="") as f:
        escritor = csv.DictWriter(f, fieldnames=campos)
        escritor.writeheader()
        for item in registros_validos.values():
            escritor.writerow(item)

    # Escribir reporte de errores en JSON
    with open(ruta_reporte_errores, mode="w", encoding="utf-8") as f:
        json.dump(
            {
                "fecha_proceso": datetime.now().isoformat(),
                "total_validos": len(registros_validos),
                "total_rechazados": len(errores),
                "rechazos": errores,
            },
            f,
            indent=2,
            ensure_ascii=False,
        )

    logging.info("✅ Proceso completado: %d registros válidos guardados en '%s'", len(registros_validos), ruta_salida_limpia)
    logging.info("⚠️ %d filas con errores documentadas en '%s'", len(errores), ruta_reporte_errores)

    return len(registros_validos), len(errores)


def main() -> int:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(os.path.dirname(os.path.dirname(base_dir)))
    archivo_erp = os.path.join(repo_root, "recursos", "caso-de-estudio", "datos", "inventario_erp.csv")
    
    salida_limpia = os.path.join(base_dir, "inventario_limpio.csv")
    reporte_errores = os.path.join(base_dir, "reporte_errores.json")

    procesar_archivo_inventario(archivo_erp, salida_limpia, reporte_errores)
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
