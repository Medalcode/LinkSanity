"""
LinkSanity - Organizador de bookmarks del navegador
Interfaz de línea de comandos (Agentic Architecture)
"""

import argparse
import sys
from pathlib import Path
from ..agents.orchestrator import OrchestratorAgent


def main():
    parser = argparse.ArgumentParser(
        description="LinkSanity (Agentic) - Organiza tus bookmarks inteligentemente",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "browser",
        choices=["chrome", "firefox", "html"],
        help="Tipo de navegador",
    )

    parser.add_argument("input_file", type=str, help="Archivo de bookmarks")

    parser.add_argument(
        "-o", "--output", type=str,
        help="Archivo de salida (.json, .html, .md)"
    )

    parser.add_argument(
        "--remove-duplicates", action="store_true", help="Eliminar duplicados"
    )

    parser.add_argument(
        "--keyword", type=str, help="Filtrar por palabra clave"
    )

    parser.add_argument(
        "--report", action="store_true", help="Generar reporte estadístico"
    )

    parser.add_argument(
        "--find-broken", action="store_true", help="Buscar URLs rotas"
    )

    args = parser.parse_args()

    # Verificar input
    if not Path(args.input_file).exists():
        print(f"❌ Error: Archivo '{args.input_file}' no encontrado.")
        sys.exit(1)

    # Instanciar el Orquestador
    orchestrator = OrchestratorAgent()

    # Ejecutar la misión
    orchestrator.run_cli_flow(
        file_path=args.input_file,
        output_path=args.output,
        browser_type=args.browser,
        remove_duplicates=args.remove_duplicates,
        find_broken=args.find_broken,
        generate_report=args.report,
        keyword=args.keyword
    )


if __name__ == "__main__":
    main()
