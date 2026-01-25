#!/usr/bin/env python3
"""
Script para organizar bookmarks de forma más visible
Agrupa por categorías principales
"""

from linksanity.services.reader import BookmarkReader
from linksanity.domain.models import Bookmark
from linksanity.services.organizer import BookmarkOrganizer
from linksanity.services.writer import BookmarkWriter
from collections import Counter

# Leer bookmarks
print("📖 Leyendo bookmarks...")
bookmarks_file = "/home/medalcode/.config/google-chrome/Default/Bookmarks"
bookmarks = BookmarkReader.read_chrome_bookmarks(bookmarks_file)

print(f"✅ {len(bookmarks)} bookmarks encontrados")

# Eliminar duplicados y formatear
bookmarks = BookmarkOrganizer.remove_duplicates(bookmarks)
bookmarks = BookmarkOrganizer.apply_formatting(bookmarks, "clean")

# Reorganizar en categorías más claras
print("\n📊 Reorganizando por categorías...")


def categorizar(bookmark):
    """Asigna bookmarks a categorías principales"""
    title = bookmark.title.lower()
    url = bookmark.url.lower()
    folder = bookmark.folder.lower()

    # Categorías basadas en contenido
    if any(x in url for x in ["github.com", "gitlab"]):
        return "bookmark_bar/🔧 GitHub & Desarrollo"
    elif any(
        x in url + title
        for x in [
            "learn.microsoft",
            "tutorial",
            "curso",
            "udemy",
            "hackerrank",
            "leetcode",
        ]
    ):
        return "bookmark_bar/📚 Aprendizaje"
    elif any(x in folder for x in ["css", "html", "tailwind"]):
        return "bookmark_bar/🎨 Frontend"
    elif any(x in folder for x in ["backend", "api"]):
        return "bookmark_bar/⚙️ Backend"
    elif any(x in folder + title for x in ["herramienta", "tool", "utilidad"]):
        return "bookmark_bar/🛠️ Herramientas"
    elif any(x in folder for x in ["trabajo", "work"]):
        return "bookmark_bar/💼 Trabajo"
    elif any(x in folder + title for x in ["ejercit", "practice", "challenge"]):
        return "bookmark_bar/🏋️ Práctica"
    elif "tryh4rdcode" in folder:
        return "bookmark_bar/🚀 TryH4rdCode"
    elif "inacap" in folder:
        return "bookmark_bar/🎓 Inacap"
    else:
        return "bookmark_bar/📁 Otros"


# Reorganizar
reorganizados = []
for bookmark in bookmarks:
    nueva_categoria = categorizar(bookmark)

    nuevo = Bookmark(
        title=bookmark.title,
        url=bookmark.url,
        folder=nueva_categoria,
        date_added=bookmark.date_added,
    )
    reorganizados.append(nuevo)

# Contar por categoría
categorias = Counter(b.folder for b in reorganizados)
print("\n📊 Bookmarks por categoría:")

for cat, count in sorted(categorias.items()):
    print(f"   {cat}: {count}")

# Guardar
print("\n💾 Guardando cambios...")
BookmarkWriter.write_chrome_bookmarks(
    reorganizados, bookmarks_file, original_file=bookmarks_file, backup=True
)

print("\n✅ ¡Listo! Ahora tus bookmarks están organizados por categorías con emojis")
print("🔄 Cierra Chrome COMPLETAMENTE y ábrelo de nuevo para ver los cambios")
