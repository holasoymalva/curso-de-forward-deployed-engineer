# Ejercicio 02: Depuración de script con bugs de producción

## 🎯 Objetivo

Aplicar el método científico de debugging (*Reproducir -> Aislar -> Formular hipótesis -> Probar cambio -> Prevenir regresiones*) para diagnosticar y reparar un script de integración con múltiples fallas lógicas, de validación y de resiliencia ante APIs.

---

## 🏢 Contexto del problema

Un colega junior dejó implementado un conector rápido en [`script_con_bugs.py`](script_con_bugs.py) para transferir los registros de inventario de Halcón hacia la API central de Nexo.

Al ejecutar el script en tu computadora con:
```bash
python script_con_bugs.py
```
El programa truena inmediatamente arrojando un `TypeError` y un `KeyError`. Además, tras una inspección estática, notas que no maneja respuestas HTTP no exitosas ni valida anomalías en el stock (como números negativos).

---

## 📝 Tareas a realizar

### Tarea 1: Reproducir y aislar las excepciones
1. Ejecuta el script tal como está y copia el stack trace inicial.
2. Identifica en qué línea exacta ocurre el primer fallo y explica qué tipo de dato provocó la discordancia.
3. Arregla el primer bug y vuelve a correr para descubrir el segundo fallo en la secuencia.

### Tarea 2: Depuración y endurecimiento del código
Corrige los 5 bugs identificados en el archivo:
1. **Tipado mixto en cantidad:** La cantidad a veces viene como cadena (`"120"`) en lugar de entero. Conviértela de forma segura.
2. **Claves faltantes:** Si un registro no contiene la clave `"cantidad"`, descártalo o márcalo con stock por defecto (`0`) emitiendo una advertencia en el log.
3. **Valores fuera de rango:** Si la cantidad es negativa (`< 0`), descártala o normalízala a `0` registrando una alerta de auditoría.
4. **Resiliencia ante error HTTP 401:** Si `cliente.enviar_lote` devuelve status `401`, renueva el token (usando `"TOKEN_RENOVADO_OK"`) y reintenta el envío.
5. **Acceso seguro al diccionario de respuesta:** No asumas que la clave `"actualizados"` siempre viene en el diccionario; verifica el código de estatus antes de imprimir los resultados.

### Tarea 3: Verificación final
Tu script corregido debe ejecutarse sin errores, procesar los registros válidos, descartar o subsanar los corruptos de forma transparente y mostrar un mensaje de éxito reportando cuántos productos fueron sincronizados.

---

## 💡 Pistas

* Usa métodos como `.get("cantidad", 0)` para evitar `KeyError`.
* Utiliza bloques `try / except (ValueError, TypeError)` al hacer conversiones numéricas.
* Aplica el patrón de cliente resiliente que vimos en el Módulo 06 para manejar el reintento de autenticación.
