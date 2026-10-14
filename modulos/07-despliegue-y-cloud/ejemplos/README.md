# Ejemplos del Módulo 07: Despliegue y cloud

Archivos de empaquetado, orquestación y automatización para ejecutar la solución completa de Distribuidora Halcón.

---

## 📂 Archivos disponibles

| Archivo | Descripción | Uso |
|---------|-------------|-----|
| [`.env.example`](.env.example) | Plantilla de configuración con variables de entorno para desarrollo y producción. | `cp .env.example .env` |
| [`Dockerfile`](Dockerfile) | Receta para construir la imagen del worker de sincronización sobre Python 3.10-slim con usuario no root. | `docker build -t nexo-worker .` |
| [`Dockerfile.api`](Dockerfile.api) | Receta para contenedorizar la API simulada de Halcón. | `docker build -f Dockerfile.api -t halcon-api .` |
| [`docker-compose.yml`](docker-compose.yml) | Orquestación multi-servicio: levanta la API y el worker en una red privada con volúmenes de datos. | `docker compose up -d` |
| [`worker_sincronizacion.py`](worker_sincronizacion.py) | Script de ejecución continua que consulta periódicamente la API y persiste alertas y existencias en SQLite. | Ejecutado dentro del contenedor |
| [`github_actions_workflow.yml`](github_actions_workflow.yml) | Pipeline modelo de CI/CD para GitHub Actions que compila la imagen y verifica el código en cada commit. | Referencia para CI/CD |

---

## 🚀 Cómo levantarlo con Docker Compose

Desde la raíz del repositorio:

```bash
# 1. Crear el archivo de entorno local
cp modulos/07-despliegue-y-cloud/ejemplos/.env.example .env

# 2. Iniciar todos los servicios orquestados
docker compose -f modulos/07-despliegue-y-cloud/ejemplos/docker-compose.yml up --build -d

# 3. Ver logs en tiempo real del worker comunicándose con la API
docker compose -f modulos/07-despliegue-y-cloud/ejemplos/docker-compose.yml logs -f

# 4. Detener los servicios
docker compose -f modulos/07-despliegue-y-cloud/ejemplos/docker-compose.yml down
```
