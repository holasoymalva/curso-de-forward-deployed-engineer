# Módulo 07: Despliegue y cloud

> **Nivel:** 🟡 Intermedio  
> **Duración aproximada:** 6 horas  
> **Prerrequisitos:** [Módulo 01: Herramientas esenciales](../01-herramientas-esenciales/README.md) y [Módulo 06: Integración de sistemas](../06-integracion-de-sistemas/README.md)  

---

## 🎯 ¿Por qué importa para un FDE?

La frase más temida en la ingeniería de software es: *"Pero en mi máquina sí funcionaba"*. 

Un Forward Deployed Engineer no entrega código suelto en carpetas de descargas ni pide al cliente que instale librerías manualmente. Un FDE entrega **aplicaciones empaquetadas en contenedores Docker**, configuradas limpiamente según los principios de *The Twelve-Factor App*, con inyección segura de secretos mediante variables de entorno y listas para correr de forma predecible tanto en una máquina virtual local (*On-Premise*) detrás de un firewall como en nubes públicas (AWS, GCP, Azure).

---

## ✅ Objetivos de aprendizaje

Al terminar este módulo podrás:

- Aplicar la metodología *12-Factor App* en integraciones: configuración desacoplada, procesos sin estado y logs como flujos.
- Construir imágenes de Docker ligeras y seguras usando archivos `Dockerfile` basados en `python:3.10-slim` ejecutando como usuario no privilegiado (`non-root`).
- Orquestar múltiples servicios locales (la API simulada + el worker de sincronización) usando `docker compose`.
- Administrar variables de entorno y secretos con archivos `.env` sin exponer credenciales en repositorios públicos.
- Comprender arquitecturas de despliegue en clientes: IaaS vs. PaaS vs. Serverless, redes privadas, VPNs y automatización básica con GitHub Actions.

---

## 📖 Lecciones

| # | Lección | Nivel | Duración |
|---|---------|-------|----------|
| 01 | [De mi máquina a producción: Metodología 12-Factor](lecciones/01-de-mi-maquina-a-produccion-12-factor.md) | 🟡 | 25 min |
| 02 | [Docker esencial: Imágenes, contenedores y Dockerfile](lecciones/02-docker-imagenes-contenedores-y-dockerfile.md) | 🟡 | 30 min |
| 03 | [Orquestación con Docker Compose y gestión de secretos](lecciones/03-orquestacion-con-docker-compose-y-secretos.md) | 🟡 | 30 min |
| 04 | [Nube, CI/CD básico y despliegues On-Premise](lecciones/04-conceptos-cloud-ci-cd-y-entornos-on-premise.md) | 🟡 | 30 min |

---

## 💻 Ejemplos

Archivos de configuración y empaquetado listos para producción:
- Consulta [ejemplos/README.md](ejemplos/README.md).
  - [Plantilla de variables de entorno (`.env.example`)](ejemplos/.env.example)
  - [Imagen Docker de producción (`Dockerfile`)](ejemplos/Dockerfile)
  - [Orquestación de servicios (`docker-compose.yml`)](ejemplos/docker-compose.yml)
  - [Worker autónomo de sincronización (`worker_sincronizacion.py`)](ejemplos/worker_sincronizacion.py)
  - [Pipeline modelo de CI/CD (`github_actions_workflow.yml`)](ejemplos/github_actions_workflow.yml)

---

## 🏋️ Ejercicios

Prácticas de contenedorización y despliegue:
- Consulta [ejercicios/README.md](ejercicios/README.md).
  - [Ejercicio 01: Dockerización segura del conector de Halcón](ejercicios/01-dockerizacion-del-conector.md)
  - [Ejercicio 02: Despliegue completo con Docker Compose y persistencia](ejercicios/02-orquestacion-con-docker-compose.md)

---

## 🎥 Guion sugerido para video

1. **Gancho (1-2 min):** *"Le mandas el script a Roberto Treviño. En su máquina falla porque él tiene Python 3.8 y tú usaste tipos de Python 3.10. Con Docker, empaquetas el intérprete, el código y las configuraciones en una caja sellada: si corre en tu laptop, corre exactamente igual en el servidor corporativo de Halcón."*
2. **Concepto (5-8 min):** Diferencia entre imagen y contenedor. Capas de Docker y buenas prácticas de seguridad (¡nunca correr como `root`!).
3. **Demo (6-8 min):** Ejecutar `docker compose up -d` y mostrar cómo la API simulada y el worker se levantan e interactúan en una red virtual privada.
4. **Cierre (1-2 min):** Resumen de cómo documentar el archivo `.env.example` y presentación del reto del Ejercicio 01.

---

## 📚 Para profundizar

- [The Twelve-Factor App (Manifiesto libre)](../../recursos/lecturas.md#☁️-despliegue-contenedores-y-buenas-prácticas).
- [Docker Documentation (Tutorial oficial)](../../recursos/lecturas.md#☁️-despliegue-contenedores-y-buenas-prácticas).

---

⬅️ [Módulo 06: Integración de sistemas](../06-integracion-de-sistemas/README.md) | 🏠 [Índice](../../README.md) | [Módulo 08: Debugging y producción](../08-debugging-y-produccion/README.md) ➡️
