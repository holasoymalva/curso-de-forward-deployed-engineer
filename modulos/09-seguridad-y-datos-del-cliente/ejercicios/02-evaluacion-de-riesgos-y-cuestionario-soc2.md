# Ejercicio 02: Evaluación de riesgos y cuestionario de seguridad SOC 2

## 🎯 Objetivo

Practicar la redacción de respuestas formales a un cuestionario de evaluación de seguridad de proveedores (*Vendor Risk Assessment*), demostrando rigor técnico, transparencia y apego a las mejores prácticas de ciberseguridad corporativa.

---

## 🏢 Contexto del problema

El Oficial de Seguridad de la Información (CISO) de Distribuidora Halcón ha condicionado la firma del contrato definitivo y la apertura del acceso al ERP de producción a la aprobación del siguiente cuestionario técnico.

Tu Tech Lead te pide responder a las siguientes 4 secciones con datos coherentes basados en la arquitectura que hemos construido para Nexo AI a lo largo del curso (Docker, APIs con tokens Bearer, cifrado TLS 1.3, SQLite/PostgreSQL y servidores en la nube).

---

## 📝 Cuestionario a responder

### Sección 1: Control de accesos y autenticación
1. *¿Cómo se gestiona el acceso de los empleados del proveedor a los datos de Distribuidora Halcón?*
2. *¿Qué políticas de autenticación y complejidad de contraseñas aplican a sus sistemas internos?*

### Sección 2: Cifrado y protección de datos
3. *¿Qué algoritmos y estándares de cifrado se utilizan para proteger nuestra información en tránsito y en reposo?*
4. *¿Cómo se gestionan las llaves de cifrado y con qué frecuencia se rotan?*

### Sección 3: Manejo de incidentes y continuidad de negocio
5. *En caso de sospecha de una brecha de seguridad que involucre nuestros datos, ¿cuál es el SLA para notificarnos y qué información contendrá el primer reporte?*
6. *¿Qué estrategia de respaldos y recuperación ante desastres (*DRP*) tienen implementada?*

### Sección 4: Cumplimiento y privacidad
7. *¿De qué manera garantizan el cumplimiento con la Ley Federal de Protección de Datos Personales en Posesión de los Particulares (LFPDPPP) en relación con los derechos ARCO de nuestros clientes y encargados de tienda?*

---

## 🔍 Criterios de evaluación

* Respuestas redactadas en tono técnico, profesional e inequívoco (evitar respuestas de una sola palabra como *"Sí"* o *"No"*).
* Mención de estándares específicos (TLS 1.3, AES-256, MFA, RBAC, etc.).
* Explicación clara de responsabilidades compartidas.
