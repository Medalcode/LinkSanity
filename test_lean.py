"""Verification script for the LEAN Architecture."""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from linksanity.agents.orchestrator import OrchestratorAgent

def test_lean_architecture():
    print("🚀 Testing LinkSanity LEAN Architecture...")
    
    orchestrator = OrchestratorAgent()
    print("✅ Agents (Orchestrator, Curator, Chronicler) initialized.")

    # Create a dummy bookmark file (JSON format)
    dummy_path = "dummy_bookmarks.json"
    dummy_data = [
        {"title": "React Docs - Official Site", "url": "https://react.dev", "folder": "Barra"},
        {"title": "Python Website", "url": "http://python.org", "folder": "Barra"},
        {"title": "React Docs - Official Site", "url": "https://react.dev", "folder": "Other"} # Duplicate
    ]
    
    import json
    with open(dummy_path, "w") as f:
        json.dump(dummy_data, f)

    print(f"\n🧪 Running Lean Flow on {dummy_path}...")
    try:
        orchestrator.run_cli_flow(
            file_path=dummy_path,
            output_path="processed_lean.json",
            provider="json",
            remove_duplicates=True
        )
        print("✅ Flow completed successfully.")
    except Exception as e:
        print(f"❌ Flow failed: {e}")
        import traceback
        traceback.print_exc()

    # Cleanup dummy files
    if os.path.exists(dummy_path): os.remove(dummy_path)
    # if os.path.exists("processed_lean.json"): os.remove("processed_lean.json")

if __name__ == "__main__":
    test_lean_architecture()
