"""API simulada de Distribuidora Halcón.

Servidor HTTP local construido solo con la biblioteca estándar de Python.
Sirve para practicar consumo de APIs, autenticación, paginación,
límites de peticiones (rate limiting), reintentos e idempotencia.

Uso:
    python servidor.py                 # puerto 8000
    PUERTO=9000 python servidor.py     # otro puerto
    FALLAS=0.2 python servidor.py      # 20 % de respuestas 503 aleatorias
    LIMITE_POR_MINUTO=10 python servidor.py
"""

from __future__ import annotations

import json
import os
import random
import secrets
import threading
import time
from datetime import date, timedelta
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

PUERTO = int(os.environ.get("PUERTO", "8000"))
TASA_FALLAS = float(os.environ.get("FALLAS", "0"))
LIMITE_POR_MINUTO = int(os.environ.get("LIMITE_POR_MINUTO", "60"))
DURACION_TOKEN_SEG = int(os.environ.get("DURACION_TOKEN_SEG", "300"))

CLIENT_ID = "nexo-demo"
CLIENT_SECRET = "secreto-de-practica"

ALMACENES = ["MTY", "GDL", "CDMX"]
ESTADOS_PEDIDO = ["pendiente", "surtido", "enviado", "entregado", "cancelado"]


# ---------------------------------------------------------------------------
# Datos deterministas
# ---------------------------------------------------------------------------
def generar_datos() -> tuple[list[dict], list[dict], list[dict]]:
    rnd = random.Random(42)
    categorias = {
        "abarrotes": ["Arroz", "Frijol", "Azúcar", "Aceite", "Atún", "Pasta", "Harina"],
        "bebidas": ["Refresco", "Agua", "Jugo", "Café", "Leche"],
        "limpieza": ["Detergente", "Cloro", "Jabón", "Suavizante"],
    }
    productos = []
    sku_n = 1000
    for categoria, nombres in categorias.items():
        for nombre in nombres:
            for presentacion in ["chico", "mediano", "grande"]:
                sku_n += 1
                productos.append(
                    {
                        "sku": f"HAL-{sku_n}",
                        "nombre": f"{nombre} {presentacion}",
                        "categoria": categoria,
                        "precio": round(rnd.uniform(12, 180), 2),
                        "stock_minimo": rnd.choice([20, 50, 100]),
                    }
                )

    inventario = []
    for p in productos:
        for almacen in ALMACENES:
            inventario.append(
                {
                    "sku": p["sku"],
                    "almacen": almacen,
                    "cantidad": rnd.randint(0, 400),
                    "actualizado": (date(2026, 10, 1) + timedelta(days=rnd.randint(0, 12))).isoformat(),
                }
            )

    pedidos = []
    for i in range(1, 251):
        lineas = [
            {"sku": rnd.choice(productos)["sku"], "cantidad": rnd.randint(1, 30)}
            for _ in range(rnd.randint(1, 5))
        ]
        pedidos.append(
            {
                "id": i,
                "tienda": f"Tienda {rnd.randint(1, 1200):04d}",
                "almacen": rnd.choice(ALMACENES),
                "estado": rnd.choice(ESTADOS_PEDIDO),
                "fecha": (date(2026, 9, 1) + timedelta(days=rnd.randint(0, 43))).isoformat(),
                "lineas": lineas,
            }
        )
    return productos, inventario, pedidos


PRODUCTOS, INVENTARIO, PEDIDOS = generar_datos()
TOKENS: dict[str, float] = {}  # token -> expiración (epoch)
LLAVES_IDEMPOTENCIA: dict[str, dict] = {}
CONTEO_PETICIONES: dict[str, list[float]] = {}
CANDADO = threading.Lock()


