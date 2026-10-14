# Ejemplos del Módulo 08: Debugging y operación en producción

Herramientas de logging estructurado, analizadores automatizados y plantillas de incidentes para dominar la operación en producción.

---

## 📂 Archivos disponibles

| Archivo | Descripción | Uso |
|---------|-------------|-----|
| [`logger_estructurado.py`](logger_estructurado.py) | Formateador nativo en Python que emite logs en formato JSON Lines (`jsonl`) con campos de contexto operativo. | Módulo reutilizable en scripts |
| [`logs_produccion_halcon.log`](logs_produccion_halcon.log) | Archivo realista de logs en JSON que contiene la simulación de un incidente nocturno en Distribuidora Halcón. | Fuente de análisis forense |
| [`analizar_logs.py`](analizar_logs.py) | Script forense en Python que lee logs en JSON, resume códigos HTTP, calcula latencias y detecta causas raíz. | `python analizar_logs.py logs_produccion_halcon.log` |
| [`plantilla_postmortem.md`](plantilla_postmortem.md) | Plantilla editable de Postmortem sin culpas (*Blameless Postmortem*) basada en el estándar SRE de Google. | Guía para documentar incidentes |
| [`postmortem_ejemplo_halcon.md`](postmortem_ejemplo_halcon.md) | Caso de estudio resuelto: Postmortem del incidente de desincronización nocturna de Monterrey. | Ejemplo de alta dirección técnica |

---

## 🚀 Cómo ejecutar el análisis forense

Desde la raíz del repositorio:

```bash
python modulos/08-debugging-y-produccion/ejemplos/analizar_logs.py modulos/08-debugging-y-produccion/ejemplos/logs_produccion_halcon.log
```
