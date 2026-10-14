# Módulo 01: Herramientas esenciales

> **Nivel:** 🟢 Principiante  
> **Duración aproximada:** 4 horas  
> **Prerrequisitos:** [Módulo 00: El rol del Forward Deployed Engineer](../00-el-rol-del-fde/README.md)  

---

## 🎯 ¿Por qué importa para un FDE?

Cuando te conectas por SSH a un servidor Linux de Distribuidora Halcón o estás sentado junto al equipo de TI, no tienes a la mano interfaces gráficas sofisticadas ni botones cómodos. Tu terminal, tu dominio de Git, el aislamiento de tus entornos en Python y utilidades como `curl` y `jq` son tu navaja suiza. 

La fluidez con estas herramientas no solo te hace diez veces más rápido: transmite seguridad técnica inmediata ante clientes exigentes y te permite diagnosticar problemas en minutos en lugar de horas.

---

## ✅ Objetivos de aprendizaje

Al terminar este módulo podrás:

- Navegar y manipular archivos en la terminal con soltura utilizando comandos Unix, pipes (`|`) y filtros (`grep`, `awk`, `head`).
- Gestionar variables de entorno (`export`, `.env`) y entender cómo influyen en la configuración de sistemas.
- Dominar el flujo de trabajo profesional en Git: control de ramas (*branching*), commits atómicos, pull requests y configuración de `.gitignore` para no filtrar secretos.
- Configurar entornos virtuales limpios en Python (`venv`, `pip`, `requirements.txt`) para aislar dependencias sin romper librerías del sistema.
- Probar APIs y procesar respuestas JSON en la línea de comandos usando `curl` y `jq`.

---

## 📖 Lecciones

| # | Lección | Nivel | Duración |
|---|---------|-------|----------|
| 01 | [Terminal y línea de comandos para integración](lecciones/01-terminal-y-linea-de-comandos.md) | 🟢 | 25 min |
| 02 | [Git profesional y trabajo colaborativo](lecciones/02-git-y-control-de-versiones.md) | 🟢 | 25 min |
| 03 | [Entorno de Python: aislamiento y dependencias](lecciones/03-entorno-python-y-paquetes.md) | 🟢 | 20 min |
| 04 | [Herramientas de diagnóstico: curl y jq](lecciones/04-herramientas-de-diagnostico-curl-jq.md) | 🟢 | 25 min |

---

## 💻 Ejemplos

Scripts listos para ejecutar y archivos de configuración modelo:
- Consulta [ejemplos/README.md](ejemplos/README.md).
  - [Script de diagnóstico del sistema (`diagnostico_sistema.sh`)](ejemplos/diagnostico_sistema.sh)
  - [Script de preparación de entorno (`preparar_entorno.sh`)](ejemplos/preparar_entorno.sh)
  - [Plantilla de `.gitignore` para proyectos de FDE](ejemplos/gitignore_ejemplo)

---

## 🏋️ Ejercicios

Casos prácticos de automatización y control de versiones:
- Consulta [ejercicios/README.md](ejercicios/README.md).
  - [Ejercicio 01: Automatización con Bash y análisis de archivos](ejercicios/01-automatizacion-con-bash.md)
  - [Ejercicio 02: Flujo completo de ramas y Pull Request en Git](ejercicios/02-flujo-de-ramas-en-git.md)

---

## 🎥 Guion sugerido para video

1. **Gancho (1-2 min):** *"Estás en una sesión compartida por Zoom con Roberto Treviño. Necesitas verificar si el servidor de Halcón puede comunicarse con la API de Nexo y extraer el token de prueba. Si abres el navegador y te pones a buscar botones, dudas. Si en la terminal tiras un comando con `curl` y filtras con `jq` en 10 segundos, tienes el control de la llamada."*
2. **Concepto (5-8 min):** Filosofía Unix: herramientas pequeñas que hacen una sola cosa bien conectadas por tuberías (`|`). Flujo de ramas en Git.
3. **Demo (6-8 min):** Ejecutar `diagnostico_sistema.sh` y hacer una consulta con `curl` y `jq` a la API simulada.
4. **Cierre (1-2 min):** Resumen de buenas prácticas de `.gitignore` (¡nunca subir contraseñas ni `.env`!) y planteamiento del Ejercicio 01.

---

## 📚 Para profundizar

- [The Missing Semester of Your CS Education (MIT)](../../recursos/lecturas.md#💻-herramientas-unix-y-git).
- [Pro Git Book (Libro libre)](../../recursos/lecturas.md#💻-herramientas-unix-y-git).

---

⬅️ [Módulo 00: El rol del FDE](../00-el-rol-del-fde/README.md) | 🏠 [Índice](../../README.md) | [Módulo 02: Python para FDE](../02-python-para-fde/README.md) ➡️
