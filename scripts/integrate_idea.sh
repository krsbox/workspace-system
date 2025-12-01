#!/bin/bash
# Integrate Idea: Safe workflow from idea to proposal

if [ $# -lt 1 ]; then
    echo "Usage: ./integrate_idea.sh <idea_id>"
    exit 1
fi

IDEA_ID=$1

# Get idea details
IDEA_DATA=$(python3 -c "
import sqlite3
conn = sqlite3.connect('workspace_knowledge.db')
c = conn.cursor()
c.execute('SELECT title, description, category, reality_score FROM ideas WHERE id=?', ($IDEA_ID,))
row = c.fetchone()
if row:
    print(f'{row[0]}|{row[1]}|{row[2]}|{row[3]}')
conn.close()
")

if [ -z "$IDEA_DATA" ]; then
    echo "✗ Idea #$IDEA_ID not found"
    exit 1
fi

IFS='|' read -r TITLE DESC CATEGORY REALITY <<< "$IDEA_DATA"

echo "============================================"
echo "Integrating Idea #$IDEA_ID"
echo "============================================"
echo "Title: $TITLE"
echo "Category: $CATEGORY"
echo "Reality: $REALITY%"
echo ""

# Check reality score
if [ "$REALITY" -lt 50 ]; then
    echo "⚠️  Low reality score (<50%). Continue? (y/n)"
    read -r response
    if [ "$response" != "y" ]; then
        echo "✗ Integration cancelled"
        exit 1
    fi
fi

# Check for duplicates
echo "Checking for duplicates..."
python3 dedup_checker.py "$TITLE"
DEDUP_STATUS=$?

if [ $DEDUP_STATUS -ne 0 ]; then
    echo ""
    echo "⚠️  Duplicates found. Continue anyway? (y/n)"
    read -r response
    if [ "$response" != "y" ]; then
        echo "✗ Integration cancelled"
        exit 1
    fi
fi

# Create proposal
echo ""
echo "Creating proposal..."
./ws propose "$TITLE"

# Run checks
echo ""
echo "Running quality checks..."
./ws check

echo ""
echo "✓ Integration complete"
echo "  Next: Review proposal and convert to todo"
