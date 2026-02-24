"""The Curator Agent: Responsible for Data Integrity, Organization & Hygiene."""

from typing import List
from ..domain.models import Bookmark
from ..engine.refinery import ContentRefinery

class CuratorAgent:
    """
    Generalist agent that handles cleaning, classification, and validation.
    Consolidates roles of Librarian, Janitor, and Medic.
    """

    def __init__(self):
        self.refinery = ContentRefinery()

    def process_collection(self, bookmarks: List[Bookmark], 
                          clean_urls: bool = True,
                          normalize_titles: bool = True,
                          categorize: bool = True,
                          deduplicate: bool = True) -> List[Bookmark]:
        """
        Unified workflow for cleaning and organizing bookmarks.
        """
        actions = []
        if normalize_titles: actions.append("normalize_title")
        if categorize: actions.append("auto_categorize")

        url_options = []
        if clean_urls: url_options.append("clean_tracking")

        processed = []
        for b in bookmarks:
            # 1. Refine URL
            new_url = self.refinery.refine_url(b.url, options=url_options)
            b.url = new_url
            
            # 2. Refine Content (Title & Category)
            refined = self.refinery.refine_bookmark(b, actions=actions)
            processed.append(refined)

        # 3. Deduplicate
        if deduplicate:
            processed = self.refinery.optimize_collection(processed, strategy="deduplicate_by_url")

        return processed

    def check_health(self, bookmarks: List[Bookmark]) -> List[Bookmark]:
        """Verify if links are still alive (Medic role)."""
        # Placeholder for network request logic
        return bookmarks
