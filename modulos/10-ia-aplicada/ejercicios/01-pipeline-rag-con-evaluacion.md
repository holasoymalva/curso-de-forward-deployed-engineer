# Ejercicio 01: Pipeline RAG con evaluación cuantitativa

## 🎯 Objetivo

Aprender a medir la calidad de un sistema RAG empresarial mediante un conjunto de evaluación (*Eval Set*) cuantitativo, calculando la tasa de acierto de recuperación (*Retrieval Hit Rate*) y la fidelidad de las respuestas frente a hechos documentados.

---

## 🏢 Contexto del problema

Laura Garza, Directora de Operaciones de Distribuidora Halcón, necesita un asistente con IA que responda dudas frecuentes de los gerentes de tienda sobre:
1. Políticas de crédito y días de gracia.
2. Tiempos máximos de reporte para devoluciones y mermas.
3. Reglas de asignación entre los almacenes de Monterrey, Guadalajara y CDMX.

Antes de desplegar el asistente en los celulares de los gerentes, Laura exige una prueba documental que demuestre que el sistema no alucina y que responde con base estricta en las políticas autorizadas por Don Javier.

---

## 📝 Tareas a realizar

### Tarea 1: Definir el conjunto de evaluación (*Eval Set*)
Diseña un catálogo de al menos 5 casos de prueba que cubran:
* Consultas estándar con respuesta clara en la documentación.
* Consultas ambiguas o sinónimos ("merma", "podrido", "devolución").
* Consultas sobre información inexistente (p. ej., *"¿Venden refacciones de automóviles?"*), donde el sistema debe responder obligatoriamente que no cuenta con esa información sin inventar nada.

### Tarea 2: Extensión del motor RAG con evaluador
Implementa un script en Python que:
1. Cargue las políticas oficiales de Halcón en el motor RAG.
2. Ejecute cada pregunta del Eval Set de forma automatizada.
3. Compare los fragmentos recuperados contra las fuentes esperadas y evalúe si la respuesta contiene las palabras clave requeridas.
4. Genere una tabla resumen en consola con la tasa de acierto (*Accuracy %*).

---

## 🔍 Criterios de evaluación

* El evaluador debe ejecutarse sin errores utilizando Python estándar.
* Si el sistema no encuentra información en los documentos, debe rechazar la respuesta sin alucinar políticas inventadas.
* El reporte debe mostrar métricas legibles: preguntas evaluadas, aciertos, fallos y porcentaje global de precisión.
