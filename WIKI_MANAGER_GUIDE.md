# Wiki Manager - Search & View Documentation

## Overview

The **Wiki Manager** is a command-line tool for searching and viewing wiki entries stored in the workspace knowledge database. It provides fast, intuitive access to documentation, guides, and project information.

## Features

✅ **List all wiki entries** with sizes
✅ **Full-text search** across titles and content
✅ **View complete entries** with formatting
✅ **Statistics** about the wiki
✅ **No database modification** - read-only tool

## Installation

The wiki manager is already included in the workspace system. No additional installation needed.

## Quick Start

```bash
# List all wiki entries
python3 wiki_manager.py list

# Search for topics
python3 wiki_manager.py search extraction
python3 wiki_manager.py search quality

# View a full entry
python3 wiki_manager.py get "Quick Start"
python3 wiki_manager.py get "System Architecture"

# Show statistics
python3 wiki_manager.py stats
```

## Commands

### `list` - List All Wiki Entries

Display all available wiki entries with ID, title, and content size.

```bash
python3 wiki_manager.py list
```

**Output:**
```
📖 Wiki Entries (18 total)
──────────────────────────────────────────────────────────────────────
ID  Title                                         Size      
──────────────────────────────────────────────────────────────────────
  1 Workspace Overview                                   97
  2 System Architecture                                2457
  3 Quick Start                                         991
  ...
```

### `search` - Search Wiki Entries

Find wiki entries by keyword. Searches both titles and content.

```bash
python3 wiki_manager.py search <query>
```

**Examples:**
```bash
python3 wiki_manager.py search extraction
python3 wiki_manager.py search quality gates
python3 wiki_manager.py search collaboration
```

**Output:**
```
🔍 Search Results for 'extraction'
──────────────────────────────────────────────────────────────────────
ID  Title                                         Size      
──────────────────────────────────────────────────────────────────────
  6 Extraction Workflow                                7101
  4 Idea Extraction Ready                               42
 11 Session Summary                                    9717
  ...
```

### `get` - View Full Wiki Entry

Display the complete content of a wiki entry with metadata.

```bash
python3 wiki_manager.py get <title>
```

The title is matched case-insensitively and supports partial matches.

**Examples:**
```bash
python3 wiki_manager.py get "Quick Start"
python3 wiki_manager.py get "System Architecture"
python3 wiki_manager.py get "Extraction"
```

**Output:**
```
══════════════════════════════════════════════════════════════════════
📖 Quick Start
══════════════════════════════════════════════════════════════════════
ID: 3 | Created: 2025-12-01T00:44:13.010178 | Updated: 2025-12-02T11:16:44.317480
──────────────────────────────────────────────────────────────────────

# Workspace Intelligence System
[Full content displayed...]
```

### `stats` - Wiki Statistics

Show aggregated statistics about the wiki database.

```bash
python3 wiki_manager.py stats
```

**Output:**
```
📊 Wiki Statistics
──────────────────────────────────────────────────────────────────────
  Total Entries: 18
  Total Size: 73.8 KB
  Average Entry: 4196 bytes
  Oldest Entry: 2025-11-30T21:52:57.805676
  Newest Update: 2025-12-02T11:16:44.317480
```

## Available Wiki Entries

The workspace includes 18 wiki entries organized by topic:

| ID | Title | Purpose |
|---|---|---|
| 1 | Workspace Overview | System introduction |
| 2 | System Architecture | Technical design |
| 3 | Quick Start | Getting started guide |
| 4 | Idea Extraction Ready | Status tracker |
| 5 | System Readiness | Integration status |
| 6 | Extraction Workflow | Process documentation |
| 7 | Implementation Guide | Implementation details |
| 8 | Human Ai Collaboration | Collaboration framework |
| 9 | Action Plan | Strategic planning |
| 10 | Duplication Analysis | Deduplication results |
| 11 | Session Summary | Project timeline |
| 12 | Installation Guide | Setup instructions |
| 13 | Testing Framework | Quality assurance |
| 14 | Project Structure | Architecture overview |
| 15 | System Integration | Integration details |
| 16 | Code Quality | Quality standards |
| 17 | Documentation Index | Doc reference |
| 18 | Project Status | Current status |

## Use Cases

### 1. Find Information About a Topic
```bash
# Search for quality-related documentation
python3 wiki_manager.py search quality

# View the quality gate guide
python3 wiki_manager.py get "Code Quality"
```

### 2. Understand the System Architecture
```bash
# Get the full architecture documentation
python3 wiki_manager.py get "System Architecture"
```

### 3. Review Project Status
```bash
# Check current project status
python3 wiki_manager.py get "Project Status"
```

### 4. Find Implementation Details
```bash
# Search for implementation-related docs
python3 wiki_manager.py search implementation

# View the implementation guide
python3 wiki_manager.py get "Implementation Guide"
```

### 5. Monitor Wiki Growth
```bash
# See wiki statistics
python3 wiki_manager.py stats
```

## Database Details

- **Database File**: `workspace_knowledge.db`
- **Table**: `wiki`
- **Columns**: `id`, `title`, `content`, `created_at`, `updated_at`
- **Current Size**: ~74 KB
- **Total Entries**: 18

## Performance

- **List**: < 10ms
- **Search**: < 50ms (across all entries)
- **Get**: < 5ms
- **Stats**: < 10ms

All operations are read-only and non-blocking.

## Tips & Tricks

### 1. Find Recent Updates
```bash
python3 wiki_manager.py stats  # Check "Newest Update" timestamp
```

### 2. Search with Multiple Keywords
```bash
# The tool searches for entries containing any keyword
python3 wiki_manager.py search "extraction workflow"
```

### 3. Partial Title Matching
```bash
# These all work - titles are matched case-insensitively
python3 wiki_manager.py get "Quick"
python3 wiki_manager.py get "quick start"
python3 wiki_manager.py get "QUICK START"
```

### 4. Integrate with Other Tools
```bash
# Pipe to other commands
python3 wiki_manager.py get "Quick Start" | head -50

# Redirect to file
python3 wiki_manager.py get "System Architecture" > docs/architecture.md
```

## Troubleshooting

### No database found
**Error**: `sqlite3.OperationalError: unable to open database file`

**Solution**: Make sure you're running the command from the workspace root directory:
```bash
cd /media/sunil-kr/workspace/workspace-system
python3 wiki_manager.py list
```

### No results found
**If search returns nothing**:
1. Try a shorter search term
2. Check spelling
3. Use `list` command to see all available entries
4. Use partial title matching

### Entry not found
**If `get` returns "Entry not found"**:
1. Check if the title exists with `list`
2. Try a shorter or partial title
3. Check case - matching is case-insensitive

## Related Tools

- **Knowledge Base Manager** (`kb_manager.py`) - Manage knowledge base entries
- **Schema Explorer** (`schema.py`) - Explore database structure
- **Session Manager** (`session_manager.py`) - Manage workspace sessions
- **Workspace CLI** (`workspace_cli.py`) - Main workspace commands

## Integration

The wiki manager integrates seamlessly with:
- Knowledge base system
- Collaboration framework
- Documentation workflows
- Project management

## Future Enhancements

Potential features for future versions:
- Export wiki entries to Markdown files
- Import wiki entries from external sources
- Wiki entry versioning and history
- Full-text search with advanced filters
- Wiki categorization and tagging
- Auto-generated table of contents
