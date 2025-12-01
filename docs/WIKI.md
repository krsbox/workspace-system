# Workspace Intelligence Wiki

**Essential knowledge base for the workspace system**

---

## 🏗️ System Architecture

### Core Components
1. **Knowledge Base** (`kb_manager.py`) - Searchable storage
2. **Workspace Manager** (`workspace_manager.py`) - Wiki, todos, progress
3. **Proposal System** (`proposal_system.py`) - Validation workflow
4. **Tools Manager** (`tools_manager.py`) - Auto-discovery & tracking
5. **Quality Gate** (`quality_gate.py`) - Quality enforcement
6. **Prevention System** (`prevention_system.py`) - Proactive checks
7. **Automation** (`automation_manager.py`, `task_automator.py`) - Self-managing
8. **Health Monitor** (`health_monitor.py`) - Continuous tracking
9. **Optimization** (`optimization_analyzer.py`) - Code improvement

### Database
- **Single SQLite**: `workspace_knowledge.db`
- **30+ Tables**: All systems share one database
- **Size**: ~270 KB
- **FTS5**: Full-text search enabled

---

## 🎯 Key Concepts

### Prevention-First Architecture
Block issues before they happen (<5ms overhead):
- Size limits, rate limits, input validation
- Guardrails for resource usage
- Early warnings at 80/90/95% thresholds

### Priority-Based Workflows
- 🔴 Urgent → 🟠 High → 🟡 Medium → 🟢 Low
- Auto-prioritization based on impact
- Focus on what matters most

### Self-Improving System
- Tracks performance metrics
- Proposes improvements automatically
- Learns from failures

---

## 📊 Data Flow

```
Proposal → Validation → Todo → Implementation → Review → Quality Gate
    ↓          ↓          ↓          ↓             ↓           ↓
Knowledge ← Sessions ← Tools ← Prevention ← Health ← Optimization
```

---

## 🔧 Common Tasks

### Add Knowledge
```bash
python3 kb_manager.py add "Title" "Content" "tags"
./ws search "query"
```

### Create Proposal
```bash
./ws propose "Add feature X"
# Auto-validates, converts to todo if approved
```

### Check System Health
```bash
./ws status    # Dashboard
./ws health    # Health check
./ws check     # All quality checks
```

### Automation
```bash
./ws backup    # Manual backup
./ws tasks     # List automated tasks
./ws improve   # What needs work
./ws optimize  # Find duplications
```

---

## 🎓 Best Practices

### DO
✅ Use `./ws` for everything  
✅ Check status daily  
✅ Run checks before commits  
✅ Search before creating  
✅ Prioritize ruthlessly  

### DON'T
❌ Bypass quality gates  
❌ Ignore prevention warnings  
❌ Skip backups  
❌ Create duplicate entries  

---

## 🔍 Troubleshooting

### Database locked
```bash
# Check for open connections
lsof workspace_knowledge.db
# Restart if needed
```

### Tool not found
```bash
python3 tools_manager.py discover
```

### Quality gate failing
```bash
./ws check  # See what's failing
# Fix issues, then retry
```

---

## 📈 Metrics

### Current System
- Complexity: 31 (LOW)
- Quality: Grade A (100/100)
- Tools: 9 active
- Success Rate: 100%

### Targets
- Complexity: <25 (VERY LOW)
- Quality: Grade A
- Tool Success: >95%
- Response Time: <100ms

---

## 🚀 Idea Extraction Ready

### Prerequisites
✅ All core systems operational  
✅ Database initialized (30+ tables)  
✅ Tools discovered (9 tools)  
✅ Documentation complete  
✅ CLI unified (12 commands)  
✅ Automation active (5 tasks)  
✅ Health monitoring enabled  

### Extraction Capabilities
- Scan project directories
- Extract TODO/FIXME comments
- Parse README files
- Catalog ideas by category
- Prioritize automatically
- Convert to proposals/todos

### Usage
```bash
python3 idea_extractor.py scan /path/to/project
python3 idea_extractor.py list
```

---

## 📝 Quick Reference

### Database Tables
- `knowledge` - Knowledge entries
- `wiki` - Wiki pages
- `todos` - Tasks by priority
- `proposals` - Proposals & reviews
- `tools` - Discovered tools
- `sessions` - Conversation history
- `quality_gates` - Quality rules
- `prevention_rules` - Prevention checks
- `health_checks` - Health history
- `optimizations` - Code improvements
- `ideas` - Extracted ideas

### File Structure
```
workspace_knowledge.db    - Single database
*.py                      - 17 Python modules
*.md                      - 10+ documentation files
ws                        - Unified CLI symlink
backups/                  - Automated backups
```

---

**Last Updated**: 2025-12-01  
**Status**: ✅ Production Ready
