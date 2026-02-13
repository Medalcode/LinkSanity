"""The Medic Agent: Health and Integrity Checks."""

import requests
from typing import List, Dict
from ..domain.models import Bookmark


class MedicAgent:
    """
    Agente encargado de verificar la salud de los enlaces.
    """

    def check_health(self, bookmarks: List[Bookmark], timeout: int = 5) -> List[Bookmark]:
        """
        Verifica una lista de bookmarks y retorna los que tienen problemas.
        Nota: Esto puede tardar mucho para listas largas.
        """
        broken_bookmarks = []
        
        # Iterar sobre bookmarks (idealmente esto sería asíncrono o paralelo en el futuro)
        for bookmark in bookmarks:
            if not self._is_url_valid(bookmark.url, timeout):
                broken_bookmarks.append(bookmark)
                
        return broken_bookmarks

    def _is_url_valid(self, url: str, timeout: int) -> bool:
        """Realiza una petición HEAD/GET para verificar si la URL responde."""
        if not url or not url.startswith(('http://', 'https://')):
            return False
            
        try:
            # Intentar HEAD primero (más rápido)
            response = requests.head(url, timeout=timeout, allow_redirects=True)
            if response.status_code < 400:
                return True
                
            # Si HEAD falla (algunos servidores no lo soportan), intentar GET
            if response.status_code == 405 or response.status_code == 403: # Method Not Allowed / Forbidden
                response = requests.get(url, timeout=timeout, stream=True)
                return response.status_code < 400
                
            return False
        except Exception:
            return False
