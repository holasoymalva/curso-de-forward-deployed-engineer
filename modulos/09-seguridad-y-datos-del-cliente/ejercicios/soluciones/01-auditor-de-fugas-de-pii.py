#!/usr/bin/env python3
"""
01-auditor-de-fugas-de-pii.py: Solución al Ejercicio 01.
Escáner automatizado de fugas de Información de Identificación Personal (PII)
en archivos de texto, CSV o logs para pipelines de CI/CD.
"""

import sys
import os
import re

PATRONES_PII = {
    "CORREO_ELECTRONICO": re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
    "TELEFONO_MEXICO": re.compile(r"(?:\+?52\s?)?(?:\(?\d{2,3}\)?[\s.-]?)?\d{3,4}[\s.-]?\d{4}\b"),
    "RFC_MEXICO": re.compile(r"\b[A-Z&Ñ]{3,4}\d{6}[A-Z0-9]{3}\b"),
    "TARJETA_CREDITO": re.compile(r"\b(?:\d{4}[-\s]?){3}\d{4}\b")
}

def ofuscar_hallazgo(texto: str) -> str:
    """Ofusca parcialmente el hallazgo para no re-exponerlo en el reporte de auditoría."""
    texto = texto.strip()
    if len(texto) <= 4:
        return "****"
    return texto[:2] + "*" * (len(texto) - 4) + texto[-2:]

def es_falso_positivo(tipo: str, valor: str) -> bool:
    """Filtra falsos positivos obvios como fechas o versiones."""
    # Los números de teléfono a veces confunden años o timestamps si no tienen formato
    if tipo == "TELEFONO_MEXICO":
        limpio = re.sub(r"\D", "", valor)
        # Excluir cadenas de solo ceros o longitud no mexicana
        if len(limpio) not in (10, 12) or limpio == "0" * len(limpio):
            return True
        # Excluir años como 20261014
        if limpio.startswith("202") and len(limpio) == 8:
            return True
    return False

def auditar_archivo(ruta_archivo: str) -> int:
    if not os.path.exists(ruta_archivo):
        print(f"Error: No se encontró el archivo '{ruta_archivo}'", file=sys.stderr)
        return 2

    print(f"==================================================")
    print(f"Auditoría de PII: Escaneando '{ruta_archivo}'")
    print(f"==================================================")

    total_lineas = 0
    infracciones = []

    with open(ruta_archivo, mode="r", encoding="utf-8", errors="ignore") as f:
        for num_linea, linea in enumerate(f, start=1):
            total_lineas += 1
            linea_str = linea.strip()

            # Evitar alertar en encabezados de CSV
            if num_linea == 1 and ("id_tienda" in linea_str or "contacto" in linea_str):
                continue

            for tipo, regex in PATRONES_PII.items():
                for m in regex.finditer(linea_str):
                    c = m.group()
                    start_idx = m.start()
                    # Si el caracter previo es un asterisco, es un correo enmascarado (p. ej. m***s@ejemplo.com)
                    if start_idx > 0 and linea_str[start_idx - 1] == "*":
                        continue
                    if "*" in c or "anonimo@" in c:
                        continue
                    if not es_falso_positivo(tipo, c):
                        infracciones.append((num_linea, tipo, ofuscar_hallazgo(c)))

    print(f"Líneas analizadas: {total_lineas}")

    if not infracciones:
        print("✅ Resultado: LIMPIO. No se detectaron fugas de PII sin enmascarar.")
        return 0

    print(f"❌ Resultado: SE DETECTARON {len(infracciones)} POSIBLES FUGAS DE PII:\n")
    print(f"{'Línea':<8} | {'Tipo de PII':<20} | {'Muestra ofuscada'}")
    print("-" * 55)
    for num, tipo, muestra in infracciones:
        print(f"{num:<8} | {tipo:<20} | {muestra}")

    print("\n[ALERTA]: El archivo no cumple con la política de privacidad de datos.")
    return 1

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python 01-auditor-de-fugas-de-pii.py <ruta_archivo>")
        sys.exit(2)

    archivo = sys.argv[1]
    codigo_salida = auditar_archivo(archivo)
    sys.exit(codigo_salida)
