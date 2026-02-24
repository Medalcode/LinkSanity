from typing import Dict, Any, Optional


class Bookmark:
    """Representa un bookmark individual"""

    def __init__(
        self, title: str, url: str, folder: str = "", date_added: Optional[int] = None
    ):

        self.title = title
        self.url = url
        self.folder = folder
        self.date_added = date_added

    def __repr__(self):
        return (
            f"Bookmark(title='{self.title}', url='{self.url}', folder='{self.folder}')"
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "url": self.url,
            "folder": self.folder,
            "date_added": self.date_added,
        }
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Bookmark":
        return Bookmark(
            title=data.get("title", ""),
            url=data.get("url", ""),
            folder=data.get("folder", ""),
            date_added=data.get("date_added")
        )
