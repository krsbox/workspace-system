#!/usr/bin/env python3
"""Improvement Analyzer: What, Why, How - Identify and improve"""
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

DB_PATH = Path("/media/sunil-kr/workspace/workspace-system/workspace_knowledge.db")


def init_db():
    """Initialize improvement tables"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Improvement opportunities
    c.execute(
        """CREATE TABLE IF NOT EXISTS improvement_opportunities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        what TEXT NOT NULL,
        why TEXT NOT NULL,
        how TEXT NOT NULL,
        impact TEXT NOT NULL,
        effort TEXT NOT NULL,
        priority INTEGER NOT NULL,
        status TEXT DEFAULT 'identified',
        created_at TEXT NOT NULL
    )"""
    )

    conn.commit()
    conn.close()


# === WHAT: Identify Issues ===
def identify_what():
    """Identify what needs to be changed"""
    issues = []
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # 1. Missing tests
    try:
        c.execute('SELECT COUNT(*) FROM tools WHERE name LIKE "%test%"')
        test_tools = c.fetchone()[0]
        if test_tools == 0:
            issues.append(
                {
                    "what": "No automated tests",
                    "category": "quality",
                    "severity": "high",
                }
            )
    except:
        pass

    # 2. No backups
    backup_file = Path(DB_PATH).parent / "workspace_knowledge.backup.db"
    if not backup_file.exists():
        issues.append(
            {
                "what": "No database backups",
                "category": "reliability",
                "severity": "high",
            }
        )

    # 3. Manual processes
    c.execute("SELECT COUNT(*) FROM automated_tasks WHERE enabled=1")
    auto_tasks = c.fetchone()[0]
    if auto_tasks < 3:
        issues.append(
            {
                "what": "Few automated tasks",
                "category": "efficiency",
                "severity": "medium",
            }
        )

    # 4. No monitoring
    c.execute("SELECT COUNT(*) FROM health_checks")
    health_checks = c.fetchone()[0]
    if health_checks == 0:
        issues.append(
            {
                "what": "No health monitoring",
                "category": "observability",
                "severity": "medium",
            }
        )

    # 5. Unused capabilities
    c.execute("SELECT COUNT(*) FROM capabilities WHERE usage_count=0")
    unused = c.fetchone()[0]
    if unused > 0:
        issues.append(
            {
                "what": f"{unused} unused capabilities",
                "category": "complexity",
                "severity": "low",
            }
        )

    # 6. Old sessions
    cutoff = (datetime.now() - timedelta(days=7)).isoformat()
    c.execute(
        'SELECT COUNT(*) FROM sessions WHERE status="active" AND started_at < ?',
        (cutoff,),
    )
    old_sessions = c.fetchone()[0]
    if old_sessions > 0:
        issues.append(
            {
                "what": f"{old_sessions} stale sessions",
                "category": "cleanup",
                "severity": "low",
            }
        )

    # 7. No documentation for tools
    c.execute('SELECT COUNT(*) FROM tools WHERE description="" OR description IS NULL')
    undocumented = c.fetchone()[0]
    if undocumented > 0:
        issues.append(
            {
                "what": f"{undocumented} undocumented tools",
                "category": "documentation",
                "severity": "low",
            }
        )

    conn.close()
    return issues


# === WHY: Explain Impact ===
def explain_why(what):
    """Explain why something needs to change"""
    reasons = {
        "No automated tests": {
            "why": "Without tests, bugs go undetected until production",
            "impact": "High risk of breaking changes, reduced confidence in deployments",
            "cost": "Manual testing takes 10x longer, bugs cost 100x more to fix in production",
        },
        "No database backups": {
            "why": "Data loss is catastrophic and unrecoverable",
            "impact": "Single point of failure, all work could be lost",
            "cost": "Recovery impossible, complete rebuild required",
        },
        "Few automated tasks": {
            "why": "Manual work is error-prone and time-consuming",
            "impact": "Reduced productivity, inconsistent execution",
            "cost": "10+ hours per week on manual tasks",
        },
        "No health monitoring": {
            "why": "Issues go unnoticed until they become critical",
            "impact": "Reactive instead of proactive, longer downtime",
            "cost": "10x more expensive to fix than prevent",
        },
    }

    # Generic reasons for pattern matching
    if "unused" in what.lower():
        return {
            "why": "Unused code increases complexity without value",
            "impact": "Harder to maintain, slower to understand",
            "cost": "Cognitive overhead, potential bugs",
        }
    elif "stale" in what.lower() or "old" in what.lower():
        return {
            "why": "Stale data clutters the system",
            "impact": "Slower queries, confusing state",
            "cost": "Wasted resources, reduced clarity",
        }
    elif "undocumented" in what.lower():
        return {
            "why": "Undocumented code is hard to use and maintain",
            "impact": "Knowledge silos, onboarding friction",
            "cost": "Repeated questions, mistakes",
        }

    return reasons.get(
        what,
        {
            "why": "Improvement needed for better system health",
            "impact": "Moderate impact on system quality",
            "cost": "Some efficiency loss",
        },
    )


# === HOW: Provide Solutions ===
def suggest_how(what):
    """Suggest how to fix the issue"""
    solutions = {
        "No automated tests": {
            "how": "Create tests/ directory with pytest tests for each module",
            "steps": [
                "mkdir tests",
                "pip install pytest pytest-cov",
                "Create test_*.py files",
                "Run: pytest --cov=. tests/",
                "Add to CI/CD pipeline",
            ],
            "effort": "medium",
            "time": "4-8 hours",
        },
        "No database backups": {
            "how": "Setup automated daily backups with rotation",
            "steps": [
                "Create backup script",
                "Add cron job: 0 2 * * * backup.sh",
                "Keep 7 daily, 4 weekly, 12 monthly",
                "Test restore process",
                "Monitor backup success",
            ],
            "effort": "low",
            "time": "1-2 hours",
        },
        "Few automated tasks": {
            "how": "Identify manual tasks and automate them",
            "steps": [
                "List all manual tasks",
                "Prioritize by frequency",
                "Create automation scripts",
                "Schedule with cron",
                "Monitor execution",
            ],
            "effort": "medium",
            "time": "2-4 hours per task",
        },
        "No health monitoring": {
            "how": "Setup continuous health monitoring",
            "steps": [
                "Already have: automation_manager.py health",
                "Schedule: 0 * * * * health check",
                "Alert on failures",
                "Dashboard for visualization",
                "Track trends",
            ],
            "effort": "low",
            "time": "1 hour",
        },
    }

    # Generic solutions
    if "unused" in what.lower():
        return {
            "how": "Remove or archive unused components",
            "steps": [
                "Identify unused items",
                "Verify no dependencies",
                "Archive to backup",
                "Remove from active system",
                "Monitor for issues",
            ],
            "effort": "low",
            "time": "30 minutes",
        }
    elif "stale" in what.lower() or "old" in what.lower():
        return {
            "how": "Cleanup old data with retention policy",
            "steps": [
                "Define retention policy",
                "Archive old data",
                "Delete after archive",
                "Automate cleanup",
                "Monitor storage",
            ],
            "effort": "low",
            "time": "1 hour",
        }
    elif "undocumented" in what.lower():
        return {
            "how": "Add documentation to all tools",
            "steps": [
                "List undocumented items",
                "Add descriptions",
                "Add usage examples",
                "Generate API docs",
                "Keep updated",
            ],
            "effort": "low",
            "time": "15 min per tool",
        }

    return solutions.get(
        what,
        {
            "how": "Analyze and implement improvement",
            "steps": ["Investigate", "Plan", "Implement", "Test", "Deploy"],
            "effort": "medium",
            "time": "2-4 hours",
        },
    )


# === ANALYZE & PRIORITIZE ===
def analyze_and_prioritize():
    """Complete analysis with prioritization"""
    issues = identify_what()

    improvements = []
    for issue in issues:
        why = explain_why(issue["what"])
        how = suggest_how(issue["what"])

        # Calculate priority (1-10)
        severity_score = {"high": 8, "medium": 5, "low": 2}[issue["severity"]]
        effort_score = {"low": 3, "medium": 2, "high": 1}[how["effort"]]
        priority = severity_score + effort_score

        improvements.append(
            {
                "what": issue["what"],
                "why": why["why"],
                "how": how["how"],
                "impact": why["impact"],
                "effort": how["effort"],
                "steps": how["steps"],
                "time": how["time"],
                "priority": priority,
                "category": issue["category"],
            }
        )

    # Sort by priority
    improvements.sort(key=lambda x: x["priority"], reverse=True)

    return improvements


# === SAVE IMPROVEMENTS ===
def save_improvements(improvements):
    """Save to database"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    now = datetime.now().isoformat()

    for imp in improvements:
        try:
            c.execute(
                """INSERT INTO improvement_opportunities 
                        (what, why, how, impact, effort, priority, created_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (
                    imp["what"],
                    imp["why"],
                    imp["how"],
                    imp["impact"],
                    imp["effort"],
                    imp["priority"],
                    now,
                ),
            )
        except:
            pass  # Already exists

    conn.commit()
    conn.close()


# === GENERATE REPORT ===
def generate_improvement_report():
    """Generate comprehensive improvement report"""
    improvements = analyze_and_prioritize()
    save_improvements(improvements)

    print("\n" + "=" * 70)
    print("IMPROVEMENT ANALYSIS REPORT")
    print("=" * 70)
    print(f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Issues Found: {len(improvements)}")

    if not improvements:
        print("\n✅ No improvements needed - system is optimal!")
        return

    # Group by priority
    urgent = [i for i in improvements if i["priority"] >= 9]
    high = [i for i in improvements if 7 <= i["priority"] < 9]
    medium = [i for i in improvements if 4 <= i["priority"] < 7]
    low = [i for i in improvements if i["priority"] < 4]

    for priority_name, items, icon in [
        ("URGENT", urgent, "🔴"),
        ("HIGH", high, "🟠"),
        ("MEDIUM", medium, "🟡"),
        ("LOW", low, "🟢"),
    ]:
        if items:
            print(f"\n{icon} {priority_name} PRIORITY ({len(items)})")
            print("-" * 70)

            for i, imp in enumerate(items, 1):
                print(f"\n{i}. WHAT: {imp['what']}")
                print(f"   WHY:  {imp['why']}")
                print(f"   HOW:  {imp['how']}")
                print(f"   IMPACT: {imp['impact']}")
                print(f"   EFFORT: {imp['effort']} ({imp['time']})")

                if imp["steps"]:
                    print("   STEPS:")
                    for step in imp["steps"]:
                        print(f"     • {step}")

    print("\n" + "=" * 70)
    print("RECOMMENDED ACTION PLAN")
    print("=" * 70)

    print("\nThis Week:")
    for i, imp in enumerate(urgent + high[:2], 1):
        print(f"  {i}. {imp['what']} ({imp['time']})")

    print("\nThis Month:")
    for i, imp in enumerate(high[2:] + medium[:3], 1):
        print(f"  {i}. {imp['what']} ({imp['time']})")

    print("\nBacklog:")
    for i, imp in enumerate(low, 1):
        print(f"  {i}. {imp['what']} ({imp['time']})")

    print("\n" + "=" * 70 + "\n")


if __name__ == "__main__":
    import sys

    init_db()

    if len(sys.argv) < 2:
        print("Usage:")
        print("  Analyze: python improvement_analyzer.py analyze")
        print("  What:    python improvement_analyzer.py what")
        print("  Why:     python improvement_analyzer.py why <issue>")
        print("  How:     python improvement_analyzer.py how <issue>")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "analyze":
        generate_improvement_report()

    elif cmd == "what":
        issues = identify_what()
        print(f"\nFound {len(issues)} issues:\n")
        for i, issue in enumerate(issues, 1):
            print(f"{i}. [{issue['severity']}] {issue['what']} ({issue['category']})")

    elif cmd == "why" and len(sys.argv) >= 3:
        what = " ".join(sys.argv[2:])
        why = explain_why(what)
        print(f"\nWHY: {why['why']}")
        print(f"IMPACT: {why['impact']}")
        print(f"COST: {why['cost']}")

    elif cmd == "how" and len(sys.argv) >= 3:
        what = " ".join(sys.argv[2:])
        how = suggest_how(what)
        print(f"\nHOW: {how['how']}")
        print(f"EFFORT: {how['effort']} ({how['time']})")
        print("\nSTEPS:")
        for step in how["steps"]:
            print(f"  • {step}")
