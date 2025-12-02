#!/usr/bin/env python3
"""Prevention System: Lightweight proactive measures to avoid issues"""
import sqlite3
import json
from datetime import datetime, timedelta
from pathlib import Path

DB_PATH = Path("/media/sunil-kr/workspace/workspace-system/workspace_knowledge.db")


def init_db():
    """Initialize prevention tables"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Prevention rules (lightweight checks)
    c.execute(
        """CREATE TABLE IF NOT EXISTS prevention_rules (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        type TEXT NOT NULL,
        condition TEXT NOT NULL,
        action TEXT NOT NULL,
        enabled INTEGER DEFAULT 1,
        overhead TEXT DEFAULT 'low',
        created_at TEXT NOT NULL
    )"""
    )

    # Prevention events (what was prevented)
    c.execute(
        """CREATE TABLE IF NOT EXISTS prevention_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        rule_id INTEGER NOT NULL,
        prevented TEXT NOT NULL,
        details TEXT,
        created_at TEXT NOT NULL,
        FOREIGN KEY (rule_id) REFERENCES prevention_rules(id)
    )"""
    )

    # Guardrails (boundaries that can't be crossed)
    c.execute(
        """CREATE TABLE IF NOT EXISTS guardrails (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        type TEXT NOT NULL,
        limit_value TEXT NOT NULL,
        enforcement TEXT DEFAULT 'hard',
        enabled INTEGER DEFAULT 1,
        created_at TEXT NOT NULL
    )"""
    )

    # Early warnings (before things go wrong)
    c.execute(
        """CREATE TABLE IF NOT EXISTS early_warnings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        component TEXT NOT NULL,
        warning_type TEXT NOT NULL,
        message TEXT NOT NULL,
        threshold_percent INTEGER,
        acknowledged INTEGER DEFAULT 0,
        created_at TEXT NOT NULL
    )"""
    )

    conn.commit()
    conn.close()


# === PREVENTION RULES ===
def add_prevention_rule(name, type, condition, action, overhead="low"):
    """Add prevention rule"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    now = datetime.now().isoformat()

    try:
        c.execute(
            """INSERT INTO prevention_rules (name, type, condition, action, overhead, created_at)
                     VALUES (?, ?, ?, ?, ?, ?)""",
            (name, type, condition, action, overhead, now),
        )
        conn.commit()
        rule_id = c.lastrowid
    except sqlite3.IntegrityError:
        rule_id = None
    finally:
        conn.close()
    return rule_id


def check_prevention_rules(context):
    """Check all prevention rules (lightweight)"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("SELECT * FROM prevention_rules WHERE enabled=1")
    rules = c.fetchall()

    prevented = []

    for rule in rules:
        rule_id, name, type, condition, action, enabled, overhead, created_at = rule

        # Quick checks only (low overhead)
        should_prevent = False
        details = {}

        if type == "size_limit":
            cond = json.loads(condition)
            if context.get("size", 0) > cond.get("max_size", float("inf")):
                should_prevent = True
                details = {"size": context["size"], "limit": cond["max_size"]}

        elif type == "rate_limit":
            cond = json.loads(condition)
            component = cond.get("component")
            max_rate = cond.get("max_per_minute")

            # Check recent events
            cutoff = (datetime.now() - timedelta(minutes=1)).isoformat()
            c.execute(
                """SELECT COUNT(*) FROM tool_executions 
                        WHERE created_at > ? AND tool_id IN 
                        (SELECT id FROM tools WHERE name=?)""",
                (cutoff, component),
            )
            count = c.fetchone()[0]

            if count >= max_rate:
                should_prevent = True
                details = {"rate": count, "limit": max_rate}

        elif type == "dependency_check":
            cond = json.loads(condition)
            required = cond.get("requires")
            if required and not context.get(required):
                should_prevent = True
                details = {"missing": required}

        elif type == "validation":
            cond = json.loads(condition)
            field = cond.get("field")
            pattern = cond.get("pattern")
            if field in context:
                import re

                if not re.match(pattern, str(context[field])):
                    should_prevent = True
                    details = {"field": field, "value": context[field]}

        if should_prevent:
            # Log prevention
            c.execute(
                """INSERT INTO prevention_events (rule_id, prevented, details, created_at)
                        VALUES (?, ?, ?, ?)""",
                (rule_id, action, json.dumps(details), datetime.now().isoformat()),
            )
            conn.commit()

            prevented.append({"rule": name, "action": action, "details": details})

    conn.close()
    return prevented


# === GUARDRAILS ===
def add_guardrail(name, type, limit_value, enforcement="hard"):
    """Add guardrail (hard boundary)"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    now = datetime.now().isoformat()

    try:
        c.execute(
            """INSERT INTO guardrails (name, type, limit_value, enforcement, created_at)
                     VALUES (?, ?, ?, ?, ?)""",
            (name, type, limit_value, enforcement, now),
        )
        conn.commit()
        guardrail_id = c.lastrowid
    except sqlite3.IntegrityError:
        guardrail_id = None
    finally:
        conn.close()
    return guardrail_id


