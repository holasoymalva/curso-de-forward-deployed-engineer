#!/usr/bin/env python3
"""cliente_api_basico.py

Demostración de consumo de API REST usando exclusivamente la
biblioteca estándar de Python (urllib.request y json).
Se conecta a la API simulada de Distribuidora Halcón.
"""

from __future__ import annotations

import json
import logging
import os
import sys
import urllib.error
import urllib.request
from typing import Any

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

BASE_URL = os.environ.get("API_BASE_URL", "http://127.0.0.1:8000")
CLIENT_ID = os.environ.get("CLIENT_ID", "nexo-demo")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET", "secreto-de-practica")


class ClienteHalconBasico:
    """Cliente HTTP mínimo para interactuar con la API simulada."""

    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url.rstrip("/")
        self.token: str | None = None

    def _peticion(
        self, metodo: str, ruta: str, payload: dict | None = None, requiere_auth: bool = True
    ) -> dict[str, Any]:
        url = f"{self.base_url}/{ruta.lstrip('/')}"
        headers = {"Content-Type": "application/json"}

        if requiere_auth:
            if not self.token:
                raise ValueError("No hay token activo. Ejecuta autenticar() primero.")
            headers["Authorization"] = f"Bearer {self.token}"

        data_bytes = json.dumps(payload).encode("utf-8") if payload is not None else None
        req = urllib.request.Request(url, data=data_bytes, headers=headers, method=metodo)

        try:
            with urllib.request.urlopen(req, timeout=5) as resp:
                cuerpo = resp.read().decode("utf-8")
                return json.loads(cuerpo) if cuerpo else {}
        except urllib.error.HTTPError as e:
            cuerpo_error = e.read().decode("utf-8")
            logging.error("HTTP %d en %s %s: %s", e.code, metodo, ruta, cuerpo_error)
            raise
        except urllib.error.URLError as e:
            logging.error("Error de conexión con el servidor: %s", e.reason)
            raise

    def verificar_salud(self) -> bool:
        """Comprueba el endpoint público /salud."""
        try:
            res = self._peticion("GET", "/salud", requiere_auth=False)
            return res.get("estado") == "ok"
        except Exception:
            return False

    def autenticar(self, client_id: str = CLIENT_ID, client_secret: str = CLIENT_SECRET) -> str:
        """Solicita un Bearer Token enviando credenciales a /auth/token."""
        logging.info("Solicitando token para client_id: %s", client_id)
        payload = {"client_id": client_id, "client_secret": client_secret}
        res = self._peticion("POST", "/auth/token", payload=payload, requiere_auth=False)
        self.token = res["access_token"]
        logging.info("Token obtenido con éxito (vigencia: %ds)", res.get("expires_in", 300))
        return self.token

    def listar_productos(self, categoria: str | None = None, limite: int = 5) -> list[dict]:
        """Consulta el catálogo de productos paginado."""
        ruta = f"/productos?por_pagina={limite}"
        if categoria:
            ruta += f"&categoria={categoria}"
        res = self._peticion("GET", ruta)
        return res.get("datos", [])


def main() -> int:
    cliente = ClienteHalconBasico()

    logging.info("--- 1. Verificando disponibilidad del servidor ---")
    if not cliente.verificar_salud():
        logging.error("❌ El servidor en %s no responde. ¿Iniciaste servidor.py?", BASE_URL)
        return 1
    logging.info("✅ Servidor activo y saludable.")

    logging.info("--- 2. Autenticándose ---")
    cliente.autenticar()

    logging.info("--- 3. Consultando productos de abarrotes ---")
    productos = cliente.listar_productos(categoria="abarrotes", limite=3)
    for p in productos:
        print(f"   📦 [{p['sku']}] {p['nombre']} - ${p['precio']:.2f}")

    logging.info("--- 4. Probando captura de error 404 (producto inexistente) ---")
    try:
        cliente._peticion("GET", "/productos/HAL-9999")
    except urllib.error.HTTPError as e:
        print(f"   Captura esperada exitosa: Código HTTP {e.code}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
