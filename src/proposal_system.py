#!/usr/bin/env python3
"""Proposal System: Submit, Review, Validate, Convert to Todos"""
import sqlite3
import json
from datetime import datetime
from pathlib import Path

DB_PATH = Path("/media/sunil-kr/workspace/workspace-system/workspace_knowledge.db")


def init_db():
    """Initialize proposal tables"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Proposals
    c.execute(
        """CREATE TABLE IF NOT EXISTS proposals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        rationale TEXT,
        impact TEXT,
        effort TEXT,
        category TEXT,
        status TEXT DEFAULT 'submitted',
        score INTEGER DEFAULT 0,
        submitted_by TEXT,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    )"""
    )

    # Reviews
    c.execute(
        """CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        proposal_id INTEGER NOT NULL,
        reviewer TEXT,
        decision TEXT NOT NULL,
        score INTEGER,
        comments TEXT,
        criteria TEXT,
        created_at TEXT NOT NULL,
        FOREIGN KEY (proposal_id) REFERENCES proposals(id)
    )"""
    )

    # Validation criteria
    c.execute(
        """CREATE TABLE IF NOT EXISTS criteria (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        description TEXT,
        weight INTEGER DEFAULT 1,
        active INTEGER DEFAULT 1
    )"""
    )

    conn.commit()
    conn.close()


def add_criteria(name, description, weight=1):
    """Add validation criteria"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute(
            "INSERT INTO criteria (name, description, weight) VALUES (?, ?, ?)",
            (name, description, weight),
        )
        conn.commit()
        crit_id = c.lastrowid
    except sqlite3.IntegrityError:
        crit_id = None
    finally:
        conn.close()
    return crit_id


