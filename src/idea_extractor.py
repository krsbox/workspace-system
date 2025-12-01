#!/usr/bin/env python3
"""Idea Extractor: Extract and catalog ideas from other projects"""
import sqlite3
import re
from pathlib import Path
from datetime import datetime

DB_PATH = Path("/media/sunil-kr/workspace/workspace-system/workspace_knowledge.db")


def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        """CREATE TABLE IF NOT EXISTS ideas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source TEXT NOT NULL,
        title TEXT NOT NULL,
        description TEXT,
        category TEXT,
        priority TEXT DEFAULT 'medium',
        status TEXT DEFAULT 'extracted',
        reality_score INTEGER DEFAULT 100,
        warnings TEXT,
        created_at TEXT NOT NULL
    )"""
    )
    conn.commit()
    conn.close()


def assess_reality(file_path, content):
    """Assess if code is real/working vs mock/simulation/outdated"""
    score = 100
    warnings = []

    # Check for mock/simulation indicators
    mock_patterns = [
        r"mock",
        r"fake",
        r"stub",
        r"dummy",
        r"test.*data",
        r"simulation",
        r"example",
        r"demo",
        r"sample",
    ]
    for pattern in mock_patterns:
        if re.search(pattern, str(file_path), re.I) or re.search(
            pattern, content[:500], re.I
        ):
            score -= 30
            warnings.append("⚠️ MOCK/SIMULATION detected")
            break

    # Check for outdated indicators
    outdated_patterns = [
        r"deprecated",
        r"obsolete",
        r"old",
        r"legacy",
        r"python\s*2",
        r"TODO.*remove",
        r"FIXME.*outdated",
    ]
    for pattern in outdated_patterns:
        if re.search(pattern, content[:1000], re.I):
            score -= 20
            warnings.append("⚠️ OUTDATED code detected")
            break

    # Check for working code indicators
    working_indicators = [
        r"def\s+\w+\(",
        r"class\s+\w+",
        r"import\s+\w+",
        r'if\s+__name__\s*==\s*["\']__main__["\']',
    ]
    working_count = sum(1 for p in working_indicators if re.search(p, content))
    if working_count >= 3:
        score += 10
        warnings.append("✓ Working code structure")

    # Check for tests (good sign)
    if re.search(r"(test_|_test\.py|assert\s+)", str(file_path)) or re.search(
        r"(import\s+unittest|import\s+pytest|def\s+test_)", content
    ):
        score -= 20
        warnings.append("⚠️ TEST code (not production)")

    # Check for actual implementation
    if len(content) < 100:
        score -= 30
        warnings.append("⚠️ Minimal/incomplete code")

    return max(0, min(100, score)), warnings


def extract_from_project(project_path):
    """Extract ideas from project directory with reality checks"""
    path = Path(project_path)
    if not path.exists():
        print(f"✗ Path not found: {project_path}")
        return []

    ideas = []
    seen_patterns = set()

    # Scan Python files for working code
    for py_file in path.rglob("*.py"):
        try:
            content = py_file.read_text(errors="ignore")
            reality_score, warnings = assess_reality(py_file, content)

            # Only extract from real working code (score >= 50)
            if reality_score < 50:
                continue

            # Extract TODO/FIXME from working code (PRIORITY)
            for i, line in enumerate(content.splitlines(), 1):
                if re.search(r"(TODO|FIXME|HACK|NOTE):", line, re.I):
                    ideas.append(
                        {
                            "source": f"{py_file.relative_to(path)}:{i}",
                            "title": line.strip()[:100],
                            "description": f"From working code (reality: {reality_score}%)",
                            "category": "todo",
                            "reality_score": reality_score,
                            "warnings": "; ".join(warnings),
                        }
                    )

            # Extract only unique class definitions as patterns (limit)
            if reality_score >= 70:
                for match in re.finditer(r"class\s+(\w+)", content):
                    class_name = match.group(1)
                    if class_name not in seen_patterns and not class_name.startswith(
                        "_"
                    ):
                        seen_patterns.add(class_name)
                        ideas.append(
                            {
                                "source": str(py_file.relative_to(path)),
                                "title": f"Pattern: class {class_name}",
                                "description": f"Working code pattern (reality: {reality_score}%)",
                                "category": "pattern",
                                "reality_score": reality_score,
                                "warnings": "; ".join(warnings),
                            }
                        )
        except Exception:
            continue

    # Scan README files (documentation)
    for readme in path.rglob("README*"):
        try:
            content = readme.read_text(errors="ignore")
            if len(content) > 100:
                ideas.append(
                    {
                        "source": str(readme.relative_to(path)),
                        "title": f"Documentation: {readme.name}",
                        "description": content[:200],
                        "category": "documentation",
                        "reality_score": 80,
                        "warnings": "✓ Documentation",
                    }
                )
        except:
            continue

    return ideas


