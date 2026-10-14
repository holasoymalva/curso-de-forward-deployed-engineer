# Módulo 05: Descubrimiento con clientes

> **Nivel:** 🟢 Principiante  
> **Duración aproximada:** 4 horas  
> **Prerrequisitos:** [Módulo 00: El rol del Forward Deployed Engineer](../00-el-rol-del-fde/README.md)  

---

## 🎯 ¿Por qué importa para un FDE?

El error más costoso en la ingeniería de software no es un punto y coma faltante ni una consulta SQL lenta: es **construir con meses de esfuerzo la solución equivocada para un problema mal entendido**.

La fase de **Descubrimiento Técnico** (*Technical Discovery*) es el momento en el que el FDE investiga los procesos de negocio reales del cliente, comprende qué motiva o preocupa a cada involucrado (*stakeholders*), traduce dolores operativos vagos en requerimientos técnicos concretos y delimita con precisión el alcance del proyecto (*Scope*) para evitar sorpresas y retrasos.

---

## ✅ Objetivos de aprendizaje

Al terminar este módulo podrás:

- Planificar y conducir entrevistas de descubrimiento técnico usando preguntas abiertas y técnicas de escucha activa (*The Mom Test*).
- Mapear a los distintos *stakeholders* de una organización (patrocinador ejecutivo, líder de TI, usuario operativo) y alinear la solución con sus incentivos individuales.
- Modelar flujos de trabajo en diagramas visuales comparando el estado actual (*As-Is*) contra el estado futuro deseado (*To-Be*).
- Redactar un **Documento de Alcance (SOW ligero)** que establezca entregables verificables, límites de alcance claros (*Out of Scope*) y criterios de éxito medibles.
- Identificar y documentar riesgos técnicos, supuestos y dependencias antes de escribir código.

---

## 📖 Lecciones

| # | Lección | Nivel | Duración |
|---|---------|-------|----------|
| 01 | [El arte del descubrimiento técnico y escucha activa](lecciones/01-el-arte-del-descubrimiento-tecnico.md) | 🟢 | 25 min |
| 02 | [Mapeo de stakeholders e incentivos ocultos](lecciones/02-identificar-stakeholders-e-incentivos.md) | 🟢 | 25 min |
| 03 | [Mapeo de procesos: De 'As-Is' a 'To-Be'](lecciones/03-mapeo-de-procesos-as-is-y-to-be.md) | 🟢 | 25 min |
| 04 | [El Documento de Alcance (SOW) y criterios de éxito](lecciones/04-documento-de-alcance-sow-y-criterios-de-exito.md) | 🟢 | 25 min |

---

## 💻 Ejemplos

Documentos modelo y casos prácticos de referencia:
- Consulta [ejemplos/README.md](ejemplos/README.md).
  - [Transcripción real de llamada de descubrimiento con Halcón](ejemplos/transcripcion_entrevista_halcon.md)
  - [Documento de síntesis de descubrimiento técnico](ejemplos/documento_descubrimiento_halcon.md)
  - [Plantilla editable de SOW ligero para implementaciones](ejemplos/plantilla_sow_ligero.md)

---

## 🏋️ Ejercicios

Casos de análisis basados en la transcripción de Distribuidora Halcón:
- Consulta [ejercicios/README.md](ejercicios/README.md).
  - [Ejercicio 01: Detección de requerimientos ocultos y riesgos](ejercicios/01-analisis-de-transcripcion-y-requerimientos.md)
  - [Ejercicio 02: Redacción de criterios de aceptación y SOW](ejercicios/02-redaccion-de-criterios-de-aceptacion.md)

---

## 🎥 Guion sugerido para video

1. **Gancho (1-2 min):** *"El cliente te dice en la primera llamada: 'Solo queremos conectar el ERP con Nexo'. Suena sencillo. Si dices '¡claro que sí!' y empiezas a programar, en la semana 3 descubrirás que su ERP es un sistema cerrado de hace 15 años, que TI no te dará acceso por SSH y que la persona que sabe cómo exportar los datos está de vacaciones. En esta lección aprenderás a hacer las preguntas correctas para no caer en esa trampa."*
2. **Concepto (5-8 min):** Preguntas abiertas vs. preguntas cerradas (*The Mom Test*). La matriz de poder e interés de stakeholders.
3. **Demo / Análisis (6-8 min):** Comparar el diagrama Mermaid del flujo actual manual de Mariana frente al flujo automatizado propuesto.
4. **Cierre (1-2 min):** La importancia de definir qué queda **fuera de alcance** (*Out of Scope*) y presentación del Ejercicio 01.

---

## 📚 Para profundizar

- [The Mom Test (Rob Fitzpatrick)](../../recursos/lecturas.md#🏛️-el-rol-de-fde-y-relación-con-clientes).
- [The Trusted Advisor (David Maister)](../../recursos/lecturas.md#🏛️-el-rol-de-fde-y-relación-con-clientes).

---

⬅️ [Módulo 04: Datos y SQL](../04-datos-y-sql/README.md) | 🏠 [Índice](../../README.md) | [Módulo 06: Integración de sistemas](../06-integracion-de-sistemas/README.md) ➡️
