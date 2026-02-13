"""The Janitor Agent: Cleanup and Hygiene."""

from typing import List, Tuple
from ..domain.models import Bookmark
from ..skills.sanitization import SanitizationSkill


class JanitorAgent:
    """
    Agente encargado de la limpieza de datos, eliminación de duplicados
    y corrección de formatos.
    """

    def __init__(self):
        self.sanitizer = SanitizationSkill()

    def clean_titles(self, bookmarks: List[Bookmark], style: str = "clean") -> List[Bookmark]:
        """Limpia los títulos de una lista de bookmarks."""
        cleaned = []
        for bookmark in bookmarks:
            new_title = self.sanitizer.normalize_title(bookmark.title, style=style)
            # Crear copia con título nuevo
            cleaned.append(Bookmark(
                title=new_title,
                url=bookmark.url,
                folder=bookmark.folder,
                date_added=bookmark.date_added
            ))
        return cleaned

    def remove_duplicates(self, bookmarks: List[Bookmark], by: str = "url") -> Tuple[List[Bookmark], int]:
        """
        Elimina duplicados de la lista.
        Retorna: (Lista limpia, Cantidad de eliminados)
        """
        original_count = len(bookmarks)
        unique_list = self.sanitizer.deduplicate_list(bookmarks, by=by)
        removed_count = original_count - len(unique_list)
        
        return unique_list, removed_count
