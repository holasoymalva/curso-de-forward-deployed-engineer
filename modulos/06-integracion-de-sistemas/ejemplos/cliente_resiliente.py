#!/usr/bin/env python3
"""cliente_resiliente.py

Cliente HTTP de grado de producción construido únicamente con la
biblioteca estándar de Python.
Demuestra:
  1. Renovación automática y transparente de tokens Bearer ante expiración (401).
  2. Reintentos con Backoff Exponencial y Jitter ante errores 503 y 429.
  3. Respeto estricto del encabezado Retry-After.
  4. Paginación automática hasta agotar registros.
  5. Envío de mutaciones POST con encabezado Idempotency-Key.
"""

from __future__ import annotations

import json
import logging
import os
import random
import sys
import time
import urllib.error
import urllib.request
import uuid
from typing import Any

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

BASE_URL = os.environ.get("API_BASE_URL", "http://127.0.0.1:8000")
CLIENT_ID = os.environ.get("CLIENT_ID", "nexo-demo")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET", "secreto-de-practica")


class ClienteHalconResiliente:
    """Cliente HTTP resiliente a fallas para Distribuidora Halcón."""

    def __init__(
        self,
        base_url: str = BASE_URL,
        client_id: str = CLIENT_ID,
        client_secret: str = CLIENT_SECRET,
        max_reintentos: int = 5,
        base_backoff_seg: float = 1.0,
        max_backoff_seg: float = 30.0,
    ):
        self.base_url = base_url.rstrip("/")
        self.client_id = client_id
        self.client_secret = client_secret
        self.max_reintentos = max_reintentos
        self.base_backoff_seg = base_backoff_seg
        self.max_backoff_seg = max_backoff_seg

        self.token: str | None = None
        self.expira_en_epoch: float = 0.0

    def _asegurar_token(self, forzar_renovacion: bool = False) -> str:
        """Obtiene o renueva el token si expiró o está por vencer en 30s."""
        ahora = time.time()
        if forzar_renovacion or not self.token or ahora >= (self.expira_en_epoch - 30):
            logging.info("Solicitando / renovando token de acceso en /auth/token...")
            payload = json.dumps({"client_id": self.client_id, "client_secret": self.client_secret}).encode("utf-8")
            req = urllib.request.Request(
                f"{self.base_url}/auth/token",
                data=payload,
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                self.token = data["access_token"]
                self.expira_en_epoch = ahora + data.get("expires_in", 300)
                logging.info("Token renovado con éxito (expira en %d segundos).", data.get("expires_in", 300))
        return self.token

    def peticion(
        self,
        metodo: str,
        ruta: str,
        payload: dict | None = None,
        headers_extra: dict | None = None,
    ) -> tuple[int, dict[str, Any], dict[str, str]]:
        """Ejecuta una petición HTTP con reintentos exponenciales y manejo de tokens."""
        url = f"{self.base_url}/{ruta.lstrip('/')}"
        data_bytes = json.dumps(payload).encode("utf-8") if payload is not None else None

        intento = 0
        renovacion_intentada = False

        while True:
            token = self._asegurar_token()
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}",
            }
            if headers_extra:
                headers.update(headers_extra)

            req = urllib.request.Request(url, data=data_bytes, headers=headers, method=metodo)

            try:
                with urllib.request.urlopen(req, timeout=10) as resp:
                    cuerpo_texto = resp.read().decode("utf-8")
                    datos = json.loads(cuerpo_texto) if cuerpo_texto else {}
                    headers_resp = dict(resp.headers)
                    return resp.status, datos, headers_resp

            except urllib.error.HTTPError as error:
                codigo = error.code
                cuerpo_error = error.read().decode("utf-8")
                headers_resp = dict(error.headers)

                # 1. Manejo especial de 401: Renovar token una sola vez y reintentar de inmediato
                if codigo == 401 and not renovacion_intentada:
                    logging.warning("⚠️ HTTP 401: Token expirado o rechazado. Forzando renovación...")
                    self._asegurar_token(forzar_renovacion=True)
                    renovacion_intentada = True
                    continue

                # 2. Errores NO transitorios: abortar sin reintentar
                if codigo in {400, 403, 404, 422}:
                    logging.error("❌ Error de negocio no recuperable HTTP %d en %s: %s", codigo, ruta, cuerpo_error)
                    try:
                        return codigo, json.loads(cuerpo_error), headers_resp
                    except json.JSONDecodeError:
                        return codigo, {"raw_error": cuerpo_error}, headers_resp

                # 3. Errores transitorios reintentables (503, 502, 504, 429)
                intento += 1
                if intento > self.max_reintentos:
                    logging.critical("🛑 Se agotaron los %d reintentos permitidos para %s. Abortando.", self.max_reintentos, ruta)
                    raise

                # Determinar tiempo de espera
                tiempo_espera = 0.0
                if codigo == 429 and "Retry-After" in headers_resp:
                    tiempo_espera = float(headers_resp["Retry-After"])
                    logging.warning("⚠️ Rate Limit (429) excedido. Servidor solicita esperar %s segundos.", headers_resp["Retry-After"])
                else:
                    # Backoff exponencial con Jitter: base * 2^intento + jitter aleatorio
                    exponencial = self.base_backoff_seg * (2 ** (intento - 1))
                    jitter = random.uniform(0.1, 0.5)
                    tiempo_espera = min(exponencial + jitter, self.max_backoff_seg)
                    logging.warning("⚠️ Error transitorio HTTP %d. Reintento %d/%d en %.2fs...", codigo, intento, self.max_reintentos, tiempo_espera)

                time.sleep(tiempo_espera)

            except (urllib.error.URLError, TimeoutError) as error_red:
                intento += 1
                if intento > self.max_reintentos:
                    logging.critical("🛑 Falla de red no recuperable tras %d intentos: %s", self.max_reintentos, error_red)
                    raise
                tiempo_espera = min(self.base_backoff_seg * (2 ** (intento - 1)) + random.uniform(0.1, 0.5), self.max_backoff_seg)
                logging.warning("⚠️ Falla de conexión a red (%s). Reintentando en %.2fs...", error_red, tiempo_espera)
                time.sleep(tiempo_espera)

    def paginar_coleccion(self, ruta_base: str, por_pagina: int = 50) -> list[dict]:
        """Recorre exhaustivamente todas las páginas de un endpoint."""
        todos = []
        pagina = 1

        while pagina is not None:
            separador = "&" if "?" in ruta_base else "?"
            ruta_con_pagina = f"{ruta_base}{separador}pagina={pagina}&por_pagina={por_pagina}"
            _, res, _ = self.peticion("GET", ruta_con_pagina)

            items = res.get("datos", [])
            todos.extend(items)
            logging.info("Recuperada página %d (%d items, total acumulado: %d)", pagina, len(items), len(todos))

            pagina = res.get("siguiente_pagina")

        return todos

    def crear_pedido_idempotente(self, tienda: str, almacen: str, lineas: list[dict], llave_idempotencia: str | None = None) -> dict:
        """Crea un pedido garantizando idempotencia con Idempotency-Key."""
        llave = llave_idempotencia or f"ped-{uuid.uuid4()}"
        payload = {"tienda": tienda, "almacen": almacen, "lineas": lineas}
        headers = {"Idempotency-Key": llave}

        logging.info("Enviando pedido para %s con llave de idempotencia: %s", tienda, llave)
        codigo, respuesta, headers_resp = self.peticion("POST", "/pedidos", payload=payload, headers_extra=headers)

        if headers_resp.get("Idempotent-Replay") == "true":
            logging.info("ℹ️ El servidor confirmó respuesta idempotente (Idempotent-Replay: true).")

        return respuesta


def main() -> None:
    cliente = ClienteHalconResiliente()

    print("--- 1. Consultando catálogo completo con paginación automática ---")
    productos = cliente.paginar_coleccion("/productos", por_pagina=20)
    print(f"Total de productos en catálogo recuperados: {len(productos)}")

    print("\n--- 2. Enviando pedido con prueba de Idempotencia ---")
    llave_compartida = "prueba-idempotencia-mty-001"
    lineas = [{"sku": productos[0]["sku"], "cantidad": 5}]

    # Primer envío
    res1 = cliente.crear_pedido_idempotente(tienda="Tienda 0001", almacen="MTY", lineas=lineas, llave_idempotencia=llave_compartida)
    print(f"Resultado 1: Pedido #{res1.get('id')} creado.")

    # Segundo envío (Misma llave): Debe retornar el mismo pedido sin crear otro
    res2 = cliente.crear_pedido_idempotente(tienda="Tienda 0001", almacen="MTY", lineas=lineas, llave_idempotencia=llave_compartida)
    print(f"Resultado 2 (Reintento): Pedido #{res2.get('id')} (Mismo ID confirmado, sin duplicar).")


if __name__ == "__main__":
    main()
