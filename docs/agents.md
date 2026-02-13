# LinkSanity Agent Architecture

This document defines the high-level agents that compose the LinkSanity system. Each agent represents a distinct area of responsibility, designed to be modular, scalable, and professional.

## 1. The Orchestrator (Coordinator)
**Role:** Mission Control & workflow management.
**Responsibility:**
- Receives user commands (CLI or Extension).
- Parses intent and configuration.
- Delegates tasks to specialized agents.
- Manages the overall lifecycle of the process (Start -> Execute -> Finish).
- Handles error propagation and final reporting.

**Dependencies:** All other agents.

## 2. The Librarian (Organizer)
**Role:** Classification and structure.
**Responsibility:**
- Analyzes bookmark content (Title, URL, Metadata).
- Assigns bookmarks to the correct category (from the 60+ available).
- Manages "Special Folders" (e.g., "10 Most Visited", "Never Visited").
- Maintains the directory structure of the bookmark tree.
- **Skill Required:** `CategorizationEngine`.

## 3. The Janitor (Cleaner)
**Role:** Maintenance and hygiene.
**Responsibility:**
- Detects and removes duplicate bookmarks.
- Normalizes titles (removes " - Google Search", emojis, excessive whitespace).
- Standardizes URL formats (stripping tracking parameters, etc.).
- **Skill Required:** `DataSanitization`.

## 4. The Medic (Validator)
**Role:** Health and integrity.
**Responsibility:**
- Checks for broken links (404, 500 errors).
- Detects redirect chains.
- Identifies insecure links (HTTP vs HTTPS).
- Marks bookmarks for review or deletion.
- **Skill Required:** `URLValidation`, `NetworkRequest`.

## 5. The Analyst (Reporter)
**Role:** Insights and metrics.
**Responsibility:**
- Generates statistics (Total links, links per category, health score).
- Identifies usage patterns (Most visited domains).
- Creates visual reports or summary text.
- **Skill Required:** `DataAnalysis`.

## 6. The Exporter (Publisher)
**Role:** Input/Output management.
**Responsibility:**
- Reads bookmarks from various sources (Chrome, Firefox, Safari, HTML files).
- Writes organized bookmarks to destination formats (JSON, HTML, Markdown, CSV).
- Ensures data integrity during import/export.
- **Skill Required:** `BrowserIntegration`, `FileGeneration`.