def add_idea(
    source,
    title,
    description="",
    category="general",
    priority="medium",
    reality_score=100,
    warnings="",
):
    """Add idea to database with reality assessment"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        """INSERT INTO ideas 
        (source, title, description, category, priority, reality_score, warnings, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            source,
            title,
            description,
            category,
            priority,
            reality_score,
            warnings,
            datetime.now().isoformat(),
        ),
    )
    idea_id = c.lastrowid
    conn.commit()
    conn.close()
    return idea_id


def list_ideas(category=None, min_reality=50):
    """List ideas filtered by reality score"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if category:
        c.execute(
            """SELECT * FROM ideas 
            WHERE category = ? AND reality_score >= ? 
            ORDER BY reality_score DESC, created_at DESC""",
            (category, min_reality),
        )
    else:
        c.execute(
            """SELECT * FROM ideas 
            WHERE reality_score >= ? 
            ORDER BY reality_score DESC, created_at DESC""",
            (min_reality,),
        )
    ideas = c.fetchall()
    conn.close()
    return ideas


if __name__ == "__main__":
    import sys

    init_db()

    if len(sys.argv) < 2:
        print("Usage:")
        print(
            "  idea_extractor.py scan <path>          - Scan project (reality >= 50%)"
        )
        print("  idea_extractor.py add <title>          - Add idea manually")
        print("  idea_extractor.py list [category]      - List ideas (reality >= 50%)")
        print(
            "  idea_extractor.py list-all [category]  - List all (including low reality)"
        )
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "scan" and len(sys.argv) > 2:
        ideas = extract_from_project(sys.argv[2])

        # Categorize by reality
        high_reality = [i for i in ideas if i.get("reality_score", 100) >= 70]
        medium_reality = [i for i in ideas if 50 <= i.get("reality_score", 100) < 70]
        low_reality = [i for i in ideas if i.get("reality_score", 100) < 50]

        print(f"\n✓ Found {len(ideas)} ideas")
        print(f"  🟢 High reality (>=70%): {len(high_reality)}")
        print(f"  🟡 Medium reality (50-69%): {len(medium_reality)}")
        print(f"  🔴 Low reality (<50%): {len(low_reality)} (skipped)")

        # Add only high and medium reality ideas
        added = 0
        for idea in high_reality + medium_reality:
            add_idea(
                idea["source"],
                idea["title"],
                idea.get("description", ""),
                idea["category"],
                "medium",
                idea.get("reality_score", 100),
                idea.get("warnings", ""),
            )
            added += 1

        print(f"✓ Added {added} ideas to database")

    elif cmd == "add" and len(sys.argv) > 2:
        title = " ".join(sys.argv[2:])
        idea_id = add_idea(
            "manual", title, "", "general", "medium", 100, "✓ Manual entry"
        )
        print(f"✓ Idea #{idea_id} added")

    elif cmd == "list":
        category = sys.argv[2] if len(sys.argv) > 2 else None
        ideas = list_ideas(category, min_reality=50)
        print(f"\n💡 IDEAS ({len(ideas)} total, reality >= 50%)")
        print("-" * 80)
        for idea in ideas[:20]:
            reality = int(idea[7]) if idea[7] else 100  # Column 7 is reality_score
            emoji = "🟢" if reality >= 70 else "🟡"
            warnings = idea[8] if idea[8] else ""  # Column 8 is warnings
            print(f"  {emoji} #{idea[0]:3} [{idea[4]}] {reality}% - {idea[2][:45]}")
            if warnings and len(warnings) < 80:
                print(f"      {warnings}")

    elif cmd == "list-all":
        category = sys.argv[2] if len(sys.argv) > 2 else None
        ideas = list_ideas(category, min_reality=0)
        print(f"\n💡 ALL IDEAS ({len(ideas)} total)")
        print("-" * 80)
        for idea in ideas[:30]:
            reality = int(idea[7]) if idea[7] else 100
            emoji = "🟢" if reality >= 70 else "🟡" if reality >= 50 else "🔴"
            print(f"  {emoji} #{idea[0]:3} [{idea[4]}] {reality}% - {idea[2][:45]}")

    else:
        print("Invalid command")
