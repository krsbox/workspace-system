#!/usr/bin/env python3
"""Workspace CLI: Unified interface for all systems"""
import sys

# Import all systems
try:
    from kb_manager import add_entry, search as kb_search
    from workspace_manager import (
        wiki_create,
        todo_add,
        todo_list,
        progress_add,
        progress_list,
    )
    from proposal_system import (
        submit_proposal,
        auto_validate,
        convert_to_todo,
        list_proposals,
    )
    from collab_system import (
        add_user,
        start_discussion,
        add_comment,
        assign_item,
        get_notifications,
    )
    from session_manager import (
        resume_session,
        add_message,
        set_state,
        get_all_state,
        add_bookmark,
    )
    from tools_manager import discover_tools, execute_tool, get_tool_stats, list_tools
    from review_tools import auto_review_code, review_proposal_quality
    from quality_gate import execute_gate, run_assessment, get_alerts
    from prevention_system import (
        check_prevention_rules,
        check_guardrails,
        proactive_check,
    )
    from maintenance_system import (
        run_due_tasks,
        get_complexity_score,
        get_utilization_summary,
    )
    from project_manager import (
        list_projects,
        get_project,
        analyze_project,
        project_summary,
    )
    from git_backup import (
        git_backup,
        git_recover,
        list_git_backups,
        cleanup_old_backups,
    )
    from smart_cleanup import (
        analyze_project as analyze_cleanup,
        auto_cleanup,
    )
    from tool_helpers import (
        add_discussion,
        get_discussions,
        resolve_discussion,
        admin_disable_tool,
        admin_enable_tool,
        admin_reset_tool_stats,
        get_admin_logs,
        get_tool_health_summary,
        get_review_summary,
    )
except ImportError as e:
    print(f"Warning: Some modules not available: {e}")


def show_help():
    """Show unified help"""
    print(
        """
Workspace CLI - Unified Interface

QUICK COMMANDS:
  ws status              - System status dashboard
  ws init <user>         - Initialize workspace for user
  ws propose <title>     - Quick proposal submission
  ws todo                - List todos by priority
  ws review <file>       - Review code file
  ws check               - Run all checks (quality, prevention, proactive)
  ws maintain            - Run maintenance tasks
  ws search <query>      - Search everything
  
NEW AUTOMATION:
  ws backup              - Create database backup
  ws health              - Check system health
  ws tasks               - List automated tasks
  ws improve             - Analyze what needs improvement
  ws optimize            - Find duplications & alternatives

PROJECT MANAGEMENT:
  ws projects            - List all projects
  ws project <name>      - Show project details
  ws project-analyze <name> - Analyze project stats

BACKUP & RECOVERY:
  ws backup <path> [reason] - Git backup (tag + stash)
  ws backups <path>      - List git backup tags
  ws recover <path> <tag> - Recover from git tag
  ws cleanup-backups <path> - Remove old backup tags

SMART CLEANUP:
  ws analyze-cleanup <path> - Find duplicates, dead code, etc.
  ws auto-cleanup <path> [--live] - Auto cleanup (safe operations)

DETAILED COMMANDS:
  Knowledge:    ws kb <add|search> ...
  Wiki:         ws wiki <create|get> ...
  Todos:        ws todo <add|list|update> ...
  Proposals:    ws proposal <submit|validate|convert> ...
  Discussions:  ws discuss <start|comment|resolve> ...
  Sessions:     ws session <start|resume> ...
  Tools:        ws tool <discover|execute|stats|health> ...
  Quality:      ws quality <gate|assess> ...
  Prevention:   ws prevent <check|proactive> ...
  Admin:        ws admin <disable|enable|reset|logs> ...

Run 'ws <command> help' for detailed usage.
"""
    )


def status_dashboard():
    """Show system status dashboard"""
    print("\n" + "=" * 60)
    print("WORKSPACE STATUS DASHBOARD")
    print("=" * 60)

    # Complexity
    try:
        complexity = get_complexity_score()
        print(f"\n📊 Complexity: {complexity['score']} ({complexity['level'].upper()})")
        print(
            f"   Capabilities: {complexity['capabilities']}, Tools: {complexity['tools']}"
        )
    except:
        print("\n📊 Complexity: N/A")

    # Todos by priority
    try:
        todos = todo_list()
        urgent = sum(1 for t in todos if t[4] == "urgent")
        high = sum(1 for t in todos if t[4] == "high")
        print(f"\n✓ Todos: {len(todos)} total ({urgent} urgent, {high} high)")
    except:
        print("\n✓ Todos: N/A")

    # Proposals
    try:
        proposals = list_proposals()
        submitted = sum(1 for p in proposals if p[7] == "submitted")
        print(f"\n📝 Proposals: {len(proposals)} total ({submitted} pending review)")
    except:
        print("\n📝 Proposals: N/A")

    # Alerts
    try:
        alerts = get_alerts()
        print(f"\n⚠️  Alerts: {len(alerts)} unresolved")
    except:
        print("\n⚠️  Alerts: N/A")

    # Tools
    try:
        tools = list_tools()
        active = sum(1 for t in tools if t[7] == "active")
        print(f"\n🔧 Tools: {active} active")
    except:
        print("\n🔧 Tools: N/A")

    # Utilization
    try:
        util = get_utilization_summary()
        if util:
            high_util = [u for u in util if u["percent"] > 80]
            if high_util:
                print(f"\n📈 High Utilization: {len(high_util)} resources > 80%")
    except:
        pass

    print("\n" + "=" * 60 + "\n")


