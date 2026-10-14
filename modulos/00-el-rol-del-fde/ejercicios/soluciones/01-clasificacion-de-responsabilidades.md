# Solución al Ejercicio 01: Clasificación de responsabilidades por rol

---

## 📋 Matriz de clasificación resuelta

| Tarea | Rol Responsable | Justificación y Postura del FDE |
|-------|-----------------|---------------------------------|
| **A. Olvido de contraseña de un supervisor en MTY** | **Soporte Técnico (Nivel 1)** | Es una solicitud de administración de usuarios rutinaria. El FDE canaliza cordialmente al usuario al flujo de autoservicio o al equipo de soporte (`soporte@nexo.com`), evitando convertirse en el cuello de botella de accesos diarios. |
| **B. Revisión de certificados TLS y reintentos con Roberto** | **Forward Deployed Engineer (FDE)** | Es el núcleo del rol de FDE: sentarse con el responsable de TI del cliente para acordar parámetros de integración, seguridad de red y límites de carga. |
| **C. Inconsistencias en el CSV del ERP (precios y mayúsculas)** | **Forward Deployed Engineer (FDE)** | Resolver el "último kilómetro" de los datos del cliente. El FDE escribe el script de normalización en Python para que el conector procese los datos sin fallar y documenta el caso para proponerlo a Core SWE. |
| **D. Cotización de nueva funcionalidad meteorológica** | **Ventas / Account Executive / CSM** | Modificaciones contractuales, adición de módulos no contemplados y presupuesto corresponden al área comercial. El FDE puede dar una estimación de viabilidad técnica si se lo piden, pero no negocia precios. |
| **E. Cuello de botella en PostgreSQL de la nube de Nexo** | **Core Software Engineer (SWE)** | Afecta la infraestructura central de producto compartida por todos los clientes. Corresponde al equipo de plataforma central. El FDE únicamente monitorea el impacto en su cliente y comunica el estatus. |
| **F. Script para alertar pedidos pendientes con >24 h de retraso** | **Forward Deployed Engineer (FDE)** | Lógica de integración específica solicitada para resolver el dolor operativo de Halcón. El FDE implementa la consulta y genera la alerta. |
| **G. Encuesta trimestral de satisfacción (NPS) y renovación** | **Customer Success Manager (CSM)** | Gestión de la relación comercial a largo plazo, métricas de satisfacción y proceso formal de renovación de contrato. |
| **H. Demo comercial de 20 minutos para prospecto aliado** | **Solutions Engineer (SE / Sales Engineer)** | Es una demostración de preventa estándar para captar un nuevo cliente. Si el equipo comercial no tiene disponibilidad, el FDE podría apoyar excepcionalmente, pero la responsabilidad primaria es de preventa. |

---

## 💡 Aprendizaje clave

Decir "no" o canalizar correctamente una tarea no es eludir responsabilidades: es proteger el tiempo de alto impacto que el cliente y tu empresa necesitan para que la integración productiva salga a tiempo.
