"""Módulo para leer bookmarks de diferentes navegadores"""

import json
from typing import List, Dict
from ..domain.models import Bookmark


class BookmarkReader:
    """Lee bookmarks de archivos de navegadores"""

    @staticmethod
    def read_chrome_bookmarks(file_path: str) -> List[Bookmark]:
        """
        Lee bookmarks de Chrome/Chromium/Edge (formato JSON)

        Args:
            file_path: Ruta al archivo Bookmarks de Chrome

        Returns:
            Lista de objetos Bookmark
        """
        bookmarks = []

        with open(file_path, "r", encoding="utf-8") as f:
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
                extract_bookmarks(root_data, root_name)

        return bookmarks

    @staticmethod
    def read_firefox_bookmarks(file_path: str) -> List[Bookmark]:
        """
        Lee bookmarks de Firefox (formato JSON desde places.sqlite exportado)

        Args:
            file_path: Ruta al archivo JSON exportado

        Returns:
            Lista de objetos Bookmark
        """
        bookmarks = []

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        def extract_bookmarks(node: Dict, folder_path: str = ""):
            """Extrae bookmarks recursivamente"""
            if node.get("type") == "text/x-moz-place":
                if node.get("uri"):  # Es un bookmark, no una carpeta
                    bookmarks.append(
                        Bookmark(
                            title=node.get("title", ""),
                            url=node.get("uri", ""),
                            folder=folder_path,
                            date_added=node.get("dateAdded"),
                        )
                    )

            # Procesar hijos
            for child in node.get("children", []):
                if child.get("type") == "text/x-moz-place-container":
                    folder_name = child.get("title", "")
                    new_path = (
                        f"{folder_path}/{folder_name}" if folder_path else folder_name
                    )
                    extract_bookmarks(child, new_path)
                else:
                    extract_bookmarks(child, folder_path)

        extract_bookmarks(data)
        return bookmarks

    @staticmethod
    def read_html_bookmarks(file_path: str) -> List[Bookmark]:
        """
        Lee bookmarks desde archivo HTML exportado (formato universal)

        Args:
            file_path: Ruta al archivo HTML de bookmarks

        Returns:
            Lista de objetos Bookmark
        """
        from html.parser import HTMLParser

        bookmarks = []
        current_folder = []

        class BookmarkHTMLParser(HTMLParser):
            def handle_starttag(self, tag, attrs):
                if tag == "h3":
                    # Inicio de carpeta
                    self.in_folder = True
                    self.folder_name = ""
                elif tag == "a":
                    # Es un bookmark
                    attrs_dict = dict(attrs)
                    url = attrs_dict.get("href", "")
                    if url:
                        self.current_url = url
                        self.current_date = attrs_dict.get("add_date")

            def handle_endtag(self, tag):
                if tag == "h3":
                    self.in_folder = False
                    if hasattr(self, "folder_name") and self.folder_name:
                        current_folder.append(self.folder_name)
                elif tag == "dl":
                    # Salir de carpeta
                    if current_folder:
                        current_folder.pop()

            def handle_data(self, data):
                if hasattr(self, "in_folder") and self.in_folder:
                    self.folder_name = data.strip()
                elif hasattr(self, "current_url"):
                    title = data.strip()
                    folder_path = "/".join(current_folder)
                    bookmarks.append(
                        Bookmark(
                            title=title,
                            url=self.current_url,
                            folder=folder_path,
                            date_added=getattr(self, "current_date", None),
                        )
                    )
                    delattr(self, "current_url")

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        parser = BookmarkHTMLParser()
        parser.feed(content)

        return bookmarks
