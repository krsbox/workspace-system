#!/usr/bin/env python3
"""Quality Gate: Assessments and gates to prevent system degradation"""
import sqlite3
import json
from datetime import datetime, timedelta
from pathlib import Path

DB_PATH = Path("/media/sunil-kr/workspace/workspace-system/workspace_knowledge.db")


def init_db():
    """Initialize quality gate tables"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Quality metrics
    c.execute(
        """CREATE TABLE IF NOT EXISTS quality_metrics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        component TEXT NOT NULL,
        metric_name TEXT NOT NULL,
        value REAL NOT NULL,
        threshold REAL NOT NULL,
        status TEXT NOT NULL,
        created_at TEXT NOT NULL
    )"""
    )

    # Quality gates
    c.execute(
        """CREATE TABLE IF NOT EXISTS quality_gates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        type TEXT NOT NULL,
        rules TEXT NOT NULL,
        enabled INTEGER DEFAULT 1,
        created_at TEXT NOT NULL
    )"""
    )

    # Gate executions
    c.execute(
        """CREATE TABLE IF NOT EXISTS gate_executions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        gate_id INTEGER NOT NULL,
        context TEXT,
        status TEXT NOT NULL,
        passed INTEGER NOT NULL,
        failed INTEGER NOT NULL,
        details TEXT,
        created_at TEXT NOT NULL,
        FOREIGN KEY (gate_id) REFERENCES quality_gates(id)
    )"""
    )

    # Assessments
    c.execute(
        """CREATE TABLE IF NOT EXISTS assessments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT NOT NULL,
        target TEXT NOT NULL,
        score REAL NOT NULL,
        grade TEXT NOT NULL,
        findings TEXT,
        recommendations TEXT,
        created_at TEXT NOT NULL
    )"""
    )

    # Degradation alerts
    c.execute(
        """CREATE TABLE IF NOT EXISTS degradation_alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        component TEXT NOT NULL,
        severity TEXT NOT NULL,
        message TEXT NOT NULL,
        metric_data TEXT,
        resolved INTEGER DEFAULT 0,
        created_at TEXT NOT NULL,
        resolved_at TEXT
    )"""
    )

    conn.commit()
    conn.close()


# === QUALITY METRICS ===
def record_metric(component, metric_name, value, threshold):
    """Record quality metric"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    now = datetime.now().isoformat()

    status = "pass" if value >= threshold else "fail"

    c.execute(
        """INSERT INTO quality_metrics (component, metric_name, value, threshold, status, created_at)
                 VALUES (?, ?, ?, ?, ?, ?)""",
        (component, metric_name, value, threshold, status, now),
    )

    conn.commit()
    metric_id = c.lastrowid
    conn.close()

    # Check for degradation
    if status == "fail":
        check_degradation(component, metric_name, value, threshold)

    return metric_id


def get_metrics(component, hours=24):
    """Get recent metrics for component"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    cutoff = (datetime.now() - timedelta(hours=hours)).isoformat()
    c.execute(
        """SELECT * FROM quality_metrics 
                 WHERE component=? AND created_at > ?
                 ORDER BY created_at DESC""",
        (component, cutoff),
    )

    results = c.fetchall()
    conn.close()
    return results


def get_metric_trend(component, metric_name, hours=24):
    """Get metric trend"""
    metrics = get_metrics(component, hours)
    relevant = [m for m in metrics if m[2] == metric_name]

    if len(relevant) < 2:
        return "stable"

    recent_avg = sum(m[3] for m in relevant[:5]) / min(5, len(relevant))
    older_avg = sum(m[3] for m in relevant[-5:]) / min(5, len(relevant))

    if recent_avg > older_avg * 1.1:
        return "improving"
    elif recent_avg < older_avg * 0.9:
        return "degrading"
    else:
        return "stable"


# === QUALITY GATES ===
def create_gate(name, type, rules):
    """Create quality gate"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    now = datetime.now().isoformat()

    try:
        c.execute(
            "INSERT INTO quality_gates (name, type, rules, created_at) VALUES (?, ?, ?, ?)",
            (name, type, json.dumps(rules), now),
        )
        conn.commit()
        gate_id = c.lastrowid
    except sqlite3.IntegrityError:
        gate_id = None
    finally:
        conn.close()
    return gate_id


