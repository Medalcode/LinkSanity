#!/usr/bin/env python3
"""
Reorganizar bookmarks Y forzar que Chrome los detecte como cambios locales nuevos
"""

import json
import hashlib
import shutil
import time
from datetime import datetime
from collections import defaultdict

# Paths
bookmarks_file = "/home/medalcode/.config/google-chrome/Default/Bookmarks"
backup_file = f"{bookmarks_file}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

# Backup
shutil.copy2(bookmarks_file, backup_file)
print(f"💾 Backup: {backup_file}")

# Leer archivo actual
with open(bookmarks_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"📖 Leyendo bookmarks...")

# Función para extraer todos los bookmarks
def extract_all_bookmarks(node, path=""):
    bookmarks = []
    if node.get('type') == 'url':
        bookmarks.append({
            'title': node.get('name', ''),
            'url': node.get('url', ''),
            'date_added': node.get('date_added'),
            'guid': node.get('guid'),
            'path': path
        })
    elif node.get('type') == 'folder':
        folder_name = node.get('name', '')
        new_path = f"{path}/{folder_name}" if path else folder_name
        for child in node.get('children', []):
            bookmarks.extend(extract_all_bookmarks(child, new_path))
    return bookmarks

# Extraer todos
all_bookmarks = []
for root_name, root_data in data['roots'].items():
    all_bookmarks.extend(extract_all_bookmarks(root_data, root_name))

print(f"✅ {len(all_bookmarks)} bookmarks encontrados")

# Eliminar duplicados
seen_urls = set()
unique_bookmarks = []
for b in all_bookmarks:
    if b['url'] not in seen_urls:
        seen_urls.add(b['url'])
        unique_bookmarks.append(b)

removed = len(all_bookmarks) - len(unique_bookmarks)
if removed > 0:
    print(f"🧹 {removed} duplicados eliminados")

# Categorizar
def categorize(bookmark):
    title = bookmark['title'].lower()
    url = bookmark['url'].lower()
    
    if 'github.com' in url or 'gitlab' in url:
        return "🔧 GitHub"
    elif any(x in url+title for x in ['learn.microsoft', 'tutorial', 'curso', 'udemy', 'hackerrank', 'leetcode']):
        return "📚 Cursos"
    elif any(x in title+url for x in ['css', 'tailwind', 'frontend', 'html']):
        return "🎨 Frontend"
    elif any(x in title+url for x in ['backend', 'api', 'node', 'python']):
        return "⚙️ Backend"
    elif any(x in title+url for x in ['tool', 'convert', 'generator', 'herramient']):
        return "🛠️ Tools"
    elif 'tryh4rd' in title+url:
        return "🚀 TryH4rd"
    elif 'inacap' in title+url:
        return "🎓 Inacap"
    elif any(x in title+url for x in ['challenge', 'ejercit', 'practice']):
        return "🏋️ Practice"
    elif 'trabajo' in title+url:
        return "💼 Trabajo"
    else:
        return "📁 Misc"

# Agrupar
by_category = defaultdict(list)
for b in unique_bookmarks:
    category = categorize(b)
    by_category[category].append(b)

print("\n📊 Reorganización:")
for cat, items in sorted(by_category.items()):
    print(f"   {cat}: {len(items)}")

# Crear nodos con timestamps MUY RECIENTES (para que Chrome los vea como nuevos)
current_time = str(int(time.time() * 1000000 + 13000000000000000))  # Chrome timestamp

def create_bookmark_node(bookmark, node_id):
    return {
        "date_added": current_time,  # Timestamp MUY reciente
        "date_last_used": "0",
        "guid": bookmark.get('guid') or f"auto_{node_id}",
        "id": str(node_id),
        "name": bookmark['title'],
        "type": "url",
        "url": bookmark['url']
    }

def create_folder_node(name, children, node_id):
    return {
        "children": children,
        "date_added": current_time,
        "date_modified": current_time,  # MUY reciente
        "date_last_used": "0",
        "guid": f"folder_{node_id}_{int(time.time())}",
        "id": str(node_id),
        "name": name,
        "type": "folder"
    }

# Reconstruir
node_id = 100
new_folders = []

for category, bookmarks in sorted(by_category.items()):
    folder_children = []
    for bookmark in sorted(bookmarks, key=lambda x: x['title'].lower()):
        node_id += 1
        folder_children.append(create_bookmark_node(bookmark, node_id))
    
    node_id += 1
    new_folders.append(create_folder_node(category, folder_children, node_id))

# Actualizar estructura
data['roots']['bookmark_bar']['children'] = new_folders
data['roots']['bookmark_bar']['date_modified'] = current_time

# Limpiar otras secciones
data['roots']['other']['children'] = []
data['roots']['synced']['children'] = []

# Actualizar version (Chrome usa esto para detectar cambios)
data['version'] = 1

# Calcular checksum
data_copy = data.copy()
if 'checksum' in data_copy:
    del data_copy['checksum']
json_str = json.dumps(data_copy, ensure_ascii=False, separators=(',', ':'), sort_keys=True)
checksum = hashlib.md5(json_str.encode('utf-8')).hexdigest()
data['checksum'] = checksum

# Guardar
with open(bookmarks_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=3)

# Tocar el archivo para actualizar su timestamp del sistema
import os
os.utime(bookmarks_file, None)

print(f"\n✅ Guardado con checksum: {checksum}")
print(f"📂 {len(unique_bookmarks)} bookmarks en {len(new_folders)} carpetas")
print("\n🚀 Abre Chrome AHORA - debería detectar los cambios como locales y sincronizarlos")
