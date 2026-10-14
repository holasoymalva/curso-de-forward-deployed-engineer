# Caso de estudio del curso

Todos los módulos usan el mismo escenario para que el aprendizaje sea acumulativo y se parezca a una implementación real.

## 🏢 Tu empresa: Nexo

**Nexo** es una startup de software que vende una plataforma para **automatizar operaciones de inventario y pedidos** en empresas de distribución. La plataforma:

- Se conecta a los sistemas del cliente (ERP, hojas de cálculo, APIs de tiendas).
- Centraliza pedidos, inventario y productos en un solo lugar.
- Genera alertas (por ejemplo, "stock bajo") y reportes.
- Recientemente agregó un **asistente con IA** que responde preguntas sobre las operaciones.

Tú eres el o la **Forward Deployed Engineer** asignada a un cliente nuevo.

## 🚚 El cliente: Distribuidora Halcón

**Distribuidora Halcón** es una distribuidora de abarrotes con sede en Monterrey, Nuevo León.

| Dato | Valor |
|------|-------|
| Almacenes | 3: Monterrey (MTY), Guadalajara (GDL) y Ciudad de México (CDMX) |
| Productos | ~500 SKUs (abarrotes, bebidas, limpieza) |
| Clientes | ~1,200 tiendas de abarrotes y minisupers |
| Pedidos | ~800 al día |
| Sistemas actuales | ERP antiguo que exporta CSV cada noche, una API interna de pedidos, y muchas hojas de cálculo |

### Personas clave (stakeholders)

| Persona | Puesto | Lo que le importa |
|---------|--------|-------------------|
| **Laura Garza** | Directora de Operaciones (patrocinadora) | Reducir faltantes de inventario y pedidos tardíos. |
| **Roberto Treviño** | Gerente de TI | Seguridad, que no se rompa nada, poco trabajo extra para su equipo. |
| **Mariana López** | Analista de inventarios | Dejar de copiar y pegar datos entre hojas de cálculo. |
| **Don Javier Halcón** | Director General | El retorno de la inversión (ROI) y que el proyecto se entregue a tiempo. |

### El problema

- El inventario de los tres almacenes se consolida **a mano** en Excel cada mañana.
- Los datos del ERP llegan con **errores**: SKUs duplicados, fechas en distintos formatos, cantidades negativas.
- Se pierden ventas porque no se detecta a tiempo cuando un producto se va a agotar.
- El equipo de TI es pequeño (3 personas) y desconfía de herramientas externas.

### El objetivo del proyecto

> Conectar los sistemas de Distribuidora Halcón a la plataforma de Nexo en **8 semanas**, con alertas de stock bajo funcionando en los tres almacenes y un tablero de operaciones diario.

## 🧪 Recursos técnicos del caso

- [API simulada de Distribuidora Halcón](../api-simulada/README.md): expone productos, inventario y pedidos.
- Datos de ejemplo (CSV con errores intencionales): [`datos/`](datos/).

## Cómo se usa en el curso

| Módulo | Cómo aparece el caso |
|--------|----------------------|
| 00 | Conoces a Nexo y al cliente; analizas qué haría un FDE en la primera semana. |
| 02 | Procesas el CSV del ERP con Python. |
| 03 | Consumes la API de pedidos. |
| 04 | Limpias y consultas los datos con SQL. |
| 05 | Preparas y simulas la entrevista de descubrimiento con Laura y Roberto. |
| 06 | Construyes la integración robusta (autenticación, paginación, reintentos). |
| 07 | Empaquetas y despliegas la integración. |
| 08 | Resuelves un incidente en producción. |
| 09 | Revisas el manejo de datos personales de las tiendas. |
| 10 | Construyes un asistente que responde preguntas sobre el inventario. |
| 11 | Presentas una demo al Director General. |
| 12 | Ejecutas la implementación completa. |
