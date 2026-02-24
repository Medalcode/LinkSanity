"""Unified Engine for Bookmark Categorization and Sanitization."""

import re
from typing import List, Optional, Any
from ..domain.models import Bookmark

class ContentRefinery:
    """The 'Processing Brain' for bookmarks."""

    @staticmethod
    def refine_url(url: str, options: List[str] = None) -> str:
        """
        Parametric URL refiner.
        options: ['clean_tracking', 'resolve_redirects', 'force_https']
        """
        options = options or []
        if not url: return ""
        
        # 1. Clean tracking parameters
        if "clean_tracking" in options:
            url = re.sub(r"([?&])utm_[^&]+&?", r"\1", url)
            url = re.sub(r"([?&])fbclid=[^&]+&?", r"\1", url)
            url = url.rstrip("&?")

        # 2. Force HTTPS
        if "force_https" in options and url.startswith("http://"):
            url = url.replace("http://", "https://", 1)

        return url

    @staticmethod
    def refine_bookmark(bookmark: Bookmark, actions: List[str] = None) -> Bookmark:
        """
        Parametric bookmark refiner.
        actions: ['normalize_title', 'auto_categorize']
        """
        actions = actions or ["normalize_title", "auto_categorize"]
        
        new_title = bookmark.title
        new_folder = bookmark.folder

        if "normalize_title" in actions:
            new_title = ContentRefinery._normalize_title(bookmark.title)

        if "auto_categorize" in actions:
            new_folder = ContentRefinery._categorize(new_title, bookmark.url)

        return Bookmark(
            title=new_title,
            url=bookmark.url,
            folder=new_folder,
            date_added=bookmark.date_added
        )

    @staticmethod
    def optimize_collection(bookmarks: List[Bookmark], strategy: str = "deduplicate_by_url") -> List[Bookmark]:
        """
        Consolidates collection-level operations.
        """
        if strategy == "deduplicate_by_url":
            seen = set()
            unique = []
            for b in bookmarks:
                if b.url not in seen:
                    seen.add(b.url)
                    unique.append(b)
            return unique
        return bookmarks

    @staticmethod
    def _normalize_title(title: str) -> str:
        if not title: return ""
        # Remove common suffixes
        title = re.sub(r"\s*-\s*(YouTube|Google|Facebook|Twitter|X|GitHub)$", "", title, flags=re.IGNORECASE)
        # Clean extra whitespace
        title = " ".join(title.split()).strip()
        # Title case if screaming or whispering
        if title.isupper() or title.islower():
            title = title.title()
        return title

    @staticmethod
    def _categorize(title: str, url: str) -> str:
        t, u = (title or "").lower(), (url or "").lower()
        if "github.com" in u: return "Repositorios"
        if any(x in u for x in ["udemy.com", "platzi.com", "coursera.org"]): return "Cursos Online"
        if any(x in t+u for x in ["python", "django", "fastapi"]): return "Python Backend"
        if any(x in t+u for x in ["react", "vue", "tailwind", "css"]): return "Frontend"
        if "inacap" in t+u: return "Inacap"
        if "tryh4rd" in t+u: return "TryH4rdCode"
        return "Sin Categorizar"
