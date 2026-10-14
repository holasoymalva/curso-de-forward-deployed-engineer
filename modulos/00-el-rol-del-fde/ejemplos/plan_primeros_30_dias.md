# 📋 Plan de acción para los primeros 30 días de implementación

**Cliente:** Distribuidora Halcón  
**Proveedor:** Plataforma Nexo  
**Responsable Técnico:** Forward Deployed Engineer (FDE)  

Este documento establece los objetivos, actividades clave y entregables verificables para asegurar un *Time-to-Value* récord y mitigar riesgos en la cuenta.

---

## 📅 Semana 1: Descubrimiento técnico y alineación de stakeholders

### Objetivos
- Identificar a todos los actores clave y comprender sus prioridades individuales.
- Levantar la arquitectura técnica actual (*As-Is*) y mapear restricciones de red y seguridad.
- Obtener muestras reales de datos y credenciales de acceso a entornos de prueba.

### Actividades
- [ ] Conducir la reunión formal de arranque (*Kickoff Meeting*) con Laura Garza y Roberto Treviño.
- [ ] Entrevistar a Mariana López para documentar el proceso manual actual de consolidación de inventario en Excel.
- [ ] Recibir el primer archivo de exportación nocturna del ERP (`inventario_erp.csv`) y analizar inconsistencias.
- [ ] Acordar con Roberto Treviño el método de autenticación y entrega de credenciales seguras.

### Entregable de la semana
- **Documento de Alcance Técnico (SOW ligero):** Especificación de arquitectura acordada, calendario y criterios de aceptación firmados.

---

## 📅 Semana 2: Construcción y validación del conector base

### Objetivos
- Desarrollar la canalización de extracción, transformación y carga (ETL).
- Validar la sanitización de datos contra casos extremos (fechas mezcladas, valores nulos, SKUs duplicados).
- Diseñar la integración con la API de pedidos con autenticación Bearer y manejo de errores.

### Actividades
- [ ] Programar script en Python para procesar el CSV del ERP y cargar los registros limpios en SQLite.
- [ ] Implementar cliente HTTP con reintentos automáticos ante códigos 429 y 503.
- [ ] Validar que las llamadas de creación de pedidos incluyan cabeceras de idempotencia.
- [ ] Presentar primer avance funcional a Mariana López para validar la lógica de negocio de stock mínimo.

### Entregable de la semana
- **Código del conector probado localmente:** Capaz de procesar el lote completo de productos sin interrupciones por datos malformados.

---

## 📅 Semana 3: Despliegue en Staging y Piloto Controlado (Monterrey)

### Objetivos
- Empaquetar la solución en contenedores Docker y desplegar en la infraestructura de prueba acordada.
- Iniciar la prueba piloto exclusivamente con el Almacén Monterrey (MTY).
- Monitorear en tiempo real la confiabilidad de las alertas de inventario.

### Actividades
- [ ] Configurar el archivo `docker-compose.yml` con inyección de variables de entorno seguras.
- [ ] Ejecutar la sincronización automática programada (cron) durante 3 días consecutivos.
- [ ] Medir discrepancias entre el inventario reportado por Nexo y el inventario físico en Monterrey.
- [ ] Redactar el manual de operación técnica (*Runbook*) con pasos claros para resolución de fallas comunes.

### Entregable de la semana
- **Piloto operativo en Monterrey:** Tablero de operaciones activo con datos en tiempo real y primer reporte de faltantes generado con éxito.

---

## 📅 Semana 4: Expansión, Capacitación y Transferencia (*Handoff*)

### Objetivos
- Extender la sincronización a los almacenes de Guadalajara (GDL) y Ciudad de México (CDMX).
- Capacitar al personal operativo y al equipo de TI para garantizar autonomía.
- Transferir la cuenta formalmente al equipo de Customer Success de Nexo.

### Actividades
- [ ] Activar los flujos de sincronización para GDL y CDMX.
- [ ] Impartir sesión de capacitación práctica de 45 minutos a los supervisores de los 3 almacenes.
- [ ] Entregar el Runbook final a Roberto Treviño y verificar que su equipo sepa reiniciar el conector.
- [ ] Realizar la demostración ejecutiva final de resultados ante Don Javier Halcón (Director General).

### Entregable de la semana
- **Puesta en marcha productiva completa (*Go-Live*):** Sistema en producción operando en los 3 almacenes, acta de cierre firmada y transferencia a Customer Success.
