#!/bin/bash
# Extract All: Scan all projects for ideas

echo "============================================"
echo "IDEA EXTRACTION - ALL PROJECTS"
echo "============================================"
echo ""

# Main project
if [ -d "./project" ]; then
    echo "📦 Scanning main project..."
    python3 idea_extractor.py scan ./project
    echo ""
fi

# Archived projects
if [ -d "./projects-old" ]; then
    echo "📦 Scanning archived projects..."
    count=0
    for dir in projects-old/*/; do
        if [ -d "$dir" ]; then
            name=$(basename "$dir")
            echo "  → $name"
            python3 idea_extractor.py scan "$dir" 2>/dev/null
            ((count++))
        fi
    done
    echo "  ✓ Scanned $count archived projects"
    echo ""
fi

# Summary
echo "============================================"
echo "EXTRACTION SUMMARY"
echo "============================================"
python3 idea_extractor.py list

echo ""
echo "✓ Extraction complete"
echo ""
echo "Next steps:"
echo "  1. Review ideas: python3 idea_extractor.py list"
echo "  2. Check duplicates: python3 dedup_checker.py '<title>'"
echo "  3. Integrate: ./integrate_idea.sh <id>"
