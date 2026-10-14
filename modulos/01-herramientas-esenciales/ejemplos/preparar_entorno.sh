#!/usr/bin/env bash
# ==============================================================================
# preparar_entorno.sh
# Automatiza la creación y verificación de un entorno virtual de Python.
# ==============================================================================

set -euo pipefail

ENTORNO_DIR=".venv"

echo "========================================================"
echo "📦 PREPARACIÓN DE ENTORNO VIRTUAL PYTHON"
echo "========================================================"

if [ -d "$ENTORNO_DIR" ]; then
    echo "ℹ️  El entorno '$ENTORNO_DIR' ya existe."
else
    echo "⚙️  Creando entorno virtual en '$ENTORNO_DIR'..."
    python3 -m venv "$ENTORNO_DIR"
    echo "✅ Entorno virtual creado exitosamente."
fi

echo ""
echo "Para activar este entorno en tu terminal, ejecuta:"
echo "--------------------------------------------------------"
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    echo "  $ENTORNO_DIR\\Scripts\\activate"
else
    echo "  source $ENTORNO_DIR/bin/activate"
fi
echo "--------------------------------------------------------"
echo "Para verificar que estés usando el Python aislado:"
echo "  which python3"
echo "========================================================"
