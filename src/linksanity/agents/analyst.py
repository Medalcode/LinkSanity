"""The Analyst Agent: Statistics and Insights."""

from typing import List, Dict
from collections import Counter
from ..domain.models import Bookmark


class AnalystAgent:
    """
    Agente encargado de analizar datos y generar reportes.
    """

    def generate_report(self, bookmarks: List[Bookmark]) -> str:
        """Genera un reporte en texto/markdown."""
        total = len(bookmarks)
        categories = Counter(b.folder for b in bookmarks)
        
        report = []
        report.append("# 📊 Reporte de Bookmarks")
        report.append(f"**Total de Elances:** {total}")
        report.append("")
        report.append("## 📂 Desglose por Categoría")
        
        for category, count in categories.most_common():
            percentage = (count / total) * 100 if total > 0 else 0
            bar = "█" * int(percentage / 5)
            report.append(f"- **{category}**: {count} ({percentage:.1f}%) {bar}")
            
        return "\n".join(report)

    def get_stats(self, bookmarks: List[Bookmark]) -> Dict:
        """Retorna estadísticas crudas."""
        return {
            "total_count": len(bookmarks),
            "category_count": len(set(b.folder for b in bookmarks)),
            "top_categories": Counter(b.folder for b in bookmarks).most_common(5)
        }
