# Ejercicio 01: Automatización con Bash y análisis de archivos

> **Nivel:** 🟢 Principiante · **Tiempo estimado:** 30 min

---

## Contexto

Cada noche a las 3:00 AM, el ERP de Distribuidora Halcón deposita el archivo `inventario_erp.csv` en una carpeta del servidor. Antes de que el conector de Python intente procesarlo, Roberto Treviño te pide un script en Bash ultra rápido que verifique si el archivo existe, cuente los registros y detecte anomalías visibles de inmediato.

---

## Lo que tienes que hacer

Escribe un script en Bash llamado `analizar_csv.sh` que reciba como argumento la ruta de un archivo CSV y realice lo siguiente:

1. **Validación de existencia:** Si el archivo no se pasa como argumento o no existe en el disco, imprimir un mensaje de error claro y salir con código de salida `1` (`exit 1`).
2. **Conteo de registros:** Imprimir el número total de líneas del archivo excluyendo la cabecera (es decir, el total de registros de datos).
3. **Detección de productos de limpieza:** Filtrar e imprimir cuántas filas pertenecen a la categoría `limpieza` (sin importar si está en mayúsculas o minúsculas).
4. **Búsqueda de anomalías:** Buscar si existe alguna fila con cantidad negativa (que contenga `-` antes de un número) o si existe la palabra `N/D` en la columna de cantidades.

---

## Criterios de aceptación

- [ ] El script es ejecutable con `bash analizar_csv.sh recursos/caso-de-estudio/datos/inventario_erp.csv`.
- [ ] Informa si el archivo no existe sin generar errores confusos de Bash.
- [ ] Imprime el conteo exacto de registros de datos.
- [ ] Detecta correctamente las filas con cantidades negativas o `N/D`.

## Pistas

<details>
<summary>Pista 1</summary>

Puedes comprobar si un archivo existe usando `if [ ! -f "$1" ]; then`.

</details>

<details>
<summary>Pista 2</summary>

Para ignorar mayúsculas y minúsculas en `grep`, usa la bandera `-i`. Para contar coincidencias, usa `grep -c`.

</details>

---

🔑 [Ver solución](soluciones/01-automatizacion-con-bash.md)
