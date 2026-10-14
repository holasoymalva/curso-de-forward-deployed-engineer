#!/usr/bin/env python3
"""
script_con_bugs.py: Script de sincronización con fallas intencionales para el Ejercicio 02.
Este script intenta sincronizar el inventario desde un diccionario simulado hacia una API,
pero contiene 5 errores comunes que un FDE debe diagnosticar y corregir.
"""

import sys
import json
import time

# Datos simulados de inventario recibidos del ERP
DATOS_ERP = [
    {"sku": "SKU-ARROZ-01", "almacen": "MTY", "cantidad": 50, "precio": "18.50"},
    {"sku": "SKU-FRIJOL-02", "almacen": "GDL", "cantidad": "120", "precio": "24.00"}, # Bug 1: cantidad es str
    {"sku": "SKU-ACEITE-03", "almacen": "CDMX", "precio": "42.50"},                    # Bug 2: falta clave 'cantidad'
    {"sku": "SKU-AZUCAR-04", "almacen": "MTY", "cantidad": -5, "precio": "28.00"},     # Bug 3: cantidad negativa
    {"sku": "SKU-LECHE-05", "almacen": "GDL", "cantidad": 80, "precio": "26.50"},
]

class ClienteAPISimulado:
    def __init__(self):
        self.intentos = 0
        self.token = "TOKEN_INICIAL"

    def enviar_lote(self, token, lote):
        self.intentos += 1
        
        # Simulación de falla de autenticación por token vencido
        if token != "TOKEN_RENOVADO_OK" and self.intentos > 2:
            return {"status": 401, "error": "Token expired"}

        # Simulación de rate-limiting si se envían peticiones consecutivas
        if self.intentos == 4:
            return {"status": 429, "error": "Rate limit exceeded", "retry_after": 1}

        return {"status": 200, "actualizados": len(lote)}

def procesar_inventario(datos):
    cliente = ClienteAPISimulado()
    lote_a_enviar = []
    
    # Procesamiento y cálculo de métricas
    total_piezas = 0
    
    for item in datos:
        # BUG 1 y 2: Asume que 'cantidad' siempre existe y es un entero
        total_piezas += item["cantidad"]
        
        # BUG 3: No valida cantidades negativas
        registro_limpio = {
            "sku": item["sku"],
            "almacen": item["almacen"],
            "stock": item["cantidad"],
            "precio": float(item["precio"])
        }
        lote_a_enviar.append(registro_limpio)

    print(f"Total estimado de piezas a procesar: {total_piezas}")

    # BUG 4: Envío sin manejo de códigos 401 (re-autenticación) ni reintentos
    token_actual = "TOKEN_INICIAL"
    resultado = cliente.enviar_lote(token_actual, lote_a_enviar)
    
    # BUG 5: Acceso ingenuo a claves sin verificar si hubo error HTTP
    print(f"Éxito: Se actualizaron {resultado['actualizados']} productos.")
    return True

if __name__ == "__main__":
    print("Iniciando procesamiento de inventario con fallas...")
    try:
        procesar_inventario(DATOS_ERP)
        print("Proceso completado exitosamente.")
    except Exception as e:
        print(f"\n[ERROR FATAL NO CONTROLADO]: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
