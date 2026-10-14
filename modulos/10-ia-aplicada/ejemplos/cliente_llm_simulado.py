#!/usr/bin/env python3
"""
cliente_llm_simulado.py: Cliente genérico de LLM para Forward Deployed Engineers.
Soporta dos modalidades:
1. Modo Simulado (por defecto): Corre de forma 100% offline sin necesidad de API keys,
   emitiendo respuestas deterministas en JSON y texto para pruebas y CI/CD.
2. Modo API Real: Si se definen las variables de entorno LLM_API_KEY y LLM_BASE_URL,
   se conecta mediante HTTP (urllib estándar) a cualquier proveedor compatible con OpenAI/Groq/Ollama.
"""

import os
import sys
import json
import urllib.request
import urllib.error
import re

class ClienteLLM:
    def __init__(self):
        self.api_key = os.environ.get("LLM_API_KEY")
        self.base_url = os.environ.get("LLM_BASE_URL", "https://api.openai.com/v1")
        self.modelo = os.environ.get("LLM_MODELO", "gpt-4o-mini")
        self.modo_simulado = not bool(self.api_key)

    def completar_chat(self, mensajes: list, temperatura: float = 0.0, response_format_json: bool = False) -> str:
        """Envía una conversación de chat al modelo y devuelve el texto generado."""
        if self.modo_simulado:
            return self._generar_respuesta_simulada(mensajes, response_format_json)
        return self._llamar_api_remota(mensajes, temperatura, response_format_json)

    def _generar_respuesta_simulada(self, mensajes: list, response_format_json: bool) -> str:
        """Simulador determinista de respuestas para pruebas del curso."""
        ultimo_mensaje = mensajes[-1]["content"] if mensajes else ""
        texto_lower = ultimo_mensaje.lower()

        # Si se solicitó formalmente JSON o el prompt exige salida exclusivamente en JSON
        pide_json_explicito = (
            response_format_json or 
            "formato json" in texto_lower or 
            "exclusivamente en json" in texto_lower or
            "responder en json" in texto_lower
        )
        if pide_json_explicito:
            # Detección inteligente de producto y tienda
            sku = "SKU-DESCONOCIDO"
            cantidad = 10
            almacen = "MTY"
            tienda = "T0001"

            if "arroz" in texto_lower:
                sku = "SKU-ARROZ-01"
            elif "frijol" in texto_lower:
                sku = "SKU-FRIJOL-02"
            elif "aceite" in texto_lower:
                sku = "SKU-ACEITE-03"
            elif "azucar" in texto_lower or "azúcar" in texto_lower:
                sku = "SKU-AZUCAR-04"
            elif "leche" in texto_lower:
                sku = "SKU-LECHE-05"

            match_cant = re.search(r"\b(\d+)\s+(?:cajas|costales|bultos|piezas|unidades|paquetes|kilos|kg|litros)\b", texto_lower)
            if not match_cant:
                match_cant = re.search(r"\b(?:enviar|mandar|ocupamos|urgen|autorizó|autorizo)\s+(\d+)\b", texto_lower)
            if match_cant:
                cantidad = int(match_cant.group(1))

            if "guadalajara" in texto_lower or "gdl" in texto_lower or "zapopan" in texto_lower:
                almacen = "GDL"
            elif "cdmx" in texto_lower or "méxico" in texto_lower:
                almacen = "CDMX"

            match_tienda = re.search(r"(t\d{4})", texto_lower)
            if match_tienda:
                tienda = match_tienda.group(1).upper()

            urgente = "urgente" in texto_lower or "asap" in texto_lower or "hoy" in texto_lower

            respuesta_dict = {
                "id_tienda": tienda,
                "almacen": almacen,
                "articulos": [
                    {
                        "sku": sku,
                        "cantidad": cantidad
                    }
                ],
                "urgente": urgente,
                "confianza": 0.98,
                "fuente_extraccion": "simulador_offline_fde"
            }
            return json.dumps(respuesta_dict, indent=2, ensure_ascii=False)

        # Aislar la pregunta del usuario si el prompt incluye contexto RAG
        if "pregunta:" in texto_lower:
            texto_consulta = texto_lower.split("pregunta:")[-1].strip()
        else:
            texto_consulta = texto_lower

        # Respuestas para consultas RAG o de texto general
        if "almacen" in texto_consulta or "almacén" in texto_consulta or "almacenes" in texto_consulta or "monterrey" in texto_consulta:
            return (
                "Distribuidora Halcón cuenta con tres almacenes principales:\n"
                "1. Monterrey (MTY): Centro de distribución norte (600 tiendas).\n"
                "2. Guadalajara (GDL): Centro de distribución occidente (350 tiendas).\n"
                "3. Ciudad de México (CDMX): Centro de distribución centro-sur (250 tiendas)."
            )

        if "devolucion" in texto_consulta or "devolución" in texto_consulta or "merma" in texto_consulta or "perecedero" in texto_consulta:
            return (
                "De acuerdo con las políticas operativas de Distribuidora Halcón:\n"
                "- Productos perecederos: El reporte de devolución debe realizarse dentro de las 24 horas siguientes a la entrega.\n"
                "- Abarrotes secos (arroz, frijol, azúcar): Cuentan con un plazo de hasta 7 días naturales con aprobación del encargado de almacén."
            )

        if "credito" in texto_consulta or "crédito" in texto_consulta or "pago" in texto_consulta:
            return (
                "Las tiendas afiliadas disponen de una línea de crédito revolvente a 15 o 30 días naturales, "
                "condicionada a no registrar saldos vencidos mayores a $50,000 MXN en el ERP."
            )

        return "La información solicitada no se encuentra disponible en las políticas oficiales de Distribuidora Halcón."

    def _llamar_api_remota(self, mensajes: list, temperatura: float, response_format_json: bool) -> str:
        """Ejecuta una petición HTTP POST real a un endpoint compatible con Chat Completions."""
        url = f"{self.base_url.rstrip('/')}/chat/completions"
        payload = {
            "model": self.modelo,
            "messages": mensajes,
            "temperature": temperatura
        }
        if response_format_json:
            payload["response_format"] = {"type": "json_object"}

        cuerpo_bytes = json.dumps(payload).encode("utf-8")
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        req = urllib.request.Request(url, data=cuerpo_bytes, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return data["choices"][0]["message"]["content"]
        except urllib.error.HTTPError as e:
            cuerpo_error = e.read().decode("utf-8", errors="ignore")
            raise RuntimeError(f"Falla HTTP al invocar LLM ({e.code}): {cuerpo_error}")
        except Exception as e:
            raise RuntimeError(f"Error de conexión con proveedor LLM: {e}")

if __name__ == "__main__":
    cliente = ClienteLLM()
    print(f"=== Inicializando Cliente LLM (Modo: {'SIMULADO (Offline)' if cliente.modo_simulado else 'CONEXIÓN REMOTA'}) ===")

    conversacion = [
        {"role": "system", "content": "Eres un extractor de pedidos en JSON para Distribuidora Halcón."},
        {"role": "user", "content": "Nos urgen 45 costales de frijol para la tienda T0003 en CDMX antes de mediodía."}
    ]

    print("\n[Pregunta / Input]:")
    print(conversacion[-1]["content"])

    print("\n[Generando respuesta estructurada...]")
    salida = cliente.completar_chat(conversacion, temperatura=0.0, response_format_json=True)
    print("\n[Salida del LLM]:")
    print(salida)
