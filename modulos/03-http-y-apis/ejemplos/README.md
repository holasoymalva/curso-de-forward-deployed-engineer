# Ejemplos del Módulo 03: HTTP y APIs

Scripts para interactuar directamente con la [API simulada](../../recursos/api-simulada/README.md) de Distribuidora Halcón.

---

## 📂 Archivos disponibles

| Archivo | Descripción | Cómo ejecutarlo |
|---------|-------------|-----------------|
| [`cliente_api_basico.py`](cliente_api_basico.py) | Cliente en Python puro (`urllib.request`) que se autentica, obtiene un token Bearer, consulta productos y maneja errores HTTP 401/404/422. | `python cliente_api_basico.py` |
| [`probar_endpoints.sh`](probar_endpoints.sh) | Script en Bash con llamadas `curl` documentadas para probar salud, login y endpoints de inventario y pedidos. | `bash probar_endpoints.sh` |

---

## 🚀 Preparación previa

Antes de ejecutar estos ejemplos, asegúrate de tener la API simulada corriendo en otra terminal:

```bash
# Iniciar la API simulada (por defecto en http://127.0.0.1:8000)
python recursos/api-simulada/servidor.py
```
