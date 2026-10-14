# Ejercicio 01: Consultor de pedidos pendientes por almacén

> **Nivel:** 🟢 Principiante · **Tiempo estimado:** 35 min

---

## Contexto

Laura Garza necesita saber cuántos pedidos se encuentran actualmente en estado `pendiente` en el almacén de Monterrey (`MTY`) para dimensionar el personal de turno de la tarde. 

La API de pedidos devuelve los resultados paginados (por defecto 20 por página). Si solo consultas la primera página, Laura tomará decisiones con datos incompletos.

---

## Lo que tienes que hacer

Escribe un script en Python llamado `consultar_pendientes.py` que:

1. Se autentique contra el endpoint `/auth/token` usando `client_id="nexo-demo"` y `client_secret="secreto-de-practica"`.
2. Consulte los pedidos filtrando por `estado=pendiente` y `almacen=MTY`.
3. **Maneje la paginación:** Si el campo `siguiente_pagina` no es `None`, consulte las páginas subsecuentes hasta acumular la totalidad de los pedidos pendientes.
4. **Imprima un resumen en consola:**
   - Total de pedidos pendientes encontrados en MTY.
   - Lista detallada mostrando: ID de pedido, nombre de la tienda y cantidad total de artículos solicitados en las líneas.

---

## Criterios de aceptación

- [ ] Implementado con `urllib.request` y `json` nativos.
- [ ] Recorre todas las páginas hasta agotar los resultados (`siguiente_pagina` es `None`).
- [ ] Suma correctamente las cantidades de las líneas de cada pedido.
- [ ] Maneja de forma limpia posibles errores de conexión informando al usuario.

---

🔑 [Ver solución](soluciones/01-consultor-de-pedidos-pendientes.py)
