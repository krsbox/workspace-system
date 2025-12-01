# Ignore Logic: Comprehensive Guide

**Philosophy:** Ignore what shouldn't be tracked, track what matters

---

## 🎯 What to Ignore

### Always Ignore
- ✓ Generated files (__pycache__, *.pyc)
- ✓ Virtual environments (.venv, venv)
- ✓ Build artifacts (dist/, build/)
- ✓ Cache directories (.pytest_cache, .ruff_cache)
- ✓ IDE files (.vscode, .idea)
- ✓ OS files (.DS_Store, Thumbs.db)
- ✓ Logs (*.log)
- ✓ Temporary files (tmp/, *.tmp)
- ✓ Environment files (.env)

### Project-Specific
- ✓ Large data files (*.db, *.sqlite)
- ✓ Experimental code (nightly/, latest/, preview/)
- ✓ Deprecated files (*.deprecated.*)
- ✓ Archive directories (archive/)
- ✓ AI assistant dirs (.amazonq/, .gemini/)

### Never Ignore
- ✗ Source code (*.py, *.js)
- ✗ Configuration (pyproject.toml, *.yaml)
- ✗ Documentation (README.md, docs/)
- ✗ Tests (tests/)
- ✗ Scripts (scripts/)
- ✗ CI/CD (.github/)

---

## 📋 Ignore Files Created

### For Current Project

1. **.gitignore** - Comprehensive Git ignore
2. **.dockerignore** - Docker build ignore
3. **.gitattributes** - Line endings & file types

### For Workspace System

1. **.gitignore** - Workspace ignore
2. **.dockerignore** - Docker ignore
3. **.gcloudignore** - Google Cloud ignore
4. **.ruffignore** - Ruff linter ignore
5. **.prettierignore** - Prettier ignore
6. **.eslintignore** - ESLint ignore
7. **.gitattributes** - Line endings

---

## 🧹 Cleaning Tracked Files

### Problem
Files that should be ignored are already tracked in Git.

### Solution
```bash
# Run cleanup script
./scripts/clean-tracked-ignored.sh
```

**What it does:**
1. Creates backup (git tag)
2. Removes from tracking (keeps local)
3. Updates ignore files
4. Shows summary

**Safe:** Files kept locally, only removed from Git

---

## 🔍 Check What's Ignored

### Test Ignore Rules
```bash
# Check if file is ignored
git check-ignore -v filename

# List all ignored files
git status --ignored

# Find tracked files that should be ignored
git ls-files | grep -E "(\.cache|\.log|tmp/)"
```

### Verify Ignore Files
```bash
# Check .gitignore syntax
git check-ignore --verbose *

# Test specific patterns
git check-ignore -v __pycache__ .venv *.log
```

---

## 📊 Current Project Issues

### Tracked But Should Be Ignored

**Deprecated files:** 6+ files
```
docs/improvements/*.deprecated.md
tools/*/intelligent_code_review.deprecated.py
```

**Experimental dirs:** 3 directories
```
nightly/ (4 files)
latest/ (4 files)
preview/ (2 files)
```

**Solution:** Run `./scripts/clean-tracked-ignored.sh`

---

## 🎯 Ignore Patterns

### Python Projects
```gitignore
# Runtime
__pycache__/
*.py[cod]
*.so

# Virtual env
.venv/
venv/

# Testing
.pytest_cache/
.coverage

# Build
dist/
build/
*.egg-info/
```

### Node Projects
```gitignore
node_modules/
package-lock.json
.npm/
.yarn/
```

### General
```gitignore
# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Temp
tmp/
*.tmp
```

---

## 🛡️ Safety Rules

### Before Cleaning
1. **Backup:** `git tag backup/before-cleanup/$(date +%Y%m%d)`
2. **Review:** Check what will be removed
3. **Test:** Run with `--dry-run` if available

### After Cleaning
1. **Verify:** `git status` should be clean
2. **Test:** Run tests to ensure nothing broken
3. **Commit:** Commit the changes

### Rollback
```bash
# If something goes wrong
git checkout backup/before-cleanup/YYYYMMDD
```

---

## 📋 Checklist

### For New Projects
- [ ] Copy .gitignore from template
- [ ] Add project-specific ignores
- [ ] Create .dockerignore
- [ ] Create .gitattributes
- [ ] Test ignore rules
- [ ] Commit ignore files

### For Existing Projects
- [ ] Review current .gitignore
- [ ] Find tracked files that should be ignored
- [ ] Backup (git tag)
- [ ] Run cleanup script
- [ ] Update ignore files
- [ ] Commit changes

---

## 🎓 Best Practices

### DO ✓
- Ignore generated files
- Ignore environment-specific files
- Ignore large binary files
- Ignore cache directories
- Keep ignore files updated

### DON'T ✗
- Ignore source code
- Ignore configuration
- Ignore documentation
- Ignore tests
- Commit secrets (use .env)

---

## 🔧 Tools

### Check Ignored Files
```bash
# What's ignored
git status --ignored

# Why is file ignored
git check-ignore -v filename

# List all ignore rules
cat .gitignore
```

### Clean Ignored Files
```bash
# Remove ignored files from working directory
git clean -fdX

# Preview what will be removed
git clean -fdXn
```

### Update Ignore Rules
```bash
# After updating .gitignore
git rm -r --cached .
git add .
git commit -m "Update ignore rules"
```

---

## 📊 Impact

### Before Cleanup
- Deprecated files: Tracked
- Experimental dirs: Tracked
- Cache files: Tracked
- Total bloat: ~100+ files

### After Cleanup
- Deprecated files: Ignored
- Experimental dirs: Ignored
- Cache files: Ignored
- Total bloat: 0 files

**Result:** Cleaner repo, faster operations

---

## 🚀 Quick Commands

```bash
# Check ignore status
git check-ignore -v *

# Clean tracked ignored files
./scripts/clean-tracked-ignored.sh

# Verify cleanup
git status --ignored

# Commit changes
git commit -m "Update ignore logic, clean tracked files"
```

---

## 💡 Key Takeaways

1. **Ignore generated files** - Don't track build artifacts
2. **Ignore environment files** - Keep .env local
3. **Ignore cache** - Regenerate as needed
4. **Track source** - Always track code
5. **Update regularly** - Keep ignore files current

---

**Status:** ✅ COMPREHENSIVE  
**Files Created:** 3 for project, 7 for workspace  
**Script:** `./scripts/clean-tracked-ignored.sh`
