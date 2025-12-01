#!/usr/bin/env python3
"""Populate System: Convert ideas to proposals, discussions, todos, and wiki"""
import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path("/media/sunil-kr/workspace/workspace-system/workspace_knowledge.db")


def get_high_value_ideas(limit=50):
    """Get high-value ideas for proposals"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        """SELECT i.id, i.title, i.description, i.category, i.reality_score
        FROM ideas i
        JOIN collaboration_modes cm ON i.id = cm.idea_id
        WHERE i.category IN ('todo', 'pattern') 
        AND i.reality_score >= 80
        AND cm.mode IN ('ai_automated', 'ai_assisted')
        ORDER BY i.reality_score DESC, i.id
        LIMIT ?""",
        (limit,),
    )
    ideas = c.fetchall()
    conn.close()
    return ideas


def create_proposals_from_ideas(ideas):
    """Create proposals from high-value ideas"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    created = 0
    for idea_id, title, desc, category, reality in ideas:
        # Check if proposal already exists
        c.execute("SELECT id FROM proposals WHERE title LIKE ?", (f"%{title[:30]}%",))
        if c.fetchone():
            continue

        # Determine impact and effort
        if reality >= 95:
            impact, effort = "high", "low"
        elif reality >= 85:
            impact, effort = "medium", "medium"
        else:
            impact, effort = "low", "high"

        # Create proposal
        proposal_title = f"{category.title()}: {title[:60]}"
        proposal_desc = f"Reality: {reality}%\nSource: Idea #{idea_id}\n\n{desc or 'Auto-generated from extracted ideas'}"
        now = datetime.now().isoformat()

        c.execute(
            """INSERT INTO proposals 
            (title, description, impact, effort, status, created_at, updated_at)
            VALUES (?, ?, ?, ?, 'submitted', ?, ?)""",
            (proposal_title, proposal_desc, impact, effort, now, now),
        )
        created += 1

    conn.commit()
    conn.close()
    return created


def create_discussions_from_proposals():
    """Create discussions for pending proposals"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Get pending proposals
    c.execute("SELECT id, title FROM proposals WHERE status='submitted' LIMIT 20")
    proposals = c.fetchall()

    created = 0
    for prop_id, title in proposals:
        # Check if discussion exists
        c.execute("SELECT id FROM discussions WHERE title LIKE ?", (f"%{title[:30]}%",))
        if c.fetchone():
            continue

        # Create discussion
        disc_title = f"Discussion: {title[:60]}"
        now = datetime.now().isoformat()
        c.execute(
            """INSERT INTO discussions (title, created_by, created_at, updated_at)
            VALUES (?, 1, ?, ?)""",
            (disc_title, now, now),
        )
        created += 1

    conn.commit()
    conn.close()
    return created


def create_todos_from_ideas():
    """Create todos from TODO category ideas"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Get TODO ideas
    c.execute(
        """SELECT i.id, i.title, i.description, i.reality_score
        FROM ideas i
        WHERE i.category = 'todo' AND i.reality_score >= 80
        ORDER BY i.reality_score DESC
        LIMIT 30"""
    )
    ideas = c.fetchall()

    created = 0
    for idea_id, title, desc, reality in ideas:
        # Check if todo exists
        c.execute("SELECT id FROM todos WHERE title LIKE ?", (f"%{title[:30]}%",))
        if c.fetchone():
            continue

        # Determine priority
        if "security" in title.lower() or "bug" in title.lower():
            priority = "urgent"
        elif reality >= 95:
            priority = "high"
        elif reality >= 85:
            priority = "medium"
        else:
            priority = "low"

        # Create todo
        todo_title = title[:100]
        todo_desc = f"Reality: {reality}%\nSource: Idea #{idea_id}\n\n{desc or ''}"
        now = datetime.now().isoformat()

        c.execute(
            """INSERT INTO todos (title, description, status, priority, created_at, updated_at)
            VALUES (?, ?, 'todo', ?, ?, ?)""",
            (todo_title, todo_desc, priority, now, now),
        )
        created += 1

    conn.commit()
    conn.close()
    return created


