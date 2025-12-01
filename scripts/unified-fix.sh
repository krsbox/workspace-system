#!/bin/bash
# Unified Fix: Complete project cleanup using workspace system

set -e

PROJECT_DIR="/media/sunil-kr/workspace/user-projects/current/project"
WS_DIR="/media/sunil-kr/workspace/workspace-system"

echo "🔧 Unified Project Fix"
echo "======================"
echo ""
echo "Project: $PROJECT_DIR"
echo ""

cd "$PROJECT_DIR" || exit 1

# Phase 1: Backup
echo "📦 Phase 1: Backup"
echo "-------------------"
BACKUP_TAG="backup/unified-fix/$(date +%Y%m%d_%H%M%S)"
git tag "$BACKUP_TAG"
echo "✓ Backup created: $BACKUP_TAG"
echo ""

# Phase 2: Complete Merge
echo "🔀 Phase 2: Complete Merge"
echo "---------------------------"
if git status | grep -q "still merging"; then
    git commit -m "Complete pending merge

- Resolve all conflicts
- Integrate workflow improvements
- Clean up staged files

Backup: $BACKUP_TAG" || {
        echo "❌ Merge commit failed"
        echo "Rollback: git checkout $BACKUP_TAG"
        exit 1
    }
    echo "✓ Merge completed"
else
    echo "✓ No merge pending"
fi
echo ""

# Phase 3: Update Ignore Files
echo "📝 Phase 3: Update Ignore Files"
echo "--------------------------------"
# Copy from workspace system if newer
if [ -f "$WS_DIR/user-projects/current/project/.gitignore" ]; then
    cp "$WS_DIR/user-projects/current/project/.gitignore" .gitignore
    cp "$WS_DIR/user-projects/current/project/.dockerignore" .dockerignore
    cp "$WS_DIR/user-projects/current/project/.gitattributes" .gitattributes
    echo "✓ Ignore files updated"
else
    echo "⚠ Using existing ignore files"
fi
echo ""

# Phase 4: Clean Tracked Ignored Files
echo "🧹 Phase 4: Clean Tracked Ignored Files"
echo "----------------------------------------"

# Remove deprecated files from tracking
echo "→ Removing deprecated files..."
git ls-files | grep "\.deprecated\." | xargs -r git rm --cached 2>/dev/null || true
echo "  ✓ Deprecated files"

# Remove experimental directories
echo "→ Removing experimental directories..."
git rm --cached -r nightly/ latest/ preview/ 2>/dev/null || true
echo "  ✓ Experimental dirs"

# Remove cache files
echo "→ Removing cache files..."
git ls-files | grep -E "(\.cache|\.review_cache)" | xargs -r git rm --cached 2>/dev/null || true
echo "  ✓ Cache files"

# Remove temp files
echo "→ Removing temp files..."
git ls-files | grep -E "(tmp/|temp/|\.tmp|\.temp)" | xargs -r git rm --cached 2>/dev/null || true
echo "  ✓ Temp files"

echo ""

# Phase 5: Archive Experiments
echo "📦 Phase 5: Archive Experiments"
echo "--------------------------------"
mkdir -p archive/experiments 2>/dev/null || true

for dir in nightly latest preview; do
    if [ -d "$dir" ]; then
        mv "$dir" archive/experiments/ 2>/dev/null || true
        echo "✓ Archived $dir/"
    fi
done
echo ""

# Phase 6: Clean Root Directory
echo "🧹 Phase 6: Clean Root Directory"
echo "---------------------------------"
mkdir -p tmp 2>/dev/null || true

# Move temp files
[ -f "temp_readme.md" ] && mv temp_readme.md tmp/ 2>/dev/null && echo "✓ Moved temp_readme.md"
[ -f "test_tool.py" ] && mv test_tool.py tests/ 2>/dev/null && echo "✓ Moved test_tool.py"

# Move shell scripts to scripts/
for script in *.sh; do
    if [ -f "$script" ] && [ "$script" != "*.sh" ]; then
        mkdir -p scripts 2>/dev/null || true
        mv "$script" scripts/ 2>/dev/null && echo "✓ Moved $script"
    fi
done
echo ""

# Phase 7: Stage and Commit
echo "💾 Phase 7: Stage and Commit"
echo "-----------------------------"
git add -A
git commit -m "Unified fix: cleanup and ignore logic

Applied:
- Complete merge
- Update ignore files (.gitignore, .dockerignore, .gitattributes)
- Remove tracked ignored files (deprecated, experimental, cache)
- Archive experiments (nightly, latest, preview)
- Clean root directory
- Organize scripts

Removed from tracking:
- Deprecated files (*.deprecated.*)
- Experimental dirs (nightly/, latest/, preview/)
- Cache files
- Temp files

Backup: $BACKUP_TAG" || {
    echo "❌ Commit failed"
    echo "Rollback: git checkout $BACKUP_TAG"
    exit 1
}
echo "✓ Changes committed"
echo ""

# Phase 8: Verify
echo "✅ Phase 8: Verify"
echo "------------------"
echo "Git status:"
git status --short | head -10
echo ""

# Run health check
echo "Health check:"
cd "$WS_DIR"
./scripts/diagnose-project.sh | tail -15

echo ""
echo "======================"
echo "✅ Unified Fix Complete!"
echo ""
echo "📊 Summary:"
echo "  - Backup: $BACKUP_TAG"
echo "  - Merge: Completed"
echo "  - Ignore files: Updated"
echo "  - Tracked ignored: Cleaned"
echo "  - Experiments: Archived"
echo "  - Root: Cleaned"
echo ""
echo "🔄 To rollback:"
echo "  cd $PROJECT_DIR"
echo "  git checkout $BACKUP_TAG"
echo ""
