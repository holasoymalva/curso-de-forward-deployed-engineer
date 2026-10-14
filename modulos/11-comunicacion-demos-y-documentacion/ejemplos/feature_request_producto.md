# Solicitud de Funcionalidad a Producto: Ingesta Asíncrona por Lotes

**Identificador:** FR-2026-NEXO-042  
**Fecha:** 14 de octubre de 2026  
**Autor:** Forward Deployed Engineer (Nexo AI)  
**Receptores:** Lead Product Manager & Tech Lead de Plataforma Core  
**Estado:** Propuesto / En revisión de Roadmap  

---

## 🏢 1. Contexto de Negocio y Cliente

* **Cliente afectado:** Distribuidora Halcón (Contrato Enterprise ARR: \$110,000 USD).
* **Otros clientes potenciales afectados:** 3 prospectos del sector abarrotero y farmacéutico mayorista actualmente en etapa de preventa técnica (pipeline de ~\$300k USD ARR).
* **Urgencia:** Alta (requerido para la expansión de la Fase 2 a los almacenes de Guadalajara y CDMX en noviembre).

---

## 🛑 2. El Dolor del Cliente (User Problem / Pain Point)

Actualmente, la API central de Nexo únicamente ofrece el endpoint sincrónico:
`POST /v1/pedidos` o `POST /v1/inventario/lotes` con una limitación estricta de **máximo 50 registros por llamada HTTP** y un timeout de red de **30 segundos**.

### Consecuencias operativas en Halcón:
1. El ERP legado de Distribuidora Halcón exporta un solo archivo masivo de 15,000 registros cada noche.
2. Para transmitir ese archivo a través de la API actual, el conector del FDE debe realizar más de **300 peticiones HTTP secuenciales**.
3. Debido a la latencia de red variable y al rate-limiting de la API de Nexo, el proceso completo tarda casi 45 minutos. Si una sola llamada en el medio falla o excede el timeout, el cliente recibe errores de red y la sincronización se detiene a la mitad.

---

## 💡 3. Solución Provisional (Workaround) Actual del FDE

Para el piloto con Monterrey, el FDE implementó un script local con hilos y reintentos agresivos (`sincronizador_inventario.py`). 

> **Problema del parche:** Este script es complejo de mantener, depende de la memoria RAM del servidor local del cliente y no escala cuando incorporemos Guadalajara y CDMX, donde el volumen subirá a 60,000 SKUs diarios.

---

## 🚀 4. Propuesta Técnica Recomendada para el Core

Crear un endpoint nativo de ingesta asíncrona mediante subida de archivos o carga en bloques grandes:

### Endpoint propuesto:
`POST /v1/ingesta/masiva`

#### Flujo de interacción:
1. El cliente envía el archivo CSV comprimido en gzip o un JSON con hasta 50,000 registros.
2. La API responde inmediatamente con código `HTTP 202 Accepted` y un objeto con identificador de tarea:
   ```json
   {
     "job_id": "job_halcon_20261014_001",
     "estado": "EN_COLA",
     "registros_recibidos": 15000,
     "estimado_segundos": 25
   }
   ```
3. El motor de procesamiento de Nexo procesa el lote en segundo plano utilizando workers internos de Redis/Celery.
4. Al terminar el procesamiento, Nexo emite un evento vía **Webhook** hacia la URL configurada por el cliente (`https://srv-integracion-01.halcon.internal/webhooks/ingesta`) con el resumen de registros creados y errores de validación.

---

## 📈 5. Impacto Estimado en el Negocio

* **Para el cliente Halcón:** El tiempo de transmisión nocturna se reducirá de 45 minutos a menos de 40 segundos, eliminando el 100% de los incidentes por timeouts de red.
* **Para Nexo AI:** Se reducirá la carga de conexiones HTTP abiertas en un 80% en los balanceadores de carga y se acelerará el cierre de nuevos clientes enterprise con sistemas legados.
