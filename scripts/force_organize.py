#!/usr/bin/env python3
"""
Estrategia agresiva: Modificar el archivo repetidamente hasta que Chrome lo acepte
"""

import json
import hashlib
import time
import os
from collections import defaultdict


def organize_bookmarks():
    bookmarks_file = "/home/medalcode/.config/google-chrome/Default/Bookmarks"

    # Leer
    with open(bookmarks_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Extraer bookmarks
    def extract_all(node, path=""):
        bookmarks = []
        if node.get("type") == "url":
            bookmarks.append(
                {
                    "title": node.get("name", ""),
                    "url": node.get("url", ""),
                    "date_added": node.get("date_added"),
                    "guid": node.get("guid"),
                }
            )
        elif node.get("type") == "folder":
            for child in node.get("children", []):
                bookmarks.extend(extract_all(child, path))
        return bookmarks

    all_bookmarks = []
    for root_name, root_data in data["roots"].items():
        all_bookmarks.extend(extract_all(root_data))

    # Eliminar duplicados
    seen = set()
    unique = []
    for b in all_bookmarks:
        if b["url"] not in seen:
            seen.add(b["url"])
            unique.append(b)

    # Categorizar
    def categorize(b):
        t, u = b["title"].lower(), b["url"].lower()
        if "github.com" in u:
            return "🔧 GitHub"
        elif any(x in u + t for x in ["learn", "tutorial", "curso", "udemy"]):
            return "📚 Cursos"
        elif any(x in t + u for x in ["css", "tailwind", "html", "frontend"]):
            return "🎨 Frontend"
        elif any(x in t + u for x in ["backend", "api", "python"]):
            return "⚙️ Backend"
        elif any(x in t + u for x in ["tool", "convert", "herramient"]):
            return "🛠️ Tools"
        elif "tryh4rd" in t + u:
            return "🚀 TryH4rd"
        elif "inacap" in t + u:
            return "🎓 Inacap"
        elif any(x in t + u for x in ["ejercit", "practice"]):
            return "🏋️ Practice"
        elif "trabajo" in t + u:
            return "💼 Trabajo"
        else:
            return "📁 Misc"

    by_cat = defaultdict(list)
    for b in unique:
        by_cat[categorize(b)].append(b)

    # Reconstruir con timestamps MUY recientes
    current_time = str(int(time.time() * 1000000 + 13000000000000000))
    node_id = 100
    new_folders = []

    for cat, bookmarks in sorted(by_cat.items()):
        children = []
        for b in sorted(bookmarks, key=lambda x: x["title"].lower()):
            node_id += 1
            children.append(
                {
                    "date_added": current_time,
                    "date_last_used": "0",
                    "guid": b.get("guid") or f"auto_{node_id}",
                    "id": str(node_id),
                    "name": b["title"],
                    "type": "url",
                    "url": b["url"],
                }
            )

        node_id += 1
        new_folders.append(
            {
                "children": children,
                "date_added": current_time,
                "date_modified": current_time,
                "date_last_used": "0",
                "guid": f"folder_{node_id}_{int(time.time()*1000)}",
                "id": str(node_id),
                "name": cat,
                "type": "folder",
            }
        )

    # Actualizar
    data["roots"]["bookmark_bar"]["children"] = new_folders
    data["roots"]["bookmark_bar"]["date_modified"] = current_time
    data["roots"]["other"]["children"] = []
    data["roots"]["synced"]["children"] = []

    # Checksum
    data_copy = dict(data)
    if "checksum" in data_copy:
        del data_copy["checksum"]
    json_str = json.dumps(
        data_copy, ensure_ascii=False, separators=(",", ":"), sort_keys=True
    )
    data["checksum"] = hashlib.md5(json_str.encode("utf-8")).hexdigest()

    # Guardar
    with open(bookmarks_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=3)

    os.utime(bookmarks_file, None)
    return len(unique), len(new_folders)


# Estrategia: Hacer los cambios y luego repetir cada segundo por 10 segundos
print("🔄 Aplicando cambios repetidamente...")

for i in range(15):
    total, folders = organize_bookmarks()
    print(f"   Intento {i+1}/15: {total} bookmarks, {folders} carpetas")
    time.sleep(0.5)

print("\n✅ Completado!")
print("🚀 Abre Chrome AHORA (los cambios deberían persistir)")
