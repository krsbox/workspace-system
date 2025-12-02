# Quick Setup & Getting Started

## Automated Setup

```bash
# Clone or navigate to repo
cd /media/sunil-kr/workspace/workspace-system

# Run core verification
python3 run_tests.py

# Expected output:
# Ran 5 tests in ~1.4s
# OK
```

## Manual Setup Steps

### 1. Verify Python
```bash
python3 --version  # Should be 3.6+
```

### 2. Check Dependencies
No external dependencies required! All imports use Python stdlib:
```bash
python3 -c "
import sqlite3, json, pathlib, re, subprocess, datetime
print('✓ All core dependencies available')
"
```

### 3. Run Tests
```bash
python3 run_tests.py
```

### 4. (Optional) Install Dev Tools
For linting and advanced testing:
```bash
# Create virtual environment (recommended)
python3 -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Install development tools
pip install -r requirements-dev.txt

# Run with pytest
pytest tests/ -v

# Lint code
ruff check src/
black --check src/
```

## Project Structure

```
workspace-system/
├── src/                          # Core Python modules (35+ files)
│   ├── workspace_manager.py      # Main workspace management
│   ├── schema.py                 # Database schema definitions
│   ├── db_utils.py              # Database connection utilities
│   └── ... (32 more modules)
├── tests/                        # Test suite
│   ├── test_src_imports.py      # Import validation tests
│   ├── test_schema.py           # Database schema tests
│   ├── conftest.py              # Pytest fixtures
│   └── __init__.py
├── docs/                         # Documentation
├── requirements.txt              # Production dependencies
├── requirements-dev.txt          # Development dependencies
├── pytest.ini                    # Pytest configuration
├── run_tests.py                  # Standalone test runner
├── TESTING.md                    # Testing guide (this file)
└── README.md                     # Project overview
```

## Core Features

✅ **11 Integrated Systems**
- Knowledge Base, Wiki & Todos, Proposals, Collaboration
- Sessions, Tools, Reviews, Quality Gates, Prevention
- Maintenance, Unified CLI

✅ **Prevention-First Architecture**
- Block issues before they happen
- < 5ms overhead per request
- No expensive recovery

✅ **Zero External Dependencies**
- Core system uses only Python stdlib
- Optional dev tools: pytest, ruff, black
- Lightweight and portable

## Quick Commands

| Command | Purpose |
|---------|---------|
| `python3 run_tests.py` | Run all tests |
| `python3 -m py_compile src/*.py` | Check syntax |
| `pytest tests/ -v` | Run tests with pytest (if installed) |
| `ruff check src/` | Lint code (if ruff installed) |
| `black src/` | Format code (if black installed) |

## Verification Checklist

- [x] Python 3.6+ installed
- [x] All modules import successfully (35+ files)
- [x] Database schema is valid
- [x] Connection context manager works
- [x] 5/5 tests passing
- [x] No syntax errors in source

## Next Steps

1. **Read**: Check out `README.md` for feature overview
2. **Test**: Run `python3 run_tests.py` to verify setup
3. **Explore**: Browse `src/` to understand architecture
4. **Contribute**: Add tests for new features (see TESTING.md)
5. **Deploy**: Use in your workspace (see README.md for usage)

## Support

- Tests: See `TESTING.md`
- Features: See `README.md`
- Architecture: See docs/ directory
- Issues: Check source code comments

---

**Status**: ✅ System Ready
**Test Results**: 5/5 PASS
**Dependencies**: All satisfied
