"""Verification script for the new Agentic Architecture."""

import sys
import os
from pathlib import Path

# Add src to path to allow imports
sys.path.append(str(Path(__file__).parent / "src"))

from linksanity.agents.orchestrator import OrchestratorAgent
from linksanity.domain.models import Bookmark

def test_architecture():
    print("🧪 Testing LinkSanity Architecture...")
    
    # 1. Instantiate Orchestrator
    try:
        orchestrator = OrchestratorAgent()
        print("✅ Orchestrator instantiated successfully.")
    except Exception as e:
        print(f"❌ Failed to instantiate Orchestrator: {e}")
        return

    # 2. Test Categorization Skill directly
    print("\n🧪 Testing Categorization Skill (Ported from JS)...")
    try:
        cat_skill = orchestrator.librarian.categorizer
        
        test_cases = [
            (Bookmark("Curso React", "https://udemy.com/course/react", "", ""), "Cursos Online"),
            (Bookmark("Docs Python", "https://docs.python.org/3/", "", ""), "Python Backend"),
            (Bookmark("Unknown Site", "https://example.com", "", ""), "Sin Categorizar"),
            (Bookmark("My Project", "https://github.com/me/repo", "", ""), "Repositorios"),
        ]
        
        for bookmark, expected in test_cases:
            result = cat_skill.categorize(bookmark)
            if result == expected:
                print(f"✅ Correctly categorized '{bookmark.title}' -> {result}")
            else:
                print(f"❌ Failed categorization for '{bookmark.title}': Expected {expected}, got {result}")
                
    except Exception as e:
        print(f"❌ Error testing categorization: {e}")

    # 3. Test Sanitization Skill
    print("\n🧪 Testing Sanitization Skill...")
    try:
        san_skill = orchestrator.librarian.sanitizer
        
        title = "  My Video - YouTube  "
        clean = san_skill.normalize_title(title)
        expected = "My Video"
        
        if clean == expected:
             print(f"✅ Correctly sanitized '{title}' -> '{clean}'")
        else:
             print(f"❌ Failed sanitization: Expected '{expected}', got '{clean}'")
             
    except Exception as e:
        print(f"❌ Error testing sanitization: {e}")

    print("\n✨ Verification Complete.")

if __name__ == "__main__":
    test_architecture()
