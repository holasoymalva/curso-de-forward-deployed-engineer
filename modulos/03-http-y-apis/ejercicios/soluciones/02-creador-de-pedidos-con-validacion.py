#!/usr/bin/env python3
"""02-creador-de-pedidos-con-validacion.py - Solución al Ejercicio 02 del Módulo 03."""

from __future__ import annotations

import json
import urllib.error
import urllib.request
import sys

BASE_URL = "http://127.0.0.1:8000"


def obtener_token() -> str:
    url = f"{BASE_URL}/auth/token"
    payload = json.dumps({"client_id": "nexo-demo", "client_secret": "secreto-de-practica"}).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"}, method="POST")

    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            return json.loads(resp.read().decode("utf-8"))["access_token"]
    except urllib.error.URLError as e:
        print(f"❌ Error conectando con autenticación: {e}", file=sys.stderr)
        sys.exit(1)


def enviar_pedido(token: str, tienda: str, almacen: str, lineas: list[dict]) -> dict | None:
    url = f"{BASE_URL}/pedidos"
    payload = {"tienda": tienda, "almacen": almacen, "lineas": lineas}
    data_bytes = json.dumps(payload).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=data_bytes,
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            datos_creados = json.loads(resp.read().decode("utf-8"))
            print(f"✅ Pedido creado exitosamente con ID #{datos_creados['id']}")
            print(f"   Tienda: {datos_creados['tienda']} | Almacén: {datos_creados['almacen']}")
            return datos_creados
    except urllib.error.HTTPError as err:
        if err.code == 422:
            detalle = json.loads(err.read().decode("utf-8"))
            print(f"⚠️ Error de validación de negocio (HTTP 422):")
            for motivo in detalle.get("detalles", []):
                print(f"   • {motivo}")
        else:
            print(f"❌ Error HTTP inesperado ({err.code}): {err.read().decode('utf-8')}")
        return None


def main() -> None:
    token = obtener_token()

    print("--- CASO 1: Creando pedido válido ---")
    pedido_valido = [
        {"sku": "HAL-1001", "cantidad": 5},
        {"sku": "HAL-1002", "cantidad": 2},
    ]
    enviar_pedido(token, tienda="Tienda Doña Mary", almacen="MTY", lineas=pedido_valido)

    print("\n--- CASO 2: Creando pedido con errores intencionales ---")
    pedido_invalido = [
        {"sku": "HAL-9999", "cantidad": 10},  # SKU inexistente
        {"sku": "HAL-1001", "cantidad": -3},  # Cantidad negativa
    ]
    enviar_pedido(token, tienda="", almacen="XYZ", lineas=pedido_invalido)


if __name__ == "__main__":
    main()
