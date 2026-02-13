# LinkSanity Skills Inventory

This document lists the granular "skills" (capabilities) that Agents can invoke. Skills are the implementation details—functions, classes, or modules—that perform specific units of work.

## 1. BrowserIntegration
**Description:** Capabilities to interact with web browsers and their local data stores.
**Capabilities:**
- `read_chrome_bookmarks(path)`: Parse Chrome's JSON bookmark file.
- `read_firefox_bookmarks(path)`: Parse Firefox's SQLite or JSONlz4 database.
- `read_edge_bookmarks(path)`: Parse Edge's bookmark file.
- `write_netscape_html(bookmarks, path)`: Generate standard HTML import file.

## 2. URLAnalysis
**Description:** Tools for dissecting and validating Uniform Resource Locators.
**Capabilities:**
- `parse_domain(url)`: Extract root domain and subdomains.
- `clean_tracking_params(url)`: Remove `utm_*`, `fbclid`, etc.
- `resolve_redirects(url)`: Follow HTTP redirects to final destination.
- `check_health(url)`: Perform HEAD/GET request to verify status code (200 OK).

## 3. CategorizationEngine
**Description:** The brain behind sorting bookmarks into checking domains and keywords.
**Capabilities:**
- `classify_by_domain(url)`: Map known domains (e.g., `github.com` -> Development) to categories.
- `classify_by_keyword(title)`: Analyze title text for topic keywords.
- `predict_category(bookmark)`: Use heuristics (or ML in future) to determine best fit.
- `get_category_tree()`: Return the hierarchy of all available categories.

## 4. DataSanitization
**Description:** Utilities for cleaning raw text and data structures.
**Capabilities:**
- `normalize_title(text)`: capitalization, stripping partial suffixes.
- `deduplicate_list(bookmarks)`: Identify unique items by URL hash.
- `merge_folders(source, target)`: Intelligence merging of bookmark trees.

## 5. ReportingGen
**Description:** Generating human-readable output from raw data.
**Capabilities:**
- `generate_summary_table(stats)`: ASCII or Markdown table of counts.
- `render_html_dashboard(data)`: Create a visual HTML report.
- `calculate_health_score(total, broken)`: Numeric metric logic.

## 6. SystemIO
**Description:** Low-level file system interactions.
**Capabilities:**
- `safe_write(path, content)`: Atomic write operations.
- `backup_file(path)`: Create timestamped backups before modification.
- `find_browser_paths(os)`: Auto-detect default browser profile paths on Linux/Windows/Mac.
