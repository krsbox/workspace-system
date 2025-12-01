# Current Project: Action Plan

**Date:** 2025-12-02  
**Health Score:** 2/10 (CRITICAL)  
**Status:** 🔴 NEEDS IMMEDIATE ACTION

---

## 🎯 Critical Issues (Fix Today)

### 1. Stuck in Merge 🔴
**Problem:** Git merge incomplete for weeks  
**Impact:** Cannot push/pull, blocking all work  
**Solution:**
```bash
cd /media/sunil-kr/workspace/user-projects/current/project
git commit -m "Complete pending merge"
```
**Time:** 2 minutes

### 2. Too Many Staged Files 🔴
**Problem:** 87 files staged but not committed  
**Impact:** Risk of losing work, unclear state  
**Solution:**
```bash
# Review and commit
git status
git commit -m "Commit staged changes"
```
**Time:** 5 minutes

---

## 📊 Current State

### Size
- **Total:** 464MB
- **Python files:** 4,828
- **All files:** 26,896
- **Lines of code:** 1.6M

### Git
- **Branch:** minimal (not standard)
- **Last commit:** Oct 24, 2025 (over month ago)
- **Status:** Stuck in merge
- **Staged:** 87 files

### Bloat
- **Experimental:** 52K (nightly, latest, preview)
- **Archive:** 304K
- **Deprecated:** 249 files
- **Large files:** 28 files > 1MB

---

## 🚀 Action Plan

### Phase 1: Unstuck (Today - 30 min)

#### Step 1: Backup First
```bash
cd /media/sunil-kr/workspace/user-projects/current/project
git tag backup/before-fixes/$(date +%Y%m%d_%H%M%S)
```

#### Step 2: Complete Merge
```bash
git commit -m "Complete pending merge with workflow improvements"
```

#### Step 3: Verify
```bash
git status  # Should be clean
git log -1  # Should show new commit
```

**Rollback if needed:**
```bash
git checkout backup/before-fixes/YYYYMMDD_HHMMSS
```

---

### Phase 2: Quick Cleanup (Today - 30 min)

#### Step 1: Archive Experiments
```bash
mkdir -p archive/experiments
git mv nightly latest preview archive/experiments/
git commit -m "Archive experimental code"
```

#### Step 2: Clean Root
```bash
git mv temp_readme.md tmp/ 2>/dev/null
git mv test_tool.py tests/ 2>/dev/null
git commit -m "Clean root directory"
```

#### Step 3: Update .gitignore
```bash
cat >> .gitignore << 'EOF'

# Cache & temp
.review_cache/
.benchmarks/
tmp/
archive/experiments/
EOF
git add .gitignore
git commit -m "Update .gitignore"
```

**Total Time:** 30 minutes

---

### Phase 3: Deep Cleanup (This Week - 2 hours)

#### Day 1: Remove Dead Code
```bash
# Install fdupes
sudo apt install fdupes

# Find duplicates
fdupes -r . > duplicates.txt

# Review and remove
fdupes -r -d .  # Interactive
```

#### Day 2: Remove Deprecated Files
```bash
# Find deprecated
find . -name "*.deprecated.*" -o -name "*old*" -o -name "*backup*"

# Review and remove
git rm <deprecated-files>
git commit -m "Remove deprecated files"
```

#### Day 3: Archive Large Files
```bash
# Find large files
find . -type f -size +1M

# Move to archive or use Git LFS
git lfs track "*.pdf"
git lfs track "*.json"
```

**Total Time:** 2 hours

---

### Phase 4: Restructure (This Month - 1 week)

#### Consider Splitting Monorepo
**Current:** 1 massive repo (1.6M lines)  
**Option 1:** Keep monorepo, enforce boundaries  
**Option 2:** Split into separate repos

**Recommendation:** Keep monorepo, add boundaries

#### Add Size Limits
```yaml
# .github/workflows/size-check.yml
- name: Check file size
  run: |
    find . -size +1M -not -path "./.git/*"
    if [ $? -eq 0 ]; then exit 1; fi
```

