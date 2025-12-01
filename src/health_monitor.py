#!/usr/bin/env python3
"""Health Monitor: Continuous system health tracking"""
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

DB_PATH = Path("/media/sunil-kr/workspace/workspace-system/workspace_knowledge.db")


def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        """CREATE TABLE IF NOT EXISTS health_checks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        status TEXT NOT NULL,
        data TEXT,
        checked_at TEXT NOT NULL
    )"""
    )
    conn.commit()
    conn.close()


def check_health():
    """Run health check and record"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Database size
    db_size = DB_PATH.stat().st_size

    # Active tools
    c.execute("SELECT COUNT(*) FROM tools")
    tools_active = c.fetchone()[0]

    # Quality grade
    c.execute("SELECT grade FROM assessments ORDER BY created_at DESC LIMIT 1")
    row = c.fetchone()
    quality_grade = row[0] if row else "N/A"

    # Unresolved alerts
    c.execute("SELECT COUNT(*) FROM degradation_alerts WHERE resolved = 0")
    alerts = c.fetchone()[0]

    # Determine status
    issues = []
    if db_size > 10 * 1024 * 1024:  # > 10MB
        issues.append("Database too large")
    if tools_active < 5:
        issues.append("Few tools active")
    if quality_grade in ["D", "F"]:
        issues.append("Low quality grade")
    if alerts > 5:
        issues.append("Many unresolved alerts")

    status = "CRITICAL" if len(issues) >= 3 else "WARNING" if issues else "HEALTHY"

    # Record check
    import json

    data = json.dumps(
        {
            "db_size": db_size,
            "tools_active": tools_active,
            "quality_grade": quality_grade,
            "alerts": alerts,
            "issues": issues,
        }
    )
    c.execute(
        """INSERT INTO health_checks (status, data, checked_at)
        VALUES (?, ?, ?)""",
        (status, data, datetime.now().isoformat()),
    )

    conn.commit()
    conn.close()

    return {
        "status": status,
        "db_size": db_size,
        "tools_active": tools_active,
        "quality_grade": quality_grade,
        "alerts": alerts,
        "issues": issues,
    }


def get_health_history(hours=24):
    """Get health history"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    since = (datetime.now() - timedelta(hours=hours)).isoformat()
    c.execute(
        """SELECT status, checked_at FROM health_checks 
        WHERE checked_at > ? ORDER BY checked_at DESC""",
        (since,),
    )

    history = c.fetchall()
    conn.close()
    return history


def print_health():
    """Print current health"""
    health = check_health()

    emoji = {"HEALTHY": "🟢", "WARNING": "🟡", "CRITICAL": "🔴"}
    print(f"\n{emoji[health['status']]} SYSTEM HEALTH: {health['status']}")
    print("-" * 60)
    print(f"  Database:     {health['db_size'] / 1024:.1f} KB")
    print(f"  Tools Active: {health['tools_active']}")
    print(f"  Quality:      {health['quality_grade']}")
    print(f"  Alerts:       {health['alerts']}")

    if health["issues"]:
        print("\n⚠️  Issues:")
        for issue in health["issues"]:
            print(f"    • {issue}")


def print_history(hours=24):
    """Print health history"""
    history = get_health_history(hours)

    print(f"\n📊 HEALTH HISTORY (last {hours}h)")
    print("-" * 60)

    if not history:
        print("  No history available")
        return

    emoji = {"HEALTHY": "🟢", "WARNING": "🟡", "CRITICAL": "🔴"}
    for status, checked_at in history[:20]:
        dt = datetime.fromisoformat(checked_at)
        print(f"  {emoji[status]} {status:10} - {dt.strftime('%Y-%m-%d %H:%M')}")


if __name__ == "__main__":
    import sys

    init_db()

    if len(sys.argv) < 2:
        print_health()
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == "check":
        print_health()
    elif cmd == "history":
        hours = int(sys.argv[2]) if len(sys.argv) > 2 else 24
        print_history(hours)
    else:
        print("Usage: health_monitor.py [check|history [hours]]")