def list_criteria():
    """List active criteria"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM criteria WHERE active=1 ORDER BY weight DESC")
    results = c.fetchall()
    conn.close()
    return results


def submit_proposal(
    title,
    description,
    rationale="",
    impact="medium",
    effort="medium",
    category="improvement",
    submitted_by="user",
):
    """Submit improvement proposal"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    now = datetime.now().isoformat()

    c.execute(
        """INSERT INTO proposals 
                 (title, description, rationale, impact, effort, category, submitted_by, created_at, updated_at)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            title,
            description,
            rationale,
            impact,
            effort,
            category,
            submitted_by,
            now,
            now,
        ),
    )

    conn.commit()
    prop_id = c.lastrowid
    conn.close()
    return prop_id


def review_proposal(
    proposal_id, decision, reviewer="system", score=0, comments="", criteria_scores=None
):
    """Review a proposal"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    now = datetime.now().isoformat()

    criteria_json = json.dumps(criteria_scores) if criteria_scores else None

    c.execute(
        """INSERT INTO reviews (proposal_id, reviewer, decision, score, comments, criteria, created_at)
                 VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (proposal_id, reviewer, decision, score, comments, criteria_json, now),
    )

    # Update proposal status and score
    if decision == "approved":
        c.execute(
            "UPDATE proposals SET status=?, score=?, updated_at=? WHERE id=?",
            ("approved", score, now, proposal_id),
        )
    elif decision == "rejected":
        c.execute(
            "UPDATE proposals SET status=?, updated_at=? WHERE id=?",
            ("rejected", now, proposal_id),
        )
    elif decision == "needs_revision":
        c.execute(
            "UPDATE proposals SET status=?, updated_at=? WHERE id=?",
            ("needs_revision", now, proposal_id),
        )

    conn.commit()
    conn.close()


def auto_validate(proposal_id):
    """Auto-validate proposal against criteria"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Get proposal
    c.execute("SELECT * FROM proposals WHERE id=?", (proposal_id,))
    proposal = c.fetchone()

    if not proposal:
        conn.close()
        return None

    # Get criteria
    c.execute("SELECT * FROM criteria WHERE active=1")
    criteria = c.fetchall()

    # Simple scoring logic
    scores = {}
    total_score = 0
    max_score = 0

    for crit in criteria:
        crit_id, name, desc, weight, _ = crit
        max_score += weight * 10

        # Score based on criteria (simplified)
        if name == "impact":
            impact_scores = {"low": 3, "medium": 6, "high": 9, "critical": 10}
            score = impact_scores.get(proposal[4], 5) * weight
        elif name == "effort":
            effort_scores = {"low": 10, "medium": 7, "high": 4, "very_high": 2}
            score = effort_scores.get(proposal[5], 5) * weight
        elif name == "clarity":
            # Score based on description length and rationale
            desc_len = len(proposal[2])
            has_rationale = len(proposal[3]) > 20
            score = (min(desc_len / 50, 10) + (5 if has_rationale else 0)) * weight / 2
        else:
            score = 5 * weight

        scores[name] = round(score, 1)
        total_score += score

    # Calculate percentage
    percentage = round((total_score / max_score * 100) if max_score > 0 else 0)

    # Auto decision
    if percentage >= 70:
        decision = "approved"
    elif percentage >= 50:
        decision = "needs_revision"
    else:
        decision = "rejected"

    conn.close()

    return {
        "decision": decision,
        "score": percentage,
        "criteria_scores": scores,
        "total": total_score,
        "max": max_score,
    }


def convert_to_todo(proposal_id):
    """Convert approved proposal to todo"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Get proposal
    c.execute("SELECT * FROM proposals WHERE id=? AND status=?", (proposal_id, "approved"))
    proposal = c.fetchone()

    if not proposal:
        conn.close()
        return None

    # Create todo
    now = datetime.now().isoformat()
    priority_map = {
        "low": "low",
        "medium": "medium",
        "high": "high",
        "critical": "urgent",
    }
    priority = priority_map.get(proposal[4], "medium")

    c.execute(
        """INSERT INTO todos (title, description, status, priority, project, created_at, updated_at)
                 VALUES (?, ?, 'todo', ?, ?, ?, ?)""",
        (proposal[1], proposal[2], priority, proposal[6], now, now),
    )

    todo_id = c.lastrowid

    # Update proposal
    c.execute(
        "UPDATE proposals SET status=?, updated_at=? WHERE id=?",
        ("converted", now, proposal_id),
    )

    conn.commit()
    conn.close()
    return todo_id


def list_proposals(status=None):
    """List proposals"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    if status:
        c.execute(
            "SELECT * FROM proposals WHERE status=? ORDER BY score DESC, created_at DESC",
            (status,),
        )
    else:
        c.execute("SELECT * FROM proposals ORDER BY status, score DESC, created_at DESC")

    results = c.fetchall()
    conn.close()
    return results


def get_proposal_reviews(proposal_id):
    """Get all reviews for a proposal"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "SELECT * FROM reviews WHERE proposal_id=? ORDER BY created_at DESC",
        (proposal_id,),
    )
    results = c.fetchall()
    conn.close()
    return results


if __name__ == "__main__":
    import sys

    init_db()

    if len(sys.argv) < 2:
        print("Usage:")
        print("  Criteria: python proposal_system.py criteria <add|list>")
        print(
            "  Submit:   python proposal_system.py submit <title> <description> [rationale] [impact] [effort]"
        )
        print("  Review:   python proposal_system.py review <id> <decision> [comments]")
        print("  Validate: python proposal_system.py validate <id>")
        print("  Convert:  python proposal_system.py convert <id>")
        print("  List:     python proposal_system.py list [status]")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "criteria":
        if len(sys.argv) > 2 and sys.argv[2] == "add":
            crit_id = add_criteria(
                sys.argv[3], sys.argv[4], int(sys.argv[5]) if len(sys.argv) > 5 else 1
            )
            print(f"Added criteria #{crit_id}")
        else:
            criteria = list_criteria()
            print("\nValidation Criteria:")
            for c in criteria:
                print(f"  [{c[3]}] {c[1]}: {c[2]}")

    elif cmd == "submit" and len(sys.argv) >= 4:
        rationale = sys.argv[5] if len(sys.argv) > 5 else ""
        impact = sys.argv[6] if len(sys.argv) > 6 else "medium"
        effort = sys.argv[7] if len(sys.argv) > 7 else "medium"
        prop_id = submit_proposal(sys.argv[2], sys.argv[3], rationale, impact, effort)
        print(f"Submitted proposal #{prop_id}")

    elif cmd == "review" and len(sys.argv) >= 4:
        comments = sys.argv[5] if len(sys.argv) > 5 else ""
        review_proposal(int(sys.argv[2]), sys.argv[3], comments=comments)
        print(f"Reviewed proposal #{sys.argv[2]}")

    elif cmd == "validate" and len(sys.argv) >= 3:
        result = auto_validate(int(sys.argv[2]))
        if result:
            print(f"\nValidation Result: {result['decision'].upper()}")
            print(f"Score: {result['score']}% ({result['total']:.1f}/{result['max']:.1f})")
            print("\nCriteria Scores:")
            for name, score in result["criteria_scores"].items():
                print(f"  {name}: {score}")

            # Auto-review
            review_proposal(
                int(sys.argv[2]),
                result["decision"],
                "system",
                result["score"],
                f"Auto-validated: {result['score']}%",
                result["criteria_scores"],
            )
            print(f"\nProposal #{sys.argv[2]} auto-reviewed")

    elif cmd == "convert" and len(sys.argv) >= 3:
        todo_id = convert_to_todo(int(sys.argv[2]))
        if todo_id:
            print(f"Converted proposal #{sys.argv[2]} to todo #{todo_id}")
        else:
            print("Proposal not approved or not found")

    elif cmd == "list":
        status = sys.argv[2] if len(sys.argv) > 2 else None
        proposals = list_proposals(status)
        print(f"\nProposals ({len(proposals)}):")
        for p in proposals:
            print(f"  [{p[7]}] #{p[0]}: {p[1]} (impact:{p[4]}, effort:{p[5]}, score:{p[8]}%)")
