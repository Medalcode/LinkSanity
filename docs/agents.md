# LinkSanity Agent Architecture

This document defines the high-level agents that compose the LinkSanity system.

## 1. The Orchestrator (Coordinator)
**Role:** Mission Control & workflow management.
**Responsibility:**
- Receives user commands (CLI or Extension).
- Parses intent and configuration.
- Delegates tasks to specialized agents.
- Manages the overall lifecycle of the process.
- Handles error propagation and final reporting.

**Dependencies:** All other agents.

## 2. The Curator (Generalist)
**Role:** Data Integrity, Organization & Hygiene.
**Responsibility:**
- **Organization:** Analyzes content and assigns categories (Librarian role).
- **Hygiene:** Detects duplicates and normalizes titles/URLs (Janitor role).
- **Validation:** Checks for broken links and redirect chains (Medic role).
- **Skill Required:** `ContentRefinery` (Parametric).

## 3. The Chronicler (Publisher)
**Role:** Insights, Metrics & I/O.
**Responsibility:**
- **Analysis:** Generates statistics and identifies usage patterns.
- **Persistence:** Reads from/Writes to various sources (JSON, HTML, Markdown, etc.).
- **Reporting:** Creates visual dashboards or summary reports.
- **Skill Required:** `UniversalIO`, `InsightEngine`.

