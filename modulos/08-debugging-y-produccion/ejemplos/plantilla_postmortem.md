# 📄 Plantilla Oficial de Postmortem sin Culpas (*Blameless Postmortem*)

**Título del Incidente:** [Breve descripción del síntoma o caída]  
**Fecha del Incidente:** [AAAA-MM-DD]  
**Severidad:** [Sev-1 / Sev-2 / Sev-3]  
**Autores / Investigadores:** [Nombres y roles]  
**Estado:** [Borrador / En Revisión / Aprobado]  

---

## 1. Resumen Ejecutivo
[Párrafo de 3-4 líneas resumiendo qué falló, cuánto tiempo duró la interrupción, qué usuarios o clientes fueron afectados y cómo se restableció la operación].

---

## 2. Impacto en el Negocio y Usuarios
- **Duración total del impacto:** [X horas Y minutos].
- **Clientes / Cuentas afectadas:** [Nombres o porcentaje].
- **Impacto cuantitativo:** [X pedidos demorados, \$X en transacciones retrasadas, X llamadas a soporte].
- **Incumplimiento de SLA:** [¿Se violó el SLA contractual? ¿Sí / No y por cuánto?].

---

## 3. Línea de Tiempo de los Hechos (*Timeline*)
*Todas las horas en horario local del cliente [Zona Horaria].*

- **HH:MM** - Ocurre el evento detonante (ej. despliegue, fallo de red, saturación).
- **HH:MM** - Se detecta la primera anomalía (alerta automática o reporte de usuario).
- **HH:MM** - Se declara formalmente el incidente y se asigna al FDE líder.
- **HH:MM** - Se implementa la primera medida de mitigación (ej. rollback o reinicio).
- **HH:MM** - Se confirma el restablecimiento de la operación normal.
- **HH:MM** - Se cierra el incidente.

---

## 4. Análisis de Causa Raíz (*Root Cause Analysis - RCA*)
*Aplicar la técnica de los 5 Porqués para llegar al fallo de proceso o salvaguarda sistémica:*
1. ¿Por qué falló el servicio? -> Porque...
2. ¿Por qué ocurrió eso? -> Porque...
3. ¿Por qué el sistema no lo previno? -> Porque...
4. ¿Por qué faltaba esa validación? -> Porque...
5. ¿Por qué el proceso lo permitió? -> Porque...

**Causa Raíz Sistémica:** [Explicación técnica del vacío de proceso o falta de automatización].

---

## 5. Lecciones Aprendidas

### ¿Qué funcionó bien?
- [Aspectos positivos de la respuesta, herramientas o comunicación].

### ¿Qué funcionó mal o fue lento?
- [Dificultades para diagnosticar, falta de logs, demoras en accesos].

### ¿Dónde tuvimos suerte?
- [Factores externos o casualidades que evitaron que el daño fuera mayor].

---

## 6. Elementos de Acción Preventiva (*Action Items*)

| # | Acción Preventiva Concreta | Tipo (Prevenir / Detectar / Mitigar) | Responsable | Fecha Límite | Ticket / PR |
|---|----------------------------|--------------------------------------|-------------|--------------|-------------|
| 1 | [Tarea técnica específica] | Prevenir | [Nombre] | [AAAA-MM-DD] | NEX-101 |
| 2 | [Crear alerta de monitoreo] | Detectar | [Nombre] | [AAAA-MM-DD] | NEX-102 |
| 3 | [Actualizar Runbook de soporte] | Mitigar | [Nombre] | [AAAA-MM-DD] | NEX-103 |
