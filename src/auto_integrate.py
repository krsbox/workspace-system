#!/usr/bin/env python3
"""Auto Integrator: Intelligent integration based on collaboration mode"""
import sqlite3
import subprocess
from pathlib import Path

DB_PATH = Path("/media/sunil-kr/workspace/workspace-system/workspace_knowledge.db")


def get_ideas_for_mode(mode, limit=10):
    """Get ideas ready for integration by mode"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    if mode == "ai_automated":
        # High confidence, no review needed
        c.execute(
            """SELECT i.id, i.title, i.category, i.reality_score, cm.confidence
            FROM ideas i
            JOIN collaboration_modes cm ON i.id = cm.idea_id
            WHERE cm.mode = ? AND cm.requires_review = 0 AND cm.reviewed_by IS NULL
            ORDER BY cm.confidence DESC, i.reality_score DESC
            LIMIT ?""",
            (mode, limit),
        )

    elif mode == "ai_assisted":
        # Approved by human
        c.execute(
            """SELECT i.id, i.title, i.category, i.reality_score, cm.confidence
            FROM ideas i
            JOIN collaboration_modes cm ON i.id = cm.idea_id
            WHERE cm.mode = ? AND cm.decision = 'approved'
            ORDER BY cm.confidence DESC, i.reality_score DESC
            LIMIT ?""",
            (mode, limit),
        )

    else:
        return []

    ideas = c.fetchall()
    conn.close()
    return ideas


def check_safe_to_integrate(idea_id, title):
    """Safety checks before integration"""
    # Check duplication
    result = subprocess.run(
        ["python3", "dedup_checker.py", title], capture_output=True, text=True
    )

    if result.returncode != 0:
        return False, "Duplicate found"

    # Check quality
    result = subprocess.run(["./ws", "check"], capture_output=True, text=True)

    if "PASS" not in result.stdout:
        return False, "Quality check failed"

    return True, "Safe to integrate"


def integrate_idea(idea_id, title, mode):
    """Integrate idea based on mode"""

    # Safety check
    safe, reason = check_safe_to_integrate(idea_id, title)
    if not safe:
        return False, reason

    # Create proposal
    result = subprocess.run(
        ["./ws", "propose", title],
        input=f"Auto-integrated via {mode} mode",
        capture_output=True,
        text=True,
    )

    if result.returncode == 0:
        # Mark as integrated
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute(
            """UPDATE collaboration_modes 
            SET reviewed_by = ?, reviewed_at = datetime('now'), decision = 'integrated'
            WHERE idea_id = ?""",
            (mode, idea_id),
        )
        conn.commit()
        conn.close()
        return True, "Integrated successfully"

    return False, "Integration failed"


def auto_integrate(mode, dry_run=False, limit=10):
    """Auto-integrate ideas by mode"""
    print(f"\n{'[DRY RUN] ' if dry_run else ''}Auto-integrating: {mode}")
    print("=" * 60)

    ideas = get_ideas_for_mode(mode, limit)
    print(f"\nFound {len(ideas)} ideas ready for integration\n")

    integrated = 0
    skipped = 0

    for idea_id, title, category, reality, confidence in ideas:
        print(f"Processing #{idea_id}: {title[:50]}...")
        print(
            f"  Category: {category}, Reality: {reality:.0f}%, Confidence: {confidence:.0%}"
        )

        if dry_run:
            print("  [DRY RUN] Would integrate")
            integrated += 1
        else:
            success, reason = integrate_idea(idea_id, title, mode)
            if success:
                print(f"  ✓ {reason}")
                integrated += 1
            else:
                print(f"  ✗ {reason}")
                skipped += 1

    print(f"\n{'[DRY RUN] ' if dry_run else ''}Summary:")
    print(f"  Integrated: {integrated}")
    print(f"  Skipped: {skipped}")

    return integrated, skipped


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage:")
        print("  auto_integrate.py ai_automated [--dry-run] [--limit N]")
        print("  auto_integrate.py ai_assisted [--dry-run] [--limit N]")
        sys.exit(1)

    mode = sys.argv[1]
    dry_run = "--dry-run" in sys.argv
    limit = 10

    if "--limit" in sys.argv:
        idx = sys.argv.index("--limit")
        limit = int(sys.argv[idx + 1])

    auto_integrate(mode, dry_run, limit)
