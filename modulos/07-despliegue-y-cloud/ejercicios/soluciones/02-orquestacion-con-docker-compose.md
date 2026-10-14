# Solución al Ejercicio 02: Despliegue completo con Docker Compose y persistencia

---

## 📄 Archivo `docker-compose.yml` completo

```yaml
version: "3.8"

services:
  # Servicio 1: API Simulada de Halcón
  api:
    build:
      context: ../../../
      dockerfile: modulos/07-despliegue-y-cloud/ejemplos/Dockerfile.api
    container_name: api_simulada
    environment:
      - PUERTO=8000
      - FALLAS=0.1
      - LIMITE_POR_MINUTO=60
    ports:
      - "8000:8000"
    networks:
      - red-interna
    restart: unless-stopped

  # Servicio 2: Worker de Sincronización
  worker:
    build:
      context: ../../../
      dockerfile: modulos/07-despliegue-y-cloud/ejemplos/Dockerfile
    container_name: worker_nexo
    depends_on:
      - api
    environment:
      # Conexión directa mediante el nombre del servicio DNS 'api'
      - API_BASE_URL=http://api:8000
      - CLIENT_ID=nexo-demo
      - CLIENT_SECRET=secreto-de-practica
      - DB_PATH=/app/datos/halcon.db
      - INTERVALO_SYNC_SEG=20
    volumes:
      - datos_volumen:/app/datos
    networks:
      - red-interna
    deploy:
      resources:
        limits:
          memory: 256M
    restart: unless-stopped

volumes:
  datos_volumen:
    name: halcon_datos_persistentes

networks:
  red-interna:
    driver: bridge
```

---

## 🛠️ Comandos de prueba y validación

```bash
# 1. Iniciar los servicios en segundo plano
docker compose up -d --build

# 2. Verificar que ambos contenedores estén corriendo
docker compose ps

# 3. Ver cómo el worker sincroniza contra la API
docker compose logs -f worker

# 4. Detener y reiniciar para validar la persistencia del volumen
docker compose down
docker compose up -d

# 5. La base de datos /app/datos/halcon.db mantiene sus datos intactos
```
