"""Skill for browser integration and file IO."""

import json
from typing import List, Dict, Optional
from ..domain.models import Bookmark


class BrowserIntegrationSkill:
    """Provee capacidades para leer y escribir formatos de navegador."""

    def read_chrome_bookmarks(self, file_path: str) -> List[Bookmark]:
        """
        Lee bookmarks de Chrome/Chromium/Edge (formato JSON).
        Adapted from services/reader.py
        """
        bookmarks = []

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            # Si falla utf-8, intentar con latín o errores
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                data = json.load(f)

        def extract_bookmarks(node: Dict, folder_path: str = ""):
            """Extrae bookmarks recursivamente del árbol"""
            if node.get("type") == "url":
                bookmarks.append(
                    Bookmark(
                        title=node.get("name", ""),
                        url=node.get("url", ""),
                        folder=folder_path,
                        date_added=node.get("date_added"),
                    )
                )
            elif node.get("type") == "folder":
                folder_name = node.get("name", "")
                new_path = (
                    f"{folder_path}/{folder_name}" if folder_path else folder_name
                )
                for child in node.get("children", []):
                    extract_bookmarks(child, new_path)

        # Chrome guarda bookmarks en roots
        roots = data.get("roots", {})
        for root_name, root_data in roots.items():
            if isinstance(root_data, dict) and root_data.get("type") == "folder":
                # Mapear nombres internos a legibles si es necesario
                visible_name = root_name
                if root_name == "bookmark_bar":
                    visible_name = "Barra de favoritos"
                elif root_name == "other":
                    visible_name = "Otros favoritos"
                elif root_name == "synced":
                    visible_name = "Favoritos del móvil"
                
                extract_bookmarks(root_data, visible_name)

        return bookmarks
