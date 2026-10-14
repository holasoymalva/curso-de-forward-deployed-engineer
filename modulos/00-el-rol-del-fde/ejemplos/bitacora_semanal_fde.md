# 📓 Bitácora semanal de un Forward Deployed Engineer

**Semana del:** 12 al 16 de Octubre  
**FDE Asignado:** Alex Morales  
**Cliente:** Distribuidora Halcón (Cuenta Estratégica)  
**Objetivo de la semana:** Validar el conector ETL de inventario nocturno y desbloquear accesos con TI.

---

## 🗓️ Lunes: Alineación y revisión de bloqueos

- **09:00 - 09:30 | Standup interno con equipo Nexo:**
  - Compartí que el conector de staging está listo pero que aún no tenemos las credenciales de la API de pedidos de Halcón.
- **10:00 - 11:00 | Llamada de sincronización técnica con Roberto Treviño (Gerente de TI Halcón):**
  - Revisamos la arquitectura de red. Roberto autorizó habilitar una IP fija de salida en su firewall para nuestro contenedor.
  - Generó y me compartió de manera segura las credenciales de prueba (`client_id` y `client_secret`).
- **11:30 - 14:00 | Trabajo técnico:**
  - Configuré las variables de entorno en nuestro contenedor de prueba local.
  - Primer prueba de autenticación contra su endpoint `/auth/token`: ¡Respuesta exitosa 200 con Bearer Token!
- **15:00 - 17:00 | Análisis de datos:**
  - Descargué el primer CSV exportado por su ERP nocturno (`inventario_erp.csv`).
  - Detecté anomalías: 2 SKUs duplicados con mayúsculas y minúsculas mixtas, y 1 registro con cantidad negativa en Guadalajara (`-5`).

---

## 🗓️ Martes: Construcción y resiliencia de código

- **09:00 - 13:00 | Programación:**
  - Escribí el módulo de sanitización de datos en Python para limpiar espacios en blanco en SKUs y convertir precios con comas a flotantes válidos.
  - Agregué una regla para marcar cantidades negativas con una alerta amarilla sin detener el proceso completo.
- **14:00 - 15:00 | Sesión de trabajo con Mariana López (Analista de Inventarios):**
  - Le mostré una previsualización de cómo se detectó el stock en cero del arroz en CDMX. Mariana confirmó que esa alerta le ahorra 40 minutos de revisión matutina en Excel.
- **15:30 - 17:30 | Pruebas de integración:**
  - Simulamos una caída de red forzando errores 503 en la API. El mecanismo de backoff exponencial esperó 2, 4 y 8 segundos hasta recuperar la conexión sin duplicar registros.

---

## 🗓️ Miércoles: Despliegue en ambiente de pruebas

- **09:30 - 11:30 | Dockerización:**
  - Armé el `docker-compose.yml` final que ejecuta el worker de sincronización en segundo plano con límites de memoria de 256 MB.
- **12:00 - 13:00 | Prueba de carga:**
  - Procesamos 1,000 registros sintéticos en 1.8 segundos. El consumo de CPU se mantuvo por debajo del 12 %.
- **15:00 - 16:30 | Reunión interna con Product Manager de Nexo:**
  - Reporté que dos clientes anteriores y ahora Halcón han necesitado normalizar precios con formato de coma decimal (`"76,50"`). Propuse incluir esta limpieza como estándar en el core de la plataforma.

---

## 🗓️ Jueves: Simulacro y mitigación de incidentes

- **10:00 - 11:30 | Prueba en vivo con datos reales de Monterrey:**
  - Al ejecutar la sincronización de las 10:30 AM, el token de acceso expiró a los 5 minutos y la API respondió con código 401.
  - El conector capturó el 401, solicitó automáticamente un nuevo token al endpoint `/auth/token` y reanudó la carga en el registro exacto donde se quedó sin tirar error crítico.
- **14:00 - 16:00 | Redacción técnica:**
  - Escribí el borrador del Runbook operativo para el equipo de soporte de Roberto Treviño.

---

## 🗓️ Viernes: Reporte ejecutivo y cierre

- **10:00 - 10:45 | Demo semanal con Laura Garza (Directora de Operaciones):**
  - Mostré el tablero de Nexo con los datos del almacén Monterrey totalmente sincronizados.
  - Destacamos la identificación inmediata de 4 productos por debajo del stock mínimo.
  - Laura aprobó iniciar la fase piloto el próximo martes.
- **11:00 - 12:30 | Envío de reporte de estatus semanal:**
  - Correo ejecutivo enviado a Laura Garza, Roberto Treviño y al Director de Operaciones de Nexo.

---

## 📊 Balance semanal

- **Tiempo en código / terminal:** 50 % (20 horas)
- **Tiempo con cliente (reuniones / demos):** 30 % (12 horas)
- **Documentación y producto:** 20 % (8 horas)
- **Resultado clave:** Monterrey listo para piloto con 0 bloqueos abiertos.
