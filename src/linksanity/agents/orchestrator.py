"""The Orchestrator Agent: Mission Control."""

import sys
from pathlib import Path
from typing import List, Optional

from ..domain.models import Bookmark
from ..agents.curator import CuratorAgent
from ..agents.chronicler import ChroniclerAgent

class OrchestratorAgent:
    """
    Main agent that coordinates the application workflow.
    Delegates to Curator (Refinery/Health) and Chronicler (IO/Reporting).
    """

    def __init__(self):
        self.curator = CuratorAgent()
        self.chronicler = ChroniclerAgent()

    def run_cli_flow(self, file_path: str, output_path: str = None, 
                     provider: str = "chrome",
                     remove_duplicates: bool = True,
                     find_broken: bool = False,
                     generate_report: bool = True):
        """
        Executes the main flow using the consolidated agent architecture.
        """
        print(f"🤖 Orchestrator: Starting mission for '{file_path}'...")

        # 1. LOAD (via Chronicler)
        try:
            bookmarks = self.chronicler.load(provider, file_path)
            print(f"📖 Loaded {len(bookmarks)} bookmarks.")
        except Exception as e:
            print(f"❌ Error loading: {e}")
            return

        # 2. PROCESS (via Curator)
        print("🔧 Curator: Refining collection...")
        processed_bookmarks = self.curator.process_collection(
            bookmarks,
            deduplicate=remove_duplicates,
            normalize_titles=True,
            categorize=True
        )
        print(f"✨ Refined {len(processed_bookmarks)} bookmarks.")

        if find_broken:
            print("⚕️ Curator: Checking link health...")
            processed_bookmarks = self.curator.check_health(processed_bookmarks)

        # 3. REPORT & SAVE (via Chronicler)
        if generate_report:
            report = self.chronicler.render_report(processed_bookmarks)
            print("\n" + report + "\n")

        if output_path:
            print(f"💾 Chronicler: Saving results to '{output_path}'...")
            ext = Path(output_path).suffix.lower().replace('.', '')
            self.chronicler.save(processed_bookmarks, ext or "json", output_path)
            print("✅ Mission complete.")

    def _show_summary(self, bookmarks: List[Bookmark]):
        """Quick console summary."""
        stats = self.chronicler.generate_stats(bookmarks)
        print(f"📊 Total Bookmarks: {stats['total_count']}")
        print(f"📂 Categories: {len(stats['category_breakdown'])}")
