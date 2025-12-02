#!/usr/bin/env python3
"""
Wiki Documentation Converter
Converts markdown documentation into wiki entries in the database
"""
import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path("workspace_knowledge.db")

# Documentation mapping: (file_path, wiki_title, section_to_extract)
DOCUMENTATION_MAPPING = [
    ("README.md", "Quick Start", "quick start|usage|features"),
    ("SETUP.md", "Installation Guide", "installation|setup|requirements"),
    ("TESTING.md", "Testing Framework", "testing|tests|pytest"),
    ("STRUCTURE.md", "Project Structure", "structure|directory|file organization"),
    ("ARCHITECTURE_OVERVIEW.txt", "System Architecture", "architecture|layers|design"),
    ("UNIFIED_SYSTEM.md", "System Integration", "integration|workflow|components"),
    ("ANALYSIS_REPORT.md", "Code Quality", "quality|analysis|verification"),
    ("INDEX.md", "Documentation Index", "index|navigation|reference"),
    ("PROJECT_REVIEW_SUMMARY.md", "Project Status", "status|progress|summary"),
]


def extract_section_from_file(filepath, keyword_pattern):
    """Extract relevant section from markdown file"""
    if not Path(filepath).exists():
        return None

    content = Path(filepath).read_text()

    # For now, return first 1000 chars of content as preview
    lines = content.split("\n")

    # Take first meaningful section
    result = []
    in_section = False
    line_count = 0

    for line in lines:
        if line_count > 30:  # Limit to ~30 lines for wiki entry
            break

        # Skip empty lines at start
        if not result and not line.strip():
            continue

        # Include lines
        if line.strip():
            result.append(line)
            line_count += 1

    return "\n".join(result) if result else content[:500]


def populate_wiki():
    """Populate wiki with documentation"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    now = datetime.now().isoformat()

    print("📖 POPULATING WIKI WITH DOCUMENTATION")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print()

    added = 0
    updated = 0

    for filepath, title, keywords in DOCUMENTATION_MAPPING:
        content = extract_section_from_file(filepath, keywords)

        if not content:
            print(f"  ✗ {title:40} (file not found: {filepath})")
            continue

        # Generate path from title
        path = title.lower().replace(" ", "-")

        # Check if entry exists
        c.execute("SELECT id FROM wiki WHERE title = ?", (title,))
        existing = c.fetchone()

        if existing:
            # Update
            c.execute(
                """UPDATE wiki SET content = ?, updated_at = ? WHERE title = ?""",
                (content, now, title),
            )
            print(f"  ✓ {title:40} (updated)")
            updated += 1
        else:
            # Insert
            c.execute(
                """INSERT INTO wiki (path, title, content, created_at, updated_at) 
                   VALUES (?, ?, ?, ?, ?)""",
                (path, title, content, now, now),
            )
            print(f"  ✓ {title:40} (added)")
            added += 1

    conn.commit()
    conn.close()

    print()
    print(f"📊 Results: {added} added, {updated} updated")
    print()


if __name__ == "__main__":
    populate_wiki()
    print("✅ Wiki population complete!")