#### Regular Cleanup Schedule
- **Daily:** Remove cache (`make clean`)
- **Weekly:** Check for duplicates
- **Monthly:** Archive old experiments
- **Quarterly:** Major cleanup

---

## 🛡️ Safety Measures

### Before Any Changes
```bash
# Git backup
git tag backup/before-cleanup/$(date +%Y%m%d)

# Or use workspace system
cd /media/sunil-kr/workspace/workspace-system
./ws backup /path/to/project "before-cleanup"
```

### After Changes
```bash
# Run tests
make test

# Check status
git status

# Verify nothing broken
make check
```

### Rollback if Needed
```bash
# Git rollback
git checkout backup/before-cleanup/YYYYMMDD

# Or workspace system
./ws recover /path/to/project backup/tag/name
```

---

## 📋 Checklist

### Immediate (Today)
- [ ] Create backup tag
- [ ] Complete merge
- [ ] Commit staged files
- [ ] Archive experiments
- [ ] Clean root directory
- [ ] Update .gitignore
- [ ] Run tests
- [ ] Push to remote

### Short Term (This Week)
- [ ] Install fdupes
- [ ] Find and remove duplicates
- [ ] Remove deprecated files (249)
- [ ] Archive large files
- [ ] Generate requirements.txt
- [ ] Update documentation

### Medium Term (This Month)
- [ ] Review monorepo structure
- [ ] Add size limits
- [ ] Setup cleanup automation
- [ ] Establish maintenance schedule
- [ ] Document architecture

---

## 🎯 Success Metrics

### Target Health Score: 8/10

**Improvements Needed:**
- ✓ Merge completed (+3)
- ✓ Files committed (+2)
- ✓ Experiments archived (+1)
- ✓ Deprecated removed (+1)
- ✓ Regular commits (+1)

**Result:** 2 → 8 (from CRITICAL to HEALTHY)

---

## 💡 Prevention (Future)

### Use Workspace System
```bash
# Daily check
./ws project-analyze project

# Weekly cleanup
./ws analyze-cleanup /path/to/project
./ws auto-cleanup /path/to/project --live

# Monthly review
./ws status
```

### Git Hooks
```bash
# .git/hooks/pre-commit
#!/bin/bash
# Prevent large files
find . -size +10M -not -path "./.git/*" && exit 1
```

### CI/CD Checks
```yaml
# Check for bloat
- name: Check project health
  run: |
    ./ws project-analyze project
    # Fail if health score < 5
```

---

## 🚀 Quick Start Script

```bash
#!/bin/bash
# quick-fix.sh

PROJECT="/media/sunil-kr/workspace/user-projects/current/project"
cd "$PROJECT"

# Backup
git tag backup/quick-fix/$(date +%Y%m%d_%H%M%S)

# Fix
git commit -m "Complete merge" || true
mkdir -p archive/experiments
git mv nightly latest preview archive/experiments/ 2>/dev/null
git add -A
git commit -m "Quick cleanup: archive experiments, clean root"

# Verify
git status
echo "✅ Quick fix complete!"
```

**Run:** `./scripts/git-safe-fix.sh`

---

## 📊 Expected Results

### Before
- Health: 2/10 (CRITICAL)
- Stuck in merge
- 87 staged files
- 249 deprecated files
- No recent commits

### After Phase 1 (Today)
- Health: 5/10 (NEEDS ATTENTION)
- Merge complete
- Files committed
- Experiments archived
- Clean root

### After Phase 2 (This Week)
- Health: 7/10 (GOOD)
- Duplicates removed
- Deprecated cleaned
- Large files archived

### After Phase 3 (This Month)
- Health: 8/10 (HEALTHY)
- Regular maintenance
- Size limits enforced
- Automated checks

---

## 🎯 Next Steps

1. **Right Now:** Run `./scripts/git-safe-fix.sh`
2. **Today:** Complete Phase 1 (30 min)
3. **This Week:** Complete Phase 2 (2 hours)
4. **This Month:** Complete Phase 3 (1 week)

---

**Status:** 📋 READY TO EXECUTE  
**Priority:** 🔴 CRITICAL  
**Time Required:** 30 min (immediate), 3 hours (total)

**Start with:** `./scripts/git-safe-fix.sh`
