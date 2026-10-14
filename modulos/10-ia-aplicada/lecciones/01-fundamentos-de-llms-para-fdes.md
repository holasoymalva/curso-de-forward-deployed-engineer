# Lección 01: Fundamentos de LLMs para FDEs

## 🎯 Objetivos de aprendizaje

* Comprender la naturaleza probabilística de los Modelos de Lenguaje Grande (*LLMs*).
* Dominar el concepto de tokens, cálculo de costos (*tokenomics*) y latencia de inferencia.
* Conocer la ventana de contexto, los parámetros de muestreo (temperatura, top-p) y las técnicas de mitigación de alucinaciones.

---

## 🧠 1. El LLM como motor de predicción de texto

Un Modelo de Lenguaje Grande (*Large Language Model*, LLM) no es una base de datos relacional ni una mente consciente: es una red neuronal autorregresiva entrenada para predecir cuál es el token más probable que continúa a una secuencia de texto dada.

Para un Forward Deployed Engineer, esto significa algo fundamental:
> **El LLM es no-determinista por naturaleza.** La misma entrada puede generar salidas ligeramente distintas a menos que se controle estrictamente su configuración.

En implementaciones corporativas (como el sistema de gestión de inventarios para Distribuidora Halcón), la predictibilidad es crucial. Un error de interpretación en un pedido de abarrotes se traduce en camiones de carga enviados al destino incorrecto.

---

## 🪙 2. Tokens y "Tokenomics"

Los modelos de lenguaje no leen palabras completas ni caracteres aislados; procesan **tokens** (fragmentos de palabras o sílabas).

* En inglés: 1 token equivale aproximadamente a 0.75 palabras (o 4 caracteres).
* En español: Debido a acentos, sufijos y menor representación en los vocabularios de tokenización estándar (como Byte-Pair Encoding), 1 palabra suele requerir entre 1.3 y 2 tokens.

### Estructura de costos de una API de LLM

Los proveedores de APIs (OpenAI, Anthropic, Google Cloud Vertex AI, Azure) cobran bajo un esquema bimodal por millón de tokens:

$$\text{Costo Total} = (\text{Tokens de Entrada} \times \text{Precio Entrada}) + (\text{Tokens de Salida} \times \text{Precio Salida})$$

> [!NOTE]
> Los tokens de salida (*generation/completion*) suelen ser entre 3 y 5 veces más costosos que los de entrada (*prompt*), debido a que la generación autorregresiva requiere ejecutar la red token por token secuencialmente.

### Ejemplo de cálculo para Distribuidora Halcón:
Si Halcón recibe 5,000 pedidos diarios por correo o WhatsApp y cada mensaje tiene un promedio de 200 tokens, más un prompt de sistema con reglas de 800 tokens:
* Tokens de entrada por día: $5,000 \times (800 + 200) = 5,000,000\text{ tokens}$.
* Tokens de salida estructurada (JSON de ~150 tokens): $5,000 \times 150 = 750,000\text{ tokens}$.
* A tarifas típicas de modelos eficientes (\$0.15 USD por millón de entrada, \$0.60 USD por millón de salida):
  * Entrada: $5 \times \$0.15 = \$0.75\text{ USD/día}$
  * Salida: $0.75 \times \$0.60 = \$0.45\text{ USD/día}$
  * Total mensual: $(\$0.75 + \$0.45) \times 30 = \$36\text{ USD/mes}$.

El FDE debe ser capaz de presentar este desglose de costos en las llamadas con directivos para disipar el miedo a "facturas de IA descontroladas".

---

## 🪟 3. Ventana de contexto y latencia

La **ventana de contexto** (*context window*) es la cantidad máxima de tokens que el modelo puede recibir y generar en una sola interacción (p. ej., 128k, 200k o hasta 1 millón de tokens en modelos modernos).

Sin embargo, que una ventana soporte 128k tokens **no significa que debas enviar 128k tokens en cada petición**:
1. **Latencia (TTFT y TPS):** El Tiempo hasta el Primer Token (*Time-To-First-Token*, TTFT) crece de forma proporcional al tamaño del prompt de entrada.
2. **Efecto "Lost in the Middle":** La capacidad del modelo para recordar hechos específicos ubicados en la mitad de un texto gigantesco disminuye respecto a la información ubicada al principio o al final del prompt.
3. **Costo acumulativo:** Enviar manuales de 50 páginas en cada llamada de API multiplica los costos exponencialmente.

---

## 🌡️ 4. Parámetros de control: Temperatura y Top-P

Cuando interactúes con las APIs, configurarás estos hiperparámetros:

* **Temperatura (`temperature` entre 0.0 y 2.0):**
  * Controla la aleatoriedad en la distribución de probabilidades de los tokens candidatos.
  * Para tareas de integración FDE (extracción de datos, validación JSON, clasificación de incidentes, RAG): **usa `0.0` o `0.1`**. Esto maximiza la consistencia y reduce la creatividad no deseada.
  * Temperaturas altas (0.7 a 1.0) se reservan para redacción creativa o generación de ideas.
* **Top-P (Nucleus Sampling):** Alternativa a la temperatura que restringe el muestreo al porcentaje más probable de la distribución acumulada.

---

## 👻 5. Alucinaciones y cómo mitigarlas

Una **alucinación** ocurre cuando el modelo genera información falsa, inexistente o contradictoria con total confianza gramatical.

### Causas comunes:
* Preguntar sobre datos privados del cliente que el modelo base nunca vio durante su pre-entrenamiento.
* Prompts ambiguos o sin restricciones explícitas.
* Contextos saturados con información contradictoria.

### Estrategias de mitigación para el FDE:
1. **Inyección de contexto con RAG:** *"Responde ÚNICAMENTE basándote en los fragmentos de texto provistos abajo. Si la respuesta no está contenida en ellos, di 'NO_DISPONIBLE'"*.
2. **Instrucciones negativas explícitas:** Prohibir explícitamente inventar precios, SKUs o nombres de almacenes.
3. **Validación de esquemas (JSON Schema):** Forzar al modelo a responder con claves y tipos de datos estrictos.

---

## 📌 Conclusiones clave

* Como FDE, diseña soluciones con `temperature=0.0` para garantizar resultados reproducibles en producción.
* Calcula siempre los costos y latencias operativas antes de desplegar un LLM en un flujo de cliente.
* La forma de erradicar alucinaciones no es "rogarle al modelo", sino restringir su contexto con RAG y validar sus salidas con código determinista.
