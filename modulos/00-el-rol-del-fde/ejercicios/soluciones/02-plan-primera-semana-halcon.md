# Solución al Ejercicio 02: Plan de trabajo para la primera semana con Halcón

---

## 🎯 1. Objetivo central de la semana

> **Entregar el viernes a las 3:00 PM una demostración en vivo con datos reales del almacén Monterrey procesados de forma automática, mostrando las primeras 3 alertas de stock bajo generadas sin intervención manual, habiendo asegurado la tranquilidad técnica de TI.**

---

## 📅 2. Distribución diaria de actividades

### Lunes: Alineación de expectativas y empatía
- **10:00 AM | Kickoff conjunto (Laura Garza y Roberto Treviño):**
  - Presentar el rol de FDE como facilitador técnico.
  - Alinear que la meta de la semana es validar la extracción de datos sin tocar la base de producción.
- **2:00 PM | Sesión de escucha con Mariana López (Analista de Inventarios):**
  - Observar cómo abre el Excel, cómo busca los productos y cómo redacta sus mensajes de WhatsApp. Tomar notas de las fórmulas que usa para calcular faltantes.
- **4:00 PM | Análisis técnico de datos:**
  - Inspeccionar el archivo `inventario_erp.csv` y documentar las 6 categorías de errores detectados (SKUs duplicados, comas en precios, fechas mixtas).

---

### Martes: Seguridad y arquitectura con TI
- **10:00 AM | Sesión de arquitectura con Roberto Treviño:**
  - Mostrarle el diagrama de cómo correrá el script: solo lectura, una vez por noche a las 3:00 AM, con límite estricto de memoria y tasa de peticiones (*rate limiting*).
  - Solicitar un usuario de prueba con permisos de solo lectura para la API y acordar entrega de llaves.
- **1:00 PM - 5:00 PM | Programación:**
  - Desarrollar el script inicial en Python que lee el CSV, sanitiza formatos y filtra las filas corruptas sin abortar el proceso.

---

### Miércoles: Prototipo funcional y alivio operativo
- **09:00 AM - 1:00 PM | Conexión con SQLite:**
  - Crear la base de datos local y cargar los datos limpios de Monterrey.
  - Escribir la consulta SQL para identificar productos con cantidad menor al `stock_minimo`.
- **3:00 PM | Mini-sesión de 15 minutos con Mariana López:**
  - Mostrarle el primer reporte generado automáticamente en formato legible.
  - Validar si los 4 productos marcados como "críticos" coinciden con su lista manual matutina. ¡Victoria temprana de empatía!

---

### Jueves: Pruebas de resiliencia y documentación
- **10:00 AM | Pruebas contra la API simulada:**
  - Probar la autenticación con token Bearer y validar que el script soporte caídas transitorias de red usando reintentos.
- **2:00 PM | Redacción del resumen de descubrimiento:**
  - Elaborar el borrador del Documento de Alcance (SOW ligero) y preparar el guion de la demo de mañana.

---

### Viernes: Demostración ejecutiva y reporte semanal
- **11:00 AM | Demostración ejecutiva (Laura Garza y Roberto Treviño):**
  - Mostrar el flujo completo: CSV del ERP -> Limpieza en Python -> Consulta SQL -> Alerta visual de stock bajo.
  - Demostrar a Roberto que la ejecución tomó 1.2 segundos y no saturó recursos.
- **3:00 PM | Envío del reporte semanal formal:**
  - Correo electrónico con resumen ejecutivo de logros, métricas alcanzadas y los próximos pasos acordados para la semana 2.

---

## 🛡️ 3. Mapeo de riesgos y mitigaciones

| Riesgo detectado | Probabilidad / Impacto | Estrategia de mitigación preventiva |
|------------------|------------------------|-------------------------------------|
| Roberto Treviño demora la entrega de accesos a la API por dudas de seguridad. | Alta / Alto | Utilizar la exportación CSV local y la API simulada durante los primeros 3 días para avanzar sin depender de sus credenciales. |
| Mariana siente que la nueva plataforma viene a sustituir su puesto de trabajo. | Media / Alto | Involucrarla desde el día 1 como co-diseñadora de las alertas, enfatizando que la herramienta eliminará el trabajo tedioso para que ella pueda enfocarse en compras estratégicas. |

---

## 🏆 4. Criterio de éxito al viernes

Al concluir la llamada del viernes:
1. Laura confirma que las alertas generadas coinciden con la realidad del almacén Monterrey.
2. Roberto manifiesta tranquilidad con el consumo de recursos y autoriza el pase a la semana 2.
3. El FDE tiene el código versionado en Git y listo para comenzar la automatización formal.
