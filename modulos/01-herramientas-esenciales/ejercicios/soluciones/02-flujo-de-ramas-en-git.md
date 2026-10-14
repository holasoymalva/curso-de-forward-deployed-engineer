# Solución al Ejercicio 02: Flujo completo de ramas y Pull Request en Git

---

## 💻 1. Comandos ejecutados en la terminal

```bash
# 1. Crear y moverse a la nueva rama
git checkout -b feature/conector-base-halcon

# 2. Verificar que .gitignore contenga las exclusiones de seguridad
cat << 'EOF' > .gitignore
.env
.venv/
*.sqlite3
__pycache__/
EOF

# 3. Crear el archivo de configuración base config.py
cat << 'EOF' > config.py
import os

CLIENT_ID = os.environ.get("CLIENT_ID", "nexo-demo")
API_BASE_URL = os.environ.get("API_BASE_URL", "http://127.0.0.1:8000")
EOF

# 4. Crear un archivo .env falso para verificar que git lo ignore
echo "CLIENT_SECRET=super_secreto_que_no_debe_subirse" > .env

# 5. Comprobar el estado de Git (el archivo .env NO debe aparecer)
git status
# Solo deben aparecer .gitignore y config.py como no rastreados

# 6. Agregar y generar commit atómico
git add .gitignore config.py
git commit -m "feat(conector): inicializar configuracion base de conexion"

# 7. Limpiar el archivo .env temporal de prueba
rm .env
```

---

## 📝 2. Plantilla de Pull Request generada

```markdown
## 📌 Resumen de los cambios

Este Pull Request inicializa la estructura de configuración para el conector de integración de **Distribuidora Halcón**.

### 🎯 Problema resuelto
Halcón requiere conectarse a la API simulada de pedidos utilizando credenciales dinámicas provistas por variables de entorno, evitando quemar secretos en el código fuente.

### 🛠️ Cambios técnicos introducidos
- Se agregó archivo `config.py` con lectura segura de variables de entorno (`CLIENT_ID`, `API_BASE_URL`) con valores por defecto para desarrollo local.
- Se configuró `.gitignore` para bloquear la subida accidental de archivos `.env`, entornos virtuales `.venv` y bases SQLite.

### 🧪 ¿Cómo se probó localmente?
1. Se definió `export CLIENT_ID="halcon-mty"` en la terminal.
2. Se ejecutó `python3 -c "import config; print(config.CLIENT_ID)"` verificando que lea el valor correctamente.
3. Se verificó que crear un archivo `.env` local sea ignorado por `git status`.
```