def execute_gate(gate_name, context=None):
    """Execute quality gate"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("SELECT * FROM quality_gates WHERE name=? AND enabled=1", (gate_name,))
    gate = c.fetchone()

    if not gate:
        conn.close()
        return None

    gate_id = gate[0]
    rules = json.loads(gate[3])

    passed = 0
    failed = 0
    details = []

    # Execute each rule
    for rule in rules:
        rule_type = rule.get("type")

        if rule_type == "metric":
            component = rule["component"]
            metric = rule["metric"]
            threshold = rule["threshold"]

            # Get latest metric
            c.execute(
                """SELECT value FROM quality_metrics 
                        WHERE component=? AND metric_name=?
                        ORDER BY created_at DESC LIMIT 1""",
                (component, metric),
            )
            result = c.fetchone()

            if result:
                value = result[0]
                if value >= threshold:
                    passed += 1
                    details.append({"rule": rule, "status": "pass", "value": value})
                else:
                    failed += 1
                    details.append({"rule": rule, "status": "fail", "value": value})
            else:
                failed += 1
                details.append({"rule": rule, "status": "no_data"})

        elif rule_type == "tool_success_rate":
            tool_name = rule["tool"]
            min_rate = rule["min_rate"]

            c.execute(
                "SELECT success_count, failure_count FROM tools WHERE name=?",
                (tool_name,),
            )
            result = c.fetchone()

            if result and (result[0] + result[1]) > 0:
                rate = result[0] / (result[0] + result[1]) * 100
                if rate >= min_rate:
                    passed += 1
                    details.append({"rule": rule, "status": "pass", "rate": rate})
                else:
                    failed += 1
                    details.append({"rule": rule, "status": "fail", "rate": rate})
            else:
                failed += 1
                details.append({"rule": rule, "status": "no_data"})

        elif rule_type == "review_score":
            min_score = rule["min_score"]

            c.execute(
                'SELECT AVG(score) FROM code_reviews WHERE created_at > datetime("now", "-7 days")'
            )
            result = c.fetchone()

            if result and result[0]:
                avg_score = result[0]
                if avg_score >= min_score:
                    passed += 1
                    details.append({"rule": rule, "status": "pass", "score": avg_score})
                else:
                    failed += 1
                    details.append({"rule": rule, "status": "fail", "score": avg_score})

    # Record execution
    status = "pass" if failed == 0 else "fail"
    c.execute(
        """INSERT INTO gate_executions (gate_id, context, status, passed, failed, details, created_at)
                 VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (
            gate_id,
            context,
            status,
            passed,
            failed,
            json.dumps(details),
            datetime.now().isoformat(),
        ),
    )

    conn.commit()
    exec_id = c.lastrowid
    conn.close()

    return {
        "gate": gate_name,
        "status": status,
        "passed": passed,
        "failed": failed,
        "details": details,
    }


def list_gates():
    """List quality gates"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM quality_gates ORDER BY name")
    results = c.fetchall()
    conn.close()
    return results


# === ASSESSMENTS ===
def run_assessment(type, target):
    """Run comprehensive assessment"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    findings = []
    recommendations = []
    score = 100

    if type == "system":
        # Check tool health
        c.execute(
            'SELECT COUNT(*), AVG(success_count * 1.0 / NULLIF(usage_count, 0)) FROM tools WHERE status="active"'
        )
        tool_stats = c.fetchone()
        if tool_stats[0] > 0:
            avg_success = (tool_stats[1] or 0) * 100
            if avg_success < 80:
                score -= 15
                findings.append(f"Tool success rate low: {avg_success:.1f}%")
                recommendations.append("Review and fix failing tools")

        # Check recent reviews
        c.execute(
            'SELECT COUNT(*) FROM code_reviews WHERE created_at > datetime("now", "-7 days")'
        )
        review_count = c.fetchone()[0]
        if review_count == 0:
            score -= 10
            findings.append("No code reviews in last 7 days")
            recommendations.append("Implement regular code reviews")

        # Check proposals
        c.execute('SELECT COUNT(*) FROM proposals WHERE status="submitted"')
        pending_proposals = c.fetchone()[0]
        if pending_proposals > 10:
            score -= 5
            findings.append(f"{pending_proposals} pending proposals")
            recommendations.append("Review and process proposals")

        # Check degradation alerts
        c.execute("SELECT COUNT(*) FROM degradation_alerts WHERE resolved=0")
        unresolved = c.fetchone()[0]
        if unresolved > 0:
            score -= unresolved * 5
            findings.append(f"{unresolved} unresolved degradation alerts")
            recommendations.append("Address degradation alerts")

    elif type == "tool":
        # Assess specific tool
        c.execute("SELECT * FROM tools WHERE name=?", (target,))
        tool = c.fetchone()

        if tool:
            usage = tool[8]
            success_rate = (tool[9] / usage * 100) if usage > 0 else 0

            if success_rate < 90:
                score -= 20
                findings.append(f"Success rate: {success_rate:.1f}%")
                recommendations.append("Investigate and fix failures")

            if tool[11] > 5:  # avg_runtime
                score -= 10
                findings.append(f"Slow execution: {tool[11]:.2f}s")
                recommendations.append("Optimize performance")

    # Determine grade
    if score >= 90:
        grade = "A"
    elif score >= 80:
        grade = "B"
    elif score >= 70:
        grade = "C"
    elif score >= 60:
        grade = "D"
    else:
        grade = "F"

    # Save assessment
    c.execute(
        """INSERT INTO assessments (type, target, score, grade, findings, recommendations, created_at)
                 VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (
            type,
            target,
            score,
            grade,
            json.dumps(findings),
            json.dumps(recommendations),
            datetime.now().isoformat(),
        ),
    )

    conn.commit()
    assessment_id = c.lastrowid
    conn.close()

    return {
        "id": assessment_id,
        "type": type,
        "target": target,
        "score": score,
        "grade": grade,
        "findings": findings,
        "recommendations": recommendations,
    }


# === DEGRADATION DETECTION ===
def check_degradation(component, metric_name, value, threshold):
    """Check for degradation and alert"""
    trend = get_metric_trend(component, metric_name)

    if trend == "degrading":
        severity = "critical" if value < threshold * 0.5 else "warning"

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        message = (
            f"{component}.{metric_name} degrading: {value} (threshold: {threshold})"
        )
        metric_data = json.dumps(
            {"value": value, "threshold": threshold, "trend": trend}
        )

        c.execute(
            """INSERT INTO degradation_alerts (component, severity, message, metric_data, created_at)
                     VALUES (?, ?, ?, ?, ?)""",
            (component, severity, message, metric_data, datetime.now().isoformat()),
        )

        conn.commit()
        conn.close()


def get_alerts(resolved=False):
    """Get degradation alerts"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "SELECT * FROM degradation_alerts WHERE resolved=? ORDER BY created_at DESC",
        (1 if resolved else 0,),
    )
    results = c.fetchall()
    conn.close()
    return results


