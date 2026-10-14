# 01. ¿Qué buscan las empresas en un Forward Deployed Engineer?

El término **Forward Deployed Engineer (FDE)** nació en empresas como Palantir a mediados de los años 2000 para describir a ingenieros de software que trabajan directamente "en el campo" con clientes estratégicos. Hoy en día, empresas como OpenAI, Anthropic, Scale AI, Databricks y cientos de startups de software B2B contratan activamente este perfil.

---

## 🎭 Variaciones del título en las ofertas de empleo

Aunque la esencia del trabajo es muy similar, distintas organizaciones usan nombres diferentes:

- **Forward Deployed Engineer (FDE):** Término clásico; enfatiza ingeniería de software de alto nivel resolviendo problemas específicos del cliente con la plataforma propia.
- **Forward Deployed Software Engineer (FDSE):** Variante explícita para diferenciarlo de roles puramente consultivos.
- **Implementation Engineer / Solutions Architect:** Título frecuente en empresas SaaS B2B tradicionales; suele enfocarse en conectar APIs y desplegar flujos de trabajo.
- **Integration Engineer:** Foco profundo en canalizaciones de datos, webhooks, middleware y APIs.
- **Technical Account Engineer / Solutions Engineer (SE):** En algunas empresas este rol participa tanto en la preventa técnica como en la integración temprana.
- **Field Engineer / Customer Facing Engineer:** Utilizado comúnmente en plataformas de hardware o infraestructura de nube.

---

## 🎯 El perfil en "T" de un FDE

Las empresas buscan profesionales con un balance entre profundidad técnica y sensibilidad de negocio:

```mermaid
flowchart TD
    subgraph Habilidades Transversales (Travesaño de la T)
        A["Comunicación técnica y ejecutiva"] --- B["Descubrimiento y empatía"] --- C["Manejo de expectativas y ambigüedad"] --- D["Pensamiento de negocio (ROI)"]
    end
    subgraph Profundidad Técnica (Tallo de la T)
        E["APIs REST, Webhooks y protocolos web"]
        F["Scripting y procesamiento de datos (Python, SQL)"]
        G["Arquitectura resiliente (reintentos, idempotencia)"]
        H["Contenedores y despliegue (Docker, Linux)"]
        I["Debugging en producción y observabilidad"]
    end
```

### 1. El tallo técnico (Engineering Rigor)
No basta con saber hacer un script simple. Las empresas evalúan:
- ¿Sabes qué pasa cuando una API responde 429 o 503?
- ¿Sabes cómo evitar duplicar transacciones financieras o pedidos de inventario usando idempotencia?
- ¿Puedes dockerizar tu conector y diagnosticar problemas leyendo logs sin acceso visual al servidor?

### 2. El travesaño transversal (Client Facing Skills)
- **Claridad comunicativa:** Explicar el mismo problema a un Director de Operaciones (en términos de retraso de pedidos y dinero) y a un Gerente de TI (en términos de llaves de cifrado y consumo de CPU).
- **Tolerancia a la ambigüedad:** Llegar con un cliente que dice *"nuestro sistema no funciona bien"* y saber formular las preguntas correctas para aislar el problema.
- **Capacidad de decir "no" con alternativas:** Evitar prometer funciones inexistentes sin romper la relación con el cliente.

---

## 🏢 ¿Qué tipo de empresas contratan FDEs?

1. **Empresas de Inteligencia Artificial (OpenAI, Anthropic, Scale AI, startups de IA vertical):**
   - Ayudan a clientes corporativos a implementar modelos de lenguaje (LLMs), canalizaciones de RAG y agentes sobre datos propietarios de la empresa.
2. **Empresas de infraestructura de datos y analítica (Databricks, Snowflake, Palantir):**
   - Conectan lagos de datos (*data lakes*), ERPs y bases de datos heredadas con la plataforma central.
3. **Startups B2B en etapa de crecimiento (Series A a C):**
   - Cuando el producto aún no tiene conectores listos para todos los ERPs del mercado, el FDE crea las integraciones personalizadas que cierran y retienen a los primeros clientes grandes.

---

⬅️ [Volver al índice de carrera](README.md) | [Siguiente: CV y LinkedIn](02-cv-y-linkedin.md) ➡️
