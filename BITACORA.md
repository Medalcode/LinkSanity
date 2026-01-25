# Bitácora de Desarrollo - LinkSanity

## 🚀 Tareas Realizadas (Estructura Escalable)

### 🏗️ Arquitectura y Refactorización

- **Nueva Estructura de Paquetes**: Se implementó una estructura basada en `src/linksanity` siguiendo el estándar de empaquetado profesional de Python.
- **Capa de Dominio**: Creación de `domain/models.py` para centralizar la entidad `Bookmark`.
- **Capa de Servicios**: Separación de lógica en servicios especializados (`reader.py`, `writer.py`, `organizer.py`, `exporter.py`).
- **Desacoplamiento del CLI**: Refactorización de `main.py` para separar la lógica de argumentos en `cli/interface.py`.
- **Organización de Scripts**: Traslado de scripts de utilidad y hacks de sincronización a la carpeta `scripts/`.
- **Gestión de Documentación**: Movimiento de reportes, ejemplos y documentación técnica a la carpeta `docs/`.

### 📦 Empaquetado y Configuración

- **Configuración de Instalación**: Creación de `setup.py` para permitir la instalación en modo editable (`pip install -e .`).
- **Unificación de Herramientas**: Actualización de `pyproject.toml` con configuraciones optimizadas para `black`, `mypy` y `pytest`.
- **Entry Points**: Definición del comando `linksanity` via `console_scripts` en `setup.py`.

### 🛠️ Calidad y Testing

- **Refactorización de Tests**: Actualización de la suite de pruebas para utilizar los nuevos modelos e importaciones absolutas.
- **Verificación Estática**: Resolución de errores de tipado (`mypy`) y estilo (`flake8`).
- **Compatibilidad**: Ajuste de importaciones y `sys.path` en scripts legacy para mantener la funcionalidad.

---

## 📅 Tareas Pendientes (Roadmap Próximo)

### 🔧 Mejoras Funcionales

- **Detección de Duplicados Inteligente**: Implementar lógica para detectar URLs similares o redirecciones.
- **Tags Personalizados**: Permitir al usuario añadir etiquetas a los bookmarks más allá de las categorías automáticas.
- **Verificación HTTP Avanzada**: Mejorar el motor de búsqueda de links rotos con reintentos y manejo de errores HTTP.

### 🌐 Interfaz y UX

- **Dashboard Web**: Creación de una interfaz web local para gestionar bookmarks visualmente.
- **Configuración Persistente**: Implementar un archivo `config.yaml` o `.json` para personalizar categorías y reglas de organización.

### 🔄 Integraciones

- **Sincronización con GitHub/Gist**: Permitir guardar backups cifrados en servicios externos.
- **Soporte para más navegadores**: Ampliar la compatibilidad nativa (Opera, Brave, Safari).
