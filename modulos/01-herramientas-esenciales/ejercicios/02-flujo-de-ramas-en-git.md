# Ejercicio 02: Flujo completo de ramas y Pull Request en Git

> **Nivel:** 🟢 Principiante · **Tiempo estimado:** 35 min

---

## Contexto

Vas a crear tu primer conector de sincronización para Distribuidora Halcón. Para no comprometer la estabilidad del repositorio del equipo, debes aplicar las mejores prácticas profesionales de Git: crear una rama de funcionalidad aislada, garantizar que ningún secreto o archivo temporal pueda ser versionado y generar commits claros con la convención estándar.

---

## Lo que tienes que hacer

Realiza la siguiente secuencia de pasos en tu terminal (puedes crear un repositorio temporal o trabajar en una rama aislada):

1. **Creación de rama:** Crea una nueva rama llamada `feature/conector-base-halcon` a partir de tu rama actual.
2. **Protección de secretos:** Crea o verifica que exista un archivo `.gitignore` que ignore expresamente archivos `.env`, carpetas `.venv/` y bases de datos `*.sqlite3`.
3. **Simulación de código:** Crea un archivo llamado `config.py` con una función sencilla que lea la variable de entorno `CLIENT_ID`.
4. **Commit atómico:** Agrega a staging únicamente los archivos relevantes (`.gitignore` y `config.py`) y genera un commit profesional siguiendo la convención de mensajes:
   - Formato: `feat(conector): inicializar configuracion base de conexion`
5. **Verificación:** Ejecuta `git log -n 1 --stat` para corroborar que el commit contenga únicamente los archivos previstos.
6. **Redacción de Pull Request:** Escribe un borrador de descripción de Pull Request (en Markdown) listo para enviar a revisión a tus compañeros de Nexo.

---

## Criterios de aceptación

- [ ] La rama `feature/conector-base-halcon` está creada.
- [ ] El `.gitignore` bloquea efectivamente la subida de un archivo ficticio `.env`.
- [ ] El mensaje de commit sigue el formato de Conventional Commits.
- [ ] La descripción del PR explica el problema de Halcón, los cambios técnicos realizados y cómo probarlo.

---

🔑 [Ver solución](soluciones/02-flujo-de-ramas-en-git.md)