def check_guardrails(type, value):
    """Check if value violates guardrails"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("SELECT * FROM guardrails WHERE type=? AND enabled=1", (type,))
    guardrails = c.fetchall()
    conn.close()

    violations = []
    for g in guardrails:
        limit = json.loads(g[3])

        if "max" in limit and value > limit["max"]:
            violations.append(
                {
                    "guardrail": g[1],
                    "type": "max_exceeded",
                    "value": value,
                    "limit": limit["max"],
                    "enforcement": g[4],
                }
            )

        if "min" in limit and value < limit["min"]:
            violations.append(
                {
                    "guardrail": g[1],
                    "type": "min_violated",
                    "value": value,
                    "limit": limit["min"],
                    "enforcement": g[4],
                }
            )

    return violations


# === EARLY WARNINGS ===
def check_early_warning(component, metric_name, current_value, threshold):
    """Issue early warning before threshold breach"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Calculate how close to threshold (percentage)
    if threshold > 0:
        percent = (current_value / threshold) * 100
    else:
        percent = 0

    # Warn at 80%, 90%, 95%
    warning_levels = [80, 90, 95]

    for level in warning_levels:
        if percent >= level:
            # Check if already warned at this level recently
            cutoff = (datetime.now() - timedelta(hours=1)).isoformat()
            c.execute(
                """SELECT COUNT(*) FROM early_warnings 
                        WHERE component=? AND warning_type=? AND threshold_percent=? 
                        AND created_at > ?""",
                (component, metric_name, level, cutoff),
            )

            if c.fetchone()[0] == 0:
                # Issue warning
                message = f"{component}.{metric_name} at {percent:.1f}% of threshold ({current_value}/{threshold})"
                c.execute(
                    """INSERT INTO early_warnings 
                            (component, warning_type, message, threshold_percent, created_at)
                            VALUES (?, ?, ?, ?, ?)""",
                    (
                        component,
                        metric_name,
                        message,
                        level,
                        datetime.now().isoformat(),
                    ),
                )
                conn.commit()

                conn.close()
                return {"level": level, "message": message, "percent": percent}

    conn.close()
    return None


def get_warnings(acknowledged=False):
    """Get early warnings"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "SELECT * FROM early_warnings WHERE acknowledged=? ORDER BY created_at DESC LIMIT 20",
        (1 if acknowledged else 0,),
    )
    results = c.fetchall()
    conn.close()
    return results


def acknowledge_warning(warning_id):
    """Acknowledge warning"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE early_warnings SET acknowledged=1 WHERE id=?", (warning_id,))
    conn.commit()
    conn.close()


# === PROACTIVE CHECKS ===
def proactive_check():
    """Run lightweight proactive checks"""
    issues = []

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Check 1: Unresolved alerts (quick)
    c.execute("SELECT COUNT(*) FROM degradation_alerts WHERE resolved=0")
    unresolved = c.fetchone()[0]
    if unresolved > 5:
        issues.append(
            {
                "type": "alerts",
                "severity": "warning",
                "message": f"{unresolved} unresolved alerts",
                "action": "Review and resolve alerts",
            }
        )

    # Check 2: Pending proposals (quick)
    c.execute('SELECT COUNT(*) FROM proposals WHERE status="submitted"')
    pending = c.fetchone()[0]
    if pending > 20:
        issues.append(
            {
                "type": "proposals",
                "severity": "info",
                "message": f"{pending} pending proposals",
                "action": "Review proposals",
            }
        )

    # Check 3: Failed tools (quick)
    c.execute(
        """SELECT name, failure_count, usage_count FROM tools 
                 WHERE usage_count > 0 AND (failure_count * 1.0 / usage_count) > 0.2"""
    )
    failing_tools = c.fetchall()
    if failing_tools:
        issues.append(
            {
                "type": "tools",
                "severity": "warning",
                "message": f"{len(failing_tools)} tools with >20% failure rate",
                "action": "Fix or disable failing tools",
                "details": [t[0] for t in failing_tools],
            }
        )

    # Check 4: Old sessions (quick)
    cutoff = (datetime.now() - timedelta(days=7)).isoformat()
    c.execute(
        'SELECT COUNT(*) FROM sessions WHERE status="active" AND started_at < ?',
        (cutoff,),
    )
    old_sessions = c.fetchone()[0]
    if old_sessions > 10:
        issues.append(
            {
                "type": "sessions",
                "severity": "info",
                "message": f"{old_sessions} sessions active >7 days",
                "action": "Clean up old sessions",
            }
        )

    conn.close()
    return issues


