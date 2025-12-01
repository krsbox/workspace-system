#!/usr/bin/env python3
"""Evolution Tracker: Track system improvements over time"""
import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path("/media/sunil-kr/workspace/workspace-system/workspace_knowledge.db")


def init_evolution_table():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        """CREATE TABLE IF NOT EXISTS system_evolution (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        metric TEXT NOT NULL,
        value REAL NOT NULL,
        notes TEXT
    )"""
    )
    conn.commit()
    conn.close()


def capture_snapshot():
    """Capture current system state"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    metrics = {}

    # Ideas
    c.execute("SELECT COUNT(*) FROM ideas WHERE reality_score >= 70")
    metrics["ideas_high_quality"] = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM ideas")
    metrics["ideas_total"] = c.fetchone()[0]

    # Proposals
    c.execute("SELECT COUNT(*) FROM proposals")
    metrics["proposals_total"] = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM proposals WHERE status='approved'")
    metrics["proposals_approved"] = c.fetchone()[0]

    # Todos
    c.execute("SELECT COUNT(*) FROM todos")
    metrics["todos_total"] = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM todos WHERE status='done'")
    metrics["todos_completed"] = c.fetchone()[0]

    # Tools
    c.execute("SELECT COUNT(*) FROM tools")
    metrics["tools_count"] = c.fetchone()[0]

    # Knowledge
    c.execute("SELECT COUNT(*) FROM knowledge")
    metrics["knowledge_items"] = c.fetchone()[0]

    conn.close()
    return metrics


def save_snapshot(metrics, notes=""):
    """Save snapshot to evolution table"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    timestamp = datetime.now().isoformat()
    for metric, value in metrics.items():
        c.execute(
            """INSERT INTO system_evolution (timestamp, metric, value, notes)
                     VALUES (?, ?, ?, ?)""",
            (timestamp, metric, value, notes),
        )

    conn.commit()
    conn.close()


def show_evolution():
    """Show system evolution over time"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Get unique timestamps
    c.execute("SELECT DISTINCT timestamp FROM system_evolution ORDER BY timestamp")
    timestamps = [row[0] for row in c.fetchall()]

    if not timestamps:
        print("No evolution data yet. Run: evolution_tracker.py snapshot")
        conn.close()
        return

    print("\n" + "=" * 70)
    print("SYSTEM EVOLUTION TIMELINE")
    print("=" * 70 + "\n")

    for ts in timestamps:
        dt = datetime.fromisoformat(ts)
        print(f"📅 {dt.strftime('%Y-%m-%d %H:%M:%S')}")

        c.execute("SELECT metric, value FROM system_evolution WHERE timestamp=?", (ts,))
        for metric, value in c.fetchall():
            print(f"  {metric:25} {int(value):,}")
        print()

    # Show growth
    if len(timestamps) >= 2:
        print("=" * 70)
        print("GROWTH METRICS")
        print("=" * 70 + "\n")

        first_ts = timestamps[0]
        last_ts = timestamps[-1]

        c.execute(
            "SELECT metric, value FROM system_evolution WHERE timestamp=?", (first_ts,)
        )
        first_metrics = dict(c.fetchall())

        c.execute(
            "SELECT metric, value FROM system_evolution WHERE timestamp=?", (last_ts,)
        )
        last_metrics = dict(c.fetchall())

        for metric in first_metrics:
            if metric in last_metrics:
                growth = last_metrics[metric] - first_metrics[metric]
                pct = (
                    (growth / first_metrics[metric] * 100)
                    if first_metrics[metric] > 0
                    else 0
                )
                emoji = "📈" if growth > 0 else "📉" if growth < 0 else "➡️"
                print(f"{emoji} {metric:25} {growth:+,.0f} ({pct:+.1f}%)")

    conn.close()


if __name__ == "__main__":
    import sys

    init_evolution_table()

    if len(sys.argv) < 2:
        print("Usage:")
        print("  evolution_tracker.py snapshot [notes]  - Capture current state")
        print("  evolution_tracker.py show              - Show evolution timeline")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "snapshot":
        notes = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else ""
        metrics = capture_snapshot()
        save_snapshot(metrics, notes)

        print("\n✓ Snapshot captured")
        print("\nCurrent metrics:")
        for metric, value in metrics.items():
            print(f"  {metric:25} {int(value):,}")

    elif cmd == "show":
        show_evolution()
