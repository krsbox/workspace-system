# Copilot Instructions for Workspace Intelligence System

## 🎯 System Overview

This is a **prevention-first workspace intelligence system** with 11 integrated subsystems unified under a single CLI interface (`./ws`). The architecture emphasizes:

- **Lightweight prevention** (< 5ms overhead) over expensive recovery
- **Priority-based workflows** (🔴 Urgent → 🟡 Medium → 🟢 Low)
- **Single SQLite database** as source of truth across all systems
- **Context preservation** through persistent sessions and knowledge base

**Total codebase**: 36 Python modules (327 KB) + 1 SQLite database (14.8 MB)

---

## 🏗️ Architecture Layers

### Data Layer
- **`schema.py`** - Database schema definitions (14+ tables, single source of truth)
- **`db_utils.py`** - Context manager for safe DB connections with auto-rollback
- **Path**: `/media/sunil-kr/workspace/workspace-system/workspace_knowledge.db`

### System Layer (11 subsystems)
Each has a dedicated module and can be invoked standalone or through CLI:

1. **Knowledge Base** (`kb_manager.py`) - Searchable entries with tags
2. **Wiki & Todos** (`workspace_manager.py`) - Documents + task management
3. **Proposals** (`proposal_system.py`) - Feature proposals with auto-validation
4. **Collaboration** (`collab_system.py`) - Users, discussions, assignments
5. **Sessions** (`session_manager.py`) - Persistent memory + context restoration
6. **Tools** (`tools_manager.py`) - Auto-discovery + execution tracking
7. **Reviews** (`review_tools.py`) - Code & proposal quality assessment
8. **Quality Gates** (`quality_gate.py`) - Metrics + degradation alerts
9. **Prevention** (`prevention_system.py`) - Lightweight proactive rules (<5ms)
10. **Maintenance** (`maintenance_system.py`) - Scheduled tasks + health monitoring
11. **Analysis** (`improvement_analyzer.py`, `optimization_analyzer.py`) - Self-improvement

### Orchestration Layer
- **`workspace_cli.py`** (19.2 KB) - Main unified CLI router
- **`automation_manager.py`** - Orchestrates complex workflows
- **`smart_workflow.py`** - Workflow engine for multi-step processes

---

## 💻 Developer Workflows

### Running Tests
```bash
# Standalone (no dependencies)
python3 run_tests.py

# With pytest (if installed)
pytest tests/ -v

# Specific test file
python3 tests/test_schema.py
```

All tests use Python stdlib (unittest). Database tests use temporary databases to avoid conflicts.

### Code Verification
```bash
# Syntax check
python3 -m py_compile src/*.py

# Linting (if ruff installed)
ruff check src/

# Formatting (if black installed)
black src/
```

### Adding New Features
1. Create new module in `src/` with docstring
2. Add database tables to `schema.py` if needed
3. Use `db_utils.get_db()` context manager for all DB access
4. Add integration to `workspace_cli.py` (import + add command)
5. Write tests in `tests/test_*.py`
6. Run full test suite: `python3 run_tests.py`

---

## 🔑 Critical Patterns & Conventions

### Database Access (ALWAYS Use Context Manager)
```python
from db_utils import get_db

with get_db() as conn:
    c = conn.cursor()
    c.execute("SELECT * FROM knowledge WHERE id = ?", (1,))
    results = c.fetchall()
    # Auto-commits on success, auto-rollbacks on error
```

### Module Structure (Per Subsystem)
```python
#!/usr/bin/env python3
"""Brief description"""
import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path("workspace_knowledge.db")

def init_db():
    """Create tables if needed - called on module import"""
    # Create tables using schema.py definitions
    pass

def public_function(param):
    """Main API - directly invoked from CLI or other modules"""
    with get_db() as conn:
        # Database operations
        pass
```

### CLI Command Pattern (in workspace_cli.py)
```python
# 1. Import system function
from proposal_system import submit_proposal, list_proposals

# 2. Add to show_help()
print("  ws propose <title>     - Submit feature proposal")

# 3. Add to main() command router
elif cmd == "propose" and len(args) > 1:
    result = submit_proposal(args[1])
    print(f"✓ Proposal #{result} submitted")
```

### Prevention Rules (<5ms Overhead)
Prevention is **lightweight** - stateless checks that run instantly:
```python
def check_prevention_rules():
    """Fast validation without database overhead"""
    # Examples:
    # - Size limits (< 100KB)
    # - Rate limits (< 100 ops/min)
    # - Input validation (regex only)
    # - Guardrails (hardcoded limits)
    # DO NOT: Run expensive queries, file I/O, or network calls
```

