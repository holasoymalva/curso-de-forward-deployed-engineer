# Solución al Ejercicio 02: Respuestas técnicas al cuestionario de seguridad

A continuación se presenta el modelo de respuesta formal que un Forward Deployed Engineer senior entrega al CISO de Distribuidora Halcón.

---

## Sección 1: Control de accesos y autenticación

### 1. ¿Cómo se gestiona el acceso de los empleados del proveedor a los datos de Distribuidora Halcón?
> **Respuesta Nexo AI:**  
> Aplicamos de manera estricta el Principio de Mínimo Privilegio (*PoLP*) y Control de Acceso Basado en Roles (*RBAC*).  
> Los datos de producción de Distribuidora Halcón no son accesibles por defecto para los desarrolladores de Nexo. Únicamente dos ingenieros designados del equipo de Forward Deployed Engineering (FDE) cuentan con credenciales con nombre propio para el entorno de producción.  
> Dichas conexiones requieren autenticación obligatoria mediante llave SSH de curva elíptica (`ed25519`) protegida por frase de paso y autenticación multifactor (MFA), originadas exclusivamente a través de la VPN corporativa de Nexo. Cada acceso y consulta a nivel de base de datos queda registrado de manera inmutable en bitácoras de auditoría de AWS CloudTrail, retenidas por un mínimo de 365 días.

### 2. ¿Qué políticas de autenticación y complejidad de contraseñas aplican a sus sistemas internos?
> **Respuesta Nexo AI:**  
> Nexo AI cuenta con un proveedor de identidad centralizado (IdP compatible con SAML 2.0 / OIDC) con política de acceso condicional. Todas las cuentas de empleados exigen contraseñas con longitud mínima de 14 caracteres alfanuméricos gestionadas por bóvedas de contraseñas corporativas, combinadas con MFA obligatorio basado en hardware (FIDO2/WebAuthn o aplicaciones TOTP como Google Authenticator). Se prohíbe el uso de SMS para verificación en dos pasos. Se aplica bloqueo de cuenta tras 5 intentos fallidos y cierre de sesión por inactividad tras 15 minutos.

---

## Sección 2: Cifrado y protección de datos

### 3. ¿Qué algoritmos y estándares de cifrado se utilizan para proteger nuestra información en tránsito y en reposo?
> **Respuesta Nexo AI:**  
> - **Cifrado en tránsito (*Data in Transit*):** Todo el tráfico entre los servidores de Halcón y la nube de Nexo, así como el tráfico interno entre microservicios, se transmite exclusivamente a través de HTTPS sobre **TLS 1.3** (con soporte de reserva para TLS 1.2), utilizando suites criptográficas seguras como `ECDHE-RSA-AES256-GCM-SHA384`. Se rechazan conexiones que utilicen TLS 1.0, 1.1 o SSLv3. La verificación de certificados SSL/TLS está activa permanentemente sin excepciones.
> - **Cifrado en reposo (*Data at Rest*):** Todos los volúmenes de almacenamiento, bases de datos (PostgreSQL/SQLite) y respaldos automatizados están cifrados mediante el estándar de la industria **AES-256** a nivel de bloque (XTS-AES-256 o AES-GCM).

### 4. ¿Cómo se gestionan las llaves de cifrado y con qué frecuencia se rotan?
> **Respuesta Nexo AI:**  
> Las llaves maestras de cifrado (*Customer Master Keys*, CMK) son administradas a través de AWS KMS (Hardware Security Modules con certificación FIPS 140-2 Nivel 3). Las llaves cuentan con rotación automática anual habilitada. Ningún empleado de Nexo tiene acceso a las llaves criptográficas privadas en texto plano. En caso de incidente de seguridad comprobado, existe un procedimiento de revocación inmediata que inutiliza los datos cifrados en menos de 10 minutos.

---

## Sección 3: Manejo de incidentes y continuidad de negocio

### 5. En caso de sospecha de una brecha de seguridad que involucre nuestros datos, ¿cuál es el SLA para notificarnos y qué información contendrá el primer reporte?
> **Respuesta Nexo AI:**  
> De conformidad con nuestro Plan de Respuesta a Incidentes (IRP) y los acuerdos de procesamiento de datos (*DPA*), nos comprometemos formalmente a notificar al CISO y al punto de contacto de seguridad de Distribuidora Halcón dentro de un plazo máximo de **24 horas posteriores a la confirmación de cualquier incidente de seguridad o acceso no autorizado que comprometa sus datos**.  
> El reporte preliminar incluirá:
> 1. Descripción técnica del incidente y vector de ataque identificado.
> 2. Tipo y volumen estimado de datos comprometidos (confirmando si existió o no exposición de PII).
> 3. Medidas de contención inmediatas implementadas (bloqueo de IPs, rotación de credenciales, desconexión de servicios).
> 4. Datos de contacto del Comandante de Incidente (*Incident Commander*) de Nexo asignado para el seguimiento.

### 6. ¿Qué estrategia de respaldos y recuperación ante desastres (*DRP*) tienen implementada?
> **Respuesta Nexo AI:**  
> Implementamos respaldos continuos con recuperación en un punto en el tiempo (*Point-in-Time Recovery*, PITR) con un **RPO** (*Recovery Point Objective*) menor a 15 minutos y un **RTO** (*Recovery Time Objective*) menor a 2 horas. Los respaldos se replican de forma asíncrona a una región secundaria geográficamente distante (us-west-2), con pruebas periódicas de restauración semestrales documentadas.

---

## Sección 4: Cumplimiento y privacidad

### 7. ¿De qué manera garantizan el cumplimiento con la Ley Federal de Protección de Datos Personales en Posesión de los Particulares (LFPDPPP) en relación con los derechos ARCO de nuestros clientes y encargados de tienda?
> **Respuesta Nexo AI:**  
> Nexo AI actúa bajo la figura legal de **Encargado** del tratamiento de datos personales, mientras que Distribuidora Halcón ostenta la figura de **Responsable**.  
> Para facilitar el ejercicio de los **Derechos ARCO (Acceso, Rectificación, Cancelación y Oposición)**:
> 1. Nuestro pipeline de ingesta implementa *minimización de datos*, descartando nombres personales y teléfonos en la capa de conector antes de persistir en la nube analítica.
> 2. Los identificadores operativos (como IDs de tienda) utilizan *hashing determinista con sal*, garantizando seudonimización irreversible.
> 3. Disponemos de un endpoint administrativo específico (`DELETE /v1/clientes/{id}/purgar-datos`) y un protocolo operativo para que, ante cualquier solicitud formal de cancelación emitida por Halcón, los datos residuales sean eliminados de bases de datos activas y marcados para purga en respaldos en un lapso no mayor a 5 días hábiles, emitiendo un certificado digital de destrucción de datos.