def resolve_alert(alert_id):
    """Resolve degradation alert"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "UPDATE degradation_alerts SET resolved=1, resolved_at=? WHERE id=?",
        (datetime.now().isoformat(), alert_id),
    )
    conn.commit()
    conn.close()


if __name__ == "__main__":
    import sys

    init_db()

    if len(sys.argv) < 2:
        print("Usage:")
        print(
            "  Metric:  python quality_gate.py metric <component> <name> <value> <threshold>"
        )
        print("  Gate:    python quality_gate.py gate <create|execute|list> ...")
        print("  Assess:  python quality_gate.py assess <type> <target>")
        print("  Alerts:  python quality_gate.py alerts [resolved]")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "metric" and len(sys.argv) >= 6:
        metric_id = record_metric(
            sys.argv[2], sys.argv[3], float(sys.argv[4]), float(sys.argv[5])
        )
        print(f"Recorded metric #{metric_id}")

        trend = get_metric_trend(sys.argv[2], sys.argv[3])
        print(f"Trend: {trend}")

    elif cmd == "gate":
        subcmd = sys.argv[2] if len(sys.argv) > 2 else None

        if subcmd == "create" and len(sys.argv) >= 5:
            rules = json.loads(sys.argv[4])
            gate_id = create_gate(sys.argv[3], "standard", rules)
            print(f"Created gate #{gate_id}")

        elif subcmd == "execute" and len(sys.argv) >= 4:
            result = execute_gate(sys.argv[3])
            if result:
                status_icon = "✓" if result["status"] == "pass" else "✗"
                print(f"\n{status_icon} Gate: {result['gate']}")
                print(f"Status: {result['status'].upper()}")
                print(f"Passed: {result['passed']}, Failed: {result['failed']}\n")
                for detail in result["details"]:
                    status = "✓" if detail["status"] == "pass" else "✗"
                    print(
                        f"  {status} {detail['rule'].get('type')}: {detail.get('value', detail.get('rate', 'N/A'))}"
                    )

        elif subcmd == "list":
            gates = list_gates()
            print(f"\nQuality Gates ({len(gates)}):")
            for g in gates:
                status = "🟢" if g[4] else "⚫"
                print(f"  {status} {g[1]} ({g[2]})")

    elif cmd == "assess" and len(sys.argv) >= 4:
        result = run_assessment(sys.argv[2], sys.argv[3])
        print(f"\nAssessment: {result['type']} - {result['target']}")
        print(f"Score: {result['score']}/100 (Grade: {result['grade']})\n")

        if result["findings"]:
            print("Findings:")
            for f in result["findings"]:
                print(f"  • {f}")

        if result["recommendations"]:
            print("\nRecommendations:")
            for r in result["recommendations"]:
                print(f"  → {r}")

    elif cmd == "alerts":
        resolved = len(sys.argv) > 2 and sys.argv[2] == "resolved"
        alerts = get_alerts(resolved)

        status_text = "Resolved" if resolved else "Active"
        print(f"\n{status_text} Alerts ({len(alerts)}):")
        for a in alerts:
            severity_icon = "🔴" if a[2] == "critical" else "🟡"
            print(f"  {severity_icon} #{a[0]}: {a[3]}")
