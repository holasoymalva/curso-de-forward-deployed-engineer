# Ejercicio 01: Normalizador de catálogo de tiendas con PII

> **Nivel:** 🟢 Principiante · **Tiempo estimado:** 40 min

---

## Contexto

Distribuidora Halcón te entrega el archivo de clientes [`recursos/caso-de-estudio/datos/tiendas.csv`](../../../recursos/caso-de-estudio/datos/tiendas.csv). Este archivo contiene los datos de contacto de los tenderos para coordinar las entregas.

Sin embargo, el archivo tiene serios problemas de calidad:
- Teléfonos en formatos mezclados: unos vienen con guiones (`81-1234-9999`), otros con paréntesis y espacios (`(33) 4455 6677`) y otros en 10 dígitos limpios.
- Correos electrónicos con sintaxis rota (por ejemplo `lupita@ejemplo` sin dominio TLD) o vacíos.
- Tiendas duplicadas por `id_tienda` (la tienda `T0002` aparece dos veces idéntica).

---

## Lo que tienes que hacer

Escribe un script en Python llamado `normalizar_tiendas.py` que:

1. Lea el archivo `tiendas.csv` usando `csv.DictReader`.
2. **Deduplique por `id_tienda`:** Si una tienda ya fue procesada, omitirla o actualizar con el último registro.
3. **Estandarice el teléfono a exactamente 10 dígitos numéricos:** Eliminando paréntesis, guiones y espacios. Si el resultado no tiene 10 dígitos o está vacío, asignar el valor `"SIN_TELEFONO"`.
4. **Valide el correo electrónico con expresiones regulares (`re`):** Si no tiene un formato válido (como `usuario@dominio.com`), asignar `"CORREO_INVALIDO"`.
5. **Escriba un nuevo archivo CSV limpio:** `tiendas_limpias.csv` con los datos normalizados.

---

## Criterios de aceptación

- [ ] Corre sin dependencias externas usando Python 3.10+.
- [ ] La tienda duplicada `T0002` solo aparece una vez en el archivo final.
- [ ] Todos los teléfonos válidos quedan en formato numérico plano de 10 dígitos (ej. `8112345678`).
- [ ] Las anomalías en correos se detectan y registran adecuadamente.

---

🔑 [Ver solución](soluciones/01-normalizador-de-csv.md)
