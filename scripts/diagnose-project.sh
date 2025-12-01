#!/bin/bash
# Quick project health diagnosis

PROJECT_DIR="/media/sunil-kr/workspace/user-projects/current/project"

echo "🔍 Project Health Diagnosis"
echo "=============================="
echo ""

cd "$PROJECT_DIR" || exit 1

# Size
echo "📊 Size:"
echo "  Total: $(du -sh . | cut -f1)"
echo "  Python files: $(find . -name "*.py" -type f | wc -l)"
echo "  All files: $(find . -type f | wc -l)"
echo ""

# Git status
echo "📝 Git Status:"
if git status | grep -q "still merging"; then
    echo "  🔴 STUCK IN MERGE"
else
    echo "  ✓ Clean"
fi
echo "  Branch: $(git branch --show-current)"
echo "  Staged: $(git diff --cached --name-only | wc -l) files"
echo "  Modified: $(git diff --name-only | wc -l) files"
echo "  Last commit: $(git log -1 --format=%cd --date=short)"
echo ""

# Experimental directories
echo "🧪 Experimental Code:"
for dir in nightly latest preview tmp; do
    if [ -d "$dir" ]; then
        size=$(du -sh "$dir" 2>/dev/null | cut -f1)
        files=$(find "$dir" -type f | wc -l)
        echo "  $dir/: $size ($files files)"
    fi
done
echo ""

# Archive
echo "📦 Archive:"
if [ -d "archive" ]; then
    size=$(du -sh archive 2>/dev/null | cut -f1)
    dirs=$(find archive -maxdepth 1 -type d | wc -l)
    echo "  Size: $size"
    echo "  Subdirs: $((dirs - 1))"
fi
echo ""

# Deprecated files
echo "🗑️  Deprecated/Old:"
deprecated=$(find . -name "*.deprecated.*" -o -name "*old*" -o -name "*backup*" 2>/dev/null | wc -l)
echo "  Files: $deprecated"
echo ""

# Health Score
echo "🎯 Health Score:"
score=10

# Deduct for issues
if git status | grep -q "still merging"; then
    score=$((score - 3))
    echo "  -3: Stuck in merge"
fi

if [ $(git diff --cached --name-only | wc -l) -gt 50 ]; then
    score=$((score - 2))
    echo "  -2: Too many staged files"
fi

if [ $(find . -name "*.py" -type f | wc -l) -gt 1000 ]; then
    score=$((score - 2))
    echo "  -2: Very large codebase"
fi

if [ $deprecated -gt 10 ]; then
    score=$((score - 1))
    echo "  -1: Many deprecated files"
fi

echo ""
echo "  Final Score: $score/10"

if [ $score -ge 8 ]; then
    echo "  Status: 🟢 HEALTHY"
elif [ $score -ge 5 ]; then
    echo "  Status: 🟡 NEEDS ATTENTION"
else
    echo "  Status: 🔴 CRITICAL"
fi

echo ""
echo "=============================="
