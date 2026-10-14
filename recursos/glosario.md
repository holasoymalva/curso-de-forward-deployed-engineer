# 📖 Glosario del curso

Términos clave del rol de Forward Deployed Engineer, de la industria del software y de la IA aplicada. Los términos en inglés aparecen en *cursiva* con su traducción cuando aplica. La columna **Módulo** indica dónde se ve el término con más detalle (consulta el [índice de módulos](../README.md#️-ruta-de-aprendizaje)).

> [!TIP]
> Si al escribir una lección introduces un término nuevo, agrégalo aquí en orden alfabético (ver [CONTRIBUTING.md](../CONTRIBUTING.md)).

**Índice:** [A](#a) · [B](#b) · [C](#c) · [D](#d) · [E](#e) · [F](#f) · [G](#g) · [H](#h) · [I](#i) · [J](#j) · [K](#k) · [L](#l) · [M](#m) · [O](#o) · [P](#p) · [R](#r) · [S](#s) · [T](#t) · [U](#u) · [V](#v) · [W](#w)

---

## A

| Término | Definición | Módulo |
|---------|------------|--------|
| **Agente** (*agent*) | Sistema basado en un LLM que decide qué pasos dar y qué herramientas usar para cumplir un objetivo, en un ciclo de razonar → actuar → observar. | 10 |
| **Alcance** (*scope*) | Lo que el proyecto incluye y, igual de importante, lo que **no** incluye. Se acuerda por escrito para evitar el *scope creep*. | 05, 12 |
| **Alucinación** (*hallucination*) | Respuesta de un modelo de lenguaje que suena convincente pero es falsa o no está respaldada por los datos. | 10 |
| **API** (*Application Programming Interface*) | Contrato que define cómo un programa puede pedirle datos o acciones a otro. | 03 |
| **API key** (*clave de API*) | Cadena secreta que identifica a quien llama una API. Debe tratarse como contraseña. | 03, 09 |
| **Autenticación** (*authentication*) | Verificar **quién** eres (por ejemplo, con usuario y contraseña o un token). | 06 |
| **Autorización** (*authorization*) | Verificar **qué** puedes hacer una vez autenticado. | 06, 09 |

## B

| Término | Definición | Módulo |
|---------|------------|--------|
| ***Backoff* exponencial** (*exponential backoff*) | Estrategia de reintentos en la que el tiempo de espera crece en cada intento (1 s, 2 s, 4 s…), normalmente con algo de aleatoriedad (*jitter*). | 06 |
| ***Bearer token*** (*token portador*) | Token que se envía en el encabezado `Authorization: Bearer <token>`; quien lo porta tiene acceso. | 06 |
| **Blocker** (*bloqueo*) | Algo que impide avanzar y requiere acción de otra persona (por ejemplo, el cliente no ha dado credenciales). | 11 |
| ***Branch*** (*rama*) | Línea de desarrollo independiente en Git. | 01 |

## C

| Término | Definición | Módulo |
|---------|------------|--------|
| ***Champion*** (*promotor interno*) | Persona dentro del cliente que impulsa el proyecto y te ayuda a abrir puertas. | 05 |
| ***Churn*** (*abandono*) | Clientes que dejan de usar o pagar el producto en un periodo. Una mala implementación es causa frecuente. | 00 |
| **CI/CD** (*Continuous Integration / Continuous Delivery*) | Integración y entrega continuas: automatizar pruebas y despliegues cada vez que cambia el código. | 07 |
| ***Commit*** | Instantánea de cambios registrada en Git con un mensaje descriptivo. | 01 |
| **Contenedor** (*container*) | Paquete ligero que incluye una aplicación y sus dependencias para que corra igual en cualquier máquina. | 07 |
| **CSV** (*Comma-Separated Values*) | Formato de texto plano para datos tabulares, separados por comas. Muy común en exportaciones de ERP. | 02, 04 |
| ***Customer Success*** (*éxito del cliente*) | Equipo que acompaña al cliente después de la venta para que obtenga valor y renueve. | 00 |

## D

| Término | Definición | Módulo |
|---------|------------|--------|
| ***Discovery*** (*descubrimiento*) | Fase en la que entiendes el problema, los procesos, los sistemas y los objetivos del cliente antes de construir. | 05 |
| **Docker** | Herramienta para construir y ejecutar contenedores. | 07 |
| ***Dockerfile*** | Archivo con las instrucciones para construir una imagen de Docker. | 07 |

## E

| Término | Definición | Módulo |
|---------|------------|--------|
| ***Embeddings*** (*incrustaciones vectoriales*) | Representación numérica (vector) de un texto que captura su significado; textos parecidos tienen vectores cercanos. | 10 |
| ***Endpoint*** | URL específica de una API que responde a un método HTTP (por ejemplo, `GET /pedidos`). | 03 |
| **ERP** (*Enterprise Resource Planning*) | Sistema central que administra inventario, compras, finanzas, etc., en una empresa. | 00, 02 |
| **Escalamiento** (*escalation*) | Llevar un problema a un nivel superior (producto, ingeniería, dirección) cuando no puede resolverse en el nivel actual. | 08, 11 |
| **ETL** (*Extract, Transform, Load*) | Proceso de extraer datos de una fuente, transformarlos (limpiar, normalizar) y cargarlos en un destino. | 04 |
| **Evaluación** (*evals*) | Conjunto de casos de prueba y métricas para medir la calidad de una solución con IA. | 10 |
| **Variable de entorno** (*environment variable*) | Valor de configuración que se lee del sistema operativo en lugar de escribirse en el código. | 07 |

## F

| Término | Definición | Módulo |
|---------|------------|--------|
| **FDE** (*Forward Deployed Engineer*) | Ingeniero o ingeniera que trabaja "en la trinchera" con el cliente para que el producto resuelva su problema real: integra, adapta, despliega y retroalimenta al equipo de producto. | 00 |
| ***Feature request*** (*solicitud de funcionalidad*) | Pedido del cliente de algo que el producto no hace hoy. El FDE lo documenta y lo lleva a producto. | 11 |
| ***Function calling*** (*llamada a funciones*) | Capacidad de un LLM de devolver una llamada estructurada a una función o herramienta definida por ti. | 10 |

## G

| Término | Definición | Módulo |
|---------|------------|--------|
| **Git** | Sistema de control de versiones distribuido. | 01 |
| ***Go-live*** (*puesta en marcha*) | Momento en que la solución empieza a usarse en producción. | 12 |

## H

| Término | Definición | Módulo |
|---------|------------|--------|
| ***Handoff*** (*traspaso*) | Entrega formal de la solución, documentación y responsabilidades al cliente o a otro equipo. | 11, 12 |
| **HTTP** (*HyperText Transfer Protocol*) | Protocolo de comunicación de la web, basado en peticiones y respuestas. | 03 |
| **Código de estado HTTP** (*status code*) | Número que resume el resultado de una petición: `2xx` éxito, `4xx` error del cliente, `5xx` error del servidor. | 03 |

## I

| Término | Definición | Módulo |
|---------|------------|--------|
| **Idempotencia** (*idempotency*) | Propiedad de una operación que produce el mismo resultado aunque se ejecute varias veces. Clave para reintentar sin duplicar pedidos. | 06 |
| ***Idempotency-Key*** | Encabezado con un identificador único que permite al servidor detectar peticiones repetidas. | 06 |
| **Incidente** (*incident*) | Interrupción o degradación de un servicio que afecta a usuarios y requiere respuesta. | 08 |
| **Integración** (*integration*) | Conectar dos o más sistemas para que intercambien datos de forma confiable. | 06 |

## J

| Término | Definición | Módulo |
|---------|------------|--------|
| **JSON** (*JavaScript Object Notation*) | Formato de texto para datos estructurados, estándar en APIs web. | 02, 03 |
| **JWT** (*JSON Web Token*) | Formato de token firmado que contiene información (*claims*) sobre el usuario. | 06 |

## K

| Término | Definición | Módulo |
|---------|------------|--------|
| ***Kickoff*** (*reunión de arranque*) | Primera reunión formal del proyecto para alinear objetivos, roles y calendario. | 05, 12 |
| **KPI** (*Key Performance Indicator*) | Indicador clave de desempeño; métrica que el cliente usa para medir éxito. | 05 |

## L

| Término | Definición | Módulo |
|---------|------------|--------|
| **Latencia** (*latency*) | Tiempo que tarda una petición en recibir respuesta. | 08 |
| **LLM** (*Large Language Model*) | Modelo de lenguaje grande entrenado con enormes cantidades de texto, capaz de generar y entender lenguaje natural. | 10 |
| ***Logs*** (*registros*) | Mensajes que una aplicación escribe para dejar rastro de lo que hace. Idealmente estructurados (JSON). | 08 |

## M

| Término | Definición | Módulo |
|---------|------------|--------|
| **Mínimo privilegio** (*least privilege*) | Principio de dar solo los permisos estrictamente necesarios para una tarea. | 09 |
| **Métricas** (*metrics*) | Mediciones numéricas a lo largo del tiempo (peticiones por minuto, errores, latencia). | 08 |

## O

| Término | Definición | Módulo |
|---------|------------|--------|
| **OAuth 2.0** | Estándar de autorización que permite a una aplicación obtener acceso limitado a recursos mediante tokens, sin compartir contraseñas. | 06 |
| **Observabilidad** (*observability*) | Capacidad de entender el estado interno de un sistema a partir de sus logs, métricas y trazas. | 08 |
| ***Onboarding*** (*incorporación*) | Proceso de poner en marcha a un cliente nuevo (o a una persona nueva en un equipo). | 00 |
| **OWASP** | Fundación que publica guías de seguridad, como el *OWASP Top 10*. | 09 |

## P

| Término | Definición | Módulo |
|---------|------------|--------|
| **Paginación** (*pagination*) | Dividir resultados grandes de una API en páginas para pedirlos por partes. | 06 |
| **Piloto** (*pilot*) | Uso real pero limitado de la solución (pocos usuarios, un almacén) para validar valor antes de escalar. | 00, 12 |
| **PII** (*Personally Identifiable Information*) | Datos personales que identifican a una persona (nombre, teléfono, correo, dirección). Requieren protección especial. | 09 |
| **POC** (*Proof of Concept*) | Prueba de concepto: demostración técnica rápida de que algo es posible, normalmente sin calidad de producción. | 00, 05 |
| ***Postmortem*** (*análisis posincidente*) | Documento que analiza un incidente: qué pasó, impacto, causa raíz y acciones para que no se repita. Idealmente sin culpas (*blameless*). | 08 |
| **Prompt** (*instrucción*) | Texto de entrada que se le da a un LLM para guiar su respuesta. | 10 |
| ***Pull request*** (PR) | Solicitud para integrar cambios de una rama a otra, con revisión de código. | 01 |

## R

| Término | Definición | Módulo |
|---------|------------|--------|
| **RAG** (*Retrieval-Augmented Generation*) | Generación aumentada con recuperación: buscar documentos relevantes y pasárselos al LLM como contexto para que responda con datos reales. | 10 |
| ***Rate limit*** (*límite de tasa*) | Número máximo de peticiones permitidas en un periodo. Al superarlo, la API suele responder `429 Too Many Requests`. | 06 |
| **REST** (*Representational State Transfer*) | Estilo de diseño de APIs basado en recursos, URLs y métodos HTTP estándar. | 03 |
| **Reintento** (*retry*) | Volver a intentar una operación fallida, idealmente solo ante errores transitorios y con *backoff*. | 06 |
| **ROI** (*Return on Investment*) | Retorno de la inversión: beneficio obtenido en relación con lo que costó. | 05, 11 |
| ***Runbook*** (*manual de operación*) | Guía paso a paso para operar un sistema o responder a un tipo de incidente. | 08 |

## S

| Término | Definición | Módulo |
|---------|------------|--------|
| **Secreto** (*secret*) | Credencial sensible (contraseña, API key, token). Nunca se sube al repositorio. | 07, 09 |
| **SLA** (*Service Level Agreement*) | Acuerdo de nivel de servicio contractual con el cliente, con consecuencias si no se cumple. | 08 |
| **SLO** (*Service Level Objective*) | Objetivo interno de nivel de servicio (por ejemplo, "99.5 % de sincronizaciones exitosas al mes"). | 08 |
| **SKU** (*Stock Keeping Unit*) | Código único que identifica un producto en inventario. | Caso de estudio |
| **SOW** (*Statement of Work*) | Documento que define entregables, alcance, tiempos y responsabilidades de un proyecto. | 05, 12 |
| **SQL** (*Structured Query Language*) | Lenguaje para consultar y manipular bases de datos relacionales. | 04 |
| **SQLite** | Base de datos relacional en un solo archivo, incluida en Python. | 04 |
| ***Stakeholder*** (*parte interesada*) | Persona con interés o influencia en el proyecto (patrocinador, TI, usuarios finales). | 05 |
| **STAR** (*Situation, Task, Action, Result*) | Método para estructurar respuestas en entrevistas conductuales. | [Carrera](carrera/04-proceso-de-entrevistas.md) |

## T

| Término | Definición | Módulo |
|---------|------------|--------|
| ***Time-to-value*** (*tiempo hasta el valor*) | Tiempo que tarda el cliente en obtener el primer beneficio tangible del producto. El FDE busca reducirlo. | 00 |
| **Token** (autenticación) | Credencial temporal que prueba que estás autenticado. | 06 |
| **Token** (IA) | Unidad mínima de texto que procesa un LLM (aprox. una parte de palabra). Determina costo y límites de contexto. | 10 |
| **Traza** (*trace*) | Registro del recorrido de una petición a través de varios servicios. | 08 |
| ***Triage*** (*clasificación*) | Priorizar problemas según impacto y urgencia. | 08 |

## U

| Término | Definición | Módulo |
|---------|------------|--------|
| ***Upsell*** (*venta adicional*) | Vender al cliente existente más producto o un plan superior. Una implementación exitosa suele habilitarlo. | 00 |

## V

| Término | Definición | Módulo |
|---------|------------|--------|
| **Ventana de contexto** (*context window*) | Cantidad máxima de tokens que un LLM puede considerar en una sola petición. | 10 |
| **Base de datos vectorial** (*vector database*) | Almacén optimizado para buscar embeddings por similitud. | 10 |

## W

| Término | Definición | Módulo |
|---------|------------|--------|
| ***Webhook*** | Notificación HTTP que un sistema envía a otro automáticamente cuando ocurre un evento ("no me llames, yo te llamo"). | 06 |
| **WSL** (*Windows Subsystem for Linux*) | Capa de Windows para ejecutar un entorno Linux. Recomendado para seguir el curso en Windows. | 01 |
