#!/usr/bin/env python3
"""
LinkSanity - Organizador de bookmarks del navegador
Interfaz de línea de comandos
"""

import argparse
import sys
from pathlib import Path
from src.bookmark_reader import BookmarkReader
from src.bookmark_organizer import BookmarkOrganizer
from src.bookmark_exporter import BookmarkExporter
from src.bookmark_writer import BookmarkWriter


def main():
    parser = argparse.ArgumentParser(
        description="LinkSanity - Organiza y gestiona tus bookmarks del navegador",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  # Leer bookmarks de Chrome y mostrar estadísticas
  python main.py chrome bookmarks.json --report

  # Leer, limpiar y exportar a HTML
  python main.py chrome bookmarks.json --format clean \\
  --remove-duplicates --output output.html

  # Leer y exportar a Markdown agrupado por carpetas
  python main.py html bookmarks.html --output bookmarks.md

  # Filtrar por palabra clave y exportar
  python main.py chrome bookmarks.json --keyword python --output python_bookmarks.json
        """,
    )

    parser.add_argument(
        "browser",
        choices=["chrome", "firefox", "html"],
        help="Tipo de navegador o formato del archivo de bookmarks",
    )

    parser.add_argument("input_file", type=str, help="Archivo de bookmarks a procesar")

    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="Archivo de salida (la extensión determina el formato: .json, html...)",
    )

    parser.add_argument(
        "--format",
        choices=["title_case", "sentence_case", "lower", "upper", "clean"],
        default="clean",
        help="Estilo de formateo para los títulos (default: clean)",
    )

    parser.add_argument(
        "--sort",
        choices=["title", "url", "folder", "date"],
        help="Ordenar bookmarks por criterio",
    )

    parser.add_argument(
        "--remove-duplicates", action="store_true", help="Eliminar bookmarks duplicados"
    )

    parser.add_argument(
        "--keyword", type=str, help="Filtrar bookmarks que contengan esta palabra clave"
    )

    parser.add_argument(
        "--folder", type=str, help="Filtrar bookmarks de una carpeta específica"
    )

    parser.add_argument(
        "--domain", type=str, help="Filtrar bookmarks de un dominio específico"
    )

    parser.add_argument(
        "--report", action="store_true", help="Generar reporte estadístico"
    )

    parser.add_argument(
        "--find-broken", action="store_true", help="Buscar URLs potencialmente rotas"
    )

    parser.add_argument(
        "--in-place",
        action="store_true",
        help="Modificar el archivo original directamente (crea backup automático)",
    )

    args = parser.parse_args()

    # Si se usa --in-place, procesar directamente
    if args.in_place:
        if args.browser != "chrome":
            print("⚠️  --in-place solo funciona con formato 'chrome'")
            sys.exit(1)

        try:
            BookmarkWriter.organize_in_place(
                args.input_file,
                remove_duplicates=args.remove_duplicates,
                format_style=args.format,
                sort_by=args.sort,
            )
            print("\n✨ ¡Reinicia Chrome para ver los cambios!")
            sys.exit(0)
        except Exception as e:
            print(f"❌ Error al organizar: {e}")
            sys.exit(1)

    # Verificar que el archivo existe
    input_path = Path(args.input_file)
    if not input_path.exists():
        print(f"❌ Error: El archivo '{args.input_file}' no existe")
        sys.exit(1)

    # Leer bookmarks según el tipo de navegador
    print(f"📖 Leyendo bookmarks desde {args.input_file}...")
    try:
        if args.browser == "chrome":
            bookmarks = BookmarkReader.read_chrome_bookmarks(args.input_file)
        elif args.browser == "firefox":
            bookmarks = BookmarkReader.read_firefox_bookmarks(args.input_file)
        elif args.browser == "html":
            bookmarks = BookmarkReader.read_html_bookmarks(args.input_file)
    except Exception as e:
        print(f"❌ Error al leer bookmarks: {e}")
        sys.exit(1)

    print(f"✅ Se encontraron {len(bookmarks)} bookmarks")

    # Aplicar filtros
    if args.keyword or args.folder or args.domain:
        print("🔍 Aplicando filtros...")
        bookmarks = BookmarkOrganizer.filter_bookmarks(
            bookmarks, keyword=args.keyword, folder=args.folder, domain=args.domain
        )
        print(f"✅ {len(bookmarks)} bookmarks después de filtrar")

    # Eliminar duplicados
    if args.remove_duplicates:
        print("🧹 Eliminando duplicados...")
        original_count = len(bookmarks)
        bookmarks = BookmarkOrganizer.remove_duplicates(bookmarks)
        removed = original_count - len(bookmarks)
        print(f"✅ Se eliminaron {removed} duplicados")

    # Formatear títulos
    print(f"✨ Formateando títulos (estilo: {args.format})...")
    bookmarks = BookmarkOrganizer.apply_formatting(bookmarks, args.format)

    # Ordenar
    if args.sort:
        print(f"📊 Ordenando por {args.sort}...")
        bookmarks = BookmarkOrganizer.sort_bookmarks(bookmarks, by=args.sort)

    # Buscar URLs rotas
    if args.find_broken:
        print("🔧 Buscando URLs potencialmente rotas...")
        broken = BookmarkOrganizer.find_broken_urls(bookmarks)
        if broken:
            print(f"⚠️  Se encontraron {len(broken)} URLs sospechosas:")
            for b in broken[:10]:  # Mostrar solo las primeras 10
                print(f"   - {b.title}: {b.url}")
            if len(broken) > 10:
                print(f"   ... y {len(broken) - 10} más")
        else:
            print("✅ No se encontraron URLs sospechosas")

    # Generar reporte
    if args.report:
        report_file = args.output or "bookmark_report.md"
        if not report_file.endswith(".md"):
            report_file = report_file.rsplit(".", 1)[0] + "_report.md"
        print(f"📊 Generando reporte en {report_file}...")
        BookmarkExporter.generate_report(bookmarks, report_file)
        print("✅ Reporte generado")

    # Exportar si se especifica archivo de salida
    if args.output and not args.report:
        output_path = Path(args.output)
        extension = output_path.suffix.lower()

        print(f"💾 Exportando a {args.output}...")

        try:
            if extension == ".json":
                BookmarkExporter.to_json(bookmarks, args.output)
            elif extension == ".html":
                BookmarkExporter.to_html(bookmarks, args.output)
            elif extension == ".md":
                BookmarkExporter.to_markdown(bookmarks, args.output)
            elif extension == ".csv":
                BookmarkExporter.to_csv(bookmarks, args.output)
            else:
                print(f"⚠️  Extensión no reconocida '{extension}', usando JSON")
                BookmarkExporter.to_json(bookmarks, args.output)

            print("✅ Bookmarks exportados exitosamente")
        except Exception as e:
            print(f"❌ Error al exportar: {e}")
            sys.exit(1)

    # Mostrar resumen
    print("\n📈 Resumen:")
    print(f"   Total de bookmarks: {len(bookmarks)}")

    grouped = BookmarkOrganizer.group_by_folder(bookmarks)
    print(f"   Carpetas: {len(grouped)}")

    if len(grouped) <= 10:
        for folder, folder_bookmarks in sorted(
            grouped.items(), key=lambda x: len(x[1]), reverse=True
        ):
            print(f"      - {folder}: {len(folder_bookmarks)}")

    print("\n✨ ¡Listo!")


if __name__ == "__main__":
    main()
