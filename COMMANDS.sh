#!/usr/bin/env bash
# WORKSPACE SYSTEM - QUICK REFERENCE CARD
# Copy and paste commands below to work with the system

# ============================================================================
# DOCUMENTATION REFERENCE
# ============================================================================

# View Quick Start
echo "cat INDEX.md"

# View Full Architecture
echo "cat ARCHITECTURE_OVERVIEW.txt"

# View File Structure  
echo "cat STRUCTURE.md"

# View Testing Guide
echo "cat TESTING.md"

# View Setup Instructions
echo "cat SETUP.md"


# ============================================================================
# TESTING COMMANDS
# ============================================================================

# Run all tests (no external dependencies)
echo "python3 run_tests.py"

# Run with pytest (if installed)
echo "pytest tests/ -v"

# Run specific test module
echo "python3 tests/test_schema.py"
echo "python3 tests/test_src_imports.py"

# Run with coverage
echo "pytest tests/ --cov=src --cov-report=term"


# ============================================================================
# CODE QUALITY COMMANDS
# ============================================================================

# Check syntax (no external deps required)
echo "python3 -m py_compile src/*.py"

# Lint with ruff (if installed)
echo "ruff check src/"
echo "ruff check tests/"

# Format code with black (if installed)
echo "black src/ tests/"

# Lint and format all
echo "ruff check . && black ."


# ============================================================================
# SETUP & INSTALLATION
# ============================================================================

# Install development dependencies
echo "pip install -r requirements-dev.txt"

# Create virtual environment (recommended)
echo "python3 -m venv .venv"
echo "source .venv/bin/activate"

# Install production dependencies
echo "pip install -r requirements.txt"


# ============================================================================
# EXPLORATION COMMANDS
# ============================================================================

# List all modules
echo "ls -lh src/"

# Count lines of code
echo "wc -l src/*.py"

# Search for specific function/class
echo "grep -rn 'function_name' src/"

# View module structure
echo "grep -n '^class\|^def' src/workspace_cli.py"

# Check database schema
echo "sqlite3 workspace_knowledge.db '.tables'"
echo "sqlite3 workspace_knowledge.db '.schema'"


# ============================================================================
# DEVELOPMENT WORKFLOW
# ============================================================================

# 1. Make changes to src/
echo "# Edit files in src/"

# 2. Run tests
echo "python3 run_tests.py"

# 3. Check code quality
echo "python3 -m py_compile src/*.py"

# 4. Format code (optional)
echo "black src/"

# 5. Commit changes
echo "git add src/"
echo "git commit -m 'Description of changes'"


# ============================================================================
# USEFUL FILE LOCATIONS
# ============================================================================

# Main entry point
echo "src/workspace_cli.py         # CLI interface"

# Core database
echo "workspace_knowledge.db       # SQLite database"

# Schema definitions
echo "src/schema.py                # Database schema"
echo "src/db_utils.py              # Database utilities"

# Test suite
echo "tests/                       # All tests"
echo "run_tests.py                 # Test runner"

# Documentation
echo "INDEX.md                     # Documentation index"
echo "STRUCTURE.md                 # File organization"
echo "ARCHITECTURE_OVERVIEW.txt    # System design"
echo "README.md                    # Feature overview"


# ============================================================================
# SYSTEM INFORMATION
# ============================================================================

# Check Python version
echo "python3 --version"

# Verify all imports
echo "python3 -c \"import sys; from pathlib import Path; [__import__(f[:-3]) for f in sorted(Path('src').glob('*.py'))] and print('✓ All imports OK')\""

# Show file statistics
echo "echo '=== Project Statistics ===' && find src -name '*.py' | wc -l && echo 'modules' && wc -l src/*.py | tail -1"

# Check test status
echo "python3 run_tests.py 2>&1 | grep -E 'Ran|OK|FAIL'"


# ============================================================================
# COMMON WORKFLOWS
# ============================================================================

# Add a new feature test
echo "cp tests/test_schema.py tests/test_myfeature.py"
echo "# Edit the test file"
echo "python3 run_tests.py"

# Debug a module import
echo "python3 -c \"import sys; sys.path.insert(0, 'src'); import module_name; print('OK')\""

# Check module docstring
echo "python3 -c \"import sys; sys.path.insert(0, 'src'); import module_name; print(module_name.__doc__)\""

# List database tables
echo "python3 -c \"import sqlite3; c = sqlite3.connect('workspace_knowledge.db').cursor(); print([row[0] for row in c.execute(\\\"SELECT name FROM sqlite_master WHERE type='table'\\\").fetchall()])\""


# ============================================================================
# ADVANCED COMMANDS
# ============================================================================

# Generate project structure visualization
echo "tree -L 2 -I '__pycache__' ."

# Find largest files
echo "find . -type f -size +1M -exec ls -lh {} \\; | awk '{print $9, $5}'"

# Count documentation lines
echo "wc -l *.md ARCHITECTURE_OVERVIEW.txt | tail -1"

# Run lint and tests together
echo "python3 -m py_compile src/*.py && python3 run_tests.py"

# Backup database
echo "cp workspace_knowledge.db workspace_knowledge.db.backup"

# Clean Python cache
echo "find . -type d -name '__pycache__' -exec rm -rf {} + 2>/dev/null"
echo "find . -type f -name '*.pyc' -delete"


# ============================================================================
# CI/CD PIPELINE COMMANDS
# ============================================================================

# Full validation pipeline
cat << 'PIPELINE'
#!/bin/bash
echo "Running validation pipeline..."
echo "1. Syntax check..." && python3 -m py_compile src/*.py
echo "2. Import test..." && python3 -c "from pathlib import Path; import sys; sys.path.insert(0, 'src'); [__import__(f.stem) for f in Path('src').glob('*.py')]"
echo "3. Unit tests..." && python3 run_tests.py
echo "4. Code quality..." && ruff check src/ 2>/dev/null || echo "   (ruff not installed)"
echo "✓ Pipeline complete!"
PIPELINE


# ============================================================================
# QUICK COPY-PASTE COMMANDS
# ============================================================================

# Everything at once
echo "
# Setup, test, and validate all at once:
python3 -m py_compile src/*.py && python3 run_tests.py && echo '✓ System Ready'
"

# Minimal startup
echo "
# Minimal: Just verify tests pass
python3 run_tests.py
"

# Full check with dev tools
echo "
# Full check (requires dev tools installed)
ruff check . && black . && pytest tests/ -v
"


# ============================================================================
# NOTES & TIPS
# ============================================================================

# 1. The system uses only Python stdlib for core functionality
# 2. Development tools (pytest, ruff, black) are optional
# 3. All tests pass without external dependencies
# 4. Database operations are isolated in tests (no conflicts)
# 5. Module imports work from any directory
# 6. See INDEX.md for full documentation guide


# ============================================================================
# HELPFUL RESOURCES
# ============================================================================

# Documentation
# - Quick Start: cat SETUP.md
# - Architecture: cat ARCHITECTURE_OVERVIEW.txt  
# - File Structure: cat STRUCTURE.md
# - Testing: cat TESTING.md
# - Everything: cat INDEX.md

# Code
# - Entry Point: src/workspace_cli.py
# - Database: src/schema.py + src/db_utils.py
# - Tests: tests/test_*.py

# Data
# - Database: workspace_knowledge.db
# - Scripts: scripts/

# Support
# - For issues: Check relevant documentation file
# - For questions: Review INDEX.md (has troubleshooting)
# - For development: Follow TESTING.md (test examples)

EOF
echo "✓ Commands ready to use!"
