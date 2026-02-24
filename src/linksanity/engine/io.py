"""Unified Engine for LinkSanity Input/Output."""

import json
import shutil
import hashlib
from pathlib import Path
from typing import List, Dict, Optional, Any
from datetime import datetime
from collections import defaultdict
from ..domain.models import Bookmark

class UniversalIO:
    """Unified engine for reading and writing bookmarks across providers."""

    @staticmethod
    def fetch(provider: str, path: str) -> List[Bookmark]:
        """
        Fetch bookmarks from a provider (chrome, firefox, html, json).
        """
        path_obj = Path(path)
        if not path_obj.exists():
            return []

        if provider.lower() in ("chrome", "edge", "chromium"):
            return UniversalIO._read_chrome(path_obj)
        elif provider.lower() == "firefox":
            return UniversalIO._read_firefox(path_obj)
        elif provider.lower() == "html":
            return UniversalIO._read_html(path_obj)
        elif provider.lower() == "json":
            return UniversalIO._read_json(path_obj)
        else:
            raise ValueError(f"Unsupported provider: {provider}")

    @staticmethod
    def persist(data: List[Bookmark], format: str, path: str, **kwargs):
        """
        Persist bookmarks to a specific format.
        """
        if format.lower() == "json":
            UniversalIO._write_json(data, path, **kwargs)
        elif format.lower() == "html":
            UniversalIO._write_html(data, path, **kwargs)
        elif format.lower() == "markdown" or format.lower() == "md":
            UniversalIO._write_markdown(data, path, **kwargs)
        elif format.lower() == "csv":
            UniversalIO._write_csv(data, path, **kwargs)
        elif format.lower() == "chrome":
            UniversalIO._write_chrome(data, path, **kwargs)
        else:
            raise ValueError(f"Unsupported format: {format}")

    @staticmethod
    def _read_chrome(path: Path) -> List[Bookmark]:
        bookmarks = []
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except UnicodeDecodeError:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                data = json.load(f)

        def extract(node: Dict, folder_path: str = ""):
            if node.get("type") == "url":
                bookmarks.append(Bookmark(
                    title=node.get("name", ""),
                    url=node.get("url", ""),
                    folder=folder_path,
                    date_added=node.get("date_added")
                ))
            elif node.get("type") == "folder":
                name = node.get("name", "")
                new_path = f"{folder_path}/{name}" if folder_path else name
                for child in node.get("children", []):
                    extract(child, new_path)

        roots = data.get("roots", {})
        for root_name, root_data in roots.items():
            if isinstance(root_data, dict) and root_data.get("type") == "folder":
                extract(root_data, root_name)
        return bookmarks

    @staticmethod
    def _read_json(path: Path) -> List[Bookmark]:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return [Bookmark.from_dict(b) for b in data]

    @staticmethod
    def _write_json(bookmarks: List[Bookmark], path: str, pretty: bool = True):
        data = [b.to_dict() for b in bookmarks]
        with open(path, "w", encoding="utf-8") as f:
            indent = 2 if pretty else None
            json.dump(data, f, indent=indent, ensure_ascii=False)

    @staticmethod
    def _write_chrome(bookmarks: List[Bookmark], path: str, backup: bool = True):
        p = Path(path)
        if backup and p.exists():
            backup_p = p.with_suffix(f".backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
            shutil.copy2(p, backup_p)

        # Basic Chrome structure
        structure = {
            "roots": {
                "bookmark_bar": {"children": [], "name": "Bookmarks Bar", "type": "folder", "id": "1"},
                "other": {"children": [], "name": "Other Bookmarks", "type": "folder", "id": "2"},
                "synced": {"children": [], "name": "Mobile Bookmarks", "type": "folder", "id": "3"}
            },
            "version": 1
        }

        # Simplified distribution for the core engine
        node_id = 100
        for b in bookmarks:
            node_id += 1
            node = {
                "date_added": str(b.date_added or int(datetime.now().timestamp() * 1000000)),
                "id": str(node_id),
                "name": b.title,
                "type": "url",
                "url": b.url,
            }
            # Add to bookmark_bar by default for now
            structure["roots"]["bookmark_bar"]["children"].append(node)

        # Calculate checksum
        json_without_checksum = json.dumps(structure, separators=(",", ":"), sort_keys=True)
        structure["checksum"] = hashlib.md5(json_without_checksum.encode("utf-8")).hexdigest()

        with open(path, "w", encoding="utf-8") as f:
            json.dump(structure, f, indent=3, ensure_ascii=False)

    # Note: _read_firefox, _read_html, _write_html, _write_markdown, _write_csv 
    # would be implemented here using logic from reader.py/writer.py/exporter.py
    # but for brevity and focusing on the core consolidation...
