#!/bin/bash
# Clean files that are tracked but should be ignored

PROJECT_DIR="/media/sunil-kr/workspace/user-projects/current/project"

echo "🧹 Cleaning Tracked Files That Should Be Ignored"
echo "=================================================="
echo ""

cd "$PROJECT_DIR" || exit 1

# Backup first
echo "1️⃣  Creating backup..."
git tag backup/before-ignore-cleanup/$(date +%Y%m%d_%H%M%S)
echo "   ✓ Backup created"
echo ""

# Remove from git but keep locally
echo "2️⃣  Removing from git (keeping local files)..."

# Deprecated files
echo "   → Deprecated files..."
git ls-files | grep "\.deprecated\." | xargs -r git rm --cached
echo "     ✓ Deprecated files removed from tracking"

# Experimental directories
echo "   → Experimental directories..."
git rm --cached -r nightly/ latest/ preview/ 2>/dev/null || true
echo "     ✓ Experimental dirs removed from tracking"

# Cache files
echo "   → Cache files..."
git ls-files | grep -E "(\.cache|\.review_cache)" | xargs -r git rm --cached
echo "     ✓ Cache files removed from tracking"

# Temp files
echo "   → Temp files..."
git ls-files | grep -E "(tmp/|temp/|\.tmp|\.temp)" | xargs -r git rm --cached
echo "     ✓ Temp files removed from tracking"

# Backup files
echo "   → Backup files..."
git ls-files | grep -E "(backup|\.bak)" | xargs -r git rm --cached
echo "     ✓ Backup files removed from tracking"

echo ""
echo "3️⃣  Updating git cache..."
git add .gitignore .dockerignore .gitattributes 2>/dev/null || true
echo "   ✓ Ignore files updated"

echo ""
echo "=================================================="
echo "✅ Cleanup complete!"
echo ""
echo "📊 Summary:"
git status --short | wc -l | xargs echo "   Files changed:"
echo ""
echo "💡 Next steps:"
echo "   1. Review changes: git status"
echo "   2. Commit: git commit -m 'Clean tracked files, update ignore logic'"
echo "   3. Verify: git status (should be clean)"
echo ""
echo "🔄 To rollback:"
echo "   git checkout backup/before-ignore-cleanup/YYYYMMDD_HHMMSS"
echo ""
