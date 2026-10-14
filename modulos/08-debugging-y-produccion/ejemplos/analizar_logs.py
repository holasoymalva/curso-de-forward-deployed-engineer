#!/usr/bin/env python3
"""analizar_logs.py

Herramienta de análisis forense para logs estructurados en JSONL.
Genera estadísticas de niveles, resumen de códigos HTTP y lista de anomalías.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from collections import Counter


def analizar_archivo_logs(ruta_archivo: str) -> int:
    if not os.path.exists(ruta_archivo):
        print(f"❌ Error: Archivo no encontrado: '{ruta_archivo}'", file=sys.stderr)
        return 1

    niveles = Counter()
    codigos_http = Counter()
    errores_detectados = []
    total_lineas = 0

    with open(ruta_archivo, mode="r", encoding="utf-8") as f:
        for num_linea, linea in enumerate(f, start=1):
            linea_limpia = linea.strip()
            if not linea_limpia:
                continue
            total_lineas += 1

            try:
                evento = json.loads(linea_limpia)
            except json.JSONDecodeError:
                errores_detectados.append({"linea": num_linea, "error": "Línea no es JSON válido", "raw": linea_limpia})
                continue

            nivel = evento.get("nivel", "DESCONOCIDO")
            niveles[nivel] += 1

            if "codigo_http" in evento:
                codigos_http[str(evento["codigo_http"])] += 1

            if nivel in {"ERROR", "CRITICAL"}:
                errores_detectados.append({
                    "linea": num_linea,
                    "timestamp": evento.get("timestamp"),
                    "mensaje": evento.get("mensaje"),
                    "codigo_http": evento.get("codigo_http"),
                    "solicitud_id": evento.get("solicitud_id"),
                })

    print("=" * 60)
    print(f"📊 INFORME DE ANÁLISIS FORENSE DE LOGS: {ruta_archivo}")
    print("=" * 60)
    print(f"Total de eventos analizados: {total_lineas}")

    print("\n--- 1. Distribución por Nivel de Severidad ---")
    for niv, cant in niveles.most_common():
        icono = "🔴" if niv in {"ERROR", "CRITICAL"} else "🟡" if niv == "WARNING" else "🟢"
        print(f"  {icono} {niv:<10}: {cant:>4} eventos ({cant/total_lineas*100:.1f}%)")

    print("\n--- 2. Códigos HTTP detectados ---")
    if codigos_http:
        for cod, cant in codigos_http.most_common():
            print(f"  Código {cod}: {cant:>3} veces")
    else:
        print("  (No se registraron códigos HTTP explícitos)")

    print("\n--- 3. Eventos Críticos y Errores Detectados ---")
    if errores_detectados:
        for err in errores_detectados:
            print(f"  • [Línea {err.get('linea')}] {err.get('timestamp')} | HTTP {err.get('codigo_http')} | {err.get('mensaje')}")
    else:
        print("  ✅ Cero errores o eventos críticos.")

    print("=" * 60)
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(description="Analizador forense de logs estructurados en JSONL.")
    parser.add_argument("archivo", nargs="?", default=os.path.join(os.path.dirname(__file__), "logs_produccion_halcon.log"), help="Ruta al archivo .log a analizar")
    args = parser.parse_args()

    sys.exit(analizar_archivo_logs(args.archivo))


if __name__ == "__main__":
    main()
