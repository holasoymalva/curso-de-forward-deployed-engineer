# Ejemplos del Módulo 02: Python para FDE

Scripts ejecutables construidos con la **biblioteca estándar de Python** para procesar y limpiar los datos reales del caso de estudio de Distribuidora Halcón.

---

## 📂 Archivos disponibles

| Script | Descripción | Comando de ejecución |
|--------|-------------|----------------------|
| [`limpiar_inventario.py`](limpiar_inventario.py) | Lee `inventario_erp.csv`, detecta anomalías (precios con coma, SKUs con espacios, almacenes inválidos, duplicados), normaliza fechas y genera un CSV limpio y un reporte de errores en JSON. | `python limpiar_inventario.py` |
| [`generar_reporte_stock.py`](generar_reporte_stock.py) | CLI con `argparse` y `logging` que analiza el inventario, filtra productos por debajo de un umbral de stock y exporta una alerta en JSON. | `python generar_reporte_stock.py --umbral 15` |

---

## 🚀 Cómo ejecutarlos

Desde la raíz del repositorio:

```bash
# 1. Probar el limpiador de inventario
python modulos/02-python-para-fde/ejemplos/limpiar_inventario.py

# 2. Probar el generador de reportes con menú de ayuda
python modulos/02-python-para-fde/ejemplos/generar_reporte_stock.py --help

# 3. Generar alerta para productos con menos de 20 unidades
python modulos/02-python-para-fde/ejemplos/generar_reporte_stock.py --umbral 20 --verbose
```
