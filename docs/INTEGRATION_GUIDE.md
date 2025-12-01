# Integration & Consolidation Guide

**Unified workspace management through a single CLI**

## 🎯 Philosophy

Instead of 11 separate commands, use **one unified interface**:
```bash
ws <command>
```

## 🚀 Quick Start

### Initialize Workspace
```bash
ws init alice
# Creates user, starts session, discovers tools
```

### Check Status
```bash
ws status
# Shows: complexity, todos, proposals, alerts, tools, utilization
```

### Daily Workflow
```bash
# 1. Check status
ws status

# 2. List todos by priority
ws todo

# 3. Submit proposal
ws propose "Add caching layer"

# 4. Review code
ws review my_file.py

# 5. Run checks
ws check

# 6. Search
ws search "caching"
```

## 📊 Unified Commands

### Status Dashboard
```bash
ws status
```
Shows:
- Complexity score
- Todos by priority
- Pending proposals
- Unresolved alerts
- Active tools
- High utilization resources

### Quick Propose
```bash
ws propose "Feature title"
# Interactive: asks for description
# Auto-validates
# Converts to todo if approved
```

### Todos by Priority
```bash
ws todo
```
Shows todos organized:
- 🔴 Urgent
- 🟠 High
- 🟡 Medium
- 🟢 Low

### Run All Checks
```bash
ws check
```
Runs:
1. Quality gate
2. Prevention rules
3. Proactive check
4. System assessment

### Maintenance
```bash
ws maintain
```
Runs all due maintenance tasks

### Universal Search
```bash
ws search "keyword"
```
Searches:
- Knowledge base
- Proposals
- Todos
- Wiki pages

## 🔗 System Integration

### Data Flow

```
User Input
    ↓
Workspace CLI (ws)
    ↓
┌─────────────────────────────────┐
│  Unified Interface              │
├─────────────────────────────────┤
│  • Status Dashboard             │
│  • Priority Management          │
│  • Integrated Search            │
│  • Consolidated Checks          │
└─────────────────────────────────┘
    ↓
┌─────────────────────────────────┐
│  Core Systems                   │
├─────────────────────────────────┤
│  Knowledge → Proposals → Todos  │
│  Sessions → Discussions         │
│  Tools → Reviews → Quality      │
│  Prevention → Maintenance       │
└─────────────────────────────────┘
    ↓
Single SQLite Database
```

### Integration Points

**1. Proposal → Todo Pipeline**
```bash
ws propose "Title"
# Auto: submit → validate → convert → assign
```

**2. Code → Review → Quality Gate**
```bash
ws review file.py
ws check
# Auto: review → gate → prevent → assess
```

**3. Session → State → Context**
```bash
ws init user
# Auto: session → state → bookmarks
```

## 📋 Task Priority System

### Priority Levels

1. **🔴 Urgent** - Do immediately
   - Security issues
   - Critical bugs
   - System down

2. **🟠 High** - Do today
   - Important features
   - Performance issues
   - User-facing bugs

3. **🟡 Medium** - Do this week
   - Enhancements
   - Refactoring
   - Documentation

4. **🟢 Low** - Do when possible
   - Nice-to-haves
   - Optimizations
   - Cleanup

### Auto-Priority Assignment

Proposals automatically get priority based on:
- **Impact**: critical → urgent, high → high, medium → medium, low → low
- **Validation score**: >90% → bump up one level
- **Dependencies**: blocking others → bump up

### Priority Commands

```bash
# List by priority
ws todo

# Filter by priority
python3 workspace_manager.py todo list urgent
python3 workspace_manager.py todo list high

# Update priority
python3 workspace_manager.py todo update <id> high
```

## 🔄 Consolidated Workflows

### 1. Feature Development

```bash
# Start
ws init developer
ws status

# Propose
ws propose "New feature X"
# → Auto-validates
# → Converts to todo if approved

# Implement
ws review feature.py
# → Auto code review

# Check quality
ws check
# → Quality gate
# → Prevention rules
# → Assessment

# Complete
python3 workspace_manager.py todo update 1 done
```

### 2. Bug Fix

```bash
# Urgent bug reported
python3 workspace_manager.py todo add "Fix critical bug" "Description" "urgent"

# Review fix
ws review bugfix.py

# Check
ws check

# Deploy
ws maintain
```

### 3. Maintenance

```bash
# Daily
ws status
ws check
ws maintain

# Weekly
ws search "TODO"
ws search "FIXME"
python3 maintenance_system.py complexity suggest
```

## 🎛️ Consolidation Benefits

### Before (11 commands)
```bash
python3 kb_manager.py search "query"
python3 proposal_system.py list
python3 workspace_manager.py todo list
python3 quality_gate.py gate execute "pre-commit"
python3 prevention_system.py proactive
# ... 6 more commands
```

### After (1 command)
```bash
ws status    # See everything
ws search    # Search everything
ws check     # Check everything
```

