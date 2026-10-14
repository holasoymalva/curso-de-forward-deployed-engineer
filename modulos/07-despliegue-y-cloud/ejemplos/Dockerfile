# ==============================================================================
# Dockerfile para Worker de Sincronización Nexo (Módulo 07)
# Basado en Python 3.10-slim con usuario no privilegiado (Seguridad empresarial).
# ==============================================================================

FROM python:3.10-slim

# Evitar que Python bufferice los logs y evitar generar archivos .pyc
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Crear usuario seguro sin privilegios de root
RUN useradd -m -u 1000 appuser

# Directorio de trabajo
WORKDIR /app

# Crear carpeta para volumen de datos y asignar permisos al usuario
RUN mkdir -p /app/datos && chown -R appuser:appuser /app

# Copiar scripts necesarios
COPY --chown=appuser:appuser modulos/06-integracion-de-sistemas/ejemplos/cliente_resiliente.py /app/cliente_resiliente.py
COPY --chown=appuser:appuser modulos/07-despliegue-y-cloud/ejemplos/worker_sincronizacion.py /app/worker_sincronizacion.py

# Cambiar a usuario no root
USER appuser

# Comando de ejecución
CMD ["python", "worker_sincronizacion.py"]
