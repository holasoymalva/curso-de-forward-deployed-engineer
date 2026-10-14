# Solución al Ejercicio 01: Automatización con Bash y análisis de archivos

A continuación se presenta el código completo del script `analizar_csv.sh` comentado paso a paso:

```bash
#!/usr/bin/env bash
set -euo pipefail

# 1. Validación de argumentos y existencia del archivo
if [ "$#" -ne 1 ]; then
    echo "❌ Error: Debes proporcionar la ruta del archivo CSV como argumento."
    echo "Uso: $0 <ruta_al_archivo.csv>"
    exit 1
fi

ARCHIVO="$1"

if [ ! -f "$ARCHIVO" ]; then
    echo "❌ Error: El archivo '$ARCHIVO' no existe o no es accesible."
    exit 1
fi

echo "=========================================================="
echo "📊 REPORTE DE ANÁLISIS RÁPIDO: $ARCHIVO"
echo "=========================================================="

# 2. Conteo de registros de datos (total de líneas menos la cabecera)
TOTAL_LINEAS=$(wc -l < "$ARCHIVO" | tr -d ' ')
REGISTROS=$((TOTAL_LINEAS - 1))
echo "Total de líneas:        $TOTAL_LINEAS"
echo "Total de registros:     $REGISTROS"

# 3. Conteo de productos de limpieza (ignorando mayúsculas/minúsculas)
LIMPIEZA=$(grep -i ",limpieza," "$ARCHIVO" | wc -l | tr -d ' ')
echo "Productos de limpieza:  $LIMPIEZA"

# 4. Búsqueda de anomalías (cantidades negativas o valores nulos/ND)
echo ""
echo "--- 🔍 BÚSQUEDA DE ANOMALÍAS EN CANTIDADES ---"

ANOMALIAS=$(grep -E ',-[0-9]+,|,,|,N/D,' "$ARCHIVO" || true)

if [ -n "$ANOMALIAS" ]; then
    echo "⚠️  Se detectaron filas con posibles datos corruptos:"
    echo "$ANOMALIAS"
else
    echo "✅ No se detectaron anomalías evidentes en cantidades."
fi

echo "=========================================================="
```

---

## Cómo probar la solución

```bash
# Otorgar permisos de ejecución
chmod +x analizar_csv.sh

# Ejecutar contra el archivo de prueba del caso de estudio
./analizar_csv.sh recursos/caso-de-estudio/datos/inventario_erp.csv
```
