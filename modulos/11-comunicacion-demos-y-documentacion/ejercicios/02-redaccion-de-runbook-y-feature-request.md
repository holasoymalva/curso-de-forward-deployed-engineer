# Ejercicio 02: Redacción de Runbook de emergencia y Feature Request

## 🎯 Objetivo

Practicar la redacción de documentación operativa crítica (Runbook) ante incidentes de degradación de red y formular una solicitud de funcionalidad técnica (Feature Request) dirigida al equipo central de producto.

---

## 🏢 Contexto del problema

Durante la tercera semana del piloto con Distribuidora Halcón se presentaron dos situaciones que requieren documentación formal:

1. **Incidente de conectividad de fin de semana:** La conexión de fibra óptica del Almacén Guadalajara experimentó micro-cortes continuos entre las 01:00 y las 04:00 AM, provocando que el contenedor de sincronización fallara repetidamente y el operador de guardia no supiera cómo verificar el estado de los lotes pendientes ni cómo forzar la reanudación manual.
2. **Necesidad de soporte multi-almacén en la API central:** Actualmente, para consultar el inventario de los tres almacenes (MTY, GDL, CDMX), el conector debe hacer 3 llamadas separadas porque la API de Nexo no acepta un filtro combinado de almacenes (`almacenes=MTY,GDL,CDMX`).

---

## 📝 Tareas a realizar

### Tarea 1: Redacción de sección de contingencia en el Runbook
Elabora un anexo para el Runbook de producción titulado:  
`Procedimiento de Recuperación de Lotes ante Degradación de Enlace WAN`.  
Debe incluir:
* Síntoma visible en consola y código HTTP de alerta.
* Comando para inspeccionar en la base de datos SQLite local qué registros quedaron en estado `PENDIENTE`.
* Comando de recuperación manual para procesar exclusivamente los registros no confirmados sin duplicar los ya sincronizados.
* Verificación final de integridad de datos.

### Tarea 2: Redacción de Feature Request a Producto
Redacta la solicitud formal de funcionalidad para el equipo de desarrollo de la plataforma Nexo:
* **Título conciso y código identificador.**
* **Contexto de cliente y volumen transaccional.**
* **Definición del dolor operativo (*Pain Point*):** Costo en tiempo y conexiones simultáneas.
* **Propuesta técnica de API:** Especificación del endpoint o parámetro sugerido con ejemplos de petición y respuesta en formato JSON.
* **Criterios de aceptación (Definition of Done) para el equipo de ingeniería.**

---

## 🔍 Criterios de evaluación

* El Runbook debe contener comandos reproducibles listos para terminal de Linux.
* El Feature Request debe justificar claramente el valor para el negocio y el retorno de inversión para la plataforma.
