# LinkSanity 🔗

**Organizador inteligente de bookmarks del navegador**

LinkSanity es una herramienta en Python para gestionar, organizar, limpiar y formatear tus favoritos del navegador. Compatible con Chrome, Firefox, Edge y archivos HTML exportados.

## 🌟 Características

- ✅ **Lectura multi-navegador**: Soporta Chrome, Firefox, Edge y archivos HTML
- 🧹 **Limpieza automática**: Elimina duplicados y formatea títulos
- 📊 **Organización inteligente**: Ordena por título, URL, carpeta o fecha
- 🔍 **Filtrado avanzado**: Busca por palabras clave, carpetas o dominios
- 📤 **Exportación múltiple**: JSON, HTML, Markdown, CSV
- 📈 **Reportes detallados**: Estadísticas y análisis de tus bookmarks
- 🔧 **Detección de URLs rotas**: Identifica bookmarks con problemas

## 🚀 Instalación

```bash
# Clonar el repositorio
git clone <tu-repo>
cd LinkSanity

# No requiere dependencias externas (usa solo la biblioteca estándar de Python)
```

## 📖 Uso

### Interfaz de línea de comandos (CLI)

```bash
# Ver ayuda
python main.py --help

# Leer bookmarks de Chrome y mostrar estadísticas
python main.py chrome ~/.config/google-chrome/Default/Bookmarks --report

# Limpiar y exportar a HTML
python main.py chrome Bookmarks --format clean --remove-duplicates --output limpio.html

# Filtrar por palabra clave y exportar a Markdown
python main.py chrome Bookmarks --keyword python --output python.md

# Ordenar por fecha y exportar a JSON
python main.py html bookmarks.html --sort date --output ordenados.json

# Buscar URLs rotas
python main.py chrome Bookmarks --find-broken

# Filtrar por carpeta específica
python main.py chrome Bookmarks --folder "Desarrollo" --output dev.html
```

### Como módulo de Python

```python
from src.bookmark_reader import BookmarkReader
from src.bookmark_organizer import BookmarkOrganizer
from src.bookmark_exporter import BookmarkExporter

# Leer bookmarks
bookmarks = BookmarkReader.read_chrome_bookmarks("Bookmarks")

# Limpiar y organizar
bookmarks = BookmarkOrganizer.remove_duplicates(bookmarks)
bookmarks = BookmarkOrganizer.apply_formatting(bookmarks, "clean")
bookmarks = BookmarkOrganizer.sort_bookmarks(bookmarks, by="title")

# Exportar
BookmarkExporter.to_html(bookmarks, "organizados.html")
BookmarkExporter.generate_report(bookmarks, "reporte.md")
```

## 📂 Estructura del Proyecto

```
LinkSanity/
├── src/
│   ├── __init__.py
│   ├── bookmark_reader.py      # Lectura de bookmarks
│   ├── bookmark_organizer.py   # Organización y filtrado
│   └── bookmark_exporter.py    # Exportación a diferentes formatos
├── main.py                     # Interfaz CLI
├── examples.py                 # Ejemplos de uso
├── requirements.txt
├── .gitignore
└── README.md
```

## 🔧 Funcionalidades Detalladas

### Lectura de Bookmarks

- **Chrome/Chromium/Edge**: Lee el archivo `Bookmarks` (formato JSON)
- **Firefox**: Lee archivos JSON exportados
- **HTML**: Lee archivos HTML exportados (formato universal)

### Formateo de Títulos

- `clean`: Elimina espacios extras y caracteres innecesarios
- `title_case`: Primera letra de cada palabra en mayúscula
- `sentence_case`: Solo la primera letra en mayúscula
- `lower`: Todo en minúsculas
- `upper`: Todo en mayúsculas

### Ordenamiento

- Por título (alfabético)
- Por URL
- Por carpeta (agrupa por carpetas)
- Por fecha de creación

### Filtrado

- Por palabra clave (busca en título y URL)
- Por carpeta
- Por dominio

### Exportación

- **JSON**: Formato estructurado para procesamiento
- **HTML**: Compatible con importación en navegadores
- **Markdown**: Ideal para documentación
- **CSV**: Para hojas de cálculo
- **Reporte**: Análisis estadístico completo

## 📍 Ubicación de Bookmarks

### Chrome/Chromium/Edge (Linux)
```
~/.config/google-chrome/Default/Bookmarks
~/.config/chromium/Default/Bookmarks
~/.config/microsoft-edge/Default/Bookmarks
```

### Chrome (Windows)
```
C:\Users\<usuario>\AppData\Local\Google\Chrome\User Data\Default\Bookmarks
```

### Chrome (macOS)
```
~/Library/Application Support/Google/Chrome/Default/Bookmarks
```

### Firefox
Exporta tus bookmarks desde Firefox:
1. Menú → Bookmarks → Manage Bookmarks
2. Import and Backup → Export Bookmarks to HTML

## 💡 Ejemplos de Uso

### Ejemplo 1: Limpieza básica
```bash
python main.py chrome ~/.config/google-chrome/Default/Bookmarks \
  --remove-duplicates \
  --format clean \
  --sort title \
  --output bookmarks_limpios.html
```

### Ejemplo 2: Análisis de bookmarks
```bash
python main.py chrome Bookmarks --report --find-broken
```

### Ejemplo 3: Extraer bookmarks de un tema
```bash
python main.py chrome Bookmarks \
  --keyword "tutorial" \
  --format title_case \
  --output tutoriales.md
```

### Ejemplo 4: Organizar por carpetas
```bash
python main.py html bookmarks.html \
  --folder "Trabajo" \
  --sort date \
  --output trabajo.json
```

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 🛣️ Roadmap

- [ ] Verificación HTTP de URLs (detectar enlaces realmente rotos)
- [ ] Interfaz gráfica (GUI)
- [ ] Sincronización con navegadores
- [ ] Detección automática de categorías con IA
- [ ] Búsqueda de duplicados por contenido similar
- [ ] Extracción de metadatos (favicon, descripción, etc.)
- [ ] Plugin/extensión para navegadores

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## 👤 Autor

Creado con ❤️ para organizar el caos digital

## 🙏 Agradecimientos

- A todos los que luchan contra el desorden de sus bookmarks
- A la comunidad Python por las excelentes herramientas

---

**¿Tienes miles de bookmarks desorganizados? ¡LinkSanity está aquí para ayudarte! 🚀**
