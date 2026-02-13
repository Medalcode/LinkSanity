"""The Orchestrator Agent: Mission Control."""

import sys
from pathlib import Path
from typing import List, Optional

from ..domain.models import Bookmark
from ..agents.librarian import LibrarianAgent
from ..agents.janitor import JanitorAgent
from ..agents.medic import MedicAgent
from ..agents.analyst import AnalystAgent
from ..skills.browser_integration import BrowserIntegrationSkill
from ..services.exporter import BookmarkExporter


class OrchestratorAgent:
    """
    Agente principal que coordina el flujo de trabajo de la aplicación.
    Recibe comandos del usuario y delega a otros agentes especializados.
    """

    def __init__(self):
        # Inicializar el equipo de agentes
        self.librarian = LibrarianAgent()
        self.janitor = JanitorAgent()
        self.medic = MedicAgent()
        self.analyst = AnalystAgent()
        
        # Skills de infraestructura
        self.browser_skill = BrowserIntegrationSkill()

    def run_cli_flow(self, file_path: str, output_path: str = None, browser_type: str = "chrome",
                     remove_duplicates: bool = False,
                     find_broken: bool = False,
                     generate_report: bool = False,
                     keyword: Optional[str] = None):
        """
        Ejecuta el flujo principal orquestando a los agentes necesarios.
        """
        print(f"🤖 Orchestrator: Iniciando misión para '{file_path}'...")

        # 1. INPUT (Browser Skill)
        try:
            if browser_type == "chrome":
                bookmarks = self.browser_skill.read_chrome_bookmarks(file_path)
            else:
                 print(f"❌ Error: Tipo de navegador '{browser_type}' no soportado aún.")
                 return
            print(f"📖 Leídos {len(bookmarks)} bookmarks.")
        except Exception as e:
            print(f"❌ Error crítico leyendo archivo: {e}")
            return

        # 2. PROCESAMIENTO (Agents Pipeline)
        
        # Filtros (Librarian/Skill) - TODO: Mover filtrado a Librarian
        if keyword:
            print(f"🔍 Filtrando por '{keyword}'...")
            bookmarks = [b for b in bookmarks if keyword.lower() in b.title.lower() or keyword.lower() in b.url.lower()]

        # Limpieza (Janitor)
        if remove_duplicates:
            print("🧹 Janitor: Eliminando duplicados...")
            bookmarks, removed = self.janitor.remove_duplicates(bookmarks)
            print(f"   - Eliminados {removed} duplicados.")

        # Organización (Librarian)
        print("📚 Librarian: Clasificando bookmarks...")
        organized_bookmarks = self.librarian.organize_bookmarks(bookmarks)
        print(f"✨ Clasificados {len(organized_bookmarks)} bookmarks.")

        # Diagnóstico (Medic) - Opcional
        if find_broken:
            print("⚕️ Medic: Verificando salud de enlaces (esto puede tardar)...")
            # Limitamos a 50 para no bloquear la demo, en producción se quitaría el límite o se haría async
            broken = self.medic.check_health(organized_bookmarks[:50]) 
            if broken:
                print(f"⚠️  Se encontraron {len(broken)} enlaces rotos (en la muestra).")
                for b in broken[:5]:
                    print(f"   - ❌ {b.title}: {b.url}")
            else:
                print("✅ Todos los enlaces verificados responden correctamente.")

        # Reporte (Analyst) - Opcional
        if generate_report:
            print("📊 Analyst: Generando reporte...")
            report = self.analyst.generate_report(organized_bookmarks)
            if output_path:
                report_path = str(Path(output_path).with_suffix('.md'))
                with open(report_path, "w") as f:
                    f.write(report)
                print(f"📝 Reporte guardado en {report_path}")
            else:
                print("\n" + report + "\n")

        # 3. OUTPUT (Exporter)
        if output_path and not generate_report:
            self._export_results(organized_bookmarks, output_path)
        elif not generate_report:
            self._show_summary(organized_bookmarks)

    def _export_results(self, bookmarks: List[Bookmark], path: str):
        """Delegar la escritura de resultados."""
        print(f"💾 Guardando resultados en '{path}'...")
        try:
            ext = Path(path).suffix.lower()
            if ext == ".json":
                BookmarkExporter.to_json(bookmarks, path)
            elif ext == ".html":
                BookmarkExporter.to_html(bookmarks, path)
            elif ext == ".md":
                BookmarkExporter.to_markdown(bookmarks, path)
            else:
                BookmarkExporter.to_json(bookmarks, path)
            print("✅ Exportación exitosa.")
        except Exception as e:
            print(f"❌ Error exportando: {e}")

    def _show_summary(self, bookmarks: List[Bookmark]):
        """Resumen rápido en consola."""
        stats = self.analyst.get_stats(bookmarks)
        print(f"📊 Categorías: {stats['category_count']}")
        for cat, count in stats['top_categories']:
            print(f"   - {cat}: {count}")
