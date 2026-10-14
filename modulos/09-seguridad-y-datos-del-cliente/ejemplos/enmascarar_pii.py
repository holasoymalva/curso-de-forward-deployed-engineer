#!/usr/bin/env python3
"""
enmascarar_pii.py: Script para sanitizar, anonimizar y enmascarar información personal (PII).
Lee el archivo de tiendas de Distribuidora Halcón y genera una versión segura
para entornos de analítica, pruebas o modelos de inteligencia artificial.
"""

import os
import csv
import re
import hashlib
import sys

def enmascarar_nombre(nombre: str) -> str:
    """Enmascara nombres personales preservando la primera letra de cada componente."""
    if not nombre or not nombre.strip():
        return "N/D"
    partes = nombre.strip().split()
    partes_enmascaradas = []
    for p in partes:
        if len(p) <= 2:
            partes_enmascaradas.append(p[0] + "*")
        else:
            partes_enmascaradas.append(p[0] + "*" * (len(p) - 2) + p[-1])
    return " ".join(partes_enmascaradas)

def enmascarar_telefono(telefono: str) -> str:
    """Conserva únicamente los últimos 4 dígitos de un número telefónico."""
    if not telefono:
        return "N/D"
    digitos = re.sub(r"\D", "", telefono)
    if len(digitos) < 4:
        return "****"
    return "*" * (len(digitos) - 4) + digitos[-4:]

def enmascarar_correo(correo: str) -> str:
    """Oculta la mayor parte del usuario de correo conservando el dominio."""
    if not correo or "@" not in correo:
        return "anonimo@dominio.oculto"
    usuario, dominio = correo.split("@", 1)
    if len(usuario) <= 2:
        usuario_mask = usuario[0] + "*"
    else:
        usuario_mask = usuario[0] + "*" * (len(usuario) - 2) + usuario[-1]
    return f"{usuario_mask}@{dominio}"

def generar_hash_pseudonimo(valor: str, salt: str = "NEXO_SALT_SECRETA_2026") -> str:
    """Genera un seudónimo alfanumérico irreversible usando SHA-256 y sal."""
    if not valor:
        return "HASH_VACIO"
    contenido = f"{valor.strip().lower()}:{salt}".encode("utf-8")
    return hashlib.sha256(contenido).hexdigest()[:12]

def procesar_tiendas(ruta_entrada: str, ruta_salida: str):
    print(f"Leyendo archivo origen: {ruta_entrada}")
    if not os.path.exists(ruta_entrada):
        print(f"Error: No existe el archivo {ruta_entrada}", file=sys.stderr)
        sys.exit(1)

    registros_procesados = 0
    duplicados_omitidos = 0
    ids_vistos = set()

    with open(ruta_entrada, mode="r", encoding="utf-8") as f_in, \
         open(ruta_salida, mode="w", encoding="utf-8", newline="") as f_out:
        
        lector = csv.DictReader(f_in)
        campos_salida = [
            "id_tienda",
            "nombre_tienda",
            "contacto_enmascarado",
            "telefono_enmascarado",
            "correo_enmascarado",
            "contacto_pseudonimo_hash",
            "ciudad",
            "estado"
        ]
        escritor = csv.DictWriter(f_out, fieldnames=campos_salida)
        escritor.writeheader()

        for fila in lector:
            id_tienda = fila.get("id_tienda", "").strip()
            
            # Control de duplicados en la capa de sanitización
            if id_tienda in ids_vistos:
                duplicados_omitidos += 1
                continue
            ids_vistos.add(id_tienda)

            contacto_original = fila.get("contacto", "")
            telefono_original = fila.get("telefono", "")
            correo_original = fila.get("correo", "")

            fila_sanitizada = {
                "id_tienda": id_tienda,
                "nombre_tienda": fila.get("nombre_tienda", "").strip(),
                "contacto_enmascarado": enmascarar_nombre(contacto_original),
                "telefono_enmascarado": enmascarar_telefono(telefono_original),
                "correo_enmascarado": enmascarar_correo(correo_original),
                "contacto_pseudonimo_hash": generar_hash_pseudonimo(contacto_original),
                "ciudad": fila.get("ciudad", "").strip(),
                "estado": fila.get("estado", "").strip()
            }
            escritor.writerow(fila_sanitizada)
            registros_procesados += 1

    print(f"\n✅ Proceso completado exitosamente.")
    print(f"• Registros válidos procesados y protegidos: {registros_procesados}")
    print(f"• Registros duplicados filtrados: {duplicados_omitidos}")
    print(f"• Archivo generado: {ruta_salida}\n")

if __name__ == "__main__":
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    ruta_datos_default = os.path.abspath(
        os.path.join(directorio_actual, "../../../recursos/caso-de-estudio/datos/tiendas.csv")
    )
    ruta_salida_default = os.path.join(directorio_actual, "tiendas_sanitizadas.csv")

    procesar_tiendas(ruta_datos_default, ruta_salida_default)
