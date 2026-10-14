#!/usr/bin/env python3
"""01-consultor-de-pedidos-pendientes.py - Solución al Ejercicio 01 del Módulo 03."""

from __future__ import annotations

import json
import urllib.error
import urllib.request
import sys

BASE_URL = "http://127.0.0.1:8000"


def obtener_token(client_id: str = "nexo-demo", client_secret: str = "secreto-de-practica") -> str:
    url = f"{BASE_URL}/auth/token"
    payload = json.dumps({"client_id": client_id, "client_secret": client_secret}).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"}, method="POST")

    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["access_token"]
    except urllib.error.URLError as e:
        print(f"❌ Error al conectar con el servidor de autenticación: {e}", file=sys.stderr)
        sys.exit(1)


def consultar_todos_los_pendientes(token: str, almacen: str = "MTY") -> list[dict]:
    pedidos_acumulados = []
    pagina_actual = 1

    print(f"🔍 Consultando pedidos pendientes para almacén {almacen}...")

    while pagina_actual is not None:
        url = f"{BASE_URL}/pedidos?almacen={almacen}&estado=pendiente&pagina={pagina_actual}&por_pagina=20"
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"}, method="GET")

        with urllib.request.urlopen(req, timeout=5) as resp:
            respuesta_json = json.loads(resp.read().decode("utf-8"))

        datos_pagina = respuesta_json.get("datos", [])
        pedidos_acumulados.extend(datos_pagina)
        print(f"   Página {pagina_actual}: {len(datos_pagina)} pedidos recuperados.")

        pagina_actual = respuesta_json.get("siguiente_pagina")

    return pedidos_acumulados


def main() -> None:
    token = obtener_token()
    pedidos = consultar_todos_los_pendientes(token, almacen="MTY")

    print("\n" + "=" * 55)
    print(f"📊 REPORTE DE PEDIDOS PENDIENTES - ALMACÉN MTY")
    print("=" * 55)
    print(f"Total de pedidos encontrados: {len(pedidos)}\n")

    for p in pedidos:
        articulos_totales = sum(linea.get("cantidad", 0) for linea in p.get("lineas", []))
        print(f" • Pedido #{p['id']:03d} | {p['tienda']:<15} | Fecha: {p['fecha']} | Unidades: {articulos_totales}")

    print("=" * 55)


if __name__ == "__main__":
    main()
