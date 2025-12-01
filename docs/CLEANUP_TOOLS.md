# Smart Cleanup: Use Proven Tools

**Philosophy:** Don't reinvent deduplication. Use proven tools.

---

## 🎯 Proven Tools We Use

### 1. fdupes - Duplicate File Finder
**Age:** 20+ years  
**Trust:** Industry standard  
**Install:** `sudo apt install fdupes`

```bash
# Find duplicates
fdupes -r /path/to/project

# Interactive removal
fdupes -r -d /path/to/project

# Delete automatically (keep first)
fdupes -r -d -N /path/to/project
```

### 2. vulture - Dead Code Finder
**Age:** 10+ years  
**Trust:** Python community standard  
**Install:** `uv pip install vulture`

```bash
# Find dead code
vulture /path/to/project

# High confidence only
vulture /path/to/project --min-confidence 80
```

### 3. autoflake - Unused Import Remover
**Age:** 10+ years  
**Trust:** Python standard  
**Install:** `uv pip install autoflake`

```bash
# Check unused imports
autoflake --check -r /path/to/project

# Remove unused imports
autoflake --in-place --remove-all-unused-imports -r /path/to/project
```

### 4. black - Code Formatter
**Age:** 7+ years  
**Trust:** Python standard (already installed)  
**Install:** `uv pip install black`

```bash
# Format code
black /path/to/project
```

### 5. find - File Search
**Age:** 50+ years  
**Trust:** Unix standard (built-in)  
**Install:** Built-in

```bash
# Find large files
find /path -type f -size +1M

# Find and remove cache
find /path -type d -name __pycache__ -exec rm -rf {} +
```

---

## 🚀 Quick Start

### Install Tools
```bash
# System tools
sudo apt install fdupes

# Python tools
source .venv/bin/activate
uv pip install vulture autoflake
```

### Run Analysis
```bash
# Analyze project
python3 src/smart_cleanup.py analyze /path/to/project

# Auto cleanup (dry run)
python3 src/smart_cleanup.py cleanup /path/to/project

# Auto cleanup (live)
python3 src/smart_cleanup.py cleanup /path/to/project --live
```

---

## 📊 What Each Tool Finds

| Tool | Finds | Safe to Auto-Remove |
|------|-------|---------------------|
| fdupes | Duplicate files | ⚠️ Review first |
| vulture | Dead code | ⚠️ Review first |
| autoflake | Unused imports | ✅ Yes |
| black | Formatting issues | ✅ Yes |
| find | Large files, cache | ✅ Cache only |

---

## 🎯 Workflow

### 1. Analyze
```bash
./ws analyze-cleanup /path/to/project
```

Shows:
- Duplicate files
- Dead code
- Large files
- Unused imports

### 2. Review
- Check report
- Decide what to remove
- Backup first (git tag)

### 3. Cleanup
```bash
# Safe auto-cleanup
./ws auto-cleanup /path/to/project

# Or manual
fdupes -r -d /path/to/project
autoflake --in-place --remove-all-unused-imports -r /path/to/project
```

---

## ⚠️ Safety

### Always Safe
- ✅ Remove unused imports (autoflake)
- ✅ Format code (black)
- ✅ Remove __pycache__

### Review First
- ⚠️ Duplicate files (might be intentional)
- ⚠️ Dead code (might be used dynamically)
- ⚠️ Large files (might be needed)

### Backup First
```bash
# Git backup
git tag backup/before-cleanup/$(date +%Y%m%d)

# Then cleanup
python3 src/smart_cleanup.py cleanup . --live
```

---

## 💡 Why Use Existing Tools?

### fdupes vs Custom
- **fdupes:** 20+ years, proven, fast
- **Custom:** Untested, slow, buggy

### vulture vs Custom
- **vulture:** AST-based, accurate
- **Custom:** Regex-based, false positives

### autoflake vs Custom
- **autoflake:** Handles all edge cases
- **Custom:** Misses edge cases

**Result:** Use proven tools, don't reinvent.

---

## 📋 Example Output

```bash
$ python3 src/smart_cleanup.py analyze /project

🔍 Smart Cleanup Analysis: project
============================================================

🔍 Finding duplicate files (using fdupes)...
📋 Found 5 duplicate file groups
   Group 1: 3 files
   Group 2: 2 files

🔍 Finding dead code (using vulture)...
📋 Found 12 dead code items
   unused function 'old_helper' (90% confidence)
   unused variable 'temp' (85% confidence)

🔍 Finding files > 1MB (using find)...
📋 Found 3 large files (>1MB)
   2.5MB: old_data.json
   1.8MB: backup.sql

🔍 Finding unused imports (using autoflake)...
📋 Found 8 unused imports
   would remove unused import 'os'
   would remove unused import 'sys'

============================================================
📊 Total Issues: 28

💡 Cleanup Commands:
   fdupes -r -d <path>
   autoflake --in-place --remove-all-unused-imports -r <path>
```

---

## 🎓 Best Practices

### DO ✓
- Use proven tools
- Backup before cleanup
- Review before removing
- Start with safe operations

### DON'T ✗
- Build custom deduplication
- Auto-remove without review
- Skip backups
- Trust custom tools over proven ones

---

## 🔧 Integration

### Add to Makefile
```makefile
cleanup-analyze:
	python3 src/smart_cleanup.py analyze .

cleanup-safe:
	python3 src/smart_cleanup.py cleanup . --live
```

### Add to CI/CD
```yaml
- name: Check for cleanup opportunities
  run: python3 src/smart_cleanup.py analyze .
```

---

## 📊 Tool Comparison

| Feature | Custom Solution | Proven Tools |
|---------|----------------|--------------|
| Development time | Weeks | Minutes |
| Reliability | Unknown | Proven |
| Maintenance | We maintain | Community |
| Features | Basic | Complete |
| Trust | None | Years of use |

**Winner:** Proven tools (obviously)

---

## ✅ Summary

**Problem:** Need to find duplicates, dead code, etc.  
**Wrong:** Build custom deduplication  
**Right:** Use fdupes, vulture, autoflake, etc.

**Tools:**
- fdupes (20+ years)
- vulture (10+ years)
- autoflake (10+ years)
- black (7+ years)
- find (50+ years)

**Result:** Proven, reliable, maintained by community

---

**Status:** ✅ USE PROVEN TOOLS  
**Install:** See above  
**Don't:** Reinvent deduplication
