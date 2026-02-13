"""The Librarian Agent: Responsible for organizing and maintaining order."""

from typing import List, Dict
from ..domain.models import Bookmark
from ..skills.categorization import CategorizationSkill
from ..skills.sanitization import SanitizationSkill


class LibrarianAgent:
    """
    Agente encargado de clasificar, limpiar y ordenar los bookmarks.
    Utiliza habilidades especializadas para realizar su trabajo.
    """

    def __init__(self):
        self.categorizer = CategorizationSkill()
        self.sanitizer = SanitizationSkill()

    def organize_bookmarks(self, bookmarks: List[Bookmark]) -> List[Bookmark]:
        """
        Flujo principal de organización:
        1. Limpieza inicial
        2. Clasificación
        3. Estructuración
        """
        cleaned_bookmarks = []
        
        # Paso 1: Limpieza y Normalización
        for bookmark in bookmarks:
            # Normalizar título
            clean_title = self.sanitizer.normalize_title(bookmark.title)
            
            # Clasificar
            category = self.categorizer.categorize(bookmark)
            
            # Crear nuevo bookmark organizado
            new_bookmark = Bookmark(
                title=clean_title,
                url=bookmark.url,
                folder=category,  # Asignar a la nueva categoría
                date_added=bookmark.date_added
            )
            cleaned_bookmarks.append(new_bookmark)
            
        # Paso 2: Deduplicación (preservando el mejor candidato si fuera necesario)
        unique_bookmarks = self.sanitizer.deduplicate_list(cleaned_bookmarks)
        
        # Paso 3: Ordenamiento (por defecto alfabético por título)
        unique_bookmarks.sort(key=lambda b: b.title.lower())
        
        return unique_bookmarks

    def create_special_folders(self, bookmarks: List[Bookmark], 
                             most_visited: List[Bookmark] = None,
                             never_visited: List[Bookmark] = None) -> Dict[str, List[Bookmark]]:
        """
        Organiza los bookmarks en una estructura de carpetas, incluyendo especiales.
        """
        structure = {}
        
        # Carpetas especiales primero (si se proveen)
        if most_visited:
            structure["⭐ 10 Más Visitados"] = most_visited
            
        if never_visited:
            structure["👻 Nunca Visitados"] = never_visited
            
        # Agrupar el resto por categorías
        for bookmark in bookmarks:
            folder = bookmark.folder or "Sin Categorizar"
            if folder not in structure:
                structure[folder] = []
            structure[folder].append(bookmark)
            
        return structure
