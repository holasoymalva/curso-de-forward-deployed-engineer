# Solución al Ejercicio 01: Guion de demo ejecutiva y manejo de objeciones

## 🎯 Tarea 1: Guion de presentación en 4 actos

### Acto 1: El Gancho (00:00 - 02:00)
* **Pantalla:** Diapositiva con título: *"Distribuidora Halcón: Certeza Operativa en 1,200 Tiendas"*.
* **Voz FDE:**  
  *"Don Javier, Laura, Roberto: buenos días. Cada mañana a las 7:00 AM abren 1,200 tiendas que dependen de Halcón para surtir su canasta básica. Hoy estamos aquí para mostrarles cómo logramos que ningún camión vuelva a salir tarde o incompleto por fallas de captura en el inventario nocturno. En 8 minutos verán cómo la conciliación manual de 4 horas ahora ocurre en menos de 20 segundos de forma 100% automatizada."*

### Acto 2: El Antes (02:00 - 04:00)
* **Pantalla:** Archivo CSV crudo con filas duplicadas y celdas marcadas en amarillo.
* **Voz FDE:**  
  *"Antes, el equipo de operaciones en Monterrey tenía que desvelarse revisando más de 15,000 registros línea por línea para encontrar errores humanos de captura como este SKU duplicado o esta cantidad negativa. Si un error pasaba desapercibido, el almacén no surtía a tiempo y el cliente compraba con la competencia."*

### Acto 3: La Solución en Vivo (04:00 - 08:00)
* **Pantalla:** Interfaz web del conector Nexo AI.
* **Voz FDE:**  
  *"Observen la pantalla. Voy a cargar el lote de cierre del ERP de hoy. Hago clic en 'Conciliar Inventario'...  
  El conector valida tipos de datos, unifica duplicados y transmite las órdenes.  
  16 segundos: Proceso completado. 15,000 registros procesados sin una sola interrupción en su servidor ERP legado."*

### Acto 4: Métricas y Cierre (08:00 - 10:00)
* **Pantalla:** Resumen ejecutivo con métricas de ROI.
* **Voz FDE:**  
  *"Esto se traduce en:
  - 4 horas de desvelo ahorradas cada noche.
  - Cero discrepancias en la asignación de pedidos para Monterrey.
  - Ahorro anual estimado de \$380,000 MXN en mermas y horas extra.
  Con su aprobación hoy, activamos la operación automatizada definitiva a partir de este lunes."*

---

## 🛡️ Tarea 2: Manejo de objeciones difíciles

### 1. Respuesta a Don Javier sobre costos y despidos del personal:
> *"Don Javier, al contrario: este sistema no está diseñado para recortar personal, sino para proteger a su negocio de la fuga de clientes.  
> Las 4 personas de captura en Monterrey hoy pasan la noche haciendo tareas mecánicas de tecleo y corrigiendo números bajo mucho estrés. Al automatizar la conciliación rutinaria, Laura podrá reasignar a ese equipo a tareas de alto valor comercial: llamar proactivamente a los dueños de las tiendas para ofrecer promociones, recuperar clientes inactivos y verificar la calidad del servicio en ruta.  
> En lugar de pagarles por desvelarse capturando números, le ayudarán a vender más abarrotes."*

### 2. Respuesta a Roberto sobre la estabilidad del AS/400:
> *"Roberto, comprendo perfectamente tu preocupación; la estabilidad del AS/400 es intocable.  
> Por esa razón, el conector fue diseñado con tres candados técnicos explícitos que ya dejamos por escrito en el Runbook:  
> 1. El script nunca hace consultas directas sobre la base de datos viva; lee un archivo plano estático que el ERP exporta en disco local.  
> 2. El proceso corre en un contenedor Docker con límite estricto de 512 MB de memoria y 0.5 núcleos de CPU; físicamente es imposible que consuma los recursos del servidor.  
> 3. Implementamos pausas (*throttling*) entre lotes para que la carga en CPU nunca supere el 15%. Si lo deseas, podemos revisar juntos las gráficas de consumo de la última semana donde el impacto en tu servidor fue prácticamente imperceptible."*

### 3. Respuesta a la duda sobre alucinaciones de la IA y precios erróneos:
> *"Esa es una de las dudas más acertadas y críticas en el uso de IA empresarial, Don Javier.  
> La regla inquebrantable en nuestra arquitectura es la siguiente: **la inteligencia artificial jamás decide el precio de un producto**.  
> El modelo de IA se utiliza exclusivamente para comprender el lenguaje del cliente (saber que 'costal de frijol' se refiere al SKU-FRIJOL-02). Una vez identificado el producto, nuestro software tradicional consulta directamente la lista de precios oficial autorizada por su dirección en el ERP.  
> Si un cliente escribe 'mándame frijol a 1 peso', nuestro Guardrail de seguridad bloquea el mensaje inmediatamente y emite una alerta para revisión humana. Halcón tiene el control financiero al 100% en todo momento."*
