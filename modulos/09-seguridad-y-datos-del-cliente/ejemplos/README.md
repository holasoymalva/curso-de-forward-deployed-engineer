# Ejemplos del Módulo 09: Seguridad y datos del cliente

Herramientas prácticas para la protección, sanitización y auditoría de seguridad en integraciones con clientes.

---

## 📂 Archivos disponibles

| Archivo | Descripción | Uso |
|---------|-------------|-----|
| [`enmascarar_pii.py`](enmascarar_pii.py) | Script de Python (biblioteca estándar) que lee `tiendas.csv`, aplica minimización de datos y enmascara campos sensibles (nombres, correos, teléfonos). | `python enmascarar_pii.py` |
| [`checklist_seguridad_implementacion.md`](checklist_seguridad_implementacion.md) | Lista de verificación pre-producción de 25 controles de seguridad indispensables antes del despliegue en un cliente enterprise. | Documento de revisión técnica |

---

## 🚀 Cómo ejecutar el ejemplo de enmascaramiento

Desde la raíz del repositorio:

```bash
python modulos/09-seguridad-y-datos-del-cliente/ejemplos/enmascarar_pii.py
```

El script leerá `recursos/caso-de-estudio/datos/tiendas.csv` y generará un archivo sanitizado en la misma carpeta demostrando la diferencia entre datos crudos y datos protegidos.
