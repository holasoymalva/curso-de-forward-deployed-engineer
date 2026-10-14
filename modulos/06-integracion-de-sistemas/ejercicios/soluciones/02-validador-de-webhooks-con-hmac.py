#!/usr/bin/env python3
"""02-validador-de-webhooks-con-hmac.py - Solución al Ejercicio 02 del Módulo 06."""

from __future__ import annotations

import hashlib
import hmac
import json
import logging
from http.server import BaseHTTPRequestHandler, HTTPServer

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

PUERTO = 9080
SECRETO_COMPARTIDO = "mi-secreto-compartido-123"

# Registro en memoria para garantizar idempotencia
EVENTOS_PROCESADOS: set[str] = set()


def calcular_hmac(cuerpo: bytes, clave: str) -> str:
    return hmac.new(clave.encode("utf-8"), cuerpo, hashlib.sha256).hexdigest()


class ManejadorSeguro(BaseHTTPRequestHandler):
    def do_POST(self) -> None:  # noqa: N802
        if self.path != "/eventos":
            self.send_response(404)
            self.end_headers()
            return

        largo = int(self.headers.get("Content-Length", 0))
        cuerpo_bytes = self.rfile.read(largo)
        firma_cliente = self.headers.get("X-Signature-SHA256", "").strip()

        # 1. Validación de firma criptográfica HMAC en tiempo constante
        firma_esperada = calcular_hmac(cuerpo_bytes, SECRETO_COMPARTIDO)
        if not firma_cliente or not hmac.compare_digest(firma_esperada, firma_cliente):
            logging.warning("🛑 Firma HMAC no coincide o no fue provista.")
            self.send_response(401)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "firma_invalida"}).encode("utf-8"))
            return

        # 2. Validación de JSON e Idempotencia
        try:
            payload = json.loads(cuerpo_bytes.decode("utf-8"))
            id_evento = str(payload.get("id_evento", "")).strip()

            if not id_evento:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "id_evento es obligatorio"}).encode("utf-8"))
                return

            # Detección de duplicado idempotente
            if id_evento in EVENTOS_PROCESADOS:
                logging.info("ℹ️ Evento '%s' recibido previamente. Respuesta idempotente 200.", id_evento)
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({
                    "estado": "ya_procesado",
                    "id_evento": id_evento,
                    "idempotente": True
                }).encode("utf-8"))
                return

            # Evento nuevo
            EVENTOS_PROCESADOS.add(id_evento)
            logging.info("✅ Nuevo evento registrado: %s (%s)", id_evento, payload.get("tipo", "general"))

            self.send_response(201)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({
                "estado": "creado_y_procesado",
                "id_evento": id_evento
            }).encode("utf-8"))

        except json.JSONDecodeError:
            self.send_response(400)
            self.end_headers()


def main() -> None:
    servidor = HTTPServer(("127.0.0.1", PUERTO), ManejadorSeguro)
    logging.info("🛡️ Servidor receptor de eventos seguro en http://127.0.0.1:%d/eventos", PUERTO)
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        logging.info("Servidor detenido.")


if __name__ == "__main__":
    main()
