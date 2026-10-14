# Ejemplos del Módulo 10: Inteligencia Artificial aplicada

Scripts ejecutables de Python diseñados para dominar el consumo de LLMs, la arquitectura RAG y la extracción estructurada sin requerir dependencias externas ni tarjetas de crédito para APIs comerciales.

---

## 📂 Archivos disponibles

| Archivo | Descripción | Modo de ejecución |
|---------|-------------|-------------------|
| [`cliente_llm_simulado.py`](cliente_llm_simulado.py) | Cliente de inferencia versátil: opera en modo simulado local determinista o contra cualquier API compatible (OpenAI, Anthropic, Ollama, Groq) si se define `LLM_API_KEY`. | `python cliente_llm_simulado.py` |
| [`rag_minimo.py`](rag_minimo.py) | Motor RAG completo en Python puro (TF-IDF y ranking de relevancia) que indexa documentos del caso de estudio de Halcón y responde preguntas operativas. | `python rag_minimo.py` |
| [`extractor_estructurado.py`](extractor_estructurado.py) | Extractor de lenguaje natural que transforma mensajes informales de encargados de tienda en objetos JSON estrictamente validados contra el catálogo del ERP. | `python extractor_estructurado.py` |

---

## 🚀 Cómo ejecutar los ejemplos

Desde la raíz del repositorio:

```bash
# 1. Probar el cliente LLM simulado
python modulos/10-ia-aplicada/ejemplos/cliente_llm_simulado.py

# 2. Consultar el motor RAG sobre la documentación de Halcón
python modulos/10-ia-aplicada/ejemplos/rag_minimo.py

# 3. Probar la extracción de pedidos estructurados
python modulos/10-ia-aplicada/ejemplos/extractor_estructurado.py
```
