# Workspace Manager Guide

Unified system for managing workspace knowledge, wiki, todos, and progress.

## Quick Start

```bash
# Make executable
chmod +x workspace_manager.py
```

## Wiki

Hierarchical documentation system with full-text search.

```bash
# Create page
python3 workspace_manager.py wiki create <path> <title> <content>
python3 workspace_manager.py wiki create "project/setup" "Setup Guide" "Installation steps..."

# Get page
python3 workspace_manager.py wiki get <path>
python3 workspace_manager.py wiki get "project/setup"

# List all pages
python3 workspace_manager.py wiki list

# Search
python3 workspace_manager.py wiki search "installation"
```

## Todos

Task management with status, priority, and project tracking.

```bash
# Add todo
python3 workspace_manager.py todo add <title> [description] [project]
python3 workspace_manager.py todo add "Fix bug" "Memory leak in parser" "project"

# List todos
python3 workspace_manager.py todo list              # All
python3 workspace_manager.py todo list todo         # By status
python3 workspace_manager.py todo list done

# Update status
python3 workspace_manager.py todo update <id> <status>
python3 workspace_manager.py todo update 1 done

# Statuses: todo, in_progress, blocked, done
# Priorities: low, medium, high, urgent
```

## Progress Tracking

Track milestones and completion percentage.

```bash
# Add milestone
python3 workspace_manager.py progress add <project> <milestone>
python3 workspace_manager.py progress add "refactor" "Phase 1 Complete"

# Update progress
python3 workspace_manager.py progress update <id> <percentage>
python3 workspace_manager.py progress update 1 50

# List progress
python3 workspace_manager.py progress list              # All
python3 workspace_manager.py progress list "refactor"   # By project
```

## Knowledge Base (Original)

Still available via `kb_manager.py`:

```bash
# Add knowledge
python3 kb_manager.py add <category> <title> <content> [tags]

# Search
python3 kb_manager.py search <query>

# List
python3 kb_manager.py list [category]
```

## Database

All data stored in: `workspace_knowledge.db`

- Persistent across sessions
- Full-text search enabled
- SQLite format (portable, no server needed)

## Use Cases

**Wiki**: Documentation, guides, architecture notes  
**Todos**: Tasks, bugs, features to implement  
**Progress**: Project milestones, completion tracking  
**Knowledge**: Quick facts, findings, reference data

## Examples

```bash
# Document a finding
python3 workspace_manager.py wiki create "findings/2025-11-30" "Session Findings" "Discovered 22 archived projects..."

# Track refactoring work
python3 workspace_manager.py todo add "Consolidate scripts" "Merge duplicate automation scripts" "refactor"
python3 workspace_manager.py progress add "refactor" "Script consolidation" "in_progress" 30

# Search everything
python3 workspace_manager.py wiki search "scripts"
python3 kb_manager.py search "automation"
```

## Integration

Can be called from:
- Shell scripts
- Python code
- Git hooks
- CI/CD pipelines
- Cron jobs

## Backup

```bash
# Backup database
cp workspace_knowledge.db workspace_knowledge.backup.db

# Export to JSON (future enhancement)
```
