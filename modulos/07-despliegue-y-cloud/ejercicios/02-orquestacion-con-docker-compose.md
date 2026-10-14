# Ejercicio 02: Despliegue completo con Docker Compose y persistencia

> **Nivel:** 🟡 Intermedio · **Tiempo estimado:** 45 min

---

## Contexto

Deseas que cualquier persona del equipo de Nexo o de Distribuidora Halcón pueda clonar el repositorio y levantar todo el sistema con un único comando: la API simulada y el worker de sincronización comunicándose en una red virtual privada y persistiendo las existencias en un volumen montado.

---

## Lo que tienes que hacer

1. Crea un archivo `docker-compose.yml` que defina:
   - **Servicio `api`:** Basado en `Dockerfile.api`, escuchando en puerto 8000.
   - **Servicio `worker`:** Basado en `Dockerfile`, dependiendo de `api` (`depends_on`), configurando `API_BASE_URL=http://api:8000`.
   - **Volumen persistente `datos_volumen`:** Montado en la ruta `/app/datos` dentro del worker.
   - **Límites de recursos:** Limitar el worker a un máximo de `256M` de memoria.
2. Inicia los servicios con `docker compose up -d`.
3. Verifica con `docker compose ps` que ambos servicios estén en estado `running`.
4. Detén los contenedores con `docker compose down` y vuelve a levantarlos para comprobar que la base de datos persistió intacta en el volumen.

---

## Criterios de aceptación

- [ ] Ambos servicios se levantan en segundo plano sin errores.
- [ ] El worker se comunica con la API resolviendo el nombre DNS `api`.
- [ ] La base SQLite persiste tras reiniciar los contenedores.
- [ ] El consumo de memoria está restringido a 256 MB.

---

🔑 [Ver solución](soluciones/02-orquestacion-con-docker-compose.md)
