#!/usr/bin/env bash
# ==============================================================================
# diagnostico_sistema.sh
# Script de diagnóstico rápido para servidores y estaciones de trabajo FDE.
# ==============================================================================

set -euo pipefail

echo "========================================================"
echo "🔍 DIAGNÓSTICO RÁPIDO DE ENTORNO FDE - PROYECTO HALCÓN"
echo "========================================================"
echo "Fecha y hora local: $(date)"
echo "Usuario actual:     $(whoami)"
echo "Directorio actual:  $(pwd)"
echo ""

echo "--- 1. VERSIONES DE HERRAMIENTAS BASE ---"
if command -v python3 &>/dev/null; then
    echo "✅ Python 3:  $(python3 --version)"
else
    echo "❌ Python 3:  No encontrado en el PATH."
fi

if command -v git &>/dev/null; then
    echo "✅ Git:       $(git --version)"
else
    echo "❌ Git:       No encontrado en el PATH."
fi

if command -v curl &>/dev/null; then
    echo "✅ cURL:      $(curl --version | head -n 1)"
else
    echo "❌ cURL:      No encontrado en el PATH."
fi

if command -v jq &>/dev/null; then
    echo "✅ jq:        $(jq --version)"
else
    echo "⚠️  jq:        No instalado (recomendado para procesar JSON)."
fi

echo ""
echo "--- 2. VARIABLES DE ENTORNO RELEVANTES ---"
echo "CLIENT_ID:    ${CLIENT_ID:-'(no configurada, usará default)'}"
echo "PUERTO:       ${PUERTO:-'8000 (default)'}"
echo ""

echo "--- 3. VERIFICACIÓN DE CONECTIVIDAD LOCAL ---"
API_URL="http://127.0.0.1:${PUERTO:-8000}/salud"
echo "Probando endpoint de salud en: $API_URL"

if curl -s --max-time 2 "$API_URL" &>/dev/null; then
    echo "✅ API simulada: Conexión exitosa y respondiendo."
else
    echo "⚠️  API simulada: No responde. ¿Iniciaste 'python recursos/api-simulada/servidor.py'?"
fi

echo ""
echo "========================================================"
echo "Diagnóstico finalizado."
echo "========================================================"