### Reduction
- **Commands**: 11 → 1
- **Complexity**: High → Low
- **Learning curve**: Steep → Gentle
- **Efficiency**: 11 steps → 1 step

## 📈 Priority-Based Execution

### Smart Task Ordering

```python
# System automatically orders by:
1. Priority (urgent > high > medium > low)
2. Dependencies (blockers first)
3. Age (older first within same priority)
4. Impact (higher impact first)
```

### Example

```bash
ws todo

# Output:
🔴 URGENT (2)
   [todo] #5: Fix security vulnerability
   [in_progress] #3: Database connection leak

🟠 HIGH (3)
   [todo] #7: Implement caching
   [todo] #4: Add API rate limiting
   [blocked] #2: Refactor auth module

🟡 MEDIUM (5)
   [todo] #8: Update documentation
   ...
```

## 🔍 Unified Search

Search across all systems with one command:

```bash
ws search "caching"

# Searches:
# - Knowledge base entries
# - Proposals (title + description)
# - Todos (title + description)
# - Wiki pages (title + content)
# - Discussions (title + comments)
# - Session messages
```

## 🛠️ Advanced Integration

### Custom Workflows

Create workflow scripts:

```bash
#!/bin/bash
# daily-workflow.sh

echo "=== Daily Workflow ==="

# 1. Status
ws status

# 2. Run checks
ws check

# 3. Maintenance
ws maintain

# 4. Review urgent todos
ws todo | grep "URGENT"

# 5. Check complexity
python3 maintenance_system.py complexity score
```

### Automation

```bash
# Cron job
0 9 * * * cd /workspace && ./daily-workflow.sh

# Git hook
# .git/hooks/pre-commit
ws check || exit 1
```

## 📊 Consolidated Metrics

### Single Dashboard

```bash
ws status
```

Shows all key metrics:
- System complexity
- Task priorities
- Quality scores
- Resource utilization
- Active alerts
- Tool health

### Trend Analysis

```python
# Track over time
- Complexity: increasing/stable/decreasing
- Quality: improving/stable/degrading
- Utilization: growing/stable/shrinking
- Productivity: todos completed per week
```

## 🎯 Focus Areas

### 1. Reduce Complexity
```bash
python3 maintenance_system.py complexity suggest
# Follow suggestions to simplify
```

### 2. Prioritize Work
```bash
ws todo
# Focus on urgent/high first
```

### 3. Maintain Quality
```bash
ws check
# Fix issues before they spread
```

### 4. Prevent Issues
```bash
# Automatic prevention rules
# Block bad changes before commit
```

## 🚀 Getting Started

### 1. Setup
```bash
chmod +x workspace_cli.py
ln -s workspace_cli.py ws
```

### 2. Initialize
```bash
ws init your-name
```

### 3. Daily Use
```bash
ws status    # Morning check
ws todo      # See priorities
ws check     # Quality check
ws maintain  # Run maintenance
```

### 4. Development
```bash
ws propose "Feature"
ws review file.py
ws check
```

## 📚 Command Reference

### Quick Commands
- `ws status` - Dashboard
- `ws init <user>` - Initialize
- `ws propose <title>` - Quick proposal
- `ws todo` - List by priority
- `ws review <file>` - Code review
- `ws check` - All checks
- `ws maintain` - Maintenance
- `ws search <query>` - Search all

### Detailed Commands
- `ws kb` - Knowledge base
- `ws wiki` - Wiki pages
- `ws proposal` - Proposals
- `ws discuss` - Discussions
- `ws session` - Sessions
- `ws tool` - Tools
- `ws quality` - Quality gates
- `ws prevent` - Prevention

## 💡 Best Practices

✅ **Use unified CLI** - `ws` instead of individual scripts  
✅ **Check status daily** - `ws status`  
✅ **Prioritize ruthlessly** - Focus on urgent/high  
✅ **Run checks often** - `ws check`  
✅ **Search before creating** - `ws search`  
✅ **Maintain regularly** - `ws maintain`  

## 🎓 Examples

### Morning Routine
```bash
ws status
ws todo
ws check
```

### Feature Development
```bash
ws propose "Feature X"
# ... implement ...
ws review feature.py
ws check
```

### Bug Fix
```bash
ws search "bug description"
# ... fix ...
ws review fix.py
ws check
```

### End of Day
```bash
ws maintain
ws status
python3 session_manager.py session end <id>
```

## 📈 Success Metrics

Track consolidation success:
- **Commands used**: Should decrease
- **Time to complete tasks**: Should decrease
- **Quality scores**: Should increase
- **Complexity**: Should stabilize
- **User satisfaction**: Should increase

## 🔗 Integration Checklist

- [x] Unified CLI (`ws`)
- [x] Status dashboard
- [x] Priority-based todos
- [x] Integrated search
- [x] Consolidated checks
- [x] Single database
- [x] Automated workflows
- [x] Documentation

## 🎯 Next Steps

1. **Use `ws` for everything**
2. **Set up daily workflow**
3. **Configure automation**
4. **Monitor metrics**
5. **Iterate and improve**
