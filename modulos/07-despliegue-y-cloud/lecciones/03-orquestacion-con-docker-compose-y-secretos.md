# Lección 03: Orquestación con Docker Compose y gestión de secretos

> **Nivel:** 🟡 Intermedio · **Duración estimada:** 30 min

---

## Situación

Para probar la solución completa de Halcón necesitas correr dos servicios coordinados:
1. La **API simulada de Halcón** (escuchando peticiones en el puerto 8000).
2. El **Worker de sincronización** que consulta pedidos y escribe alertas en SQLite.

Levantar ambos a mano en terminales separadas, configurando IPs y puertos manualmente, es propenso a errores. Además, ¿cómo se comunican dos contenedores entre sí sin exponer puertos al exterior?

La herramienta estándar para orquestar múltiples contenedores y redes locales es **Docker Compose**.

---

## Conceptos clave

### 1. ¿Qué es Docker Compose?

Docker Compose es una herramienta para definir y ejecutar aplicaciones multi-contenedor mediante un archivo declarativo en formato YAML (`docker-compose.yml`).

Con un solo comando (`docker compose up -d`):
- Se crea una **red virtual privada** donde los contenedores se descubren por su nombre de servicio (DNS interno).
- Se inyectan las variables de entorno desde un archivo `.env` seguro.
- Se configuran **volúmenes persistentes** para que las bases de datos no se borren al apagar el contenedor.

```mermaid
flowchart TD
    subgraph Red Virtual Privada (halcon-net)
        API["Servicio 1: api-halcon<br/>(Expone puerto 8000)"]
        WORKER["Servicio 2: worker-sync<br/>(Consume http://api-halcon:8000)"]
        API <-->|"Comunicación directa por DNS"| WORKER
    end

    VOL[("Volumen en disco local<br/>/datos -> halcon.db")]
    WORKER -->|"Persistencia atómica"| VOL
```

---

### 2. Estructura de `docker-compose.yml`

```yaml
version: "3.8"

services:
  # Servicio 1: API de pruebas del cliente
  api-halcon:
    build:
      context: ../../../
      dockerfile: modulos/07-despliegue-y-cloud/ejemplos/Dockerfile.api
    container_name: halcon_api
    environment:
      - PUERTO=8000
      - FALLAS=0.1 # 10 % de fallas para probar resiliencia
      - LIMITE_POR_MINUTO=30
    ports:
      - "8000:8000"
    networks:
      - red-halcon

  # Servicio 2: Worker de sincronización de Nexo
  worker-sync:
    build:
      context: ../../../
      dockerfile: modulos/07-despliegue-y-cloud/ejemplos/Dockerfile
    container_name: nexo_worker
    depends_on:
      - api-halcon
    environment:
      - API_BASE_URL=http://api-halcon:8000 # ¡Se conecta usando el nombre del servicio!
      - CLIENT_ID=${CLIENT_ID:-nexo-demo}
      - CLIENT_SECRET=${CLIENT_SECRET:-secreto-de-practica}
      - INTERVALO_SEG=60
    volumes:
      - datos_db:/app/datos
    networks:
      - red-halcon
    deploy:
      resources:
        limits:
          memory: 256M

volumes:
  datos_db:

networks:
  red-halcon:
    driver: bridge
```

---

### 3. Resolución de nombres interna (DNS de Docker)

Fíjate en esta línea:
```yaml
API_BASE_URL=http://api-halcon:8000
```

Dentro de la red privada de Docker, los contenedores **no usan `localhost` ni IPs numéricas fijas**. Docker incluye un servidor DNS interno que resuelve automáticamente el nombre del servicio (`api-halcon`) hacia la IP virtual asignada a ese contenedor.

---

### 4. Ciclo de vida con Docker Compose

```bash
# Iniciar todos los servicios en segundo plano y compilar si es necesario
docker compose up -d --build

# Ver el estado y consumo de los servicios
docker compose ps

# Ver logs consolidados de ambos contenedores
docker compose logs -f

# Detener los servicios sin borrar los volúmenes de datos
docker compose down

# Detener los servicios y limpiar volúmenes (¡destruye datos locales!)
docker compose down -v
```

---

## Errores comunes

- **Usar `localhost` dentro de un contenedor para hablar con otro contenedor:** Para un contenedor, `localhost` es **él mismo**. Si el worker llama a `http://localhost:8000`, buscará la API dentro de su propio contenedor y fallará con `Connection refused`. Debe usar el nombre del servicio: `http://api-halcon:8000`.
- **Olvidar persistir datos con volúmenes:** Si guardas una base SQLite dentro del contenedor sin montar un volumen, cuando ejecutes `docker compose down`, la base de datos se destruirá para siempre.
- **Subir el archivo `.env` a Git:** Los valores sensibles de producción se gestionan en el servidor del cliente, no en el repositorio.

---

## En el día a día de un FDE

En una demostración técnica con Roberto Treviño, ejecutas un único comando:
`docker compose up -d` y en 5 segundos le muestras la arquitectura completa corriendo de forma aislada, sin haber instalado una sola librería en su máquina.

---

## Resumen

- Docker Compose permite definir arquitecturas multi-contenedor en un archivo YAML declarativo.
- Los contenedores se comunican en una red privada usando los nombres de los servicios como dominios DNS.
- Los volúmenes montados garantizan la persistencia de bases de datos independientemente del ciclo de vida del contenedor.
- Permite fijar límites de memoria y CPU para garantizar estabilidad en servidores de clientes.

---

## Preguntas de repaso

1. Si el contenedor A necesita enviar una petición HTTP al contenedor B en Docker Compose, ¿por qué no debe utilizar la dirección `http://localhost`?
2. ¿Qué comando detiene los contenedores de Docker Compose conservando intactos los datos de la base de datos montada en volúmenes?
3. ¿Cómo define Docker Compose los límites máximos de memoria RAM que puede consumir un contenedor?

---

⬅️ [Lección anterior: Docker esencial](02-docker-imagenes-contenedores-y-dockerfile.md) | 📦 [Módulo](../README.md) | [Siguiente lección: Cloud y CI/CD](04-conceptos-cloud-ci-cd-y-entornos-on-premise.md) ➡️