# === PREVENTION STATS ===
def get_prevention_stats():
    """Get prevention statistics"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Count preventions
    c.execute("SELECT COUNT(*) FROM prevention_events")
    total_prevented = c.fetchone()[0]

    # Recent preventions
    cutoff = (datetime.now() - timedelta(days=7)).isoformat()
    c.execute("SELECT COUNT(*) FROM prevention_events WHERE created_at > ?", (cutoff,))
    recent_prevented = c.fetchone()[0]

    # Active rules
    c.execute("SELECT COUNT(*) FROM prevention_rules WHERE enabled=1")
    active_rules = c.fetchone()[0]

    # Active guardrails
    c.execute("SELECT COUNT(*) FROM guardrails WHERE enabled=1")
    active_guardrails = c.fetchone()[0]

    # Unacknowledged warnings
    c.execute("SELECT COUNT(*) FROM early_warnings WHERE acknowledged=0")
    pending_warnings = c.fetchone()[0]

    conn.close()

    return {
        "total_prevented": total_prevented,
        "recent_prevented": recent_prevented,
        "active_rules": active_rules,
        "active_guardrails": active_guardrails,
        "pending_warnings": pending_warnings,
    }


if __name__ == "__main__":
    import sys

    init_db()

    if len(sys.argv) < 2:
        print("Usage:")
        print("  Rule:      python prevention_system.py rule <add|check> ...")
        print("  Guardrail: python prevention_system.py guardrail <add|check> ...")
        print("  Warning:   python prevention_system.py warning <check|list> ...")
        print("  Proactive: python prevention_system.py proactive")
        print("  Stats:     python prevention_system.py stats")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "rule":
        subcmd = sys.argv[2] if len(sys.argv) > 2 else None

        if subcmd == "add" and len(sys.argv) >= 6:
            rule_id = add_prevention_rule(sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
            print(f"Added prevention rule #{rule_id}")

        elif subcmd == "check":
            context = json.loads(sys.argv[3]) if len(sys.argv) > 3 else {}
            prevented = check_prevention_rules(context)
            if prevented:
                print(f"\n⚠️  Prevented {len(prevented)} actions:")
                for p in prevented:
                    print(f"  • {p['rule']}: {p['action']}")
            else:
                print("✓ All checks passed")

    elif cmd == "guardrail":
        subcmd = sys.argv[2] if len(sys.argv) > 2 else None

        if subcmd == "add" and len(sys.argv) >= 5:
            guardrail_id = add_guardrail(sys.argv[3], sys.argv[4], sys.argv[5])
            print(f"Added guardrail #{guardrail_id}")

        elif subcmd == "check" and len(sys.argv) >= 5:
            violations = check_guardrails(sys.argv[3], float(sys.argv[4]))
            if violations:
                print(f"\n🚫 {len(violations)} guardrail violations:")
                for v in violations:
                    print(f"  • {v['guardrail']}: {v['type']} ({v['value']} vs {v['limit']})")
            else:
                print("✓ Within guardrails")

    elif cmd == "warning":
        subcmd = sys.argv[2] if len(sys.argv) > 2 else None

        if subcmd == "check" and len(sys.argv) >= 6:
            warning = check_early_warning(
                sys.argv[3], sys.argv[4], float(sys.argv[5]), float(sys.argv[6])
            )
            if warning:
                print(f"⚠️  Warning at {warning['level']}%: {warning['message']}")
            else:
                print("✓ No warnings")

        elif subcmd == "list":
            warnings = get_warnings()
            print(f"\nEarly Warnings ({len(warnings)}):")
            for w in warnings:
                print(f"  [{w[4]}%] {w[1]}.{w[2]}: {w[3]}")

    elif cmd == "proactive":
        issues = proactive_check()
        if issues:
            print(f"\n🔍 Proactive Check: {len(issues)} issues found\n")
            for issue in issues:
                severity_icon = "🔴" if issue["severity"] == "warning" else "ℹ️"
                print(f"{severity_icon} [{issue['type']}] {issue['message']}")
                print(f"   → {issue['action']}\n")
        else:
            print("✓ Proactive check: All clear")

    elif cmd == "stats":
        stats = get_prevention_stats()
        print("\nPrevention Statistics:")
        print(f"  Total prevented: {stats['total_prevented']}")
        print(f"  Recent (7d): {stats['recent_prevented']}")
        print(f"  Active rules: {stats['active_rules']}")
        print(f"  Active guardrails: {stats['active_guardrails']}")
        print(f"  Pending warnings: {stats['pending_warnings']}")