### Priority System (Auto-Applied)
Todos/proposals automatically prioritized by impact score:
- **🔴 Urgent**: Critical impact (>80) OR explicitly marked urgent
- **🟠 High**: High impact (60-80)
- **🟡 Medium**: Medium impact (40-60)  
- **🟢 Low**: Low impact (<40)

Search for `priority` in `proposal_system.py` to see auto-prioritization logic.

---

## 📚 Key Files to Know

| File | Purpose | Size |
|------|---------|------|
| `workspace_cli.py` | Main CLI router, entry point | 19.2 KB |
| `schema.py` | Database schema definitions | 4.2 KB |
| `db_utils.py` | Safe DB connection context manager | 1.1 KB |
| `workspace_manager.py` | Core workspace operations | 10.4 KB |
| `proposal_system.py` | Proposal submission + validation | 10.9 KB |
| `prevention_system.py` | Lightweight prevention rules | 15.7 KB |
| `quality_gate.py` | Quality metrics + assessments | 15.9 KB |
| `automation_manager.py` | Workflow orchestration | 16.7 KB |
| `improvement_analyzer.py` | Self-improvement suggestions | 14.1 KB |

---

## 🚀 Common Tasks

### Add a New Database Table
1. Define in `schema.py` TABLES dictionary
2. Add to `init_all()` function
3. Run `python3 -c "from schema import init_all; init_all()"` to create

### Add a New CLI Command
1. Create function in appropriate module (e.g., `proposal_system.py`)
2. Import in `workspace_cli.py`
3. Add help text to `show_help()`
4. Add router logic in `main()` function
5. Test with `python3 workspace_cli.py <command>`

### Query Data Across Systems
Use `kb_manager.search()` for unified search across knowledge base, wiki, todos, proposals. It returns ranked results by relevance.

### Handle Errors in Async Operations
Check `automation_manager.py` for error handling patterns - it includes retry logic with exponential backoff for failed tasks.

---

## ⚡ Performance Considerations

- **Prevention overhead**: Must stay < 5ms (profile with `timeit` module)
- **Database queries**: Avoid N+1 patterns - use bulk queries when possible
- **Session persistence**: Store in database, not memory (survives restarts)
- **Large operations**: Use pagination for results > 100 items

---

## 🔍 Debugging Tips

1. **Check database state**: `sqlite3 workspace_knowledge.db ".schema"`
2. **See last operations**: Query `tool_executions` table for runtime data
3. **Trace CLI execution**: Add `print()` statements (stderr not captured by tests)
4. **Verify imports**: `python3 -c "import workspace_cli; print('✓ CLI loads')"` 
5. **Check prevention overhead**: `python3 -c "import timeit; print(timeit.timeit('prevention_system.check_prevention_rules()', number=100))"`

---

## 📋 Testing Standards

- All new modules must be importable: `python3 -c "from src.module_name import *"`
- Database operations must use context manager (auto-tested in `test_schema.py`)
- Write unit tests for new functions in `tests/test_*.py`
- Run full suite before commits: `python3 run_tests.py`

---

## 🔗 Integration Points

- **External tools**: Discovered automatically and tracked in `tools` table
- **Git integration**: `git_backup.py` handles versioning + recovery
- **Collaboration**: `collab_system.py` bridges human-AI via discussions
- **Self-improvement**: Feedback loop from `quality_gate.py` → `improvement_analyzer.py`

---

## 📖 Essential Reading

- `README.md` - Feature overview + quick start
- `STRUCTURE.md` - Complete file layout + navigation guide
- `UNIFIED_SYSTEM.md` - System design decisions
- `ARCHITECTURE_OVERVIEW.txt` - Data flow diagrams
- `TESTING.md` - Testing infrastructure

---

## 🎓 When Implementing Changes

✅ **DO**:
- Preserve database transactions (use context manager)
- Add help text to CLI when adding commands
- Write tests for new database operations
- Keep prevention rules stateless and fast
- Document assumptions in module docstring

❌ **DON'T**:
- Import modules directly from other subsystems (use CLI or shared API)
- Add database operations outside `schema.py` table definitions
- Store context in module-level variables (use sessions table)
- Add expensive operations to prevention layer
- Skip error handling in automation workflows

---

Last Updated: December 2, 2025  
Python: 3.6+  
Dependencies: Python stdlib only (core system)
