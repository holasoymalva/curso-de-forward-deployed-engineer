# Lección 04: Nube, CI/CD básico y despliegues On-Premise

> **Nivel:** 🟡 Intermedio · **Duración estimada:** 30 min

---

## Situación

Laura Garza te comenta: *"En el futuro queremos migrar todo nuestro centro de datos a la nube para no tener servidores físicos en Monterrey, pero por ahora nuestro ERP debe quedarse en nuestras instalaciones. ¿Su solución puede correr hoy en nuestros servidores locales y migrarse a la nube mañana sin tener que programar todo de nuevo?"*.

El ecosistema empresarial contemporáneo es **híbrido**: conviven infraestructuras físicas locales (*On-Premise*), nubes privadas virtuales (*VPC*) y servicios gestionados en la nube pública (AWS, Google Cloud, Azure).

---

## Conceptos clave

### 1. El espectro de infraestructura: IaaS vs. PaaS vs. Serverless

```mermaid
flowchart TD
    subgraph On-Premise (Local)
        A["Servidor Físico del Cliente<br/>(Halcón gestiona hardware, red, SO y parches)"]
    end

    subgraph IaaS (Infraestructura como Servicio)
        B["Máquinas Virtuales en la Nube<br/>(AWS EC2, GCP Compute Engine, Azure VM)"]
    end

    subgraph PaaS / Contenedores Gestionados
        C["Plataformas de Contenedores<br/>(AWS ECS, GCP Cloud Run, Azure Container Apps)"]
    end

    subgraph Serverless
        D["Funciones sin servidor<br/>(AWS Lambda, GCP Cloud Functions)"]
    end
```

| Modelo | Qué gestiona el proveedor de nube | Qué gestionas tú como FDE | Cuándo se usa con clientes |
|--------|------------------------------------|---------------------------|----------------------------|
| **On-Premise** | Nada (el cliente es dueño del metal) | La aplicación y el runtime de Docker | Clientes tradicionales o regulados (banca, salud, ERPs viejos). |
| **IaaS (VMs)** | Hardware físico, centro de datos, virtualización | Sistema Operativo, Docker, parches y red | Cuando el cliente migra sus servidores a la nube sin rediseñar arquitectura. |
| **PaaS / Containers** | Hardware, Sistema Operativo, escalamiento | El contenedor de la aplicación únicamente | Arquitecturas modernas escalables y de bajo mantenimiento. |

---

### 2. Restricciones típicas de redes empresariales

En despliegues corporativos te enfrentarás a:
- **Redes Privadas Virtuales (VPN):** Túneles cifrados (como WireGuard, OpenVPN o IPsec) necesarios para acceder a los servidores de desarrollo del cliente desde fuera de sus oficinas.
- **Listas Blancas de IP (*IP Whitelisting*):** Reglas de firewall que solo permiten conexiones entrantes provenientes de una IP pública fija previamente autorizada.
- **Proxies Corporativos:** Toda petición saliente a internet debe pasar por un proxy que inspecciona el tráfico.

---

### 3. Automatización con CI/CD (GitHub Actions)

Para asegurar que ningún código roto o sin pruebas llegue al cliente, usamos **Integración Continua** (*CI*): cada vez que subes un commit a Git, un robot en la nube ejecuta las pruebas y compila el contenedor automáticamente.

Ejemplo conceptual de flujo en GitHub Actions (`.github/workflows/ci.yml`):

```yaml
name: Integración Continua Nexo

on:
  push:
    branches: [main, feature/*]
  pull_request:
    branches: [main]

jobs:
  pruebas-y-calidad:
    runs-on: ubuntu-latest

    steps:
      - name: Clonar repositorio
        uses: actions/checkout@v4

      - name: Configurar Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.10"

      - name: Verificar sintaxis del código
        run: |
          python -m py_compile modulos/06-integracion-de-sistemas/ejemplos/cliente_resiliente.py

      - name: Construir imagen Docker de prueba
        run: |
          docker build -t nexo/conector-test:latest -f modulos/07-despliegue-y-cloud/ejemplos/Dockerfile .
```

---

## Errores comunes

- **Asumir que el servidor del cliente tiene acceso irrestricto a internet:** En muchas empresas, los servidores no pueden salir a internet por el puerto 80 ni descargar imágenes de Docker Hub directamente. En esos casos, se exportan las imágenes a un archivo tar (`docker save`) y se transfieren por SFTP.
- **No documentar los puertos requeridos en la arquitectura:** Pedirle a TI que *"abra los puertos necesarios"*. Roberto necesita saber exactamente: Protocolo (TCP), Puerto de destino (443), Dirección IP/Dominio y Dirección del tráfico (Saliente).
- **Saltarse las pruebas automatizadas de CI:** Enviar código directamente a producción sin haber corrido pruebas de compilación en un entorno limpio.

---

## En el día a día de un FDE

Un FDE moderno diseña soluciones **agnósticas de la infraestructura**: tu contenedor corre hoy en la máquina virtual Linux de Roberto en Monterrey con Docker Compose, y dentro de un año correrá idéntico en Amazon ECS o Google Cloud Run cuando Halcón migre a la nube, sin cambiar una sola línea de código.

---

## Resumen

- Los despliegues de FDE oscilan entre entornos locales *On-Premise* y nubes públicas.
- Empaquetar en Docker garantiza portabilidad total entre nubes y servidores físicos.
- Respeta las restricciones corporativas de red (VPNs, firewalls, proxies).
- Las canalizaciones de CI/CD garantizan que solo el código probado y verificado se despliegue en clientes.

---

## Preguntas de repaso

1. ¿Qué ventajas ofrece empaquetar una integración en Docker si el cliente planea migrar de servidores físicos a la nube el próximo año?
2. ¿Qué significa el término *IP Whitelisting* y cómo afecta a las conexiones de un conector?
3. ¿Cuál es el objetivo principal de una canalización de Integración Continua (CI) en un proyecto de software?

---

⬅️ [Lección anterior: Docker Compose](03-orquestacion-con-docker-compose-y-secretos.md) | 📦 [Módulo](../README.md) | [Ir a Ejemplos del módulo](01-de-mi-maquina-a-produccion-12-factor.md) ➡️
