"""Módulo para organizar y formatear bookmarks"""

import re
from typing import List, Dict, Optional

from collections import defaultdict
from src.bookmark_reader import Bookmark


class BookmarkOrganizer:
    """Organiza y formatea bookmarks"""

    @staticmethod
    def format_title(title: str, style: str = "title_case") -> str:
        """
        Formatea el título del bookmark

        Args:
            title: Título original
            style: Estilo de formateo
            ('title_case', 'sentence_case', 'lower', 'upper', 'clean')


        Returns:
            Título formateado
        """
        # Limpiar espacios extras
        title = " ".join(title.split())

        if style == "title_case":
            return title.title()
        elif style == "sentence_case":
            return title.capitalize()
        elif style == "lower":
            return title.lower()
        elif style == "upper":
            return title.upper()
        elif style == "clean":
            # Eliminar caracteres especiales innecesarios
            title = re.sub(
                r"(\s*[|\-–—]+)+\s*$", "", title
            )  # Eliminar separadores al final
            title = re.sub(r"\s{2,}", " ", title)  # Múltiples espacios a uno
            title = title.strip()
            return title

        return title

    @staticmethod
    def remove_duplicates(bookmarks: List[Bookmark], by: str = "url") -> List[Bookmark]:
        """
        Elimina bookmarks duplicados

        Args:
            bookmarks: Lista de bookmarks
            by: Criterio para detectar duplicados ('url', 'title', 'both')

        Returns:
            Lista sin duplicados
        """
        seen = set()
        unique_bookmarks = []

        for bookmark in bookmarks:
            key_tuple: tuple
            if by == "url":
                key_tuple = (bookmark.url,)

            elif by == "title":
                key_tuple = (bookmark.title,)
            elif by == "both":
                key_tuple = (bookmark.title, bookmark.url)
            else:
                # Default to URL if 'by' is an unrecognized value
                key_tuple = (bookmark.url,)

            if key_tuple not in seen:
                seen.add(key_tuple)

                unique_bookmarks.append(bookmark)

        return unique_bookmarks

    @staticmethod
    def sort_bookmarks(
        bookmarks: List[Bookmark], by: str = "title", reverse: bool = False
    ) -> List[Bookmark]:
        """
        Ordena bookmarks

        Args:
            bookmarks: Lista de bookmarks
            by: Criterio de ordenamiento ('title', 'url', 'folder', 'date')
            reverse: Orden descendente si es True

        Returns:
            Lista ordenada
        """
        if by == "title":
            return sorted(bookmarks, key=lambda b: b.title.lower(), reverse=reverse)
        elif by == "url":
            return sorted(bookmarks, key=lambda b: b.url.lower(), reverse=reverse)
        elif by == "folder":
            return sorted(
                bookmarks, key=lambda b: (b.folder, b.title.lower()), reverse=reverse
            )
        elif by == "date":
            return sorted(bookmarks, key=lambda b: b.date_added or 0, reverse=reverse)

        return bookmarks

    @staticmethod
    def group_by_folder(bookmarks: List[Bookmark]) -> Dict[str, List[Bookmark]]:
        """
        Agrupa bookmarks por carpeta

        Args:
            bookmarks: Lista de bookmarks

        Returns:
            Diccionario con carpetas como claves y listas de bookmarks como valores
        """
        grouped = defaultdict(list)

        for bookmark in bookmarks:
            folder = bookmark.folder or "Sin carpeta"
            grouped[folder].append(bookmark)

        return dict(grouped)

    @staticmethod
    def filter_bookmarks(
        bookmarks: List[Bookmark],
        keyword: Optional[str] = None,
        folder: Optional[str] = None,
        domain: Optional[str] = None,
    ) -> List[Bookmark]:
        """
        Filtra bookmarks según criterios

        Args:
            bookmarks: Lista de bookmarks
            keyword: Palabra clave en título o URL
            folder: Carpeta específica
            domain: Dominio específico (ej: 'github.com')

        Returns:
            Lista filtrada
        """
        filtered = bookmarks

        if keyword:
            keyword_lower = keyword.lower()
            filtered = [
                b
                for b in filtered
                if keyword_lower in b.title.lower() or keyword_lower in b.url.lower()
            ]

        if folder:
            filtered = [b for b in filtered if folder.lower() in b.folder.lower()]

        if domain:
            filtered = [b for b in filtered if domain.lower() in b.url.lower()]

        return filtered

    @staticmethod
    def find_broken_urls(bookmarks: List[Bookmark]) -> List[Bookmark]:
        """
        Encuentra URLs potencialmente rotas (básico, sin verificación HTTP)

        Args:
            bookmarks: Lista de bookmarks

        Returns:
            Lista de bookmarks con URLs sospechosas
        """
        suspicious = []

        for bookmark in bookmarks:
            url = bookmark.url

            # Verificaciones básicas
            if not url or url.strip() == "":
                suspicious.append(bookmark)
            elif not url.startswith(("http://", "https://", "ftp://", "file://")):
                suspicious.append(bookmark)

        return suspicious

    @staticmethod
    def apply_formatting(
        bookmarks: List[Bookmark], title_style: str = "clean"
    ) -> List[Bookmark]:
        """
        Aplica formateo a todos los bookmarks

        Args:
            bookmarks: Lista de bookmarks
            title_style: Estilo de formateo para títulos

        Returns:
            Lista con bookmarks formateados
        """
        formatted = []

        for bookmark in bookmarks:
            new_bookmark = Bookmark(
                title=BookmarkOrganizer.format_title(bookmark.title, title_style),
                url=bookmark.url,
                folder=bookmark.folder,
                date_added=bookmark.date_added,
            )
            formatted.append(new_bookmark)

        return formatted
