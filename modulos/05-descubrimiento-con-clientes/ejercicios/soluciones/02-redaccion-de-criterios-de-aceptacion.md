# Solución al Ejercicio 02: Redacción de criterios de aceptación y SOW

---

## 🚫 1. Exclusiones Explícitas (*Out of Scope*) para Fase 1

1. **Modificaciones al ERP:** No se modificará el código fuente, la estructura de base de datos ni los procesos internos del ERP heredado de Halcón.
2. **Facturación Fiscal:** Queda excluida cualquier integración con el Servicio de Administración Tributaria (SAT) o generación de timbrado CFDI.
3. **Módulos para choferes y clientes finales:** No incluye el desarrollo de aplicaciones móviles, portales de rastreo para choferes ni notificaciones masivas por correo o SMS para las tiendas.
4. **Carga histórica masiva:** No se procesarán ni depurarán archivos de inventario anteriores a la fecha de inicio del proyecto (octubre de 2026).

---

## ✅ 2. Criterios de Aceptación Objetivos

- [ ] **Criterio 1 (Velocidad de carga):** El pipeline ETL procesa el archivo nocturno completo (hasta 1,000 registros de catálogo e inventario) en menos de **30 segundos** en la máquina virtual asignada.
- [ ] **Criterio 2 (Auditoría de datos):** El 100 % de los registros que presenten campos corruptos (cantidades negativas, textos nulos o almacenes desconocidos) se almacenan en la tabla `auditoria_rechazos` indicando número de línea y causa del descarte, sin interrumpir la carga de las filas válidas.
- [ ] **Criterio 3 (Ventana de disponibilidad):** Las alertas de existencias críticas se encuentran publicadas en la base de datos y disponibles para visualización en el tablero de Nexo antes de las **04:30 AM** durante al menos 5 días hábiles consecutivos de prueba piloto.
- [ ] **Criterio 4 (Restricción de recursos):** El contenedor Docker en ejecución no supera en ningún momento un consumo de **200 MB de memoria RAM** ni el **15 % de CPU** de la máquina virtual anfitriona.

---

## ✉️ 3. Correo de respuesta a Laura Garza ("Decir no con alternativa")

**Asunto:** Re: Notificaciones por correo a tiendas sobre pedidos enviados  
**De:** Alex Morales (FDE - Nexo)  
**Para:** Laura Garza (Directora de Operaciones - Distribuidora Halcón)  
**CC:** Roberto Treviño (Gerente de TI)  

Hola Laura,

Me parece una iniciativa extraordinaria para mejorar la experiencia de servicio con las tiendas abarroteras. Definitivamente es el tipo de automatización de alto valor que Nexo puede potenciar en una etapa posterior.

Para ser completamente transparente contigo y cuidar nuestro compromiso de tener el tablero de inventario y las alertas operativas listas para el turno de las 6:00 AM este mismo viernes, sugiero que mantengamos el foco actual:
1. Si introducimos ahora un servicio de envíos masivos de correo para 1,200 destinatarios, tendríamos que configurar servidores SMTP seguros, validar políticas antispam y gestionar rebotes de correos con el equipo de TI, lo cual retrasaría la salida en vivo de Monterrey al menos 2 semanas.
2. Te propongo que anotemos este módulo de notificaciones a clientes como la **Prioridad Número 1 de la Fase 2**, la cual podremos iniciar formalmente en cuanto validemos la estabilidad de las alertas de inventario la próxima semana.

¿Te parece bien si mantenemos el plan de pruebas de inventario para este viernes y revisamos la propuesta técnica de los correos el próximo lunes?

¡Muchas gracias por tu liderazgo e ideas!

Saludos cordiales,  
**Alex Morales**  
Forward Deployed Engineer · Nexo
