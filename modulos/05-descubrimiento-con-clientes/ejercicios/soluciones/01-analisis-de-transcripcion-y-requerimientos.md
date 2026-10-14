# Solución al Ejercicio 01: Detección de requerimientos ocultos y riesgos

---

## 📋 1. Clasificación de Requerimientos

### Requerimientos Funcionales (Lo que el sistema debe hacer)
1. **Extracción y limpieza de inventario:** El sistema debe ingerir diariamente el archivo `inventario_erp.csv`, normalizar formatos de fecha y precio, eliminar SKUs duplicados y descartar almacenes no reconocidos.
2. **Generación de alertas de stock mínimo:** El sistema debe contrastar las existencias físicas de cada SKU contra su valor de `stock_minimo` y emitir una alerta destacada para cualquier producto con déficit de inventario.
3. **Consulta de pedidos pendientes:** El sistema debe conectarse a la API interna de pedidos de Halcón para consultar las órdenes en estado `pendiente` asignadas a cada almacén.

### Requerimientos No Funcionales (Restricciones y estándares técnicos)
1. **Ventana de tiempo y disponibilidad:** El pipeline completo de sincronización y generación de alertas debe concluir antes de las **06:00 AM** para estar disponible al arranque del turno operativo.
2. **Aislamiento y consumo de recursos:** El conector debe ejecutarse encapsulado en un contenedor Docker en una máquina virtual de pruebas, con un límite máximo de **256 MB de memoria RAM** y bajo uso de CPU para no impactar la infraestructura de TI.
3. **Mínimo privilegio de acceso:** La integración únicamente tendrá permisos de **solo lectura** sobre la carpeta compartida donde se deposita el CSV del ERP, sin acceso de escritura ni conexión directa a la base de datos de producción.

---

## 🧠 2. Análisis de Stakeholders

- **Roberto Treviño (TI):** Su principal temor es la saturación de servidores y la pérdida de control técnico. No quiere que un software externo tire el ERP heredado ni que su pequeño equipo de 3 personas deba atender guardias nocturnas. Exigirá ver los límites del contenedor Docker, la ausencia de librerías globales y los logs de consumo antes de dar el visto bueno final.
- **Laura Garza (Operaciones):** Busca recuperar el control de sus métricas de entrega, eliminar los \$80,000 pesos semanales en cancelaciones y consolidar su liderazgo operativo ante Don Javier Halcón demostrando que modernizó las operaciones en tiempo récord.

---

## ⚠️ 3. Riesgos no mencionados en la llamada

- **Retraso o bloqueo en la exportación nocturna del ERP:** ¿Qué sucede si a las 3:00 AM el ERP se congela o realiza un respaldo pesado y el archivo `inventario_erp.csv` no aparece a las 3:15 AM? Si el script asume ciegamente que el archivo siempre está ahí, fallará silenciosamente. El conector debe implementar un mecanismo de sondeo con espera prudencial (*polling con timeout*) y alertar a TI si el archivo no ha sido generado antes de las 4:00 AM.