def consolidate_docs_to_wiki():
    """Convert documentation files to wiki pages"""
    docs_dir = Path(__file__).parent

    # Find all markdown docs
    doc_files = [
        "SYSTEM_READINESS.md",
        "EXTRACTION_WORKFLOW.md",
        "IMPLEMENTATION_GUIDE.md",
        "HUMAN_AI_COLLABORATION.md",
        "ACTION_PLAN.md",
        "DUPLICATION_ANALYSIS.md",
        "SESSION_SUMMARY.md",
    ]

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    created = 0
    for doc_file in doc_files:
        doc_path = docs_dir / doc_file
        if not doc_path.exists():
            continue

        # Read content
        content = doc_path.read_text()
        title = doc_file.replace(".md", "").replace("_", " ").title()

        # Check if wiki page exists
        c.execute("SELECT id FROM wiki WHERE title = ?", (title,))
        if c.fetchone():
            continue

        # Create wiki page
        path = title.lower().replace(" ", "-")
        now = datetime.now().isoformat()
        c.execute(
            """INSERT INTO wiki (title, path, content, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?)""",
            (title, path, content, now, now),
        )
        created += 1

    conn.commit()
    conn.close()
    return created


def review_growth():
    """Review system growth metrics"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    metrics = {}

    # Count everything
    tables = [
        "ideas",
        "proposals",
        "todos",
        "discussions",
        "wiki",
        "knowledge",
        "collaboration_modes",
        "ai_suggestions",
    ]

    for table in tables:
        try:
            c.execute(f"SELECT COUNT(*) FROM {table}")
            metrics[table] = c.fetchone()[0]
        except:
            metrics[table] = 0

    # Get status breakdowns
    c.execute("SELECT status, COUNT(*) FROM proposals GROUP BY status")
    metrics["proposals_by_status"] = dict(c.fetchall())

    c.execute("SELECT priority, COUNT(*) FROM todos GROUP BY priority")
    metrics["todos_by_priority"] = dict(c.fetchall())

    c.execute("SELECT mode, COUNT(*) FROM collaboration_modes GROUP BY mode")
    metrics["ideas_by_mode"] = dict(c.fetchall())

    conn.close()
    return metrics


if __name__ == "__main__":
    import sys

    print("\n" + "=" * 60)
    print("SYSTEM POPULATION & GROWTH REVIEW")
    print("=" * 60 + "\n")

    # Review current state
    print("📊 Current State:")
    metrics = review_growth()
    print(f"  Ideas: {metrics.get('ideas', 0):,}")
    print(f"  Proposals: {metrics.get('proposals', 0)}")
    print(f"  Todos: {metrics.get('todos', 0)}")
    print(f"  Discussions: {metrics.get('discussions', 0)}")
    print(f"  Wiki pages: {metrics.get('wiki', 0)}")
    print(f"  Knowledge items: {metrics.get('knowledge', 0)}")
    print()

    if len(sys.argv) > 1 and sys.argv[1] == "populate":
        print("🚀 Populating system...\n")

        # Get high-value ideas
        ideas = get_high_value_ideas(50)
        print(f"Found {len(ideas)} high-value ideas")

        # Create proposals
        proposals = create_proposals_from_ideas(ideas)
        print(f"✓ Created {proposals} proposals")

        # Create discussions
        discussions = create_discussions_from_proposals()
        print(f"✓ Created {discussions} discussions")

        # Create todos
        todos = create_todos_from_ideas()
        print(f"✓ Created {todos} todos")

        # Consolidate docs to wiki
        wiki_pages = consolidate_docs_to_wiki()
        print(f"✓ Created {wiki_pages} wiki pages")

        print("\n" + "=" * 60)
        print("📊 Updated State:")
        metrics = review_growth()
        print(f"  Proposals: {metrics.get('proposals', 0)} (+{proposals})")
        print(f"  Todos: {metrics.get('todos', 0)} (+{todos})")
        print(f"  Discussions: {metrics.get('discussions', 0)} (+{discussions})")
        print(f"  Wiki pages: {metrics.get('wiki', 0)} (+{wiki_pages})")
        print("=" * 60)
    else:
        print("Usage: populate_system.py populate")
        print("\nThis will:")
        print("  • Create proposals from high-value ideas")
        print("  • Create discussions for proposals")
        print("  • Create todos from TODO ideas")
        print("  • Convert documentation to wiki pages")
