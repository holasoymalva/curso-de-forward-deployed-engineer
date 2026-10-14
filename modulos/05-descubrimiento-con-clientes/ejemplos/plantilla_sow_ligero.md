# 📄 Documento de Alcance Técnico (SOW Ligero)

**Proyecto:** [Nombre del Proyecto de Integración]  
**Cliente:** [Nombre de la Empresa Cliente]  
**Proveedor:** [Tu Empresa / Plataforma]  
**Fecha de emisión:** [AAAA-MM-DD]  
**Versión:** 1.0  

---

## 1. Objetivo General y Justificación de Negocio

[Describir en 1 o 2 párrafos el problema central que se resuelve y la meta cuantificable que se alcanzará al concluir la implementación].

---

## 2. Alcance Incluido en el Proyecto (*In-Scope*)

El equipo de implementación entregará exclusivamente los siguientes componentes funcionales:

- [ ] **Componente 1:** [ej. Conector automatizado en contenedor Docker para extracción nocturna de datos].
- [ ] **Componente 2:** [ej. Módulo de sanitización y limpieza de catálogo maestro y existencias].
- [ ] **Componente 3:** [ej. Reglas de alerta temprana para productos por debajo del stock mínimo].
- [ ] **Componente 4:** [ej. Integración con la API interna de pedidos para consulta de órdenes pendientes].
- [ ] **Documentación:** [ej. Manual operativo (Runbook) y sesión de capacitación de 1 hora para el equipo de soporte].

---

## 3. Exclusiones Explícitas (*Out-of-Scope*)

Para garantizar la entrega puntual y la estabilidad del proyecto, los siguientes aspectos **no forman parte** de esta fase de implementación:

- ❌ Modificación o desarrollo de código fuente dentro de los sistemas legados o ERPs del cliente.
- ❌ Integración con sistemas fiscales o de facturación electrónica.
- ❌ Creación de aplicaciones móviles o portales web no contemplados en la licencia estándar.
- ❌ Migración o corrección de datos históricos con más de [X] meses de antigüedad.

---

## 4. Criterios de Aceptación Objetivos

El cliente considerará concluida y aprobada la implementación cuando se cumplan las siguientes condiciones medibles:

1. El pipeline procese el archivo de datos diario de forma automática en un tiempo inferior a [X] minutos.
2. La tasa de disponibilidad de las alertas en el tablero sea superior al 99 % antes de las [HH:MM] AM durante 5 días hábiles consecutivos.
3. El contenedor no exceda los límites de recursos pactados ([X] MB de memoria RAM / [X] % de CPU).
4. El personal designado del cliente haya recibido la capacitación y el Runbook técnico.

---

## 5. Cronograma por Hitos y Dependencias

| Hito | Entregable Técnico | Semana Estimada | Dependencia del Cliente |
|------|--------------------|-----------------|-------------------------|
| **H1** | SOW firmado y accesos recibidos | Semana 1 | Entrega de credenciales de API y máquina de pruebas por parte de TI. |
| **H2** | Conector probado en ambiente Staging | Semana 2 | Validación de datos limpios por parte del equipo de analistas. |
| **H3** | Piloto en producción (Almacén Inicial) | Semana 3 | Autorización de red y confirmación de inicio de pruebas en vivo. |
| **H4** | Go-Live general y entrega de Runbook | Semana 4 | Aprobación final de la junta directiva. |

---

## 6. Firmas y Aprobaciones

| Por el Cliente | Por el Proveedor |
|----------------|------------------|
| **Nombre:** [Nombre del Sponsor] | **Nombre:** [Nombre del FDE] |
| **Puesto:** [Puesto / Cargo] | **Puesto:** Forward Deployed Engineer |
| **Fecha:** __________________ | **Fecha:** __________________ |
