# Solución al Ejercicio 01: Normalizador de catálogo de tiendas con PII

Código completo del script `normalizar_tiendas.py`:

```python
#!/usr/bin/env python3
"""normalizar_tiendas.py - Solución al Ejercicio 01."""

from __future__ import annotations

import csv
import os
import re
import sys

PATRON_EMAIL = re.compile(r"^[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}$")


def limpiar_telefono(tel_raw: str) -> str:
    """Extrae únicamente los dígitos numéricos y valida que sean exactamente 10."""
    if not tel_raw:
        return "SIN_TELEFONO"
    digitos = re.sub(r"\D", "", tel_raw)
    if len(digitos) == 10:
        return digitos
    return "SIN_TELEFONO"


def validar_email(email_raw: str) -> str:
    """Verifica si el email tiene una estructura estándar válida."""
    email = email_raw.strip().lower()
    if not email:
        return "SIN_CORREO"
    if PATRON_EMAIL.match(email):
        return email
    return "CORREO_INVALIDO"


def normalizar_archivo_tiendas(ruta_entrada: str, ruta_salida: str) -> None:
    if not os.path.exists(ruta_entrada):
        print(f"❌ Error: Archivo no encontrado en '{ruta_entrada}'", file=sys.stderr)
        sys.exit(1)

    tiendas_unicas: dict[str, dict[str, str]] = {}
    duplicados_omitidos = 0

    with open(ruta_entrada, mode="r", encoding="utf-8") as f:
        lector = csv.DictReader(f)
        for fila in lector:
            id_tienda = fila["id_tienda"].strip().upper()
            if id_tienda in tiendas_unicas:
                duplicados_omitidos += 1
                continue

            tiendas_unicas[id_tienda] = {
                "id_tienda": id_tienda,
                "nombre_tienda": fila["nombre_tienda"].strip(),
                "contacto": fila["contacto"].strip(),
                "telefono": limpiar_telefono(fila.get("telefono", "")),
                "correo": validar_email(fila.get("correo", "")),
                "ciudad": fila["ciudad"].strip(),
                "estado": fila["estado"].strip(),
            }

    campos = ["id_tienda", "nombre_tienda", "contacto", "telefono", "correo", "ciudad", "estado"]
    with open(ruta_salida, mode="w", encoding="utf-8", newline="") as f:
        escritor = csv.DictWriter(f, fieldnames=campos)
        escritor.writeheader()
        for t in tiendas_unicas.values():
            escritor.writerow(t)

    print(f"✅ Proceso terminado exitosamente.")
    print(f"   Tiendas únicas guardadas: {len(tiendas_unicas)}")
    print(f"   Duplicados omitidos:     {duplicados_omitidos}")
    print(f"   Archivo generado:        {ruta_salida}")


if __name__ == "__main__":
    entrada = sys.argv[1] if len(sys.argv) > 1 else "recursos/caso-de-estudio/datos/tiendas.csv"
    salida = sys.argv[2] if len(sys.argv) > 2 else "tiendas_limpias.csv"
    normalizar_archivo_tiendas(entrada, salida)
```
