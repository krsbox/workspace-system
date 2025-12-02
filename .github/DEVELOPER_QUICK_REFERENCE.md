# Developer Quick Reference

Essential commands and patterns for the Workspace Intelligence System.

## 🚀 Quick Start

```bash
# Navigate to project
cd /media/sunil-kr/workspace/workspace-system

# Run tests (no dependencies required)
python3 run_tests.py

# Start using the CLI
./ws init your-name
./ws status
```

## 📋 Essential Commands

### Daily Development
```bash
# Check system status
./ws status

# View todos by priority
./ws todo

# Run all checks (quality, prevention, health)
./ws check

# Run maintenance
./ws maintain

# Search across all systems
./ws search "keyword"
```

### Code Quality
```bash
# Syntax check
python3 -m py_compile src/*.py

# Lint (if installed)
ruff check src/

# Format code (if installed)
black src/

# Run tests with coverage (if pytest installed)
pytest tests/ --cov=src
```

### Database Management
```bash
# View database schema
sqlite3 workspace_knowledge.db ".schema"

# Query specific table
sqlite3 workspace_knowledge.db "SELECT * FROM todos ORDER BY priority DESC;"

# Backup database
cp workspace_knowledge.db workspace_knowledge.db.backup
```

### Collaboration
```bash
# List all discussions
./ws collab list-discussions

# Add comment to discussion
./ws collab comment 1 "Your response here"

# Create new discussion
./ws collab create-discussion "Title" "Description"
```

## 🔑 Core Patterns

### Database Access
```python
from db_utils import get_db

# ALWAYS use context manager
with get_db() as conn:
    c = conn.cursor()
    c.execute("SELECT * FROM todos WHERE id = ?", (1,))
    return c.fetchone()
```

### Adding a CLI Command
```python
# 1. src/my_system.py
def my_function(param):
    with get_db() as conn:
        # implementation
        pass

# 2. src/workspace_cli.py - Add import
from my_system import my_function

# 3. Add to show_help()
print("  ws mycommand <param>  - Description")

# 4. Add to main() router
elif cmd == "mycommand" and len(args) > 1:
    result = my_function(args[1])
    print(f"✓ Result: {result}")
```

### Prevention Rules (< 5ms)
```python
def check_prevention_rules():
    """Must be stateless and lightweight"""
    # ✅ DO: Simple regex validation
    if not re.match(r'^[a-z0-9_]+$', input_str):
        return False
    
    # ❌ DON'T: Database queries
    # ❌ DON'T: File I/O
    # ❌ DON'T: Network calls
```

## 📁 File Structure Quick Lookup

| Path | Purpose |
|------|---------|
| `src/workspace_cli.py` | CLI entry point |
| `src/schema.py` | Database schema definitions |
| `src/db_utils.py` | Database connection utilities |
| `src/prevention_system.py` | Prevention rules & guards |
| `src/quality_gate.py` | Quality metrics & assessments |
| `.github/copilot-instructions.md` | AI agent guidelines |
| `.github/DISCUSSION_GUIDE.md` | Discussion channel guide |
| `tests/` | Test suite |
| `docs/` | Documentation |

## 🧪 Testing Checklist

Before committing:
```bash
# 1. Run tests
python3 run_tests.py

# 2. Check syntax
python3 -m py_compile src/*.py

# 3. Verify new module imports
python3 -c "from src.my_module import *"

# 4. If adding database operations, verify context manager usage
grep -n "get_db()" src/my_module.py

# 5. Run linter (optional)
ruff check src/
```

## 🐛 Debugging

### Database Issues
```bash
# Check table structure
sqlite3 workspace_knowledge.db ".schema <table_name>"

# Inspect data
sqlite3 workspace_knowledge.db ".mode column" ".headers on"
sqlite3 workspace_knowledge.db "SELECT * FROM <table_name> LIMIT 10;"
```

### Import Errors
```bash
# Verify module imports
python3 -c "from src.module_name import function_name; print('OK')"

# Check all modules load
python3 -c "import sys; sys.path.insert(0, 'src'); import workspace_cli; print('✓ CLI loads')"
```

### Performance Issues
```bash
# Profile prevention overhead
python3 -c "
import timeit
t = timeit.timeit('from src.prevention_system import check_prevention_rules; check_prevention_rules()', number=1000)
print(f'Prevention avg: {t/1000*1000:.2f}ms')
"
```

## 📊 Common Tasks

### Add New Subsystem
1. Create `src/my_system.py` with `init_db()` function
2. Define tables in `schema.py`
3. Use `db_utils.get_db()` for all DB operations
4. Import in `workspace_cli.py`
5. Add command to `show_help()` and `main()`
6. Write tests in `tests/test_my_system.py`
7. Run `python3 run_tests.py`

### Query Across Systems
```python
# Use unified search
from kb_manager import search

results = search("query_text", max_results=10)
# Returns ranked results from knowledge base, wiki, todos, proposals
```

### Handle Errors
```python
# Pattern from automation_manager.py
def with_retry(func, max_retries=3, backoff=2):
    """Retry with exponential backoff"""
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(backoff ** attempt)
            else:
                raise
```

## 🎯 Before Making Changes

✅ **DO**:
- Update tests when changing existing functions
- Use context manager for DB access
- Profile prevention rules (must stay < 5ms)
- Document new patterns in docstrings
- Add help text for CLI commands

❌ **DON'T**:
- Mix database operations with business logic
- Store state in module-level variables
- Add expensive operations to prevention layer
- Import between subsystems directly
- Skip error handling in automation workflows

## 📚 Documentation References

- **Getting Started**: See `README.md`
- **Architecture**: See `UNIFIED_SYSTEM.md` and `ARCHITECTURE_OVERVIEW.txt`
- **Testing Guide**: See `TESTING.md`
- **AI Instructions**: See `.github/copilot-instructions.md`
- **Discussions**: See `.github/DISCUSSION_GUIDE.md`

## 🔗 Repository Links

- **GitHub**: https://github.com/krsbox/workspace-system
- **Issues**: https://github.com/krsbox/workspace-system/issues
- **Discussions**: https://github.com/krsbox/workspace-system/discussions

---

**Last Updated**: December 2, 2025  
**Current Branch**: copilot  
**Python**: 3.6+  
**Dependencies**: Python stdlib only (core)
