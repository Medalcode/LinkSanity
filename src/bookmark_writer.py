"""Módulo para escribir bookmarks directamente en formato de navegador"""

import json
import shutil
import hashlib
from pathlib import Path
from typing import List, Dict
from datetime import datetime
from collections import defaultdict
from src.bookmark_reader import Bookmark


class BookmarkWriter:
    """Escribe bookmarks en formato nativo de navegadores"""
    
    @staticmethod
    def write_chrome_bookmarks(bookmarks: List[Bookmark], output_file: str, 
                               original_file: str = None, backup: bool = True):
        """
        Escribe bookmarks en formato JSON de Chrome (reemplaza el archivo original)
        
        Args:
            bookmarks: Lista de bookmarks a escribir
            output_file: Archivo de destino (generalmente el archivo Bookmarks de Chrome)
            original_file: Archivo original para preservar metadatos (opcional)
            backup: Si True, crea un backup antes de sobrescribir
        """
        # Crear backup si se solicita
        if backup and Path(output_file).exists():
            backup_file = f"{output_file}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            shutil.copy2(output_file, backup_file)
            print(f"💾 Backup creado: {backup_file}")
        
        # Leer estructura original si existe
        base_structure = {
            "checksum": "",
            "roots": {
                "bookmark_bar": {
                    "children": [],
                    "date_added": "13000000000000000",
                    "date_last_used": "0",
                    "date_modified": "0",
                    "guid": "00000000-0000-4000-A000-000000000002",
                    "id": "1",
                    "name": "Barra de favoritos",
                    "type": "folder"
                },
                "other": {
                    "children": [],
                    "date_added": "13000000000000000",
                    "date_last_used": "0",
                    "date_modified": "0",
                    "guid": "00000000-0000-4000-A000-000000000003",
                    "id": "2",
                    "name": "Otros favoritos",
                    "type": "folder"
                },
                "synced": {
                    "children": [],
                    "date_added": "13000000000000000",
                    "date_last_used": "0",
                    "date_modified": "0",
                    "guid": "00000000-0000-4000-A000-000000000004",
                    "id": "3",
                    "name": "Favoritos del dispositivo",
                    "type": "folder"
                }
            },
            "version": 1
        }
        
        # Si existe archivo original, preservar su estructura base
        if original_file and Path(original_file).exists():
            try:
                with open(original_file, 'r', encoding='utf-8') as f:
                    original_data = json.load(f)
                    base_structure = {
                        "checksum": original_data.get("checksum", ""),
                        "roots": {
                            "bookmark_bar": {
                                **original_data["roots"]["bookmark_bar"],
                                "children": []
                            },
                            "other": {
                                **original_data["roots"]["other"],
                                "children": []
                            },
                            "synced": {
                                **original_data["roots"]["synced"],
                                "children": []
                            }
                        },
                        "version": original_data.get("version", 1)
                    }
            except Exception as e:
                print(f"⚠️  No se pudo leer estructura original: {e}")
        
        # Organizar bookmarks por carpetas
        bookmarks_by_folder = defaultdict(list)
        for bookmark in bookmarks:
            bookmarks_by_folder[bookmark.folder].append(bookmark)
        
        # Generar ID único
        current_id = 10
        
        def create_folder_structure(folder_path: str, bookmarks_list: List[Bookmark]) -> Dict:
            """Crea la estructura de carpetas anidadas"""
            nonlocal current_id
            
            parts = [p for p in folder_path.split('/') if p]
            
            # Estructura de la carpeta
            folder_structure = {
                "children": [],
                "date_added": str(int(datetime.now().timestamp() * 1000000)),
                "date_modified": str(int(datetime.now().timestamp() * 1000000)),
                "id": str(current_id),
                "name": parts[-1] if parts else "Sin carpeta",
                "type": "folder",
                "guid": f"bookmark_{current_id}"
            }
            current_id += 1
            
            # Agregar bookmarks a la carpeta
            for bookmark in bookmarks_list:
                bookmark_node = {
                    "date_added": str(bookmark.date_added or int(datetime.now().timestamp() * 1000000)),
                    "guid": f"bookmark_{current_id}",
                    "id": str(current_id),
                    "name": bookmark.title,
                    "type": "url",
                    "url": bookmark.url
                }
                current_id += 1
                folder_structure["children"].append(bookmark_node)
            
            return folder_structure
        
        # Distribuir bookmarks en las raíces correctas
        for folder_path, folder_bookmarks in sorted(bookmarks_by_folder.items()):
            # Determinar a qué raíz pertenece
            if folder_path.startswith("bookmark_bar"):
                root = "bookmark_bar"
                # Eliminar el prefijo "bookmark_bar/"
                clean_path = folder_path.replace("bookmark_bar/", "")
            elif folder_path.startswith("other"):
                root = "other"
                clean_path = folder_path.replace("other/", "")
            elif folder_path.startswith("synced"):
                root = "synced"
                clean_path = folder_path.replace("synced/", "")
            else:
                root = "bookmark_bar"
                clean_path = folder_path
            
            # Si no hay subcarpetas, agregar directamente
            if not clean_path or clean_path == folder_path.split('/')[-1]:
                for bookmark in folder_bookmarks:
                    bookmark_node = {
                        "date_added": str(bookmark.date_added or int(datetime.now().timestamp() * 1000000)),
                        "guid": f"bookmark_{current_id}",
                        "id": str(current_id),
                        "name": bookmark.title,
                        "type": "url",
                        "url": bookmark.url
                    }
                    current_id += 1
                    base_structure["roots"][root]["children"].append(bookmark_node)
            else:
                # Crear estructura de carpetas
                folder_struct = create_folder_structure(clean_path, folder_bookmarks)
                base_structure["roots"][root]["children"].append(folder_struct)
        
        # Calcular checksum MD5 (Chrome lo usa para validar el archivo)
        # El checksum es el MD5 de la estructura JSON sin el campo checksum
        json_without_checksum = json.dumps(base_structure, ensure_ascii=False, separators=(',', ':'), sort_keys=True)
        checksum = hashlib.md5(json_without_checksum.encode('utf-8')).hexdigest()
        base_structure["checksum"] = checksum
        
        # Escribir archivo
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(base_structure, f, ensure_ascii=False, indent=3)
    
    @staticmethod
    def organize_in_place(bookmarks_file: str, remove_duplicates: bool = True,
                         format_style: str = "clean", sort_by: str = "folder"):
        """
        Organiza los bookmarks directamente en el archivo de Chrome
        
        Args:
            bookmarks_file: Ruta al archivo Bookmarks de Chrome
            remove_duplicates: Si True, elimina duplicados
            format_style: Estilo de formateo de títulos
            sort_by: Criterio de ordenamiento
        """
        from src.bookmark_reader import BookmarkReader
        from src.bookmark_organizer import BookmarkOrganizer
        
        print(f"📖 Leyendo bookmarks desde {bookmarks_file}...")
        bookmarks = BookmarkReader.read_chrome_bookmarks(bookmarks_file)
        original_count = len(bookmarks)
        print(f"✅ Se encontraron {original_count} bookmarks")
        
        # Aplicar transformaciones
        if remove_duplicates:
            print("🧹 Eliminando duplicados...")
            bookmarks = BookmarkOrganizer.remove_duplicates(bookmarks)
            removed = original_count - len(bookmarks)
            if removed > 0:
                print(f"✅ Se eliminaron {removed} duplicados")
        
        print(f"✨ Formateando títulos (estilo: {format_style})...")
        bookmarks = BookmarkOrganizer.apply_formatting(bookmarks, format_style)
        
        if sort_by:
            print(f"📊 Ordenando por {sort_by}...")
            bookmarks = BookmarkOrganizer.sort_bookmarks(bookmarks, by=sort_by)
        
        print("💾 Guardando cambios en el archivo original...")
        BookmarkWriter.write_chrome_bookmarks(bookmarks, bookmarks_file, 
                                             original_file=bookmarks_file, backup=True)
        
        print(f"✅ ¡Bookmarks organizados exitosamente!")
        print(f"   Total final: {len(bookmarks)} bookmarks")
