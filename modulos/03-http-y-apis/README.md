# Módulo 03: HTTP y APIs

> **Nivel:** 🟢 Principiante  
> **Duración aproximada:** 5 horas  
> **Prerrequisitos:** [Módulo 02: Python para FDE](../02-python-para-fde/README.md)  

---

## 🎯 ¿Por qué importa para un FDE?

Las APIs (*Application Programming Interfaces*) son el sistema circulatorio del software moderno. Como Forward Deployed Engineer, más del 60 % de tus implementaciones consistirán en conectar la plataforma de tu empresa con APIs de clientes, ERPs en la nube, pasarelas de pago o proveedores logísticos.

Dominar el protocolo HTTP a bajo nivel (métodos, códigos de estado, encabezados de autenticación y serialización JSON) te permite diagnosticar de inmediato por qué una petición es rechazada, entender la documentación técnica de cualquier proveedor y escribir clientes confiables desde Python.

---

## ✅ Objetivos de aprendizaje

Al terminar este módulo podrás:

- Explicar el ciclo de petición y respuesta en el modelo cliente-servidor y el funcionamiento de HTTP/HTTPS.
- Identificar y usar con precisión los métodos HTTP (`GET`, `POST`, `PUT`, `DELETE`) y los códigos de estado más comunes (`200`, `201`, `400`, `401`, `404`, `422`, `429`, `503`).
- Comprender los principios de una arquitectura REST y cómo leer especificaciones de APIs.
- Consumir APIs REST seguras desde Python utilizando `urllib.request` de la biblioteca estándar (y conocer la alternativa popular `requests`).
- Autenticarte mediante tokens Bearer contra la [API simulada](../../recursos/api-simulada/README.md) de Distribuidora Halcón.

---

## 📖 Lecciones

| # | Lección | Nivel | Duración |
|---|---------|-------|----------|
| 01 | [Cómo funciona la Web: Modelo cliente-servidor y HTTP](lecciones/01-como-funciona-la-web-y-http.md) | 🟢 | 20 min |
| 02 | [Anatomía de una petición y respuesta HTTP](lecciones/02-anatomia-de-peticion-y-respuesta.md) | 🟢 | 25 min |
| 03 | [Arquitectura REST y lectura de documentación](lecciones/03-principios-rest-y-diseno-de-apis.md) | 🟢 | 25 min |
| 04 | [Consumir APIs desde Python sin dependencias](lecciones/04-consumir-apis-desde-python.md) | 🟢 | 30 min |

---

## 💻 Ejemplos

Scripts listos para interactuar con la API simulada del curso:
- Consulta [ejemplos/README.md](ejemplos/README.md).
  - [Cliente base en Python (`cliente_api_basico.py`)](ejemplos/cliente_api_basico.py)
  - [Pruebas rápidas de endpoints en Bash (`probar_endpoints.sh`)](ejemplos/probar_endpoints.sh)

---

## 🏋️ Ejercicios

Prácticas contra la API simulada de Distribuidora Halcón:
- Consulta [ejercicios/README.md](ejercicios/README.md).
  - [Ejercicio 01: Consultor de pedidos pendientes por almacén](ejercicios/01-consultor-de-pedidos-pendientes.md)
  - [Ejercicio 02: Creador de pedidos con validación de SKUs](ejercicios/02-creador-de-pedidos-con-validacion.md)

---

## 🎥 Guion sugerido para video

1. **Gancho (1-2 min):** *"El cliente te dice: 'Les mandé el pedido por la API pero no aparece'. Haces una prueba y recibes un código 422 con un JSON que dice 'sku desconocido'. En 10 segundos sabes que el problema no es tu servidor, sino que el cliente intentó pedir un producto que ya no existe en su propio catálogo."*
2. **Concepto (5-8 min):** Petición y respuesta HTTP: Método + URL + Headers + Body. La diferencia entre errores 4xx (culpa del cliente) y 5xx (culpa del servidor).
3. **Demo (6-8 min):** Ejecutar `cliente_api_basico.py` contra la API simulada, obteniendo el token y listando productos.
4. **Cierre (1-2 min):** Resumen de buenas prácticas con `urllib` vs `requests` y presentación del reto del Ejercicio 01.

---

## 📚 Para profundizar

- [MDN Web Docs: Guías HTTP (Mozilla)](../../recursos/lecturas.md#🌐-http-apis-y-arquitectura-de-integración).
- [Documentación de la API simulada](../../recursos/api-simulada/README.md).

---

⬅️ [Módulo 02: Python para FDE](../02-python-para-fde/README.md) | 🏠 [Índice](../../README.md) | [Módulo 04: Datos y SQL](../04-datos-y-sql/README.md) ➡️
