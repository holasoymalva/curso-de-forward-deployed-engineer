# Ejercicios del Módulo 08: Debugging y operación en producción

Ejercicios prácticos para entrenar tus habilidades de diagnóstico forense de incidentes y depuración sistemática de código en entornos empresariales.

---

## 🎯 Lista de ejercicios

| Ejercicio | Nivel | Enfoque | Archivo de práctica |
|-----------|-------|---------|---------------------|
| [**01. Análisis de Causa Raíz en Logs**](01-analisis-de-causa-raiz-en-logs.md) | 🟡 Intermedio | Forense de logs JSON, técnica de los 5 Porqués y redacción de comunicado de incidente. | [`../ejemplos/logs_produccion_halcon.log`](../ejemplos/logs_produccion_halcon.log) |
| [**02. Depuración de Script con Bugs**](02-depuracion-de-script-con-bugs.md) | 🟡 Intermedio | Detección y corrección sistemática de errores lógicos, excepciones no manejadas y fallas de concurrencia/tokens. | [`script_con_bugs.py`](script_con_bugs.py) |

---

## 🛠️ Instrucciones de trabajo

1. Lee detenidamente el enunciado de cada ejercicio antes de comenzar.
2. Para el ejercicio 1, apóyate en el script `analizar_logs.py` o realiza consultas con herramientas de consola (`grep`, `jq`, `python`).
3. Para el ejercicio 2, corre primero el script para observar las excepciones reales y formula tus hipótesis antes de cambiar líneas de código.
4. Consulta las soluciones de referencia en [`soluciones/`](soluciones/) únicamente después de intentar resolver los problemas por tu cuenta.
