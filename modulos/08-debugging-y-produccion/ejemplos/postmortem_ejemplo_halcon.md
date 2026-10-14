# Postmortem de Incidente: Falla en Sincronización Nocturna de Inventario

**Identificador:** INC-2026-10-14-HALCON-01  
**Fecha del incidente:** 14 de octubre de 2026  
**Severidad:** SEV-1 (Crítico de Negocio)  
**Servicio afectado:** Conector de Sincronización Nexo-Halcón (Almacén MTY)  
**Cliente:** Distribuidora Halcón S.A. de C.V.  
**Autor:** Forward Deployed Engineer (Nexo AI)  
**Revisores:** Laura Garza (Directora de Operaciones, Halcón), Tech Lead (Nexo AI)  
**Estado:** Resuelto / Acción correctiva en marcha  

---

## 1. Resumen Ejecutivo (Executive Summary)

A las 02:00 CST del 14 de octubre de 2026, el proceso programado (*cron job*) de sincronización de inventario para el almacén principal de Monterrey (MTY) experimentó fallas consecutivas, provocando que 1,200 tiendas no recibieran la asignación automática de reabastecimiento matutino.

El incidente tuvo una duración total de **2 horas con 35 minutos**, con un impacto en el 100% de los pedidos de la zona norte. La causa raíz fue la falta de renovación proactiva del token Bearer de autenticación al procesar un volumen inusualmente alto de 15,000 SKUs, provocando errores HTTP `401 Unauthorized`. La política de reintentos con backoff ingenuo sin límite saturó el *rate limit* de la API (`429 Too Many Requests`). 

La mitigación manual se completó a las 04:35 CST mediante ejecución de script con renovación de credenciales, logrando que el 100% de las tiendas operaran con stock actualizado a las 06:15 CST, antes de la apertura al público.

---

## 2. Impacto en el Negocio y SLA

* **Clientes afectados:** Distribuidora Halcón (1 cliente enterprise, 1,200 tiendas afiliadas indirectamente).
* **Impacto en ingresos:** \$0 en cancelaciones directas gracias a que la resolución ocurrió antes de la apertura de sucursales (07:00 CST). Riesgo latente de desabasto estimado en \$450,000 MXN si se hubiera retrasado 2 horas más.
* **Degradación de SLA:** Disponibilidad de sincronización nocturna cayó de 99.9% a 92.5% para esa ventana operativa.

---

## 3. Línea de Tiempo (Timeline CST)

| Hora (CST) | Evento |
|------------|--------|
| **02:00** | Inicia el cron job `sincronizar_inventario.py` para Almacén MTY. Obtiene token Bearer válido por 3,600 segundos (1 hora). |
| **02:45** | Se procesan los primeros 8,000 registros con éxito. La base de datos del ERP local de Halcón responde más lento de lo usual (latencia de 450ms por página). |
| **03:00** | El token Bearer expira. El conector recibe HTTP `401 Unauthorized` en el lote 81. |
| **03:01** | El conector reintenta en bucle cerrado cada 2 segundos sin re-autenticar. El servidor activa limitador de tasa respondiendo HTTP `429 Too Many Requests`. |
| **03:15** | La alerta de Datadog / CloudWatch se dispara: *Tasa de error > 10% en conector Halcón*. Se envía SMS y notificación a PagerDuty del FDE en guardia. |
| **03:22** | El FDE se conecta a la VPN de Halcón, revisa logs centralizados en formato JSON y confirma que el conector sigue en bucle `401 -> 429`. |
| **03:30** | El FDE declara formalmente SEV-1. Envía primer reporte de estatus por correo a Laura Garza y Roberto Treviño. |
| **03:45** | El FDE detiene el proceso atascado para liberar el *rate limiter* de la API simulada. |
| **04:10** | El FDE aplica hotfix en el contenedor: agrega bloque `if response.status == 401: autenticar()` y eleva el umbral de reintentos con backoff exponencial. |
| **04:20** | Se inicia sincronización manual selectiva de los lotes pendientes (SKU 8,001 a 15,000). |
| **04:35** | Finaliza exitosamente la carga del Almacén MTY. Todos los inventarios coinciden con el ERP. |
| **04:45** | Se envía reporte de mitigación a los directivos de Halcón. Incidente mitigado. |

---

## 4. Análisis de Causa Raíz (5 Porqués)

1. **¿Por qué falló la sincronización nocturna del Almacén Monterrey?**  
   Porque el script de sincronización abortó tras acumular más de 50 reintentos fallidos de conexión.
2. **¿Por qué fallaron los reintentos de conexión?**  
   Porque la API de Nexo rechazó las peticiones con código HTTP `401 Unauthorized` y posteriormente con `429 Too Many Requests`.
3. **¿Por qué la API devolvió HTTP 401?**  
   Porque el token de acceso expiró a los 60 minutos de haber iniciado la corrida, y el script asumía que el token inicial duraría toda la ejecución.
4. **¿Por qué la corrida tomó más de 60 minutos en esta ocasión?**  
   Porque el catálogo creció un 40% este fin de mes y la base de datos de Halcón tuvo alta contención de bloqueos (*locks*), aumentando la latencia por lote de 120ms a 450ms.
5. **¿Por qué el script no renovó automáticamente el token ni manejó el backoff adecuadamente?**  
   Porque el conector original fue diseñado para el piloto con un conjunto de datos pequeño (3,000 SKUs) y nunca se actualizó con el cliente HTTP resiliente que implementa interceptores de re-autenticación y respeto a `Retry-After`.

---

## 5. Factores Contribuyentes

* **Falta de pruebas de carga en pre-producción:** El conector solo se probó con catálogos de 3,000 registros; nunca se simuló una corrida de 15,000 registros con latencia de red degradada.
* **Manejo ingenuo de expiración:** La lógica de autenticación estaba acoplada al inicio del script en lugar de estar encapsulada en una sesión HTTP resiliente.
* **Monitoreo tardío:** La alerta tardó 15 minutos en dispararse debido a que la ventana de agregación de métricas de error estaba configurada a 15 minutos en vez de 5.

---

## 6. ¿Qué funcionó bien?

* El formato de **logging estructurado en JSON** permitió al FDE filtrar en menos de 3 minutos el código de error exacto (`401` seguido de `429`) y el lote exacto en el que ocurrió la falla.
* La comunicación proactiva con el cliente: el equipo de Halcón fue notificado a las 03:30 CST antes de que sus propios operadores notaran discrepancias.
* La mitigación ocurrió a tiempo para evitar desabasto físico en las tiendas afiliadas.

---

## 7. Elementos de Acción (Action Items)

| ID | Acción | Responsable | Tipo | Fecha Compromiso |
|----|--------|-------------|------|------------------|
| **ACT-01** | Migrar el script de producción para usar la clase `ClienteResiliente` (con renovación automática de token en 401 y backoff exponencial con jitter). | FDE | Prevención | 16 de octubre de 2026 |
| **ACT-02** | Reducir la ventana de alerta de tasa de error en CloudWatch/Datadog de 15 a 5 minutos para integraciones críticas. | DevOps / FDE | Detección | 15 de octubre de 2026 |
| **ACT-03** | Implementar pruebas de estrés en CI/CD que simulen sincronizaciones de 30,000 registros con tokens de vida corta (10 minutos) y latencias inyectadas. | QA / FDE | Prevención | 22 de octubre de 2026 |
| **ACT-04** | Documentar en el Runbook de Halcón el procedimiento de recuperación manual de lotes no sincronizados. | FDE | Documentación | 17 de octubre de 2026 |
