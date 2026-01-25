"""Módulo para exportar bookmarks en diferentes formatos"""

import json
from typing import List
from datetime import datetime
from ..domain.models import Bookmark


class BookmarkExporter:
    """Exporta bookmarks a diferentes formatos"""

    @staticmethod
    def to_json(bookmarks: List[Bookmark], output_file: str, pretty: bool = True):
        """
        Exporta bookmarks a formato JSON

        Args:
            bookmarks: Lista de bookmarks
            output_file: Ruta del archivo de salida
            pretty: Si True, formatea el JSON con indentación
        """
        data = [bookmark.to_dict() for bookmark in bookmarks]

        with open(output_file, "w", encoding="utf-8") as f:
            if pretty:
                json.dump(data, f, indent=2, ensure_ascii=False)
            else:
                json.dump(data, f, ensure_ascii=False)

    @staticmethod
    def to_html(bookmarks: List[Bookmark], output_file: str, title: str = "Bookmarks"):
        """
        Exporta bookmarks a formato HTML (compatible con navegadores)

        Args:
            bookmarks: Lista de bookmarks
            output_file: Ruta del archivo de salida
            title: Título del documento HTML
        """
        from collections import defaultdict

        # Agrupar por carpeta
        by_folder = defaultdict(list)
        for bookmark in bookmarks:
            folder = bookmark.folder or "Sin carpeta"
            by_folder[folder].append(bookmark)

        html = f"""<!DOCTYPE NETSCAPE-Bookmark-file-1>
<!-- This is an automatically generated file.
     It will be read and overwritten.
     DO NOT EDIT! -->
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
<TITLE>{title}</TITLE>
<H1>{title}</H1>
<DL><p>
"""

        for folder, folder_bookmarks in sorted(by_folder.items()):
            html += f"    <DT><H3>{folder}</H3>\n"
            html += "    <DL><p>\n"

            for bookmark in sorted(folder_bookmarks, key=lambda b: b.title):
                date_str = (
                    f' ADD_DATE="{bookmark.date_added}"' if bookmark.date_added else ""
                )
                html += (
                    f'        <DT><A HREF="{bookmark.url}"{date_str}>'
                    f"{bookmark.title}</A>\n"
                )

            html += "    </DL><p>\n"

        html += "</DL><p>\n"

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(html)

    @staticmethod
    def to_markdown(
        bookmarks: List[Bookmark], output_file: str, group_by_folder: bool = True
    ):
        """
        Exporta bookmarks a formato Markdown

        Args:
            bookmarks: Lista de bookmarks
            output_file: Ruta del archivo de salida
            group_by_folder: Si True, agrupa por carpetas
        """
        from collections import defaultdict

        md = "# Bookmarks\n\n"
        md += f"*Generado el {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n"

        if group_by_folder:
            by_folder = defaultdict(list)
            for bookmark in bookmarks:
                folder = bookmark.folder or "Sin carpeta"
                by_folder[folder].append(bookmark)

            for folder, folder_bookmarks in sorted(by_folder.items()):
                md += f"## {folder}\n\n"

                for bookmark in sorted(folder_bookmarks, key=lambda b: b.title):
                    md += f"- [{bookmark.title}]({bookmark.url})\n"

                md += "\n"
        else:
            for bookmark in sorted(bookmarks, key=lambda b: b.title):
                folder_info = f" *({bookmark.folder})*" if bookmark.folder else ""
                md += f"- [{bookmark.title}]({bookmark.url}){folder_info}\n"

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(md)

    @staticmethod
    def to_csv(bookmarks: List[Bookmark], output_file: str):
        """
        Exporta bookmarks a formato CSV

        Args:
            bookmarks: Lista de bookmarks
            output_file: Ruta del archivo de salida
        """
        import csv

        with open(output_file, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Título", "URL", "Carpeta", "Fecha añadido"])

            for bookmark in bookmarks:
                writer.writerow(
                    [
                        bookmark.title,
                        bookmark.url,
                        bookmark.folder,
                        bookmark.date_added or "",
                    ]
                )

    @staticmethod
    def generate_report(bookmarks: List[Bookmark], output_file: str):
        """
        Genera un reporte detallado de los bookmarks

        Args:
            bookmarks: Lista de bookmarks
            output_file: Ruta del archivo de salida
        """
        from collections import Counter
        from urllib.parse import urlparse

        # Estadísticas
        total = len(bookmarks)
        folders = Counter(b.folder or "Sin carpeta" for b in bookmarks)
        domains = Counter(urlparse(b.url).netloc for b in bookmarks)

        report = f"""# Reporte de Bookmarks - LinkSanity
Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Estadísticas Generales
- Total de bookmarks: {total}
- Carpetas únicas: {len(folders)}
- Dominios únicos: {len(domains)}

## Bookmarks por Carpeta
"""

        for folder, count in folders.most_common():
            report += f"- {folder}: {count}\n"

        report += "\n## Dominios más guardados\n"
        for domain, count in domains.most_common(20):
            report += f"- {domain}: {count}\n"

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(report)
