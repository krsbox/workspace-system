#!/usr/bin/env python3
"""Human-AI Collaboration: Intelligent idea management with human oversight"""
import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path("/media/sunil-kr/workspace/workspace-system/workspace_knowledge.db")


def init_collaboration_tables():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Collaboration modes
    c.execute(
        """CREATE TABLE IF NOT EXISTS collaboration_modes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        idea_id INTEGER,
        mode TEXT NOT NULL,
        confidence REAL,
        requires_review BOOLEAN DEFAULT 1,
        reviewed_by TEXT,
        reviewed_at TEXT,
        decision TEXT,
        notes TEXT,
        created_at TEXT NOT NULL
    )"""
    )

    # AI suggestions
    c.execute(
        """CREATE TABLE IF NOT EXISTS ai_suggestions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        idea_id INTEGER,
        suggestion_type TEXT,
        suggestion TEXT,
        confidence REAL,
        reasoning TEXT,
        accepted BOOLEAN,
        human_feedback TEXT,
        created_at TEXT NOT NULL
    )"""
    )

    # Human overrides
    c.execute(
        """CREATE TABLE IF NOT EXISTS human_overrides (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        idea_id INTEGER,
        ai_decision TEXT,
        human_decision TEXT,
        reason TEXT,
        created_at TEXT NOT NULL
    )"""
    )

    conn.commit()
    conn.close()


def classify_idea_mode(idea_id, reality_score, category):
    """Classify idea into collaboration mode"""

    # AI-in-the-loop: High confidence, automated
    if reality_score >= 90 and category in ["pattern", "documentation"]:
        return {
            "mode": "ai_automated",
            "confidence": 0.95,
            "requires_review": False,
            "reasoning": "High reality score + safe category",
        }

    # AI-assisted: Medium confidence, human approval
    elif reality_score >= 70:
        return {
            "mode": "ai_assisted",
            "confidence": 0.75,
            "requires_review": True,
            "reasoning": "Good quality, needs human validation",
        }

    # Human-in-the-loop: Low confidence, human decision
    elif reality_score >= 50:
        return {
            "mode": "human_primary",
            "confidence": 0.50,
            "requires_review": True,
            "reasoning": "Medium quality, human judgment required",
        }

    # Human-only: Very low confidence
    else:
        return {
            "mode": "human_only",
            "confidence": 0.25,
            "requires_review": True,
            "reasoning": "Low quality, manual review essential",
        }


def suggest_action(idea_id, title, category, reality_score):
    """AI suggests action for idea"""

    suggestions = []

    # Pattern suggestions
    if category == "pattern" and reality_score >= 85:
        suggestions.append(
            {
                "type": "integrate",
                "action": "Add to pattern library",
                "confidence": 0.90,
                "reasoning": "High-quality reusable pattern",
            }
        )

    # TODO suggestions
    if category == "todo":
        if "security" in title.lower() or "bug" in title.lower():
            suggestions.append(
                {
                    "type": "urgent",
                    "action": "Create high-priority proposal",
                    "confidence": 0.95,
                    "reasoning": "Security/bug related",
                }
            )
        elif "deprecated" in title.lower():
            suggestions.append(
                {
                    "type": "technical_debt",
                    "action": "Schedule for refactoring",
                    "confidence": 0.80,
                    "reasoning": "Technical debt item",
                }
            )

    # Documentation suggestions
    if category == "documentation" and reality_score >= 75:
        suggestions.append(
            {
                "type": "consolidate",
                "action": "Merge with existing docs",
                "confidence": 0.85,
                "reasoning": "Good documentation quality",
            }
        )

    return suggestions


