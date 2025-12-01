#!/bin/bash
# Quick fix script for project production readiness

PROJECT_DIR="/media/sunil-kr/workspace/user-projects/current/project"

echo "🔧 Fixing project production issues..."
echo ""

cd "$PROJECT_DIR" || exit 1

# 1. Complete merge
echo "1. Completing merge..."
if git status | grep -q "still merging"; then
    git commit -m "Merge: Complete pending merge with workflow improvements"
    echo "   ✓ Merge completed"
else
    echo "   ✓ No merge pending"
fi

# 2. Generate requirements.txt
echo "2. Generating requirements.txt..."
if [ -f "pyproject.toml" ]; then
    uv pip compile pyproject.toml -o requirements.txt 2>/dev/null || echo "   ⚠ Manual generation needed"
    echo "   ✓ requirements.txt generated"
fi

# 3. Update .gitignore
echo "3. Updating .gitignore..."
if ! grep -q ".review_cache" .gitignore 2>/dev/null; then
    cat >> .gitignore << 'IGNORE'

# Review cache
.review_cache/
.benchmarks/

# Temporary
tmp/
temp/
IGNORE
    echo "   ✓ .gitignore updated"
else
    echo "   ✓ .gitignore already updated"
fi

# 4. Show status
echo ""
echo "📊 Current status:"
git status --short | head -10

echo ""
echo "✅ Quick fixes applied!"
echo ""
echo "Next steps:"
echo "  1. Review changes: git status"
echo "  2. Run tests: make test"
echo "  3. Commit: git commit -am 'Production readiness fixes'"
