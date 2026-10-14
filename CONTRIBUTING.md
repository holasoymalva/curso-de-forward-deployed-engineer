# Guía de contribución y mantenimiento

Este documento define las convenciones del curso para que el material se mantenga **consistente, fácil de actualizar y fácil de escalar**.

## 1. Estructura de un módulo

Cada módulo vive en `modulos/NN-nombre-en-kebab-case/` y sigue esta estructura:

```text
modulos/NN-nombre-del-modulo/
├── README.md              # Basado en plantillas/plantilla-modulo.md
├── lecciones/
│   ├── 01-tema.md         # Basado en plantillas/plantilla-leccion.md
│   └── 02-tema.md
├── ejemplos/
│   ├── README.md          # Cómo ejecutar los ejemplos
│   └── *.py | *.sql | ...
└── ejercicios/
    ├── README.md          # Lista de ejercicios del módulo
    ├── 01-ejercicio.md    # Basado en plantillas/plantilla-ejercicio.md
    └── soluciones/
        └── 01-ejercicio.md (o .py, .sql)
```

## 2. Convenciones de nombres

| Elemento | Convención | Ejemplo |
|----------|------------|---------|
| Carpetas de módulo | `NN-nombre-kebab-case` (dos dígitos) | `06-integracion-de-sistemas` |
| Lecciones | `NN-tema-kebab-case.md` | `02-autenticacion.md` |
| Ejercicios | `NN-nombre-kebab-case.md` | `01-cliente-con-reintentos.md` |
| Código | `snake_case.py` | `cliente_paginado.py` |

- Sin acentos, eñes ni espacios en nombres de archivos y carpetas.
- Los títulos dentro de los archivos **sí** llevan acentos y ortografía correcta.

## 3. Niveles

Cada módulo, lección y ejercicio declara su nivel:

- 🟢 **Principiante**
- 🟡 **Intermedio**
- 🔵 **Integrador**

## 4. Estilo de redacción

- Tono cercano, directo y profesional. Habla al estudiante de "tú".
- Explica primero el **por qué** (el problema real del cliente) y después el **cómo**.
- Cada lección termina con un **resumen** y **preguntas de repaso**.
- Usa el [caso de estudio del curso](recursos/caso-de-estudio/README.md) en ejemplos y ejercicios siempre que sea posible.
- Los términos técnicos en inglés se escriben en *cursiva* la primera vez y se agregan al [glosario](recursos/glosario.md).

## 5. Código

- Python 3.10+ y, cuando sea posible, **solo biblioteca estándar** para reducir fricción de instalación.
- Si se necesita una dependencia, declárala en un `requirements.txt` dentro de la carpeta `ejemplos/` del módulo.
- Todo ejemplo debe poder ejecutarse con un comando documentado en `ejemplos/README.md`.
- Nunca incluyas credenciales reales. Usa variables de entorno y archivos `.env.example`.

## 6. Agregar un módulo nuevo

1. Copia `plantillas/plantilla-modulo.md` a `modulos/NN-nuevo-modulo/README.md`.
2. Crea las carpetas `lecciones/`, `ejemplos/` y `ejercicios/soluciones/`.
3. Agrega el módulo a la tabla correspondiente en el [README principal](README.md).
4. Si introduces términos nuevos, actualiza el [glosario](recursos/glosario.md).
5. Revisa que todos los enlaces relativos funcionen.

## 7. Checklist antes de publicar cambios

- [ ] Los enlaces relativos funcionan.
- [ ] Los ejemplos se ejecutan sin errores.
- [ ] Cada ejercicio tiene su solución.
- [ ] El nivel y la duración están indicados.
- [ ] El índice del README principal está actualizado.
