# LinkSanity 🔗

**Organizador inteligente de bookmarks del navegador**

LinkSanity es una extensión de Chrome y herramienta en Python para gestionar, organizar, limpiar y formatear tus favoritos del navegador. Compatible con Chrome, Firefox, Edge y archivos HTML exportados.

## 🌟 Características

### Extensión de Chrome (Recomendado)

- ✅ **Organización inteligente**: 60+ categorías específicas sin emojis
- ⭐ **10 Más Visitados**: Carpeta especial con tus bookmarks más usados
- 👻 **Nunca Visitados**: Descubre bookmarks que nunca has abierto
- 🧹 **Elimina duplicados**: Automáticamente al organizar
- 🔗 **Verifica links rotos**: Detecta URLs que no funcionan
- ✨ **Limpieza de títulos**: Formatea y mejora nombres automáticamente
- 📊 **Reportes estadísticos**: Análisis de tus bookmarks

### Herramientas Python (CLI)

- 📖 **Lectura multi-navegador**: Chrome, Firefox, Edge, HTML
- 🔍 **Filtrado avanzado**: Por palabras clave, carpetas o dominios
- 📤 **Exportación múltiple**: JSON, HTML, Markdown, CSV
- 📈 **Reportes detallados**: Estadísticas y análisis completos

## 🚀 Instalación Rápida - Extensión de Chrome

### Paso 1: Cargar la extensión

1. Abre Chrome y ve a: `chrome://extensions/`
2. Activa el **"Modo de desarrollador"** (arriba a la derecha)
3. Click en **"Cargar extensión sin empaquetar"**
4. Selecciona la carpeta: `/home/medalcode/Antigravity/LinkSanity/extension`
5. ¡Listo! Verás el ícono de LinkSanity

### Paso 2: Usa la extensión

1. Click en el ícono de LinkSanity en la barra de Chrome
2. Click en **"✨ Organizar Ahora"**
3. Acepta el permiso de historial (para las carpetas especiales)
4. ¡Tus bookmarks estarán organizados!

## 📚 Categorías Inteligentes

La extensión organiza automáticamente en 60+ categorías:

**Carpetas Especiales:**

- ⭐ 10 Más Visitados (con contador)
- 👻 Nunca Visitados

**Educación:**

- Inacap, TryH4rdCode, Cursos Online, Referencias Web

**Desarrollo Frontend:**

- CSS Frameworks, HTML, Colores, Tipografia
- Componentes UI, Inspiracion Diseno, Herramientas Diseno

**JavaScript:**

- React, Vue, Angular, Svelte, Next.js, TypeScript
- JavaScript Vanilla

**Backend:**

- Node.js, Python Backend, PHP, Java, APIs

**Bases de Datos:**

- SQL Databases, NoSQL Databases

**DevOps:**

- Docker Kubernetes, AWS, Azure, Heroku, Netlify, Vercel
- Git, Hosting Deploy

**Herramientas:**

- Editores Online, Regex, Convertidores, Testing
- Iconos, Imagenes, Optimizacion

**Contenido:**

- YouTube, Medium, Dev.to, Stack Overflow
- Blogs Tutoriales, Documentacion, Cheat Sheets

**Otros:**

- Inteligencia Artificial, Email Services
- Ejercicios, Desafios Frontend, Repositorios
- Sin Categorizar (fallback)

## 🎛️ Funciones de la Extensión

### ✨ Organizar Ahora

- Elimina duplicados automáticamente
- Limpia y formatea títulos
- Categoriza inteligentemente
- Crea carpetas especiales (Más Visitados / Nunca Visitados)
- Ordena alfabéticamente dentro de cada carpeta

### 🧹 Eliminar Duplicados

- Solo elimina duplicados sin reorganizar
- Útil para limpieza rápida

### 🔗 Verificar Links

- Verifica todos tus bookmarks
- Detecta URLs rotas o con problemas
- Muestra un reporte detallado

### 📊 Ver Reporte

- Estadísticas de tus bookmarks
- Conteo por categoría
- Total de bookmarks

## 📖 Uso - Herramientas CLI (Python)

### Interfaz de línea de comandos

```bash
# Instalar en modo editable
pip install -e .

# Ver ayuda
linksanity --help

# O usando el script principal
python3 main.py --help

# Leer bookmarks de Chrome y mostrar estadísticas
linksanity chrome ~/.config/google-chrome/Default/Bookmarks --report
```

