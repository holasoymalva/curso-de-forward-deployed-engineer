# Lección 03: Entorno de Python: aislamiento y dependencias

> **Nivel:** 🟢 Principiante · **Duración estimada:** 20 min

---

## Situación

Llegas a un servidor Linux en las oficinas de Distribuidora Halcón. Intentas ejecutar un script instalando un paquete globalmente con `pip install requests` y la terminal te arroja un error alarmante:

```text
error: externally-managed-environment
× This environment is externally managed
╰─> To install Python packages system-wide, try apt install python3-xyz...
```

O peor aún: instalas una librería que actualiza una dependencia del sistema y dejas de poder usar herramientas críticas del servidor de Roberto Treviño.

Aislar tus entornos en Python no es opcional: es la única forma de garantizar que tu código funcione exactamente igual en tu computadora portátil, en el servidor de pruebas y en el entorno productivo del cliente.

---

## Conceptos clave

### 1. ¿Por qué necesitamos entornos virtuales?

Por defecto, Python instala librerías en una carpeta compartida a nivel de todo el sistema operativo. Si el Proyecto A necesita `urllib3==1.26.15` y el Proyecto B requiere `urllib3==2.1.0`, ambos entrarán en conflicto destructivo (*dependency hell*).

Un **entorno virtual** (`venv`) es simplemente un directorio autocontenido que contiene una copia limpia de Python y su propio gestor `pip`:

```mermaid
flowchart TD
    subgraph Sistema Operativo
        PySys["Python del Sistema (3.10)"]
    end

    subgraph Entorno Virtual (Proyecto Halcon)
        VenvPy["Python aislado"]
        VenvPip["pip propio"]
        VenvLibs["Librerías instaladas aisladas"]
    end

    PySys -->|"Crea sandbox"| VenvPy
    VenvPip -->|"Instala únicamente en"| VenvLibs
```

---

### 2. Creación y activación de un entorno virtual con `venv`

La herramienta `venv` viene incluida en la biblioteca estándar de Python (no necesitas instalar nada externo):

```bash
# 1. Crear el entorno en una carpeta llamada '.venv'
python3 -m venv .venv

# 2. Activar el entorno (en Linux / macOS)
source .venv/bin/activate

# (En Windows PowerShell sería: .venv\Scripts\Activate.ps1)

# Notarás que el prompt de tu terminal cambia para indicar que está activo:
# (.venv) usuario@maquina:~/proyecto $
```

Para salir del entorno virtual cuando termines de trabajar:
```bash
deactivate
```

---

### 3. Congelar y reproducir dependencias con `requirements.txt`

Cuando entregas tu solución a un cliente o a otro miembro del equipo, no subes la carpeta `.venv` a Git (¡pesa cientos de megabytes y no es portable entre distintos sistemas operativos!). 

En su lugar, declaras tus dependencias en un archivo de texto llamado `requirements.txt`:

```text
# Dependencias necesarias para el conector de Halcon
requests>=2.31.0
python-dotenv>=1.0.0
```

Para instalar todas las dependencias declaradas en una sola instrucción:
```bash
pip install -r requirements.txt
```

Para listar las versiones exactas instaladas en tu entorno:
```bash
pip freeze > requirements.lock
```

---

### 4. La filosofía de este curso: Priorizar la biblioteca estándar

Siempre que sea posible, un FDE experimentado prefiere resolver problemas utilizando la **biblioteca estándar de Python**:
- Manejo de archivos JSON: módulo `json`
- Archivos tabulares: módulo `csv`
- Conexión a bases de datos relacionales: módulo `sqlite3`
- Consumo HTTP básico y servidores locales: módulos `urllib.request` y `http.server`
- Línea de comandos estructurada: módulo `argparse`

¿Por qué? Porque un script que solo usa la biblioteca estándar puede ejecutarse **en cualquier servidor del cliente sin necesidad de instalar dependencias externas ni pedir permisos especiales a TI**.

---

## Errores comunes

- **Olvidar activar el entorno virtual antes de instalar librerías:** Terminas instalando paquetes en el Python global de tu computadora sin darte cuenta.
- **Subir la carpeta `venv/` o `.venv/` a Git:** Llena el repositorio de archivos binarios innecesarios. Debe estar siempre en tu `.gitignore`.
- **No fijar versiones mínimas en `requirements.txt`:** Si dejas librerías sin versión, una actualización futura del proveedor puede romper tu conector sin previo aviso.

---

## En el día a día de un FDE

En la primera hora con Roberto Treviño, cuando te pregunte: *"¿Cuántas librerías y componentes externos necesitan que instalemos en nuestro servidor principal?"*, tú podrás responder con total calma:

> *"Ninguna, Roberto. El conector corre sobre el Python 3.10 que ya tienen instalado y solo utiliza librerías nativas del sistema, o bien corre encapsulado en un contenedor Docker sin tocar nada de su servidor"*. 

Esa respuesta elimina semanas de burocracia de aprobaciones de seguridad.

---

## Resumen

- Los entornos virtuales aíslan las librerías de cada proyecto para evitar conflictos de versiones.
- El comando `python3 -m venv .venv` crea el entorno y `source .venv/bin/activate` lo habilita.
- `requirements.txt` permite reproducir el entorno en cualquier máquina con `pip install -r`.
- Maximizar el uso de la biblioteca estándar de Python ahorra fricciones de despliegue en clientes corporativos.

---

## Preguntas de repaso

1. ¿Por qué nunca se debe subir la carpeta `.venv` a un repositorio de Git?
2. ¿Cómo verificas qué versión de Python y qué ejecutable de `pip` estás utilizando en este momento?
3. ¿Qué ventaja operativa tiene para un FDE escribir un conector que no requiere `pip install`?

---

⬅️ [Lección anterior: Git profesional](02-git-y-control-de-versiones.md) | 📦 [Módulo](../README.md) | [Siguiente lección: curl y jq](04-herramientas-de-diagnostico-curl-jq.md) ➡️
