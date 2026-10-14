# 05. Banco de preguntas frecuentes en entrevistas para FDE

Más de 40 preguntas organizadas por categoría para practicar antes de tus entrevistas.

---

## 🔌 1. Integración de Sistemas, HTTP y APIs

1. **¿Cuál es la diferencia entre un código de error 400, 401, 403, 404, 422, 429 y 503?**
   * *Guía:* Explica qué entidad falló (cliente vs. servidor) y qué acción correctiva corresponde en cada caso (ej. 429 esperar con `Retry-After`, 401 renovar token, 422 corregir validación).
2. **¿Qué es la idempotencia y por qué es crucial al procesar pagos o pedidos de inventario?**
   * *Guía:* Una operación es idempotente si repetirla produce el mismo efecto. En redes inestables, si no recibes respuesta a un POST, una llave de idempotencia previene cobrar doble o apartar inventario dos veces.
3. **¿Cómo implementarías una estrategia de reintentos con *backoff* exponencial y *jitter*?**
   * *Guía:* Aumentar el tiempo base multiplicado por $2^n$ y agregar aleatoriedad para evitar que cientos de clientes reintenten en el mismo milisegundo provocando una tormenta de peticiones (*thundering herd*).
4. **¿Qué diferencias hay entre consultar datos vía *Polling* recurrente vs. suscribirse a *Webhooks*?**
   * *Guía:* Polling genera tráfico constante e ineficiente; los webhooks son en tiempo real pero requieren que expongas un endpoint público seguro con validación de firmas criptográficas HMAC.
5. **Si una API externa no tiene paginación por cursor sino por offset (`page`/`limit`), ¿qué problemas de concurrencia pueden ocurrir?**
   * *Guía:* Si se insertan registros nuevos mientras paginas, los elementos pueden saltarse o aparecer duplicados entre páginas contiguas.
6. **¿Cómo funciona el flujo OAuth 2.0 Client Credentials y cuándo se usa?**
   * *Guía:* Comunicación servidor a servidor (M2M) sin interacción de usuario humano; se intercambia `client_id` y `client_secret` por un token Bearer temporal.
7. **¿Qué encabezados HTTP usarías para verificar que un webhook proviene realmente del proveedor legítimo?**
   * *Guía:* Encabezados de firma HMAC (como `X-Signature-SHA256`) comparando el digest calculado con el secreto compartido.
8. **¿Cómo manejarías una API que responde con un cuerpo de 500 MB en una sola petición?**
   * *Guía:* Procesamiento en flujo (*streaming*) leyendo bloques (*chunks*) para no desbordar la memoria RAM.

---

## 🗄️ 2. Manipulación de Datos y SQL

9. **¿Cuál es la diferencia práctica entre un `INNER JOIN`, un `LEFT JOIN` y un `FULL OUTER JOIN`?**
10. **¿Cómo detectarías y eliminarías registros duplicados en una tabla sin borrar los datos originales?**
11. **¿Qué es una CTE (*Common Table Expression*) en SQL y cuándo es preferible sobre una subconsulta?**
12. **¿Por qué nunca deberías concatenar variables directamente en una cadena de consulta SQL?**
    * *Guía:* Exposición crítica a Inyección de SQL (*SQL Injection*); siempre deben usarse consultas parametrizadas (`?` o `:nombre`).
13. **¿Cómo limpiarías una columna de fechas que contiene mezclas de formatos como `2026-10-01`, `01/10/2026` y `4 oct 2026`?**
14. **En un pipeline ETL, ¿cuál es la diferencia entre una carga completa (*full load*) y una sincronización incremental (*delta load*)?**
15. **¿Qué ventajas ofrece SQLite para herramientas locales y conectores de FDE frente a bases de datos cliente-servidor?**

---

## 🐳 3. Despliegue, Linux y Producción

16. **¿Qué diferencia hay entre una imagen de Docker y un contenedor?**
17. **¿Por qué es una mala práctica ejecutar contenedores como usuario `root` en entornos de clientes?**
18. **¿Cómo inyectas credenciales sensibles en una aplicación contenedorizada sin escribirlas en el Dockerfile?**
    * *Guía:* Mediante variables de entorno en tiempo de ejecución, archivos `.env` no commiteados o gestores de secretos (Vault, AWS Secrets Manager).
19. **¿Qué comando de Linux usarías para buscar un SKU específico en 50 archivos de log comprimidos?**
    * *Guía:* `zgrep "HAL-1001" *.log.gz` o `grep -rn "HAL-1001" /var/log/`.
20. **¿Cómo diagnosticarías si un proceso en producción se detuvo por falta de memoria (OOM Killer)?**
    * *Guía:* Consultando `dmesg -T | grep -i oom` o inspeccionando los logs del sistema en `/var/log/messages`.
21. **Explica el concepto de observabilidad y sus tres pilares (Logs, Métricas, Trazas).**
22. **¿Qué es un postmortem sin culpa (*blameless postmortem*) y cuál es su objetivo?**

---

## 🤝 4. Trato con Clientes y Descubrimiento (Situacionales)

23. **El cliente insiste en que necesita que la integración esté lista en 3 días, pero el análisis técnico indica que tomará al menos 3 semanas. ¿Cómo respondes?**
    * *Guía:* No digas un "no" seco. Explica los riesgos y ofrece una fase 1 acotada: *"En 3 días no podemos tener la integración automática completa sin riesgo de perder pedidos, pero podemos habilitar una carga asistida diaria para que no detengan su operación mientras terminamos el conector robusto"*.
24. **Durante una llamada, el Gerente de TI se muestra hostil y afirma que la herramienta de tu empresa no sirve y es insegura. ¿Cómo manejas la conversación?**
    * *Guía:* Valida sus preocupaciones técnicas, no te pongas a la defensiva, ofrece datos técnicos concretos (cifrado, SOC 2) y coordina una sesión específica de arquitectura para revisar sus requisitos de red.
25. **¿Qué preguntas harías en una primera llamada de descubrimiento para entender el flujo de inventario de un cliente?**
26. **¿Cómo identificas la diferencia entre un "deseo" de un usuario y una "necesidad crítica de negocio"?**
27. **¿Qué harías si descubres un bug crítico en producción antes de que el cliente lo note?**
    * *Guía:* Evaluar impacto, preparar solución/mitigación, y notificar al cliente de forma transparente y proactiva con la solución en marcha antes de que ellos experimenten el problema.

---

## 🤖 5. Inteligencia Artificial Aplicada para FDE

28. **¿Qué es RAG (*Retrieval-Augmented Generation*) y cuándo es mejor que hacer fine-tuning de un modelo?**
    * *Guía:* RAG es ideal cuando los datos cambian con frecuencia, se requiere citar fuentes exactas y se desea reducir costos y evitar alucinaciones.
29. **¿Qué es la ventana de contexto de un LLM y cómo gestionas límites de tokens?**
30. **¿Cómo garantizas que la salida de un modelo de lenguaje sea un JSON válido que tu backend pueda procesar?**
    * *Guía:* Uso de Structured Outputs nativos de la API, esquemas JSON estrictos y validación con Pydantic o biblioteca estándar.
31. **¿Qué es una inyección de prompt (*prompt injection*) y cómo afecta a un conector empresarial?**

---

⬅️ [04. Proceso de entrevistas](04-proceso-de-entrevistas.md) | [Índice de carrera](README.md) | [06. Planes de estudio](06-plan-de-estudio.md) ➡️
