# Ejemplos del Módulo 01: Herramientas esenciales

Esta carpeta contiene scripts de apoyo y archivos modelo para automatizar tareas rutinarias de desarrollo y diagnóstico en servidores.

---

## 📂 Archivos disponibles

| Archivo | Descripción | Cómo ejecutarlo |
|---------|-------------|-----------------|
| [`diagnostico_sistema.sh`](diagnostico_sistema.sh) | Script en Bash que inspecciona el entorno del sistema operativo: versión de Python, espacio en disco, variables de entorno y disponibilidad de la API simulada. | `bash diagnostico_sistema.sh` |
| [`preparar_entorno.sh`](preparar_entorno.sh) | Script que automatiza la creación de un entorno virtual `.venv` limpio y verifica librerías básicas. | `bash preparar_entorno.sh` |
| [`gitignore_ejemplo`](gitignore_ejemplo) | Archivo modelo de `.gitignore` listo para copiar en la raíz de cualquier proyecto de integración FDE. | `cp gitignore_ejemplo .gitignore` |

---

## 🛠️ Requisitos

- Sistema operativo tipo Unix (macOS, Linux o Windows con WSL).
- `bash` o `zsh`.
- `curl` instalado en tu sistema.
