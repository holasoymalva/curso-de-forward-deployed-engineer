# Ejercicio 01: Auditor automatizado de fugas de PII

## 🎯 Objetivo

Construir un script en Python (biblioteca estándar) que audite archivos de texto plano, CSVs o archivos de logs para detectar automáticamente la presencia de Información de Identificación Personal (PII) no enmascarada, emitiendo un reporte con las líneas y el tipo de dato sensible detectado.

---

## 🏢 Contexto del problema

Durante una revisión de seguridad interna previa al lanzamiento con Distribuidora Halcón, el líder de seguridad te solicita verificar que ningún archivo generado en el pipeline de sincronización exponga PII de clientes o empleados en texto claro.

Para automatizar esta verificación en el pipeline de CI/CD, debes crear un script CLI llamado `auditor_pii.py`.

---

## 📝 Requisitos del script

El script debe recibir como argumento la ruta de un archivo de texto o log y buscar mediante expresiones regulares (`re`):
1. **Correos electrónicos personales o corporativos:** Formato estándar `usuario@dominio.com`.
2. **Números telefónicos en México:** Formatos comunes de 10 dígitos:
   * Directo: `8112345678`, `5511122233`
   * Con guiones o espacios: `81-1234-9999`, `(33) 4455 6677`
3. **RFC mexicanos (Registro Federal de Contribuyentes):**
   * Personas físicas (4 letras + 6 números + 3 homoclave opcional)
   * Personas morales (3 letras + 6 números + 3 homoclave opcional)
   * Ejemplo: `MOMA850101XYZ` o `DHA980415AB1`
4. **Números de tarjetas de crédito:** Bloques de 16 dígitos separados por guiones o espacios (`4111-2222-3333-4444`).

### Formato del reporte en consola:
El script debe imprimir un resumen:
* Número total de líneas analizadas.
* Lista de infracciones encontradas (número de línea, tipo de PII y fragmento enmascarado para no re-exponerlo en el reporte).
* Código de salida (*exit code*): `0` si el archivo está limpio; `1` si se detectaron fugas de PII.

---

## 🧪 Datos de prueba

Prueba tu script contra el archivo crudo:
`recursos/caso-de-estudio/datos/tiendas.csv` (debe detectar múltiples infracciones).
Y luego contra el archivo sanitizado:
`modulos/09-seguridad-y-datos-del-cliente/ejemplos/tiendas_sanitizadas.csv` (debe pasar con 0 infracciones).
