#!/usr/bin/env python3
"""logger_estructurado.py

Módulo de logging estructurado que emite registros en formato JSON
(JSON Lines) usando exclusivamente la biblioteca estándar de Python.
"""

from __future__ import annotations

import json
import logging
from datetime import datetime
from typing import Any


class FormateadorJSON(logging.Formatter):
    """Convierte cualquier LogRecord en una sola línea JSON válida."""

    def format(self, record: logging.LogRecord) -> str:
        registro: dict[str, Any] = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "nivel": record.levelname,
            "logger": record.name,
            "modulo": record.module,
            "linea": record.lineno,
            "mensaje": record.getMessage(),
        }

        # Inyectar campos de contexto si se pasaron en el argumento 'extra'
        if hasattr(record, "contexto") and isinstance(record.contexto, dict):
            registro.update(record.contexto)

        if record.exc_info:
            registro["traceback"] = self.formatException(record.exc_info)

        return json.dumps(registro, ensure_ascii=False)


def obtener_logger(nombre: str = "nexo_fde", nivel: int = logging.INFO) -> logging.Logger:
    """Configura y retorna un logger listo para producción con salida a stdout."""
    logger = logging.getLogger(nombre)
    logger.setLevel(nivel)

    if not logger.handlers:
        manejador = logging.StreamHandler()
        manejador.setFormatter(FormateadorJSON())
        logger.addHandler(manejador)

    return logger


if __name__ == "__main__":
    log = obtener_logger("demo_estructurada", logging.DEBUG)
    log.info("Servicio iniciado", extra={"contexto": {"puerto": 8000, "ambiente": "staging"}})
    log.warning("Falla transitoria de red", extra={"contexto": {"reintento": 1, "codigo_http": 503, "duracion_ms": 350.2}})
    log.error("Pedido rechazado por validación", extra={"contexto": {"tienda": "Tienda 0001", "codigo_http": 422, "sku": "HAL-9999"}})
