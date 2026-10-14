#!/usr/bin/env python3
"""
02-depuracion-de-script-con-bugs.py: Solución al Ejercicio 02.
Versión corregida y endurecida del script de sincronización.
"""

import sys
import json
import time

DATOS_ERP = [
    {"sku": "SKU-ARROZ-01", "almacen": "MTY", "cantidad": 50, "precio": "18.50"},
    {"sku": "SKU-FRIJOL-02", "almacen": "GDL", "cantidad": "120", "precio": "24.00"}, # str corregido
    {"sku": "SKU-ACEITE-03", "almacen": "CDMX", "precio": "42.50"},                    # sin cantidad corregido
    {"sku": "SKU-AZUCAR-04", "almacen": "MTY", "cantidad": -5, "precio": "28.00"},     # cantidad negativa corregida
    {"sku": "SKU-LECHE-05", "almacen": "GDL", "cantidad": 80, "precio": "26.50"},
]

class ClienteAPISimulado:
    def __init__(self):
        self.intentos = 0

    def enviar_lote(self, token, lote):
        self.intentos += 1
        
        # Simulación: rechaza token si no ha sido renovado
        if token != "TOKEN_RENOVADO_OK" and self.intentos > 1:
            return {"status": 401, "error": "Token expired"}

        return {"status": 200, "actualizados": len(lote)}

def normalizar_cantidad(valor_crudo, sku):
    """Convierte el valor de cantidad de manera segura a un entero positivo."""
    if valor_crudo is None:
        print(f"[ALERTA AUDITORÍA] SKU {sku} no reporta cantidad; asignando 0.")
        return 0
    try:
        val = int(valor_crudo)
        if val < 0:
            print(f"[ALERTA AUDITORÍA] SKU {sku} tiene stock negativo ({val}); normalizado a 0.")
            return 0
        return val
    except (ValueError, TypeError):
        print(f"[ERROR AUDITORÍA] Valor de cantidad inválido '{valor_crudo}' en SKU {sku}; asignando 0.")
        return 0

def procesar_inventario(datos):
    cliente = ClienteAPISimulado()
    lote_a_enviar = []
    total_piezas = 0

    print("=== Fase 1: Limpieza y validación de datos ===")
    for item in datos:
        sku = item.get("sku", "SKU-DESCONOCIDO")
        almacen = item.get("almacen", "GENERICO")
        
        # Solución Bugs 1, 2 y 3: uso de .get() y normalización robusta
        cantidad = normalizar_cantidad(item.get("cantidad"), sku)
        total_piezas += cantidad

        try:
            precio = float(item.get("precio", 0.0))
        except (ValueError, TypeError):
            precio = 0.0

        registro_limpio = {
            "sku": sku,
            "almacen": almacen,
            "stock": cantidad,
            "precio": precio
        }
        lote_a_enviar.append(registro_limpio)

    print(f"Total estimado de piezas validadas: {total_piezas}")
    print(f"Total de registros a sincronizar: {len(lote_a_enviar)}")

    print("\n=== Fase 2: Envío resiliente a la API ===")
    token_actual = "TOKEN_INICIAL"
    max_reintentos = 3
    intento = 0
    exito = False

    while intento < max_reintentos and not exito:
        intento += 1
        print(f"Enviando lote a la API (Intento {intento}/{max_reintentos}) con token: {token_actual}...")
        respuesta = cliente.enviar_lote(token_actual, lote_a_enviar)

        status = respuesta.get("status", 500)

        # Solución Bug 4: Detección de 401 y renovación de credenciales
        if status == 401:
            print("[ADVERTENCIA] Sesión expirada (HTTP 401). Renovando token de autenticación...")
            token_actual = "TOKEN_RENOVADO_OK"
            time.sleep(0.5)
            continue
        
        # Solución Bug 5: Verificación segura del payload de respuesta
        if status == 200:
            actualizados = respuesta.get("actualizados", 0)
            print(f"[ÉXITO] Lote recibido y procesado por la API. Productos actualizados: {actualizados}")
            exito = True
        else:
            error_msg = respuesta.get("error", "Error desconocido")
            print(f"[ERROR] La API devolvió código {status}: {error_msg}")
            time.sleep(1)

    if not exito:
        raise RuntimeError("No se pudo sincronizar el inventario tras agotar los reintentos.")

    return True

if __name__ == "__main__":
    print("Iniciando procesamiento de inventario endurecido...")
    try:
        procesar_inventario(DATOS_ERP)
        print("\n[PROCESO FINALIZADO CON ÉXITO]")
    except Exception as e:
        print(f"\n[FALLA INESPERADA]: {e}")
        sys.exit(1)