### Como módulo de Python

```python
from linksanity.services.reader import BookmarkReader
from linksanity.services.organizer import BookmarkOrganizer
from linksanity.services.exporter import BookmarkExporter

# Leer bookmarks
bookmarks = BookmarkReader.read_chrome_bookmarks("Bookmarks")

# Limpiar y organizar
bookmarks = BookmarkOrganizer.remove_duplicates(bookmarks)
bookmarks = BookmarkOrganizer.apply_formatting(bookmarks, "clean")
bookmarks = BookmarkOrganizer.sort_bookmarks(bookmarks, by="title")

# Exportar
BookmarkExporter.to_html(bookmarks, "organizados.html")
```

## 📂 Estructura del Proyecto

```
LinkSanity/
├── extension/             # Extensión de Chrome (HTML/JS)
├── src/
│   └── linksanity/        # Paquete Principal (Python)
│       ├── domain/        # Entidades y modelos
│       ├── services/      # Lógica de negocio (Reader, Writer, etc.)
│       └── cli/           # Interfaz de línea de comandos
├── scripts/               # Scripts de utilidad y hacks de sync
├── docs/                  # Documentación y reportes
├── tests/                 # Pruebas automatizadas (Pytest)
├── main.py                # Punto de entrada ligero
├── pyproject.toml         # Configuración de herramientas
├── setup.py               # Configuración de instalación
└── README.md
```

## 🔧 Requisitos

### Para la extensión:

- Google Chrome (o Chromium)
- No requiere instalación adicional

### Para herramientas CLI:

- Python 3.9+
- Pip (para instalar herramientas de desarrollo)

### 💻 Desarrollo y Calidad de Código

Este proyecto utiliza herramientas modernas de Python para asegurar la calidad y estabilidad del código.

1.  **Configuración del Entorno**:

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

2.  **Ejecutar Pruebas (Pytest)**:

    ```bash
    pytest
    ```

3.  **Calidad de Código**:
    ```bash
    black .    # Formateo
    flake8 .   # Linting
    mypy .     # Tipado estático
    ```

## 💡 Consejos de Uso

1. **Primera vez**: La extensión pedirá permiso para acceder al historial (necesario para "Más Visitados")
2. **Backups automáticos**: Chrome mantiene tu historial de sincronización
3. **Recarga la extensión**: Después de actualizaciones, recarga en `chrome://extensions/`
4. **Carpetas especiales**: Aparecen siempre al principio de tu barra de favoritos
5. **Verificación de links**: Puede tardar según la cantidad de bookmarks

## 🐛 Solución de Problemas

### La extensión no aparece

- Verifica que el "Modo de desarrollador" esté activado
- Recarga la extensión en `chrome://extensions/`

### No se organizan los bookmarks

- Recarga la extensión
- Cierra y abre Chrome
- Verifica que no haya errores en la consola de la extensión

### Faltan permisos

- La extensión pedirá permisos la primera vez
- Ve a `chrome://extensions/` y verifica que tenga acceso a bookmarks e historial

### Links rotos no se detectan correctamente

- Algunos sitios bloquean verificación automática
- La detección es por intento de conexión, no garantiza 100% precisión

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Puedes consultar el estado del proyecto en la [Bitácora de Desarrollo](BITACORA.md).

1. Fork el proyecto
2. Crea una rama: `git checkout -b feature/MejoraPendiente`
3. Commit: `git commit -m 'Agregar nueva característica'`
4. Push: `git push origin feature/MejoraPendiente`
5. Abre un Pull Request

## 🛣️ Roadmap

- [x] Extensión de Chrome funcional
- [x] Categorización inteligente (60+ categorías)
- [x] Carpetas especiales (Más Visitados / Nunca Visitados)
- [x] Verificación de links rotos
- [x] Limpieza de títulos
- [ ] Dashboard web con búsqueda
- [ ] Configuración personalizable
- [ ] Detección de duplicados inteligente (URLs similares)
- [ ] Exportar/importar configuración
- [ ] Tags personalizados
- [ ] Notas en bookmarks
- [ ] Sincronización con GitHub

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## 👤 Autor

Creado para organizar el caos digital de los bookmarks 🚀

## 🙏 Agradecimientos

- A todos los que luchan contra miles de bookmarks desorganizados
- A la comunidad de desarrollo web por las herramientas increíbles

---

**¿Miles de bookmarks sin orden? ¡LinkSanity está aquí para ayudarte!**
