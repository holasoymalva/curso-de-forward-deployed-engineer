# Checklist de Seguridad para Implementaciones de FDE

Este documento contiene la lista de verificación obligatoria de 25 controles que todo Forward Deployed Engineer debe validar antes de desplegar un conector, worker o servicio en el entorno de producción de un cliente.

---

## 🔐 1. Gestión de accesos y credenciales

- [ ] **1.1. Principio de mínimo privilegio aplicado:** El usuario de base de datos o token de API asignado a la solución tiene únicamente permisos de lectura/escritura sobre las tablas y endpoints estrictamente necesarios.
- [ ] **1.2. Cero secretos en repositorios:** Se ejecutó un escaneo con herramientas de detección de secretos (`git-secrets` o `trufflehog`) confirmando que no hay API keys, tokens o contraseñas en el historial de Git.
- [ ] **1.3. Inyección vía variables de entorno:** Todas las credenciales se cargan exclusivamente en tiempo de ejecución desde variables de entorno del sistema o un gestor de secretos (AWS Secrets Manager, GCP Secret Manager, Vault).
- [ ] **1.4. Archivo `.env.example` actualizado:** El repositorio incluye una plantilla sin valores reales y el archivo `.env` está expresamente excluido en `.gitignore`.
- [ ] **1.5. Plan de rotación establecido:** Se documentó el procedimiento para rotar credenciales cada 90 días o de forma inmediata en caso de sospecha de compromiso.

---

## 👤 2. Protección de datos personales (PII) y privacidad

- [ ] **2.1. Minimización de datos en ingesta:** Se analizaron todos los esquemas de entrada y se descartaron campos personales no indispensables (nombres, CURP, RFC, correos personales, domicilios).
- [ ] **2.2. Enmascaramiento activo:** Los campos personales requeridos para auditoría o conciliación visual están ofuscados o seudonimizados antes de viajar fuera de la red del cliente.
- [ ] **2.3. Sanitización de logs:** Los formateadores de logs estructurados excluyen encabezados de autorización (`Authorization: Bearer ...`), contraseñas y cuerpos de petición con PII.
- [ ] **2.4. Política de retención de archivos temporales:** Los archivos CSV intermedios almacenados en carpetas temporales (`/tmp`) se borran automáticamente tras el procesamiento.
- [ ] **2.5. Cláusula de confidencialidad (NDA):** Se verificó que el acuerdo de confidencialidad y el anexo de tratamiento de datos personales (*DPA*) estén firmados entre ambas empresas.

---

## 🌐 3. Seguridad de red y comunicaciones

- [ ] **3.1. Cifrado obligatorio en tránsito (TLS):** Todas las comunicaciones HTTP utilizan HTTPS sobre TLS 1.2 o TLS 1.3 con certificados válidos emitidos por una CA oficial.
- [ ] **3.2. Verificación de certificados activa:** En ningún script o cliente HTTP se desactiva la verificación de certificados SSL (`verify=False` prohibido).
- [ ] **3.3. Segmentación de red y firewalls:** El tráfico hacia la infraestructura del cliente proviene de un conjunto conocido y estático de direcciones IP públicas (IP Whitelisting) o a través de un túnel VPN dedicado.
- [ ] **3.4. Cierre de puertos innecesarios:** Los servidores o contenedores desplegados no exponen puertos administrativos (como SSH 22 o bases de datos 5432) a internet abierto.

---

## 💾 4. Cifrado y almacenamiento en reposo

- [ ] **4.1. Volúmenes de disco cifrados:** Las bases de datos locales (SQLite) o volúmenes de contenedores donde se almacene información de catálogo utilizan cifrado de bloque a nivel de disco (AES-256).
- [ ] **4.2. Respaldos protegidos:** Los respaldos de base de datos se generan cifrados y se transmiten mediante canales seguros con permisos de acceso restringidos.
- [ ] **4.3. Separación física o lógica multitenant:** Los datos del cliente están aislados lógicamente por identificador de organización (`tenant_id`) en bases de datos compartidas, impidiendo accesos cruzados.

---

## 📦 5. Seguridad en código y contenedores (Docker)

- [ ] **5.1. Usuario no-root en contenedores:** Los `Dockerfile` ejecutan los procesos con un usuario de sistema dedicado sin privilegios (evitando `USER root`).
- [ ] **5.2. Imágenes base mínimas y actualizadas:** Se utilizan imágenes oficiales ligeras (`python:3.11-slim` o Alpine) sin paquetes o herramientas de compilación innecesarias.
- [ ] **5.3. Escaneo de vulnerabilidades de dependencias:** Se ejecutó `pip audit` o `trivy` para garantizar que no existan vulnerabilidades críticas conocidas (CVEs) en las bibliotecas utilizadas.
- [ ] **5.4. Límite de recursos:** La configuración de despliegue (Docker Compose o Kubernetes) define límites máximos de memoria RAM y CPU para prevenir ataques de denegación de servicio por agotamiento de recursos.

---

## 🚨 6. Operación y respuesta a incidentes

- [ ] **6.1. Canal de comunicación de seguridad definido:** Se acordaron los contactos de emergencia entre el FDE y el equipo de seguridad/TI del cliente (teléfonos y correos para alertas 24/7).
- [ ] **6.2. Procedimiento de desconexión rápida (Kill-Switch):** Existe un mecanismo rápido y documentado para apagar el conector o revocar el token en menos de 5 minutos si se detecta una anomalía.
- [ ] **6.3. Trazabilidad de auditoría:** Cada acción de sincronización emite un identificador de correlación (`correlation_id`) para facilitar investigaciones forenses conjuntas.
