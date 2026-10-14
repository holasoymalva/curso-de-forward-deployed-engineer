# Lección 04: Cuestionarios de seguridad y cumplimiento normativo

## 🎯 Objetivos de aprendizaje

* Conocer los principales marcos normativos y de certificación (LFPDPPP, GDPR, SOC 2, ISO 27001) a nivel conceptual y técnico.
* Entender qué es un Cuestionario de Evaluación de Proveedores (*Vendor Security Assessment*) y cuál es el rol del FDE al responderlo.
* Saber cómo articular respuestas técnicas claras y transparentes para el equipo de seguridad o CISO del cliente.

---

## 📜 1. Panorama de marcos normativos y certificaciones

*(Nota: Esta sección provee orientación técnica y de ingeniería; no constituye asesoría legal).*

Cuando una empresa grande evalúa contratar a una startup de tecnología, el departamento legal y el equipo de Seguridad de la Información (*InfoSec*) realizan un proceso de debida diligencia (*Due Diligence*). Los marcos más comunes con los que interactuarás son:

### A. Ley Federal de Protección de Datos Personales en Posesión de los Particulares (LFPDPPP - México)
* **Objetivo:** Regular el tratamiento legítimo, controlado e informado de los datos personales en México.
* **Conceptos clave:**
  * **Responsable:** La empresa cliente (Distribuidora Halcón) que decide sobre el tratamiento de los datos.
  * **Encargado:** Tu empresa proveedora (Nexo AI) que procesa datos por cuenta del responsable.
  * **Derechos ARCO:** Acceso, Rectificación, Cancelación y Oposición del titular sobre sus datos.
* **Implicación para el FDE:** Debes poder garantizar que si un cliente solicita la cancelación de los datos de un usuario o tienda, el sistema cuenta con los mecanismos para localizarlos y eliminarlos de forma comprobable.

### B. Reglamento General de Protección de Datos (GDPR - Unión Europea)
* El estándar global más estricto sobre privacidad, consentimiento explícito, derecho al olvido y transferencia internacional de datos personales.

### C. SOC 2 (Service Organization Control 2 - Tipo I y Tipo II)
* Estándar de auditoría independiente desarrollado por el AICPA estadounidense, muy solicitado por empresas SaaS globales.
* Evalúa 5 principios de confianza (*Trust Services Criteria*): **Seguridad**, **Disponibilidad**, **Integridad de procesamiento**, **Confidencialidad** y **Privacidad**.
* Como FDE, tus procesos de control de versiones, revisión de código (*Pull Requests*) y registro de cambios en producción son evidencia para la auditoría SOC 2.

### D. ISO/IEC 27001
* Estándar internacional para implementar un Sistema de Gestión de Seguridad de la Información (SGSI).

---

## 📋 2. El Cuestionario de Seguridad de Proveedores (Security Assessment)

Antes de firmar el contrato definitivo o desplegar la solución en producción, el CISO o Gerente de Seguridad de Halcón enviará un cuestionario en Excel o plataforma web (como Whistic, OneTrust o Panorays) con entre 50 y 200 preguntas técnicas.

El equipo comercial no tiene las respuestas técnicas; **es el FDE quien debe redactar o validar las respuestas de arquitectura**.

### Preguntas típicas y cómo responderlas como FDE

| Pregunta típica del cliente | Respuesta técnica adecuada (FDE) | ❌ Lo que nunca debes responder |
|-----------------------------|----------------------------------|--------------------------------|
| *"¿Dónde se almacenan nuestros datos y quién tiene acceso a ellos?"* | *"Los datos se alojan en una base de datos PostgreSQL alojada en AWS región us-east-1 (N. Virginia), cifrada en reposo con AES-256 (KMS). Solo 2 ingenieros de operaciones cuentan con acceso restringido mediante MFA y llaves efímeras, auditado en CloudTrail."* | *"En nuestros servidores en la nube y nadie que no deba los ve."* (Vago e informal). |
| *"¿Qué hacen en caso de una brecha de seguridad (*data breach*)?"* | *"Contamos con un Plan de Respuesta a Incidentes (IRP) documentado con notificación al cliente en menos de 24 horas y severidades SEV-1 definidas para movilización inmediata."* | *"Nunca nos han hackeado, nuestro sistema es 100% seguro."* (Inexperto y falso). |
| *"¿Realizan pruebas de penetración (*pentesting*) periódicas?"* | *"Sí, anualmente a través de una firma externa certificada y ejecutamos escaneos automatizados de vulnerabilidades (SAST/DAST) en cada Pull Request de GitHub."* | *"No, pero revisamos bien el código antes de mandarlo."* |

---

## 🤝 3. Construyendo confianza con el CISO del cliente

El equipo de seguridad del cliente suele ser visto erróneamente por los desarrolladores como un obstáculo. Un FDE senior entiende que el CISO es un aliado clave:
1. **Sé transparente:** Si tu sistema no soporta una característica (por ejemplo, integración con Active Directory on-premise), dilo con honestidad y propón la alternativa técnica (OAuth 2.0 / Okta).
2. **Entrega documentación formal:** Ten listos los diagramas de arquitectura de red (Data Flow Diagrams), políticas de retención y certificados de cumplimiento.
3. **No improvises promesas legales:** Si te preguntan sobre indemnizaciones por pérdida de datos, canaliza la respuesta con tu equipo legal interno.

---

## 📌 Conclusiones clave

* La seguridad y el cumplimiento normativo son requisitos no funcionales tan importantes como el rendimiento del código.
* Las respuestas a cuestionarios de seguridad deben ser precisas, con nombres de tecnologías, regiones y algoritmos específicos.
* La transparencia técnica genera ventas enterprise; la vaguedad o las falsas promesas destruyen contratos.
