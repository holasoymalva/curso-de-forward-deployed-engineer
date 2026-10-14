# 📑 Documento de síntesis de descubrimiento técnico

**Cliente:** Distribuidora Halcón  
**Elaborado por:** Alex Morales (FDE - Nexo)  
**Fecha:** 14 de Octubre de 2026  
**Versión:** 1.0 (Aprobado)  

---

## 1. Resumen Ejecutivo del Problema

Distribuidora Halcón pierde recurrentemente ventas y fidelidad de clientes (más de \$80,000 MXN en un solo fin de semana) debido al desfase de información entre las existencias físicas en sus 3 almacenes y los pedidos despachados. El proceso actual de consolidación depende de una analista que procesa datos manualmente en Excel durante 3 a 4 horas matutinas, provocando que las alertas de desabasto lleguen horas después de que los camiones han salido a ruta.

---

## 2. Diagnóstico Técnico del Estado Actual (*As-Is*)

| Componente | Hallazgo Técnico | Riesgo Detectado |
|------------|------------------|------------------|
| **ERP Central** | Windows Server heredado, sin APIs REST nativas. Solo lectura permitida. | Imposibilidad de consultar stock en tiempo real mediante webhook directo. |
| **Exportación CSV** | Tarea programada a las 3:00 AM que genera `inventario_erp.csv`. | Formatos de fecha mixtos, SKUs con espacios accidentales, precios con comas y registros duplicados. |
| **API de Pedidos** | Servicio HTTP REST interno con autenticación Bearer (`/auth/token`). | Requiere reintentos automáticos y tokens temporales con expiración. |
| **Restricciones de TI** | Equipo de 3 personas; cero tolerancia a sobrecarga de servidores o instalación de software global. | La solución debe ejecutarse en un contenedor Docker con límite estricto de memoria (máx. 256 MB) y solo lectura de archivos. |

---

## 3. Arquitectura Propuesta (*To-Be*)

1. **Worker de Sincronización en Docker:**
   - Desplegado en VM de pruebas provista por Roberto Treviño.
   - Activación automática por cron a las 03:15 AM (15 minutos después de la exportación del ERP).
2. **Sanitización y Base de Datos Local:**
   - Módulo en Python estándar que filtra duplicados y corrige anomalías de formato.
   - Carga transaccional en SQLite local (`halcon.db`) con tabla de auditoría de rechazos.
3. **Generación de Alertas y Tablero Nexo:**
   - Cálculo automático de productos con `cantidad <= stock_minimo`.
   - Publicación de alertas en el tablero de operaciones antes de las 04:30 AM.
   - Disponibilidad garantizada para los supervisores antes del inicio de turno de las 06:00 AM.

---

## 4. Matriz de Stakeholders y Plan de Alineación

- **Laura Garza (Operaciones):** Foco en cumplimiento de entrega antes de las 6:00 AM y reporte de faltantes.
- **Roberto Treviño (TI):** Foco en mínimo privilegio, aislamiento en Docker y reporte de consumo de recursos.
- **Mariana López (Analista):** Acompañamiento en la semana 2 para validar las alertas contra su rutina diaria y eliminar el trabajo repetitivo en Excel.
