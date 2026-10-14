# Ejercicio 01: Dockerización segura del conector de Halcón

> **Nivel:** 🟡 Intermedio · **Tiempo estimado:** 40 min

---

## Contexto

Roberto Treviño (Gerente de TI) te autoriza a correr el conector en la máquina virtual de Halcón bajo tres condiciones estrictas de seguridad corporativa:
1. La imagen debe basarse en una distribución Linux ligera con parches de seguridad recientes (ej. Debian slim).
2. El proceso **no puede ejecutarse como usuario `root`**; debe correr bajo un usuario del sistema dedicado con UID 1000.
3. Ninguna clave, contraseña ni archivo `.env` puede quedar grabado en las capas de la imagen.

---

## Lo que tienes que hacer

1. Crea un archivo `.dockerignore` en la carpeta de trabajo que excluya explícitamente `.git`, `.env`, `*.db` y `__pycache__`.
2. Escribe un `Dockerfile` que:
   - Use `python:3.10-slim`.
   - Cree un usuario `nexo-app` sin privilegios.
   - Configure variables `PYTHONUNBUFFERED=1`.
   - Copie el script de sincronización.
   - Cambie al usuario no privilegiado con `USER nexo-app`.
   - Establezca el comando de ejecución.
3. Compila la imagen con el tag `nexo/conector-halcon:1.0`.
4. Ejecuta un contenedor de prueba verificando que el usuario activo sea `nexo-app` (`docker run --rm nexo/conector-halcon:1.0 whoami`).

---

## Criterios de aceptación

- [ ] `whoami` dentro del contenedor devuelve `nexo-app` (no `root`).
- [ ] La imagen pesa menos de 200 MB.
- [ ] Ningún secreto ni archivo `.env` está presente dentro de la imagen.

---

🔑 [Ver solución](soluciones/01-dockerizacion-del-conector.md)
