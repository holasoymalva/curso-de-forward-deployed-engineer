# Solución al Ejercicio 01: Dockerización segura del conector de Halcón

---

## 📄 1. Archivo `.dockerignore`

```text
.git
.gitignore
.env
.env.*
!.env.example
__pycache__/
*.pyc
*.db
*.sqlite3
logs/
*.log
```

---

## 🐳 2. Archivo `Dockerfile` seguro

```dockerfile
# 1. Imagen base oficial ligera
FROM python:3.10-slim

# 2. Configurar entorno de Python
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# 3. Crear usuario no privilegiado con UID explícito
RUN useradd -m -u 1000 nexo-app

# 4. Directorio de trabajo
WORKDIR /app

# 5. Crear carpeta de persistencia y asignar permisos
RUN mkdir -p /app/datos && chown -R nexo-app:nexo-app /app

# 6. Copiar dependencias y código con permisos del usuario seguro
COPY --chown=nexo-app:nexo-app modulos/06-integracion-de-sistemas/ejemplos/cliente_resiliente.py /app/cliente_resiliente.py
COPY --chown=nexo-app:nexo-app modulos/07-despliegue-y-cloud/ejemplos/worker_sincronizacion.py /app/worker.py

# 7. Cambiar al usuario no privilegiado
USER nexo-app

# 8. Comando de ejecución
CMD ["python", "worker.py"]
```

---

## 💻 3. Comandos de verificación en la terminal

```bash
# 1. Construir la imagen
docker build -t nexo/conector-halcon:1.0 -f Dockerfile .

# 2. Verificar que no se ejecuta como root (debe imprimir 'nexo-app')
docker run --rm nexo/conector-halcon:1.0 whoami

# 3. Verificar el peso de la imagen (debe rondar los 130-150 MB)
docker images | grep nexo/conector-halcon
```
