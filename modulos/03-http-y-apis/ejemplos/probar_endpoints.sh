#!/usr/bin/env bash
# ==============================================================================
# probar_endpoints.sh
# Demostración en curl para probar los endpoints clave de la API simulada.
# ==============================================================================

set -euo pipefail

BASE_URL="${API_BASE_URL:-http://127.0.0.1:8000}"

echo "=========================================================="
echo "🌐 PROBANDO API SIMULADA EN: $BASE_URL"
echo "=========================================================="

echo "1. Comprobando /salud..."
curl -s "$BASE_URL/salud"
echo -e "\n"

echo "2. Solicitando Token Bearer..."
AUTH_RESP=$(curl -s -X POST "$BASE_URL/auth/token" \
  -H "Content-Type: application/json" \
  -d '{"client_id": "nexo-demo", "client_secret": "secreto-de-practica"}')

echo "Respuesta de autenticación: $AUTH_RESP"

# Extraer token usando Python estándar si jq no está presente
TOKEN=$(python3 -c "import json, sys; print(json.loads('''$AUTH_RESP''')['access_token'])")
echo "Token obtenido: $TOKEN"
echo -e "\n"

echo "3. Consultando 2 pedidos pendientes de Monterrey..."
curl -s "$BASE_URL/pedidos?almacen=MTY&estado=pendiente&por_pagina=2" \
  -H "Authorization: Bearer $TOKEN"
echo -e "\n"

echo "4. Probando error 401 intencional con token falso..."
curl -s -i "$BASE_URL/pedidos" -H "Authorization: Bearer token_invalido" | head -n 5
echo -e "\n"

echo "=========================================================="
echo "Pruebas finalizadas."
echo "=========================================================="
