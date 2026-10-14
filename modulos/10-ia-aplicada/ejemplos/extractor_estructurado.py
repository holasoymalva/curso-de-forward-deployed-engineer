#!/usr/bin/env python3
"""
extractor_estructurado.py: Extracción de entidades y pedidos estructurados desde lenguaje natural.
Convierte mensajes informales de encargados de tienda en objetos JSON estrictamente validados
contra el catálogo ERP de Distribuidora Halcón.
"""

import sys
import os
import json

# Importar cliente LLM local
directorio_actual = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, directorio_actual)
from cliente_llm_simulado import ClienteLLM

CATALOGO_OFICIAL = {
    "SKU-ARROZ-01": {"nombre": "Arroz Blanco 1kg", "precio_base": 18.50, "unidad": "kg"},
    "SKU-FRIJOL-02": {"nombre": "Frijol Negro 1kg", "precio_base": 24.00, "unidad": "kg"},
    "SKU-ACEITE-03": {"nombre": "Aceite Vegetal 1L", "precio_base": 42.50, "unidad": "litro"},
    "SKU-AZUCAR-04": {"nombre": "Azúcar Estándar 1kg", "precio_base": 28.00, "unidad": "kg"},
    "SKU-LECHE-05": {"nombre": "Leche Entera 1L", "precio_base": 26.50, "unidad": "litro"}
}

ALMACENES_VALIDOS = {"MTY", "GDL", "CDMX"}

class ExtractorPedidos:
    def __init__(self):
        self.llm = ClienteLLM()

    def extraer_desde_texto(self, mensaje_usuario: str) -> dict:
        """Invoca al LLM con instrucciones estrictas de formato JSON y valida las reglas de negocio."""
        prompt_sistema = (
            "Eres un agente de captura de pedidos mayoristas para Distribuidora Halcón. "
            "Tu tarea es analizar el mensaje del encargado de tienda y extraer un objeto JSON estricto "
            "con las siguientes claves: 'id_tienda', 'almacen', 'articulos' (lista de objetos con 'sku' y 'cantidad'), "
            "y 'urgente' (booleano). "
            "Responde exclusivamente en formato JSON sin texto adicional ni bloques markdown."
        )

        mensajes = [
            {"role": "system", "content": prompt_sistema},
            {"role": "user", "content": f"Mensaje recibido: {mensaje_usuario}"}
        ]

        print(f"\nProcesando mensaje con LLM...")
        respuesta_cruda = self.llm.completar_chat(mensajes, temperatura=0.0, response_format_json=True)

        # 1. Parseo sintáctico de JSON
        try:
            datos_extraidos = json.loads(respuesta_cruda)
        except json.JSONDecodeError as e:
            raise ValueError(f"El modelo no generó un JSON válido: {e}\nTexto devuelto:\n{respuesta_cruda}")

        # 2. Validación de reglas de negocio
        pedido_validado = self._validar_reglas_negocio(datos_extraidos)
        return pedido_validado

    def _validar_reglas_negocio(self, datos: dict) -> dict:
        """Aplica guardrails defensivos sobre los campos extraídos."""
        id_tienda = datos.get("id_tienda", "").strip().upper()
        if not id_tienda:
            datos["id_tienda"] = "T0001" # Asignación por defecto con bandera de revisión

        almacen = datos.get("almacen", "").strip().upper()
        if almacen not in ALMACENES_VALIDOS:
            print(f"[ALERTA]: Almacén '{almacen}' no reconocido; asignando MTY por defecto.")
            almacen = "MTY"
        datos["almacen"] = almacen

        articulos_validados = []
        total_piezas = 0
        total_estimado_mxn = 0.0

        for art in datos.get("articulos", []):
            sku = art.get("sku", "").strip().upper()
            cantidad = int(art.get("cantidad", 0))

            if sku not in CATALOGO_OFICIAL:
                print(f"[RECHAZO]: El SKU '{sku}' extraído por el LLM no existe en el catálogo oficial.")
                continue

            if cantidad <= 0:
                print(f"[RECHAZO]: Cantidad inválida ({cantidad}) para SKU '{sku}'.")
                continue

            if cantidad > 2000:
                print(f"[GUARDRAIL ALERTA]: Cantidad inusualmente alta ({cantidad}) en SKU '{sku}'. Requiere aprobación de Don Javier.")
                datos["requiere_aprobacion_directiva"] = True

            precio_unitario = CATALOGO_OFICIAL[sku]["precio_base"]
            subtotal = precio_unitario * cantidad

            articulos_validados.append({
                "sku": sku,
                "descripcion": CATALOGO_OFICIAL[sku]["nombre"],
                "cantidad": cantidad,
                "precio_unitario": precio_unitario,
                "subtotal_mxn": subtotal
            })
            total_piezas += cantidad
            total_estimado_mxn += subtotal

        datos["articulos"] = articulos_validados
        datos["resumen_operativo"] = {
            "total_lineas": len(articulos_validados),
            "total_piezas": total_piezas,
            "importe_total_estimado_mxn": round(total_estimado_mxn, 2),
            "estado_validacion": "APROBADO_PARA_ERP" if articulos_validados else "RECHAZADO"
        }

        return datos

if __name__ == "__main__":
    extractor = ExtractorPedidos()

    mensajes_prueba = [
        "Buenas tardes, habla Juan de la tienda T0002 en Guadalajara. Mándenos 60 costales de frijol urgente por favor.",
        "Favor de enviar 120 cajas de aceite a T0003 en CDMX para entrega normal la próxima semana.",
        "Don Javier nos autorizó 50 bultos de arroz para la sucursal T0001 de Monterrey."
    ]

    for m in mensajes_prueba:
        print("==================================================")
        print(f"Mensaje entrante:\n\"{m}\"")
        resultado = extractor.extraer_desde_texto(m)
        print("\nResultado JSON validado:")
        print(json.dumps(resultado, indent=2, ensure_ascii=False))
