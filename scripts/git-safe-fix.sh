#!/bin/bash
# Safe fixes using Git (don't reinvent the wheel)

set -e

PROJECT_DIR="/media/sunil-kr/workspace/user-projects/current/project"

echo "🛡️  Git-Based Safe Fix"
echo "======================"
echo ""

cd "$PROJECT_DIR" || exit 1

# Step 1: Git backup (stash + tag)
echo "1️⃣  Creating git backup..."
BACKUP_TAG=$(python3 /media/sunil-kr/workspace/workspace-system/src/git_backup.py backup . "before-fixes" | grep "Backup created:" | cut -d: -f2 | xargs)

if [ -z "$BACKUP_TAG" ]; then
    echo "❌ Backup failed! Aborting."
    exit 1
fi

echo "   ✓ Backup tag: $BACKUP_TAG"
echo ""

# Step 2: Apply fixes
echo "2️⃣  Applying fixes..."

# Complete merge if needed
if git status | grep -q "still merging"; then
    echo "   → Completing merge..."
    git commit -m "Merge: Complete pending merge" || {
        echo "❌ Merge failed! Rolling back..."
        git checkout "$BACKUP_TAG"
        exit 1
    }
    echo "     ✓ Merge completed"
fi

# Move experimental dirs
echo "   → Archiving experiments..."
mkdir -p archive/experiments
for dir in nightly latest preview; do
    [ -d "$dir" ] && git mv "$dir" archive/experiments/ 2>/dev/null && echo "     ✓ Moved $dir/"
done

# Clean root
echo "   → Cleaning root..."
[ -f "temp_readme.md" ] && git mv temp_readme.md tmp/ 2>/dev/null
[ -f "test_tool.py" ] && git mv test_tool.py tests/ 2>/dev/null

# Update .gitignore
if ! grep -q ".review_cache" .gitignore; then
    cat >> .gitignore << 'EOF'

# Cache & temp
.review_cache/
.benchmarks/
tmp/
archive/experiments/
EOF
    git add .gitignore
    echo "     ✓ Updated .gitignore"
fi

# Commit changes
echo "   → Committing changes..."
git add -A
git commit -m "Production readiness fixes

- Complete pending merge
- Archive experimental code (nightly, latest, preview)
- Clean root directory
- Update .gitignore

Backup: $BACKUP_TAG" || {
    echo "❌ Commit failed! Rolling back..."
    git checkout "$BACKUP_TAG"
    exit 1
}

echo ""
echo "✅ Fixes completed successfully!"
echo ""
echo "📊 Summary:"
echo "  - Backup: $BACKUP_TAG"
echo "  - Changes committed"
echo ""
echo "🔄 To rollback:"
echo "  git checkout $BACKUP_TAG"
echo ""
