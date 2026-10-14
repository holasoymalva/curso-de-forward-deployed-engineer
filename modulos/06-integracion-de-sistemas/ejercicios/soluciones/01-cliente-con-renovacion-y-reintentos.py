#!/usr/bin/env python3
"""01-cliente-con-renovacion-y-reintentos.py - Solución al Ejercicio 01 del Módulo 06."""

from __future__ import annotations

import json
import logging
import os
import random
import time
import urllib.error
import urllib.request
from typing import Any

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

BASE_URL = os.environ.get("API_BASE_URL", "http://127.0.0.1:8000")


class GestorAutenticacion:
    def __init__(self, base_url: str = BASE_URL, client_id: str = "nexo-demo", client_secret: str = "secreto-de-practica"):
        self.base_url = base_url.rstrip("/")
        self.client_id = client_id
        self.client_secret = client_secret
        self.token: str | None = None
        self.expira_epoch: float = 0.0

    def obtener_token(self, forzar: bool = False) -> str:
        ahora = time.time()
        if forzar or not self.token or ahora >= (self.expira_epoch - 30):
            logging.info("Solicitando nuevo token a /auth/token...")
            payload = json.dumps({"client_id": self.client_id, "client_secret": self.client_secret}).encode("utf-8")
            req = urllib.request.Request(f"{self.base_url}/auth/token", data=payload, headers={"Content-Type": "application/json"}, method="POST")
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                self.token = data["access_token"]
                self.expira_epoch = ahora + data.get("expires_in", 300)
                logging.info("Token obtenido con éxito (expira en %ds).", data.get("expires_in", 300))
        return self.token


def consultar_con_resiliencia(ruta: str, auth_manager: GestorAutenticacion, max_intentos: int = 4) -> dict[str, Any]:
    url = f"{BASE_URL}/{ruta.lstrip('/')}"
    intento = 0
    renovado_por_401 = False

    while True:
        token = auth_manager.obtener_token()
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"})

        try:
            with urllib.request.urlopen(req, timeout=5) as resp:
                return json.loads(resp.read().decode("utf-8"))

        except urllib.error.HTTPError as error:
            codigo = error.code
            cuerpo = error.read().decode("utf-8")
            headers = dict(error.headers)

            # 1. Código 401: Renovar token una sola vez
            if codigo == 401 and not renovado_por_401:
                logging.warning("⚠️ Error 401 detectado. Renovando token y reintentando...")
                auth_manager.obtener_token(forzar=True)
                renovado_por_401 = True
                continue

            # 2. Errores no recuperables: abortar inmediatamente
            if codigo in {400, 403, 404, 422}:
                logging.error("❌ Error no reintentable HTTP %d: %s", codigo, cuerpo)
                return {"error": codigo, "detalle": cuerpo}

            # 3. Errores transitorios (503, 429)
            intento += 1
            if intento > max_intentos:
                logging.critical("🛑 Se agotaron los %d intentos para %s", max_intentos, ruta)
                raise

            if codigo == 429 and "Retry-After" in headers:
                espera = float(headers["Retry-After"])
                logging.warning("⚠️ Rate limit 429. Respetando Retry-After: %s segundos.", espera)
            else:
                espera = (1.0 * (2 ** (intento - 1))) + random.uniform(0.1, 0.4)
                logging.warning("⚠️ Falla transitoria HTTP %d. Reintento %d/%d en %.2fs...", codigo, intento, max_intentos, espera)

            time.sleep(espera)


def main() -> None:
    auth = GestorAutenticacion()
    print("Probando 5 consultas consecutivas con resiliencia...")
    for i in range(1, 6):
        res = consultar_con_resiliencia("/pedidos?por_pagina=2", auth)
        print(f"Consulta {i}: {len(res.get('datos', []))} pedidos obtenidos con éxito.")


if __name__ == "__main__":
    main()
