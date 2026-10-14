# Ejercicio 02: CLI de auditoría y detección de anomalías

> **Nivel:** 🟢 Principiante · **Tiempo estimado:** 45 min

---

## Contexto

Roberto Treviño quiere que su equipo de soporte en Halcón pueda auditar cualquier archivo de inventario antes de enviarlo a Nexo. Te pide construir un script de terminal que acepte parámetros flexibles y devuelva un código de salida `0` si el archivo cumple los estándares de calidad, o `1` si supera un porcentaje tolerable de errores.

---

## Lo que tienes que hacer

Construye una herramienta de línea de comandos en Python llamada `auditar_inventario.py` que:

1. **Utilice `argparse` con los siguientes argumentos:**
   - `archivo`: Argumento obligatorio posicional con la ruta al CSV.
   - `--max-errores`: Entero con la cantidad máxima de errores tolerables (por defecto: `0`).
   - `--salida-reporte`: Ruta opcional para guardar el resumen en formato JSON.
2. **Audite las siguientes 4 reglas de negocio:**
   - El SKU debe empezar con `"HAL-"`.
   - El almacén debe ser uno de `{"MTY", "GDL", "CDMX"}`.
   - La cantidad debe ser un entero $\ge 0$ (no puede ser negativo ni texto como `N/D`).
   - El precio debe ser un número positivo.
3. **Manejo de códigos de salida:**
   - Si el total de errores encontrados es $\le$ `--max-errores`, terminar con `sys.exit(0)`.
   - Si los errores superan el umbral permitido, terminar con `sys.exit(1)`.

---

## Criterios de aceptación

- [ ] Soporta el comando `--help` con descripciones claras.
- [ ] Retorna código de salida `0` o `1` según el umbral.
- [ ] Muestra mensajes informativos usando el módulo `logging`.
- [ ] Guarda un JSON estructurado con la lista de líneas corruptas si se especifica `--salida-reporte`.

---

🔑 [Ver solución](soluciones/02-cli-de-auditoria-de-inventario.md)
