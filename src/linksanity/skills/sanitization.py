"""Skill for data sanitization and cleaning."""

import re
from typing import List, Tuple
from ..domain.models import Bookmark


class SanitizationSkill:
    """Provee capacidades para limpiar y normalizar datos."""

    def normalize_title(self, title: str, style: str = "clean") -> str:
        """
        Formatea y limpia el título de un bookmark.
        Adapted from services/organizer.py + extension/background.js logic
        """
        if not title:
            return ""

        # Limpiar espacios extras
        title = " ".join(title.split())

        if style == "clean":
            # 1. Eliminar separadores comunes al final
            title = re.sub(r"\s*[|\-–—]+\s*$", "", title)
            
            # 2. Eliminar patrones comunes de sitios (Logic from background.js)
            title = re.sub(r"\s*-\s*(YouTube|Google|Facebook|Twitter|X)$", "", title, flags=re.IGNORECASE)
            title = re.sub(r"^\[.*?\]\s*", "", title)  # Eliminar [tags] al inicio

            # 3. Capitalización inteligente si está todo en mayúsculas/minúsculas
            if title.isupper() or title.islower():
                # Esta lógica simple puede mejorarse, por ahora usaremos capitalize()
                # O title() que es lo más cercano en Python estándar
                title = title.title()
                
            title = title.strip()

        elif style == "title_case":
            return title.title()
        elif style == "sentence_case":
            return title.capitalize()
        elif style == "lower":
            return title.lower()
        elif style == "upper":
            return title.upper()

        return title

    def find_duplicates(self, bookmarks: List[Bookmark], by: str = "url") -> List[Tuple[Bookmark, str]]:
        """
        Identifica duplicados en una lista.
        Returns: Lista de tuplas (bookmark_duplicado, motivo)
        """
        seen = set()
        duplicates = []

        for bookmark in bookmarks:
            key_tuple: tuple
            if by == "url":
                key_tuple = (bookmark.url,)
            elif by == "title":
                key_tuple = (bookmark.title,)
            elif by == "both":
                key_tuple = (bookmark.title, bookmark.url)
            else:
                key_tuple = (bookmark.url,)

            if key_tuple in seen:
                duplicates.append((bookmark, "duplicate_" + by))
            else:
                seen.add(key_tuple)

        return duplicates
        
    def deduplicate_list(self, bookmarks: List[Bookmark], by: str = "url") -> List[Bookmark]:
        """Devuelve la lista filtrada sin duplicados (manteniendo el primero encontrado)"""
        seen = set()
        unique = []
        
        for bookmark in bookmarks:
            key_tuple: tuple
            if by == "url":
                key_tuple = (bookmark.url,)
            elif by == "title":
                key_tuple = (bookmark.title,)
            elif by == "both":
                key_tuple = (bookmark.title, bookmark.url)
            else:
                key_tuple = (bookmark.url,)

            if key_tuple not in seen:
                seen.add(key_tuple)
                unique.append(bookmark)
                
        return unique
