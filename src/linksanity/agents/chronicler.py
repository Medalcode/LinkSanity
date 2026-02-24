"""The Chronicler Agent: Responsible for Insights, Metrics & I/O."""

from typing import List, Dict
from collections import Counter
from ..domain.models import Bookmark
from ..engine.io import UniversalIO

class ChroniclerAgent:
    """
    Agent responsible for data persistence and reporting.
    Consolidates roles of Analyst and Exporter.
    """

    def __init__(self):
        self.io = UniversalIO()

    def load(self, provider: str, path: str) -> List[Bookmark]:
        """Load bookmarks from any supported source."""
        return self.io.fetch(provider, path)

    def save(self, bookmarks: List[Bookmark], format: str, path: str):
        """Save bookmarks to any supported format."""
        self.io.persist(bookmarks, format, path)

    def generate_stats(self, bookmarks: List[Bookmark]) -> Dict:
        """Analyze collection and return metrics."""
        total = len(bookmarks)
        categories = Counter(b.folder for b in bookmarks)
        
        return {
            "total_count": total,
            "category_breakdown": dict(categories.most_common()),
            "health_score": 100 # Placeholder
        }

    def render_report(self, bookmarks: List[Bookmark]) -> str:
        """Create a human-readable summary."""
        stats = self.generate_stats(bookmarks)
        report = [f"# LinkSanity Report", f"Total Bookmarks: {stats['total_count']}", ""]
        report.append("## Categories")
        for cat, count in stats['category_breakdown'].items():
            report.append(f"- {cat}: {count}")
        return "\n".join(report)
