"""
Ejemplo de uso de LinkSanity como módulo
"""

from linksanity.services.reader import BookmarkReader
from linksanity.services.organizer import BookmarkOrganizer
from linksanity.services.exporter import BookmarkExporter


def ejemplo_basico():
    """Ejemplo básico de lectura y organización"""

    # 1. Leer bookmarks de Chrome
    bookmarks = BookmarkReader.read_chrome_bookmarks("ruta/a/Bookmarks")

    # 2. Eliminar duplicados
    bookmarks = BookmarkOrganizer.remove_duplicates(bookmarks)

    # 3. Formatear títulos
    bookmarks = BookmarkOrganizer.apply_formatting(bookmarks, title_style="clean")

    # 4. Ordenar alfabéticamente
    bookmarks = BookmarkOrganizer.sort_bookmarks(bookmarks, by="title")

    # 5. Exportar a HTML
    BookmarkExporter.to_html(bookmarks, "bookmarks_organizados.html")

    print(f"✅ {len(bookmarks)} bookmarks procesados")


def ejemplo_filtrado():
    """Ejemplo de filtrado y búsqueda"""

    # Leer bookmarks
    bookmarks = BookmarkReader.read_html_bookmarks("bookmarks.html")

    # Filtrar solo bookmarks de GitHub
    github_bookmarks = BookmarkOrganizer.filter_bookmarks(
        bookmarks, domain="github.com"
    )

    # Filtrar por palabra clave
    python_bookmarks = BookmarkOrganizer.filter_bookmarks(bookmarks, keyword="python")

    # Agrupar por carpeta
    por_carpeta = BookmarkOrganizer.group_by_folder(bookmarks)

    print(f"GitHub bookmarks: {len(github_bookmarks)}")
    print(f"Python bookmarks: {len(python_bookmarks)}")
    print(f"Carpetas: {len(por_carpeta)}")


def ejemplo_analisis():
    """Ejemplo de análisis y reportes"""

    bookmarks = BookmarkReader.read_chrome_bookmarks("Bookmarks")

    # Buscar URLs rotas
    broken = BookmarkOrganizer.find_broken_urls(bookmarks)
    print(f"URLs sospechosas: {len(broken)}")

    # Generar reporte completo
    BookmarkExporter.generate_report(bookmarks, "reporte.md")

    # Exportar a múltiples formatos
    BookmarkExporter.to_json(bookmarks, "bookmarks.json")
    BookmarkExporter.to_markdown(bookmarks, "bookmarks.md")
    BookmarkExporter.to_csv(bookmarks, "bookmarks.csv")


if __name__ == "__main__":
    print("Ejecuta las funciones de ejemplo:")
    print("  ejemplo_basico()")
    print("  ejemplo_filtrado()")
    print("  ejemplo_analisis()")
