# Lección 04: Herramientas CLI con argparse y logging profesional

> **Nivel:** 🟢 Principiante · **Duración estimada:** 25 min

---

## Situación

Terminaste el script de limpieza de datos. Para probarlo, dejaste fijas las rutas en el código:
```python
ARCHIVO = "/Users/tu-usuario/Documents/inventario_erp.csv"
UMBRAL_STOCK = 50
```

Se lo envías a Roberto Treviño para que lo pruebe en el servidor de Halcón. Inmediatamente falla con `FileNotFoundError`. Además, como llenaste tu código de `print("procesando...")` y `print("error!")`, la terminal se inunda de texto desordenado sin fecha, hora ni nivel de severidad.

Para que tu código sea adoptado por el cliente, necesita comportarse como una herramienta de línea de comandos profesional: configurable con argumentos (`--archivo`, `--umbral`) y con logs estructurados.

---

## Conceptos clave

### 1. Construcción de CLIs profesionales con `argparse`

El módulo nativo `argparse` genera automáticamente interfaces de línea de comandos robustas con menú de ayuda (`--help`), validación de tipos y valores por defecto:

```python
import argparse

def parsear_argumentos() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Limpia y valida el archivo de inventario de Distribuidora Halcón."
    )
    # Argumento obligatorio posicional
    parser.add_argument(
        "archivo_entrada",
        type=str,
        help="Ruta al archivo CSV exportado por el ERP"
    )
    # Argumento opcional con bandera
    parser.add_argument(
        "-s", "--salida",
        type=str,
        default="inventario_limpio.json",
        help="Ruta donde se guardará el JSON limpio (default: inventario_limpio.json)"
    )
    # Argumento numérico con valor por defecto
    parser.add_argument(
        "-u", "--umbral",
        type=int,
        default=20,
        help="Cantidad mínima de stock para considerar alerta (default: 20)"
    )
    # Bandera booleana para modo debug
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Activar registro detallado en consola"
    )
    return parser.parse_args()
```

Ahora el usuario puede ejecutar:
```bash
python script.py --help
python script.py datos/inventario_erp.csv --umbral 50 --verbose
```

---

### 2. Adiós a `print()`, hola al módulo `logging`

`print()` envía texto plano a la salida estándar sin contexto. El módulo `logging` permite:
- Asignar niveles de severidad (`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`).
- Filtrar la verbosidad según el entorno (ej. `INFO` en producción, `DEBUG` en desarrollo).
- Incluir automáticamente timestamp, nombre del archivo y nivel.

```python
import logging

def configurar_logging(verbose: bool) -> None:
    nivel = logging.DEBUG if verbose else logging.INFO
    formato = "%(asctime)s [%(levelname)s] %(message)s"
    logging.basicConfig(level=nivel, format=formato, datefmt="%Y-%m-%d %H:%M:%S")

# Uso en tu código
logging.info("Iniciando procesamiento de archivo: %s", "inventario_erp.csv")
logging.warning("SKU HAL-1002 con cantidad negativa (-5). Marcado para revisión.")
logging.error("No se pudo conectar a la base de datos local.")
```

---

### 3. El punto de entrada estándar `if __name__ == "__main__":`

Para que tus scripts puedan ejecutarse directamente desde la terminal pero también importarse en pruebas unitarias sin disparar la ejecución automática:

```python
def main() -> int:
    args = parsear_argumentos()
    configurar_logging(args.verbose)
    logging.info("Procesando...")
    # Lógica principal
    return 0  # 0 indica éxito al sistema operativo

if __name__ == "__main__":
    import sys
    sys.exit(main())
```

---

## Errores comunes

- **Usar `sys.argv` directamente a mano:** Parsear `sys.argv[1]` se rompe fácilmente si el usuario pasa las banderas en otro orden o no proporciona argumentos. `argparse` maneja todo eso de forma estándar.
- **Enviar mensajes de error a `sys.stdout` en lugar de `sys.stderr`:** Cuando otros scripts encadenan comandos con pipes, mezclar logs de error con la salida de datos corrompe el flujo.
- **Dejar logs de nivel `DEBUG` quemados en producción con datos confidenciales:** Imprimir tokens o datos personales de clientes en logs que luego se guardan en texto plano en el servidor.

---

## En el día a día de un FDE

Cuando le entregas a Roberto Treviño un script con `--help` bien documentado y logs estructurados, su equipo puede programarlo en el `cron` del servidor en 5 minutos. Si algo falla a las 3:00 AM, el archivo `sync.log` tendrá la línea exacta y la hora en que ocurrió el error.

---

## Resumen

- `argparse` permite crear utilidades de línea de comandos flexibles y auto-documentadas.
- Usa `logging` para registrar eventos con timestamp y severidad en lugar de llamadas desordenadas a `print()`.
- Estructura tus programas con una función `main()` y el bloque `if __name__ == "__main__":` retornando códigos de salida estándar (0 = éxito, 1+ = error).

---

## Preguntas de repaso

1. ¿Qué comando genera `argparse` automáticamente para que los usuarios aprendan a usar tu script?
2. ¿Cuáles son los 5 niveles estándar de severidad en el módulo `logging` de Python?
3. ¿Por qué es importante que un script de procesamiento termine con `sys.exit(1)` cuando detecta una falla crítica no recuperable?

---

⬅️ [Lección anterior: Manejo de errores](03-manejo-de-errores-y-validaciones.md) | 📦 [Módulo](../README.md) | [Ir a Ejemplos del módulo](01-fundamentos-y-estructuras-de-datos.md) ➡️
