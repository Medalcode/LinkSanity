# LinkSanity Skills Inventory

## 1. UniversalIO (Super-Skill)
**Description:** Unified interface for all I/O operations (Browser, File System, Cloud).
**Capabilities (Parametric):**
- `fetch(provider, path)`: Replaces `read_chrome`, `read_firefox`, etc. Works for local files or browser profiles.
- `persist(data, format, path)`: Replaces `write_netscape_html`, etc. Supports JSON, HTML, MD, CSV.
- `manage_fs(action)`: Parametric handler for `safe_write`, `backup`, and `path_auto_detect`.

## 2. ContentRefinery (Super-Skill)
**Description:** The "Processing Brain" for bookmarks.
**Capabilities (Parametric):**
- `refine_url(url, options=[])`: Consolidates `parse_domain`, `clean_tracking`, `resolve_redirects`, and `check_health`.
- `refine_bookmark(bookmark, actions=[])`: Consolidates `classify_by_domain/keyword` and `normalize_title`.
- `optimize_collection(list, strategy)`: Consolidates `deduplicate` and `merge_folders`.

## 3. InsightEngine (Super-Skill)
**Description:** Analytic engine for generating value from the bookmark set.
**Capabilities (Parametric):**
- `analyze(bookmarks, metrics=[])`: Consolidates `calculate_health_score` and general statistics.
- `render(data, template)`: Consolidates `generate_summary_table` and `render_html_dashboard`.

