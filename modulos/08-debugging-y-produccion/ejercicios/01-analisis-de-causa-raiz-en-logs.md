# Ejercicio 01: Análisis de causa raíz en logs de producción

## 🎯 Objetivo

Aprender a realizar un análisis forense sobre archivos de registros estructurados en producción, identificar los síntomas iniciales frente a la verdadera causa raíz, y redactar una comunicación profesional de incidente para los líderes técnicos del cliente.

---

## 🏢 Contexto del problema

Son las 03:15 de la mañana y tu sistema de monitoreo en la nube te despierta con la siguiente alerta:
`[ALERTA CRÍTICA] Tasa de error > 15% en conector Halcón (Monterrey)`.

El equipo de soporte de Distribuidora Halcón te ha proporcionado el archivo con los logs capturados del contenedor durante la ventana de la falla:
[`../ejemplos/logs_produccion_halcon.log`](../ejemplos/logs_produccion_halcon.log)

---

## 📝 Tareas a realizar

### Tarea 1: Inspección forense con herramientas de línea de comandos o script
Examina el archivo de logs utilizando Python o utilidades estándar (`grep`, `jq`, `analizar_logs.py`) y responde con datos concretos:
1. ¿A qué hora exacta inició el proceso y cuándo ocurrió el primer error?
2. ¿Cuál fue el primer código de estado HTTP erróneo recibido? ¿Qué mensaje de error arrojó el servidor?
3. ¿Qué código HTTP empezó a recibir el conector poco después y por qué cambió el tipo de error?
4. ¿Cuántos lotes (`batches`) se procesaron con éxito antes de que se presentara la primera falla?
5. ¿Cuál fue la latencia promedio de las peticiones exitosas frente a las fallidas?

### Tarea 2: Diagrama de los 5 Porqués (Root Cause Analysis)
Construye la cadena causal de 5 niveles que explique cómo una condición aparente de saturación de red (`429 Too Many Requests`) se originó en realidad por un diseño deficiente en la expiración del token Bearer.

### Tarea 3: Redacción de comunicado ejecutivo del incidente
Escribe el mensaje de correo o Slack que enviarías a las **03:30 AM** a:
* **Destinatarios:** Laura Garza (Directora de Operaciones) y Roberto Treviño (Gerente de TI).
* **Objetivo:** Informar el incidente con empatía, claridad y sin tecnicismos innecesarios, comunicando que el problema está identificado, las acciones de mitigación en curso y la próxima hora estimada de actualización.

---

## 🔍 Criterios de evaluación

* Los números de lotes, códigos de estado y marcas de tiempo deben coincidir con la información de `logs_produccion_halcon.log`.
* La distinción entre causa raíz (*root cause*) y síntomas secundarios (*cascading failure*) debe ser clara y precisa.
* La comunicación no debe culpar a nadie (*blameless*) ni generar pánico; debe transmitir control técnico riguroso.