def init_workspace(user):
    """Initialize workspace for user"""
    print(f"Initializing workspace for {user}...")

    # Add user
    try:
        add_user(user, "contributor")
        print(f"✓ User '{user}' created")
    except:
        print(f"✓ User '{user}' exists")

    # Start session
    try:
        session_id, is_new = resume_session(user)
        if is_new:
            print(f"✓ Session #{session_id} started")
        else:
            print(f"✓ Session #{session_id} resumed")
    except Exception as e:
        print(f"✗ Session error: {e}")

    # Discover tools
    try:
        discovered = discover_tools()
        print(f"✓ Discovered {len(discovered)} tools")
    except Exception as e:
        print(f"✗ Discovery error: {e}")

    print(f"\n✓ Workspace ready for {user}")


def quick_propose(title):
    """Quick proposal submission with auto-validation"""
    print(f"Submitting proposal: {title}")

    # Get description
    print("Description (press Enter twice to finish):")
    lines = []
    while True:
        line = input()
        if not line and lines:
            break
        lines.append(line)
    description = "\n".join(lines)

    # Submit
    try:
        prop_id = submit_proposal(title, description, "", "medium", "medium")
        print(f"✓ Proposal #{prop_id} submitted")

        # Auto-validate
        result = auto_validate(prop_id)
        print(f"✓ Validation: {result['decision'].upper()} (score: {result['score']}%)")

        if result["decision"] == "approved":
            # Convert to todo
            todo_id = convert_to_todo(prop_id)
            print(f"✓ Converted to todo #{todo_id}")
        else:
            print("→ Needs revision. Improve and resubmit.")

        return prop_id
    except Exception as e:
        print(f"✗ Error: {e}")
        return None


def list_todos_by_priority():
    """List todos organized by priority"""
    try:
        todos = todo_list()

        # Group by priority
        by_priority = {"urgent": [], "high": [], "medium": [], "low": []}

        for t in todos:
            priority = t[4]
            by_priority[priority].append(t)

        print("\n" + "=" * 60)
        print("TODOS BY PRIORITY")
        print("=" * 60)

        for priority in ["urgent", "high", "medium", "low"]:
            items = by_priority[priority]
            if items:
                icon = (
                    "🔴"
                    if priority == "urgent"
                    else (
                        "🟠"
                        if priority == "high"
                        else "🟡" if priority == "medium" else "🟢"
                    )
                )
                print(f"\n{icon} {priority.upper()} ({len(items)})")
                for t in items[:5]:  # Show top 5
                    status = t[3]
                    print(f"   [{status}] #{t[0]}: {t[1]}")

        print("\n" + "=" * 60 + "\n")
    except Exception as e:
        print(f"Error: {e}")


def run_all_checks():
    """Run all quality, prevention, and proactive checks"""
    print("\n" + "=" * 60)
    print("RUNNING ALL CHECKS")
    print("=" * 60)

    # Quality gate
    print("\n1. Quality Gate...")
    try:
        result = execute_gate("pre-commit")
        if result:
            status = "✓ PASS" if result["status"] == "pass" else "✗ FAIL"
            print(
                f"   {status} ({result['passed']}/{result['passed']+result['failed']})"
            )
    except:
        print("   ⊘ No gate configured")

    # Prevention check
    print("\n2. Prevention Rules...")
    try:
        prevented = check_prevention_rules({})
        if prevented:
            print(f"   ⚠️  {len(prevented)} actions prevented")
        else:
            print("   ✓ All clear")
    except:
        print("   ⊘ No rules configured")

    # Proactive check
    print("\n3. Proactive Check...")
    try:
        issues = proactive_check()
        if issues:
            print(f"   ⚠️  {len(issues)} issues found")
            for issue in issues[:3]:
                print(f"      - {issue['message']}")
        else:
            print("   ✓ All clear")
    except:
        print("   ⊘ Check failed")

    # Assessment
    print("\n4. System Assessment...")
    try:
        assessment = run_assessment("system", "workspace")
        print(f"   Score: {assessment['score']}/100 (Grade: {assessment['grade']})")
    except:
        print("   ⊘ Assessment failed")

    print("\n" + "=" * 60 + "\n")


