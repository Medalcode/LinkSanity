import pytest
from linksanity.services.organizer import BookmarkOrganizer
from linksanity.domain.models import Bookmark


@pytest.fixture
def sample_bookmarks():
    return [
        Bookmark(title="Google", url="https://google.com", folder="Search"),
        Bookmark(title="GitHub", url="https://github.com", folder="Dev"),
        Bookmark(title="Python", url="https://python.org", folder="Dev"),
        Bookmark(
            title="Google", url="https://google.com", folder="Search"
        ),  # Duplicate
        Bookmark(title="Broken", url="invalid-url", folder="Misc"),
    ]


class TestBookmarkOrganizer:
    def test_format_title_clean(self):
        title = "  Example Title - | "
        formatted = BookmarkOrganizer.format_title(title, style="clean")
        assert formatted == "Example Title"

    def test_format_title_cases(self):
        title = "hello WORLD"
        assert BookmarkOrganizer.format_title(title, style="lower") == "hello world"
        assert BookmarkOrganizer.format_title(title, style="upper") == "HELLO WORLD"
        assert (
            BookmarkOrganizer.format_title(title, style="title_case") == "Hello World"
        )
        assert (
            BookmarkOrganizer.format_title(title, style="sentence_case")
            == "Hello world"
        )

    def test_remove_duplicates(self, sample_bookmarks):
        unique = BookmarkOrganizer.remove_duplicates(sample_bookmarks, by="url")
        assert len(unique) == 4
        assert len([b for b in unique if b.url == "https://google.com"]) == 1

    def test_sort_bookmarks(self, sample_bookmarks):
        sorted_list = BookmarkOrganizer.sort_bookmarks(sample_bookmarks, by="title")
        assert sorted_list[0].title == "Broken"  # "Broken" comes first alphabetically

        sorted_list = BookmarkOrganizer.sort_bookmarks(sample_bookmarks, by="folder")
        # "Dev" comes before "Misc" and "Search"
        assert sorted_list[0].folder == "Dev"

    def test_filter_bookmarks(self, sample_bookmarks):
        filtered = BookmarkOrganizer.filter_bookmarks(sample_bookmarks, keyword="git")
        assert len(filtered) == 1
        assert filtered[0].title == "GitHub"

        filtered = BookmarkOrganizer.filter_bookmarks(sample_bookmarks, folder="Search")
        assert len(filtered) == 2  # Including duplicate

    def test_find_broken_urls(self, sample_bookmarks):
        broken = BookmarkOrganizer.find_broken_urls(sample_bookmarks)
        assert len(broken) == 1
        assert broken[0].url == "invalid-url"
