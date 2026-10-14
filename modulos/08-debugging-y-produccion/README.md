# Módulo 08: Debugging y operación en producción

> **Nivel:** 🟡 Intermedio  
> **Duración aproximada:** 5 horas  
> **Prerrequisitos:** [Módulo 06: Integración de sistemas](../06-integracion-de-sistemas/README.md) y [Módulo 07: Despliegue y cloud](../07-despliegue-y-cloud/README.md)  

---

## 🎯 ¿Por qué importa para un FDE?

Cuando un sistema falla en producción un viernes a las 6:30 PM, no puedes permitirte el lujo de cambiar líneas de código al azar *"a ver si jala"*. Esa improvisación empeora las caídas, genera pánico en el cliente y destruye la confianza técnica construida durante semanas.

Un Forward Deployed Engineer profesional domina el **método científico de debugging**: reproduce la falla de manera aislada, formula hipótesis fundamentadas en datos objetivos, inspecciona logs estructurados en JSON y resuelve la causa raíz de fondo. Además, sabe liderar una llamada de incidente con calma, mitigar el impacto operativo antes de corregir el bug y redactar un **postmortem sin culpa (*blameless*)** que convierta la crisis en una mejora permanente para toda la compañía.

---

## ✅ Objetivos de aprendizaje

Al terminar este módulo podrás:

- Aplicar el método sistemático de resolución de problemas en 4 pasos: Reproducir, Aislar, Hipotetizar y Verificar.
- Implementar **logging estructurado en JSON** con campos de contexto (`cliente_id`, `solicitud_id`, `duracion_ms`, `codigo_http`).
- Comprender los tres pilares de la observabilidad (Logs, Métricas y Trazas) y definir objetivos de servicio (SLI / SLO) prácticos.
- Gestionar incidentes de producción clasificando severidades (Sev-1 a Sev-3) y comunicando el estatus al cliente con transparencia y templanza.
- Redactar un postmortem sin culpas (*blameless*) enfocado en fallas de procesos y salvaguardas sistémicas, no en señalar personas.

---

## 📖 Lecciones

| # | Lección | Nivel | Duración |
|---|---------|-------|----------|
| 01 | [El método sistemático de debugging en sistemas distribuidos](lecciones/01-metodo-sistematico-de-debugging.md) | 🟡 | 25 min |
| 02 | [Logging estructurado en JSON y contexto operativo](lecciones/02-logging-estructurado-y-niveles.md) | 🟡 | 25 min |
| 03 | [Observabilidad práctica: Métricas, trazas y SLOs](lecciones/03-observabilidad-metricas-trazas-y-slos.md) | 🟡 | 25 min |
| 04 | [Gestión de incidentes con clientes y postmortems sin culpa](lecciones/04-gestion-de-incidentes-y-postmortems-blameless.md) | 🟡 | 30 min |

---

## 💻 Ejemplos

Herramientas y artefactos de incidentes reales:
- Consulta [ejemplos/README.md](ejemplos/README.md).
  - [Módulo de logging estructurado (`logger_estructurado.py`)](ejemplos/logger_estructurado.py)
  - [Archivo de logs de incidente real de Halcón (`logs_produccion_halcon.log`)](ejemplos/logs_produccion_halcon.log)
  - [Analizador automatizado de logs (`analizar_logs.py`)](ejemplos/analizar_logs.py)
  - [Plantilla oficial de Postmortem sin culpas](ejemplos/plantilla_postmortem.md)
  - [Postmortem real del incidente de Halcón](ejemplos/postmortem_ejemplo_halcon.md)

---

## 🏋️ Ejercicios

Casos de investigación de causa raíz y depuración de código:
- Consulta [ejercicios/README.md](ejercicios/README.md).
  - [Ejercicio 01: Análisis de causa raíz en logs de producción](ejercicios/01-analisis-de-causa-raiz-en-logs.md)
  - [Ejercicio 02: Depuración y corrección de un conector con 4 bugs](ejercicios/02-depuracion-de-script-con-bugs.md)

---

## 🎥 Guion sugerido para video

1. **Gancho (1-2 min):** *"Suena la alarma a las 7:00 AM: el conector no actualizó los datos de Monterrey y los camiones están parados. Laura Garza está llamando al Director General. Si entras en pánico y empiezas a cambiar código a lo loco, la caída durará horas. En esta lección aprenderás a abrir los logs, filtrar con un script en 30 segundos y decir con calma: 'Identificamos la causa: el token de la API expiró a las 03:22 AM y el servidor rechazó las peticiones. La mitigación ya está en marcha'."*
2. **Concepto (5-8 min):** Por qué los logs en texto desordenado son inútiles a escala. Cómo el logging estructurado en JSON permite hacer filtros precisos por `solicitud_id`.
3. **Demo (6-8 min):** Ejecutar `analizar_logs.py` sobre `logs_produccion_halcon.log` para aislar el error en vivo.
4. **Cierre (1-2 min):** La cultura del postmortem *blameless* del SRE Book de Google y presentación del Ejercicio 01.

---

## 📚 Para profundizar

- [Site Reliability Engineering (SRE Book - Google)](../../recursos/lecturas.md#🔍-observabilidad-debugging-y-operaciones).
- [The Art of Troubleshooting (Jason Maxham)](../../recursos/lecturas.md#🔍-observabilidad-debugging-y-operaciones).

---

⬅️ [Módulo 07: Despliegue y cloud](../07-despliegue-y-cloud/README.md) | 🏠 [Índice](../../README.md) | [Módulo 09: Seguridad y datos del cliente](../09-seguridad-y-datos-del-cliente/README.md) ➡️
