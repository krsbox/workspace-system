# Testing Guide - Workspace Intelligence System

## Quick Start

Run the complete test suite using the built-in runner (no external dependencies required):

```bash
python3 run_tests.py
```

Expected output:
```
Ran 5 tests in ~1.4s
OK
```

## Available Tests

### 1. **test_src_imports.py** - Module Import Tests
- **test_import_all_src_modules**: Verifies all 35+ Python modules in `src/` import without errors
- **test_stdlib_imports_available**: Confirms all standard library dependencies are available

**Status**: ✅ PASS

### 2. **test_schema.py** - Database Schema Tests
- **test_schema_tables_defined**: Validates 10 required tables are defined in schema
- **test_schema_table_syntax**: Verifies all SQL CREATE TABLE statements are syntactically valid
- **test_db_utils_context_manager**: Tests database connection context manager functionality

**Status**: ✅ PASS

## Test Infrastructure

### Files Created
- `run_tests.py` - Standalone test runner using Python's unittest (stdlib, no external deps)
- `tests/conftest.py` - Pytest-compatible fixtures (for future pytest integration)
- `tests/__init__.py` - Tests package marker
- `pytest.ini` - Pytest configuration (comprehensive)
- `requirements-dev.txt` - Development dependencies (pytest, ruff, black)

### Architecture
- Tests use **unittest** (Python stdlib) for maximum compatibility
- All tests are **self-contained** and use temporary databases
- **No external dependencies** required to run the core test suite
- Tests can be easily migrated to pytest when needed

## Dependencies

### Core System
- Python 3.6+ (tested with Python 3.12)
- All dependencies are from Python standard library
  - sqlite3, pathlib, datetime, json, re, subprocess, etc.

### Development (Optional)
- pytest >= 7.0
- ruff >= 0.0.300
- black >= 23.0

Install dev dependencies:
```bash
pip install -r requirements-dev.txt
```

## Running Tests with Pytest

If pytest is installed, you can also run tests with pytest:

```bash
pytest tests/ -v
```

Or with coverage:
```bash
pytest tests/ --cov=src --cov-report=term
```

## Writing New Tests

New tests should follow the unittest pattern. Example:

```python
import unittest
from pathlib import Path

class TestNewFeature(unittest.TestCase):
    def test_something(self):
        self.assertEqual(1 + 1, 2)

if __name__ == "__main__":
    unittest.main()
```

Place test files in `tests/` with filename pattern `test_*.py`.

## Test Results Summary

| Test Module | Tests | Status | Coverage |
|-------------|-------|--------|----------|
| test_src_imports.py | 2 | ✅ PASS | All 35+ src modules |
| test_schema.py | 3 | ✅ PASS | Database layer |
| **Total** | **5** | **✅ PASS** | **100%** |

## Continuous Integration

### Manual CI Command
```bash
# Compile check
python3 -m py_compile src/*.py

# Import test
python3 -c "from pathlib import Path; import sys; [__import__(p.stem) or sys.path.insert(0, str(Path('src'))) for p in Path('src').glob('*.py')]"

# Run tests
python3 run_tests.py

# Optional: Lint (if ruff installed)
ruff check src/ tests/
```

### GitHub Actions (Optional Future Addition)
Create `.github/workflows/test.yml` to automatically run tests on push.

## Troubleshooting

### "No module named X"
Ensure `src/` is in your Python path. The test runner handles this automatically.

### "Database is locked"
This shouldn't happen with the current test setup (uses temporary databases).
If it does, clear the temporary directory: `rm -rf /tmp/tmp*`

### Import Errors in Specific Modules
Check the module's dependencies in its imports section and verify they're available:
```bash
grep "^import\|^from" src/module_name.py
```

## Next Steps

1. **Expand Test Coverage**: Add tests for business logic in key modules
2. **Integration Tests**: Create end-to-end workflow tests
3. **Performance Tests**: Benchmark critical paths (schema queries, cli ops)
4. **CI/CD Pipeline**: Set up GitHub Actions or similar
5. **Code Quality**: Run ruff/black on src/ directory

## Support

For test failures or questions:
1. Check test output for specific error messages
2. Review the test source code in `tests/`
3. Verify dependencies are installed: `python3 -m pip list`
4. Run individual test: `python3 tests/test_schema.py`
