import pytest
from src.bookmark_reader import Bookmark

class TestBookmark:
    def test_bookmark_initialization(self):
        b = Bookmark(title="Test", url="http://test.com", folder="Folder", date_added=123456)
        assert b.title == "Test"
        assert b.url == "http://test.com"
        assert b.folder == "Folder"
        assert b.date_added == 123456

    def test_bookmark_to_dict(self):
        b = Bookmark(title="Test", url="http://test.com")
        data = b.to_dict()
        assert data["title"] == "Test"
        assert data["url"] == "http://test.com"
        assert data["folder"] == ""
        assert data["date_added"] is None
