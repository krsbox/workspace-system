#!/bin/bash
# Folder Reorganization: Separate workspace from projects

echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║                                                                  ║"
echo "║              FOLDER ARCHITECTURE REORGANIZATION                  ║"
echo "║                                                                  ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""

# Current structure
CURRENT_DIR="/media/sunil-kr/workspace/projects"

# Proposed structure
WORKSPACE_DIR="/media/sunil-kr/workspace"
PROJECTS_DIR="/media/sunil-kr/workspace/user-projects"
ARCHIVE_DIR="/media/sunil-kr/workspace/user-projects/archive"

echo "📊 CURRENT STRUCTURE:"
echo "  /media/sunil-kr/workspace/projects/"
echo "    ├── project/              (active project)"
echo "    ├── projects-old/         (21 archived projects)"
echo "    ├── *.py                  (workspace tools)"
echo "    ├── *.md                  (documentation)"
echo "    └── workspace_knowledge.db"
echo ""

echo "📊 PROPOSED STRUCTURE:"
echo "  /media/sunil-kr/workspace/"
echo "    ├── workspace-system/     (workspace management)"
echo "    │   ├── *.py              (all tools)"
echo "    │   ├── *.md              (all docs)"
echo "    │   ├── *.sh              (scripts)"
echo "    │   └── workspace_knowledge.db"
echo "    │"
echo "    └── user-projects/        (user projects)"
echo "        ├── current/          (active project)"
echo "        └── archive/          (archived projects)"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Ask for confirmation
read -p "Proceed with reorganization? (y/n): " confirm

if [ "$confirm" != "y" ]; then
    echo "✗ Reorganization cancelled"
    exit 0
fi

echo ""
echo "🚀 Starting reorganization..."
echo ""

# Step 1: Create new directories
echo "Step 1: Creating new directory structure..."
mkdir -p "$WORKSPACE_DIR/workspace-system"
mkdir -p "$PROJECTS_DIR/current"
mkdir -p "$ARCHIVE_DIR"
echo "  ✓ Directories created"

# Step 2: Move workspace files
echo ""
echo "Step 2: Moving workspace management files..."
cd "$CURRENT_DIR"

# Move Python tools
mv *.py "$WORKSPACE_DIR/workspace-system/" 2>/dev/null
echo "  ✓ Python tools moved"

# Move shell scripts
mv *.sh "$WORKSPACE_DIR/workspace-system/" 2>/dev/null
echo "  ✓ Shell scripts moved"

# Move documentation
mv *.md "$WORKSPACE_DIR/workspace-system/" 2>/dev/null
echo "  ✓ Documentation moved"

# Move database
mv workspace_knowledge.db "$WORKSPACE_DIR/workspace-system/" 2>/dev/null
echo "  ✓ Database moved"

# Move backups
mv backups "$WORKSPACE_DIR/workspace-system/" 2>/dev/null
echo "  ✓ Backups moved"

# Move __pycache__
mv __pycache__ "$WORKSPACE_DIR/workspace-system/" 2>/dev/null
echo "  ✓ Cache moved"

# Step 3: Move active project
echo ""
echo "Step 3: Moving active project..."
mv project "$PROJECTS_DIR/current/" 2>/dev/null
echo "  ✓ Active project moved"

# Step 4: Move archived projects
echo ""
echo "Step 4: Moving archived projects..."
mv projects-old/* "$ARCHIVE_DIR/" 2>/dev/null
rmdir projects-old 2>/dev/null
echo "  ✓ Archived projects moved"

# Step 5: Create symlinks for easy access
echo ""
echo "Step 5: Creating convenience symlinks..."
cd "$WORKSPACE_DIR/workspace-system"
ln -sf "$WORKSPACE_DIR/workspace-system" "$WORKSPACE_DIR/ws-system" 2>/dev/null
ln -sf "$PROJECTS_DIR" "$WORKSPACE_DIR/projects" 2>/dev/null
echo "  ✓ Symlinks created"

# Step 6: Update paths in scripts
echo ""
echo "Step 6: Updating paths in scripts..."

# Update DB_PATH in Python files
for file in "$WORKSPACE_DIR/workspace-system"/*.py; do
    if [ -f "$file" ]; then
        sed -i 's|Path(__file__).parent / "workspace_knowledge.db"|Path("/media/sunil-kr/workspace/workspace-system/workspace_knowledge.db")|g' "$file"
    fi
done
echo "  ✓ Paths updated"

# Step 7: Update ws symlink
echo ""
echo "Step 7: Updating workspace CLI..."
cd "$WORKSPACE_DIR/workspace-system"
rm ws 2>/dev/null
ln -s workspace_cli.py ws
chmod +x ws
echo "  ✓ CLI updated"

# Step 8: Clean up old directory
echo ""
echo "Step 8: Cleaning up..."
cd "$WORKSPACE_DIR"
rmdir "$CURRENT_DIR" 2>/dev/null || echo "  ⚠️  Old directory not empty (contains hidden files)"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "✅ REORGANIZATION COMPLETE!"
echo ""
echo "📊 NEW STRUCTURE:"
echo "  Workspace System: $WORKSPACE_DIR/workspace-system/"
echo "  Active Project:   $PROJECTS_DIR/current/project/"
echo "  Archived:         $ARCHIVE_DIR/ (21 projects)"
echo ""
echo "🔧 UPDATED COMMANDS:"
echo "  cd /media/sunil-kr/workspace/workspace-system"
echo "  ./ws status"
echo "  ./ws check"
echo ""
echo "📁 QUICK ACCESS:"
echo "  Workspace: cd ~/workspace/workspace-system"
echo "  Projects:  cd ~/workspace/user-projects"
echo ""
