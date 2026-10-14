# Lección 02: Consumo de APIs y salidas estructuradas

## 🎯 Objetivos de aprendizaje

* Dominar la estructura estándar de las APIs de Chat Completion (`system`, `user`, `assistant`).
* Aplicar técnicas de ingeniería de prompts profesionales: *Few-Shot Prompting* y *Chain-of-Thought*.
* Implementar salidas estructuradas estrictas mediante esquemas JSON (*JSON Schema* y *Structured Outputs*) y validación defensiva en Python.

---

## 💬 1. Anatomía de una petición de Chat Completion

Casi todos los proveedores modernos de LLMs (OpenAI, Anthropic, Google Cloud Vertex AI, Groq, Ollama) han convergido en una interfaz de mensajes estructurados:

```json
{
  "model": "gpt-4o-mini",
  "temperature": 0.0,
  "messages": [
    {
      "role": "system",
      "content": "Eres un analista de datos especializado en inventarios mayoristas de abarrotes para Distribuidora Halcón. Tu trabajo es interpretar pedidos no estructurados y responder exclusivamente en JSON."
    },
    {
      "role": "user",
      "content": "Hola, ocupamos 40 cajas de aceite y 20 de frijol para la tienda T0001 de Monterrey urgente."
    }
  ]
}
```

### Roles fundamentales:
* **`system`:** Define la personalidad, restricciones inviolables, formato de salida y reglas de negocio. Es la instrucción de mayor autoridad.
* **`user`:** Contiene la entrada variable del usuario, cliente o sistema externo.
* **`assistant`:** Representa respuestas previas del modelo, permitiendo mantener conversaciones multi-turno.

---

## 🎯 2. Técnicas de ingeniería de prompts para FDEs

El prompt engineering para un FDE no es "probar frases bonitas"; es **especificación formal de requisitos en lenguaje natural**.

### A. Few-Shot Prompting (Aprender por ejemplos)
Incluir 2 o 3 ejemplos reales de entrada y salida esperada dentro del prompt incrementa drásticamente la precisión del modelo:

```text
Entrada: "Manda 10 cajas de leche a la sucursal de Zapopan"
Salida: {"sku": "SKU-LECHE-05", "cantidad": 10, "almacen": "GDL", "urgencia": "NORMAL"}

Entrada: "Nos urge que lleguen 50 costales de arroz a Monterrey antes de las 3pm"
Salida: {"sku": "SKU-ARROZ-01", "cantidad": 50, "almacen": "MTY", "urgencia": "ALTA"}
```

### B. Chain-of-Thought (Razonamiento paso a paso)
Para problemas lógicos o de conciliación compleja, pedirle al modelo que explique su razonamiento antes de emitir el veredicto final reduce los errores de cálculo:
> *"Primero identifica los productos mencionados en el texto. Luego asocia cada producto con el catálogo oficial de SKUs. Si algún producto no existe, márcalo como NO_IDENTIFICADO. Finalmente genera el objeto JSON."*

---

## 🧱 3. Salidas estructuradas (Structured Outputs)

El mayor dolor de cabeza de los desarrolladores al inicio era recibir texto como:
`"Claro, aquí tienes tu JSON:\n```json\n{\n  \"sku\": ...\n}\n```\nEspero que te sirva!"`

Esto obligaba a escribir expresiones regulares frágiles para extraer el bloque de texto. Hoy en día, los proveedores ofrecen soporte nativo para **Structured Outputs**:
1. Le envías un esquema formal **JSON Schema** en la petición (`response_format`).
2. El motor del LLM restringe la decodificación de tokens en tiempo de inferencia para garantizar que la respuesta cumpla al 100% con la gramática de ese esquema.

### Definición de esquema JSON para pedidos de Halcón:

```python
ESQUEMA_PEDIDO = {
    "type": "object",
    "properties": {
        "id_tienda": {"type": "string"},
        "almacen": {"type": "string", "enum": ["MTY", "GDL", "CDMX"]},
        "articulos": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "sku": {"type": "string"},
                    "cantidad": {"type": "integer", "minimum": 1}
                },
                "required": ["sku", "cantidad"]
            }
        },
        "urgente": {"type": "boolean"}
    },
    "required": ["id_tienda", "almacen", "articulos", "urgente"]
}
```

---

## 🛡️ 4. Validación defensiva en Python

A pesar de que el modelo garantice la estructura sintáctica del JSON, el FDE debe aplicar **validación semántica de negocio** en Python antes de interactuar con la base de datos o el ERP:

```python
import json

def validar_y_procesar_pedido(json_texto: str, catalogo_skus_validos: set) -> dict:
    try:
        data = json.loads(json_texto)
    except json.JSONDecodeError as e:
        raise ValueError(f"Falla de decodificación JSON: {e}")

    # Validación semántica: ¿Existen los SKUs en nuestro catálogo real?
    for item in data.get("articulos", []):
        sku = item.get("sku")
        if sku not in catalogo_skus_validos:
            raise ValueError(f"El SKU '{sku}' extraído por el LLM no existe en el catálogo ERP.")

    return data
```

---

## 📌 Conclusiones clave

* Configura siempre el rol `system` con límites claros y formato exclusivo en JSON.
* Usa *Few-Shot examples* para eliminar ambigüedades en nombres de productos regionales (p. ej., "bultos", "costales", "cajas").
* Valida semánticamente la salida del LLM contra tus fuentes de datos relacionales antes de ejecutar acciones en producción.
