#!/usr/bin/env python3
"""servidor_webhook.py

Servidor receptor de Webhooks ligero construido con http.server.
Valida la firma criptográfica HMAC-SHA256 en la cabecera X-Signature-SHA256
usando hmac.compare_digest para prevenir ataques de temporización.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import logging
import os
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

PUERTO_WEBHOOK = int(os.environ.get("PUERTO_WEBHOOK", "9050"))
WEBHOOK_SECRET = os.environ.get("WEBHOOK_SECRET", "secreto-seguro-halcon-nexo-2026")


def calcular_firma(cuerpo_bytes: bytes, secreto: str) -> str:
    return hmac.new(secreto.encode("utf-8"), cuerpo_bytes, hashlib.sha256).hexdigest()


class ManejadorWebhook(BaseHTTPRequestHandler):
    def do_POST(self) -> None:  # noqa: N802
        if self.path != "/webhook":
            self.send_response(404)
            self.end_headers()
            return

        largo = int(self.headers.get("Content-Length", 0))
        cuerpo_bytes = self.rfile.read(largo)
        firma_recibida = self.headers.get("X-Signature-SHA256", "").strip()

        # Validación criptográfica en tiempo constante
        firma_esperada = calcular_firma(cuerpo_bytes, WEBHOOK_SECRET)
        if not firma_recibida or not hmac.compare_digest(firma_esperada, firma_recibida):
            logging.warning("🛑 Webhook RECHAZADO: Firma HMAC inválida o ausente.")
            self.send_response(401)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "firma_invalida"}).encode("utf-8"))
            return

        try:
            evento = json.loads(cuerpo_bytes.decode("utf-8"))
            logging.info("✅ Webhook RECIBIDO y AUTENTICADO con éxito:")
            logging.info("   Tipo de evento: %s", evento.get("evento", "desconocido"))
            logging.info("   Datos:          %s", evento.get("datos", {}))

            # Responder 200 OK de inmediato
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"estado": "recibido", "id_evento": evento.get("id")}).encode("utf-8"))

        except json.JSONDecodeError:
            self.send_response(400)
            self.end_headers()


def main() -> None:
    servidor = HTTPServer(("127.0.0.1", PUERTO_WEBHOOK), ManejadorWebhook)
    logging.info("🚀 Receptor de Webhooks escuchando en http://127.0.0.1:%d/webhook", PUERTO_WEBHOOK)
    logging.info("   Secreto compartido configurado: %s***", WEBHOOK_SECRET[:4])
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        logging.info("Servidor de Webhook detenido.")


if __name__ == "__main__":
    main()
