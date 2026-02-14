#!/usr/bin/env python3
"""
LinkSanity - Entry Point
"""

import sys
from pathlib import Path

# Ensure the project's `src` directory is on sys.path so the package imports
# (e.g. `linksanity.cli.interface`) resolve when running this script directly.
_project_root = Path(__file__).resolve().parent
_src_dir = _project_root / "src"
if str(_src_dir) not in sys.path:
    sys.path.insert(0, str(_src_dir))

if __name__ == "__main__":
    try:
        # Perform the import at runtime to avoid import-time failures when
        # the environment isn't configured (e.g., running from repo root).
        from linksanity.cli.interface import main
    except Exception as e:
        # Provide a clearer, actionable error message so the user can fix import issues.
        print("❌ No se pudo importar el paquete 'linksanity'.")
        print("Posibles soluciones:")
        print(
            "  - Ejecuta este script desde la raíz del proyecto (donde está este archivo)."
        )
        print("  - Asegúrate de que el directorio 'src' exista y sea accesible.")
        print("  - Instala el paquete en modo editable desde la raíz del proyecto:")
        print("      pip install -e .")
        print("")
        print("Detalles del error:")
        print(f"  {e}")
        sys.exit(1)

    main()