def paginar(elementos: list[dict], query: dict[str, list[str]]) -> dict:
    pagina = max(int(query.get("pagina", ["1"])[0]), 1)
    por_pagina = min(max(int(query.get("por_pagina", ["20"])[0]), 1), 100)
    inicio = (pagina - 1) * por_pagina
    total = len(elementos)
    return {
        "datos": elementos[inicio : inicio + por_pagina],
        "pagina": pagina,
        "por_pagina": por_pagina,
        "total": total,
        "siguiente_pagina": pagina + 1 if inicio + por_pagina < total else None,
    }


class Manejador(BaseHTTPRequestHandler):
    server_version = "HalconAPI/1.0"

    # -- utilidades ---------------------------------------------------------
    def responder(self, codigo: int, cuerpo: dict | list, encabezados: dict | None = None) -> None:
        datos = json.dumps(cuerpo, ensure_ascii=False).encode("utf-8")
        self.send_response(codigo)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(datos)))
        for k, v in (encabezados or {}).items():
            self.send_header(k, str(v))
        self.end_headers()
        self.wfile.write(datos)

    def leer_json(self) -> dict | None:
        largo = int(self.headers.get("Content-Length", "0"))
        if largo == 0:
            return {}
        try:
            return json.loads(self.rfile.read(largo))
        except json.JSONDecodeError:
            return None

    def token_valido(self) -> str | None:
        auth = self.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            return None
        token = auth.removeprefix("Bearer ").strip()
        with CANDADO:
            exp = TOKENS.get(token)
        if exp is None or exp < time.time():
            return None
        return token

    def excede_limite(self, token: str) -> int | None:
        ahora = time.time()
        with CANDADO:
            historial = [t for t in CONTEO_PETICIONES.get(token, []) if ahora - t < 60]
            if len(historial) >= LIMITE_POR_MINUTO:
                CONTEO_PETICIONES[token] = historial
                return int(60 - (ahora - historial[0])) + 1
            historial.append(ahora)
            CONTEO_PETICIONES[token] = historial
        return None

    def pre_validar(self) -> bool:
        """Falla aleatoria, autenticación y rate limit. Regresa False si ya respondió."""
        if TASA_FALLAS and random.random() < TASA_FALLAS:
            self.responder(503, {"error": "servicio_no_disponible", "mensaje": "Intenta de nuevo más tarde."})
            return False
        token = self.token_valido()
        if token is None:
            self.responder(401, {"error": "no_autorizado", "mensaje": "Token ausente, inválido o expirado."})
            return False
        espera = self.excede_limite(token)
        if espera is not None:
            self.responder(
                429,
                {"error": "demasiadas_peticiones", "mensaje": f"Límite de {LIMITE_POR_MINUTO}/min excedido."},
                {"Retry-After": espera},
            )
            return False
        return True

    def log_message(self, formato: str, *args) -> None:  # noqa: D401
        print(f"[{self.log_date_time_string()}] {self.command} {self.path} -> {args[1] if len(args) > 1 else ''}")

    # -- rutas --------------------------------------------------------------
    def do_GET(self) -> None:  # noqa: N802
        url = urlparse(self.path)
        query = parse_qs(url.query)
        partes = [p for p in url.path.split("/") if p]

        if url.path == "/salud":
            return self.responder(200, {"estado": "ok"})

        if not self.pre_validar():
            return

        if partes == ["productos"]:
            elementos = PRODUCTOS
            if "categoria" in query:
                elementos = [p for p in elementos if p["categoria"] == query["categoria"][0]]
            return self.responder(200, paginar(elementos, query))

        if len(partes) == 2 and partes[0] == "productos":
            producto = next((p for p in PRODUCTOS if p["sku"] == partes[1]), None)
            if producto is None:
                return self.responder(404, {"error": "no_encontrado", "mensaje": f"SKU {partes[1]} no existe."})
            return self.responder(200, producto)

        if partes == ["inventario"]:
            elementos = INVENTARIO
            if "almacen" in query:
                elementos = [i for i in elementos if i["almacen"] == query["almacen"][0].upper()]
            return self.responder(200, paginar(elementos, query))

        if partes == ["pedidos"]:
            with CANDADO:
                elementos = list(PEDIDOS)
            if "estado" in query:
                elementos = [p for p in elementos if p["estado"] == query["estado"][0]]
            if "almacen" in query:
                elementos = [p for p in elementos if p["almacen"] == query["almacen"][0].upper()]
            return self.responder(200, paginar(elementos, query))

        if len(partes) == 2 and partes[0] == "pedidos":
            if not partes[1].isdigit():
                return self.responder(400, {"error": "solicitud_invalida", "mensaje": "El id debe ser numérico."})
            with CANDADO:
                pedido = next((p for p in PEDIDOS if p["id"] == int(partes[1])), None)
            if pedido is None:
                return self.responder(404, {"error": "no_encontrado", "mensaje": f"Pedido {partes[1]} no existe."})
            return self.responder(200, pedido)

        return self.responder(404, {"error": "ruta_no_encontrada", "mensaje": url.path})

    def do_POST(self) -> None:  # noqa: N802
        url = urlparse(self.path)
        cuerpo = self.leer_json()
        if cuerpo is None:
            return self.responder(400, {"error": "json_invalido", "mensaje": "El cuerpo no es JSON válido."})

        if url.path == "/auth/token":
            if cuerpo.get("client_id") != CLIENT_ID or cuerpo.get("client_secret") != CLIENT_SECRET:
                return self.responder(401, {"error": "credenciales_invalidas", "mensaje": "Revisa client_id y client_secret."})
            token = secrets.token_hex(16)
            with CANDADO:
                TOKENS[token] = time.time() + DURACION_TOKEN_SEG
            return self.responder(200, {"access_token": token, "token_type": "Bearer", "expires_in": DURACION_TOKEN_SEG})

        if url.path == "/pedidos":
            if not self.pre_validar():
                return
            llave = self.headers.get("Idempotency-Key")
            if llave:
                with CANDADO:
                    previo = LLAVES_IDEMPOTENCIA.get(llave)
                if previo:
                    return self.responder(200, previo, {"Idempotent-Replay": "true"})

            errores = []
            if cuerpo.get("almacen", "").upper() not in ALMACENES:
                errores.append(f"almacen debe ser uno de {ALMACENES}")
            if not cuerpo.get("tienda"):
                errores.append("tienda es obligatorio")
            lineas = cuerpo.get("lineas") or []
            if not lineas:
                errores.append("lineas debe tener al menos un elemento")
            skus = {p["sku"] for p in PRODUCTOS}
            for linea in lineas:
                if linea.get("sku") not in skus:
                    errores.append(f"sku desconocido: {linea.get('sku')}")
                if not isinstance(linea.get("cantidad"), int) or linea["cantidad"] <= 0:
                    errores.append(f"cantidad inválida para {linea.get('sku')}")
            if errores:
                return self.responder(422, {"error": "validacion", "detalles": errores})

            with CANDADO:
                nuevo = {
                    "id": max(p["id"] for p in PEDIDOS) + 1,
                    "tienda": cuerpo["tienda"],
                    "almacen": cuerpo["almacen"].upper(),
                    "estado": "pendiente",
                    "fecha": date.today().isoformat(),
                    "lineas": lineas,
                }
                PEDIDOS.append(nuevo)
                if llave:
                    LLAVES_IDEMPOTENCIA[llave] = nuevo
            return self.responder(201, nuevo)

        return self.responder(404, {"error": "ruta_no_encontrada", "mensaje": url.path})


def main() -> None:
    servidor = ThreadingHTTPServer(("127.0.0.1", PUERTO), Manejador)
    print(f"API simulada de Distribuidora Halcón en http://127.0.0.1:{PUERTO}")
    print(f"  Credenciales: client_id={CLIENT_ID} client_secret={CLIENT_SECRET}")
    print(f"  Fallas aleatorias: {TASA_FALLAS:.0%} | Límite: {LIMITE_POR_MINUTO}/min | Token: {DURACION_TOKEN_SEG}s")
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido.")


if __name__ == "__main__":
    main()