def save_collaboration_mode(idea_id, mode_info):
    """Save collaboration mode for idea"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        """INSERT INTO collaboration_modes 
        (idea_id, mode, confidence, requires_review, created_at)
        VALUES (?, ?, ?, ?, ?)""",
        (
            idea_id,
            mode_info["mode"],
            mode_info["confidence"],
            mode_info["requires_review"],
            datetime.now().isoformat(),
        ),
    )
    conn.commit()
    conn.close()


def save_ai_suggestion(idea_id, suggestion):
    """Save AI suggestion"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        """INSERT INTO ai_suggestions
        (idea_id, suggestion_type, suggestion, confidence, reasoning, created_at)
        VALUES (?, ?, ?, ?, ?, ?)""",
        (
            idea_id,
            suggestion["type"],
            suggestion["action"],
            suggestion["confidence"],
            suggestion["reasoning"],
            datetime.now().isoformat(),
        ),
    )
    conn.commit()
    conn.close()


def get_ideas_by_mode(mode):
    """Get ideas by collaboration mode"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        """SELECT i.id, i.title, i.category, i.reality_score, cm.confidence
        FROM ideas i
        JOIN collaboration_modes cm ON i.id = cm.idea_id
        WHERE cm.mode = ?
        ORDER BY cm.confidence DESC, i.reality_score DESC""",
        (mode,),
    )
    ideas = c.fetchall()
    conn.close()
    return ideas


def human_review(idea_id, decision, notes=""):
    """Record human review decision"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        """UPDATE collaboration_modes
        SET reviewed_by = 'human', reviewed_at = ?, decision = ?, notes = ?
        WHERE idea_id = ?""",
        (datetime.now().isoformat(), decision, notes, idea_id),
    )
    conn.commit()
    conn.close()


def record_override(idea_id, ai_decision, human_decision, reason):
    """Record when human overrides AI"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        """INSERT INTO human_overrides
        (idea_id, ai_decision, human_decision, reason, created_at)
        VALUES (?, ?, ?, ?, ?)""",
        (idea_id, ai_decision, human_decision, reason, datetime.now().isoformat()),
    )
    conn.commit()
    conn.close()


if __name__ == "__main__":
    import sys

    init_collaboration_tables()

    if len(sys.argv) < 2:
        print("Usage:")
        print("  human_ai_collaboration.py classify      - Classify all ideas")
        print("  human_ai_collaboration.py suggest <id>  - Get AI suggestions")
        print("  human_ai_collaboration.py review <mode> - Review ideas by mode")
        print("  human_ai_collaboration.py stats         - Show collaboration stats")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "classify":
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT id, title, category, reality_score FROM ideas LIMIT 100")
        ideas = c.fetchall()
        conn.close()

        for idea_id, title, category, reality in ideas:
            mode_info = classify_idea_mode(idea_id, reality, category)
            save_collaboration_mode(idea_id, mode_info)

            suggestions = suggest_action(idea_id, title, category, reality)
            for suggestion in suggestions:
                save_ai_suggestion(idea_id, suggestion)

        print(f"✓ Classified {len(ideas)} ideas")

    elif cmd == "review":
        mode = sys.argv[2] if len(sys.argv) > 2 else "ai_assisted"
        ideas = get_ideas_by_mode(mode)

        print(f"\n{mode.upper()} IDEAS ({len(ideas)} total)\n")
        for idea_id, title, category, reality, confidence in ideas[:20]:
            print(
                f"  #{idea_id:5} [{category:12}] {reality:.0f}% conf:{confidence:.0%}"
            )
            print(f"         {title[:70]}")

    elif cmd == "stats":
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        print("\n" + "=" * 60)
        print("COLLABORATION STATISTICS")
        print("=" * 60 + "\n")

        c.execute(
            "SELECT mode, COUNT(*), AVG(confidence) FROM collaboration_modes GROUP BY mode"
        )
        for mode, count, avg_conf in c.fetchall():
            print(f"{mode:20} {count:6,} ideas (avg confidence: {avg_conf:.0%})")

        print()
        c.execute("SELECT COUNT(*) FROM collaboration_modes WHERE requires_review = 1")
        needs_review = c.fetchone()[0]
        print(f"Needs human review: {needs_review:,}")

        c.execute(
            "SELECT COUNT(*) FROM collaboration_modes WHERE reviewed_by IS NOT NULL"
        )
        reviewed = c.fetchone()[0]
        print(f"Already reviewed: {reviewed:,}")

        conn.close()