def search_all(query):
    """Search across all systems"""
    print(f"\nSearching for: {query}\n")

    results_found = False

    # Knowledge base
    try:
        kb_results = kb_search(query)
        if kb_results:
            print(f"📚 Knowledge Base ({len(kb_results)}):")
            for r in kb_results[:3]:
                print(f"   [{r[1]}] {r[2]}")
            results_found = True
    except:
        pass

    # Proposals
    try:
        proposals = list_proposals()
        matching = [
            p
            for p in proposals
            if query.lower() in p[1].lower() or query.lower() in p[2].lower()
        ]
        if matching:
            print(f"\n📝 Proposals ({len(matching)}):")
            for p in matching[:3]:
                print(f"   [{p[7]}] #{p[0]}: {p[1]}")
            results_found = True
    except:
        pass

    # Todos
    try:
        todos = todo_list()
        matching = [t for t in todos if query.lower() in t[1].lower()]
        if matching:
            print(f"\n✓ Todos ({len(matching)}):")
            for t in matching[:3]:
                print(f"   [{t[3]}] #{t[0]}: {t[1]}")
            results_found = True
    except:
        pass

    if not results_found:
        print("No results found.")


def main():
    if len(sys.argv) < 2:
        show_help()
        sys.exit(0)

    cmd = sys.argv[1]

    # Quick commands
    if cmd == "status":
        status_dashboard()

    elif cmd == "init" and len(sys.argv) >= 3:
        init_workspace(sys.argv[2])

    elif cmd == "propose" and len(sys.argv) >= 3:
        title = " ".join(sys.argv[2:])
        quick_propose(title)

    elif cmd == "todo":
        if len(sys.argv) == 2:
            list_todos_by_priority()
        else:
            print("Use: ws todo (to list) or ws todo add <title> (to add)")

    elif cmd == "review" and len(sys.argv) >= 3:
        file_path = sys.argv[2]
        print(f"Reviewing {file_path}...")
        try:
            review_id = auto_review_code(file_path)
            print(f"✓ Review #{review_id} complete")
        except Exception as e:
            print(f"✗ Error: {e}")

    elif cmd == "check":
        run_all_checks()

    elif cmd == "maintain":
        print("Running maintenance tasks...")
        try:
            results = run_due_tasks()
            if results:
                print(f"✓ Ran {len(results)} tasks")
                for r in results:
                    status = "✓" if r["status"] == "success" else "✗"
                    print(f"   {status} {r['task']}")
            else:
                print("No tasks due")
        except Exception as e:
            print(f"✗ Error: {e}")

    elif cmd == "backup":
        import subprocess

        subprocess.run(["python3", "backup_manager.py", "backup"])

    elif cmd == "health":
        import subprocess

        subprocess.run(["python3", "health_monitor.py", "check"])

    elif cmd == "tasks":
        import subprocess

        subprocess.run(["python3", "task_automator.py", "list"])

    elif cmd == "improve":
        import subprocess

        subprocess.run(["python3", "improvement_analyzer.py", "analyze"])

    elif cmd == "optimize":
        import subprocess

        subprocess.run(["python3", "optimization_analyzer.py"])

    elif cmd == "discuss":
        if len(sys.argv) < 3:
            print("Usage: ws discuss <add|list|resolve> ...")
            return
        subcmd = sys.argv[2]
        if subcmd == "add" and len(sys.argv) >= 6:
            review_id, review_type, user, message = (
                sys.argv[3],
                sys.argv[4],
                sys.argv[5],
                " ".join(sys.argv[6:]),
            )
            disc_id = add_discussion(int(review_id), review_type, user, message)
            print(f"✓ Discussion #{disc_id} added")
        elif subcmd == "list" and len(sys.argv) >= 5:
            review_id, review_type = int(sys.argv[3]), sys.argv[4]
            discussions = get_discussions(review_id, review_type)
            for d in discussions:
                status = "✓" if d["resolved"] else "○"
                print(f"{status} [{d['user']}] {d['message']}")
        elif subcmd == "resolve" and len(sys.argv) >= 4:
            resolve_discussion(int(sys.argv[3]))
            print("✓ Discussion resolved")

    elif cmd == "admin":
        if len(sys.argv) < 3:
            print("Usage: ws admin <disable|enable|reset|logs> ...")
            return
        subcmd = sys.argv[2]
        if subcmd == "disable" and len(sys.argv) >= 5:
            admin_user, tool_id, reason = (
                sys.argv[3],
                int(sys.argv[4]),
                " ".join(sys.argv[5:]),
            )
            admin_disable_tool(admin_user, tool_id, reason)
            print(f"✓ Tool #{tool_id} disabled")
        elif subcmd == "enable" and len(sys.argv) >= 5:
            admin_user, tool_id = sys.argv[3], int(sys.argv[4])
            admin_enable_tool(admin_user, tool_id)
            print(f"✓ Tool #{tool_id} enabled")
        elif subcmd == "reset" and len(sys.argv) >= 5:
            admin_user, tool_id = sys.argv[3], int(sys.argv[4])
            admin_reset_tool_stats(admin_user, tool_id)
            print(f"✓ Tool #{tool_id} stats reset")
        elif subcmd == "logs":
            logs = get_admin_logs()
            for log in logs:
                print(
                    f"[{log['created_at']}] {log['admin']}: {log['action']} on {log['target_type']}#{log['target_id']}"
                )

    elif cmd == "summary":
        print("\n📊 System Summary\n")
        tool_health = get_tool_health_summary()
        print(f"Tools: {tool_health['status_counts']}")
        print(f"Avg Success Rate: {tool_health['avg_success_rate']}%")
        review_summary = get_review_summary()
        print(f"\nReviews: {review_summary['review_counts']}")
        print(f"Avg Score: {review_summary['avg_score']}")

    elif cmd == "search" and len(sys.argv) >= 3:
        query = " ".join(sys.argv[2:])
        search_all(query)

    elif cmd == "projects":
        projects = list_projects()
        if projects:
            print("\n📁 Projects:")
            for p in projects:
                status_icon = "✓" if p[3] == "active" else "📦"
                print(f"  {status_icon} [{p[3]}] {p[1]}")
                print(f"     {p[2]}")
        else:
            print("\n📁 No projects registered")
            print("   Run: python3 src/project_manager.py scan")

    elif cmd == "project" and len(sys.argv) >= 3:
        name = sys.argv[2]
        project = get_project(name)
        if project:
            print(f"\n📁 Project: {project[1]}")
            print(f"Status: {project[3]}")
            print(f"Path: {project[2]}")
            if project[4]:
                print(f"Description: {project[4]}")
            print(f"Created: {project[5]}")
            print(f"Updated: {project[6]}")
        else:
            print(f"✗ Project '{name}' not found")

    elif cmd == "project-analyze" and len(sys.argv) >= 3:
        name = sys.argv[2]
        project = get_project(name)
        if project:
            stats = analyze_project(project[2])
            if stats:
                print(f"\n📊 Project Analysis: {name}")
                print(f"Path: {stats['path']}")
                print(f"Files: {stats['files_count']:,}")
                print(f"Python files: {stats['py_files']:,}")
                print(f"Lines of code: {stats['lines_count']:,}")
                print(f"Git: {'✓' if stats['has_git'] else '✗'}")
                print(f"Tests: {'✓' if stats['has_tests'] else '✗'}")
                print(f"Venv: {'✓' if stats['has_venv'] else '✗'}")
                print(f"Requirements: {'✓' if stats['has_requirements'] else '✗'}")
                if stats["last_commit"]:
                    print(f"Last commit: {stats['last_commit']}")
        else:
            print(f"✗ Project '{name}' not found")

    elif cmd == "backup" and len(sys.argv) >= 3:
        path = sys.argv[2]
        reason = sys.argv[3] if len(sys.argv) > 3 else "manual"
        tag = git_backup(path, reason)
        if tag:
            print(f"\n✓ Git backup created: {tag}")

    elif cmd == "backups" and len(sys.argv) >= 3:
        path = sys.argv[2]
        backups = list_git_backups(path)
        if backups:
            print(f"\n📦 Git Backups ({len(backups)}):")
            for tag in backups:
                print(f"  {tag}")
        else:
            print("\n📦 No git backups found")

    elif cmd == "recover" and len(sys.argv) >= 4:
        path = sys.argv[2]
        tag = sys.argv[3]
        success = git_recover(tag, path)
        if success:
            print("\n✓ Recovery complete")

    elif cmd == "cleanup-backups" and len(sys.argv) >= 3:
        path = sys.argv[2]
        keep = int(sys.argv[3]) if len(sys.argv) > 3 else 5
        removed = cleanup_old_backups(path, keep)

    elif cmd == "analyze-cleanup" and len(sys.argv) >= 3:
        path = sys.argv[2]
        analyze_cleanup(path)

    elif cmd == "auto-cleanup" and len(sys.argv) >= 3:
        path = sys.argv[2]
        live = "--live" in sys.argv
        auto_cleanup(path, dry_run=not live)

    elif cmd == "help":
        show_help()

    else:
        print(f"Unknown command: {cmd}")
        print("Run 'ws help' for usage")


if __name__ == "__main__":
    main()
