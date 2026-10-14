# Ejercicios del Módulo 10: Inteligencia Artificial aplicada

Prácticas para construir, evaluar y asegurar soluciones de IA para clientes empresariales.

---

## 🎯 Lista de ejercicios

| Ejercicio | Nivel | Enfoque | Archivos relacionados |
|-----------|-------|---------|-----------------------|
| [**01. Pipeline RAG con evaluación cuantitativa**](01-pipeline-rag-con-evaluacion.md) | 🟡 Intermedio | Indexación de políticas operativas de Halcón, recuperación contextual y cálculo de métricas de precisión. | [`../ejemplos/rag_minimo.py`](../ejemplos/rag_minimo.py) |
| [**02. Extractor de pedidos con guardrails de seguridad**](02-extractor-de-tickets-con-guardrails.md) | 🟡 Intermedio | Detección y neutralización de ataques de inyección de prompts en mensajes de WhatsApp y validación de esquemas JSON. | [`../ejemplos/extractor_estructurado.py`](../ejemplos/extractor_estructurado.py) |

---

## 🛠️ Instrucciones de trabajo

1. Los ejercicios están diseñados para correr tanto en modo offline simulado como contra endpoints reales si configuras `LLM_API_KEY`.
2. Para el **Ejercicio 01**, extenderás el motor RAG para ejecutar una batería de pruebas de evaluación (*Eval Set*) y generar un reporte cuantitativo.
3. Para el **Ejercicio 02**, implementarás guardrails deterministas que detecten intentos maliciosos de saltarse validaciones de crédito o alterar precios.
4. Consulta las soluciones en [`soluciones/`](soluciones/) al concluir tu implementación.
