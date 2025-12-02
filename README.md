# Workspace Intelligence System

**Complete workspace management with prevention-first architecture**

## 🤖 AI Team

**Three AI assistants integrated into the workspace**:

- **Copilot** (GitHub) - Code generation, refactoring, tooling
- **Kiro** (AWS) - Cloud operations, reviews, quality assurance
- **Gemini** (Google) - Reasoning, multimodal understanding, problem-solving

See `AI_TEAM.md` for details on AI collaboration.

## 💬 Discussion Channels

Join the conversation! We have three complementary channels:

| Channel | Best For | How to Access |
|---------|----------|---------------|
| **Workspace Discussions** | 🤖 AI team coordination, architecture decisions | `./ws collab list-discussions` |
| **GitHub Discussions** | 💡 Feature ideas, Q&A, public visibility | [github.com/.../discussions](https://github.com/krsbox/workspace-system/discussions) |
| **GitHub Issues** | 🐛 Bug reports, feature requests, tasks | [github.com/.../issues](https://github.com/krsbox/workspace-system/issues) |

👉 **New contributor?** Start with [Discussion Guide](.github/DISCUSSION_GUIDE.md) to learn which channel to use.

---

## 🚀 Quick Start

```bash
# Initialize
./ws init your-name

# Daily workflow
./ws status      # Check dashboard
./ws todo        # See priorities
./ws check       # Run all checks
./ws maintain    # Maintenance
```

## 📦 What's Included

**11 Integrated Systems** in one unified CLI:

1. **Knowledge Base** - Searchable storage
2. **Wiki & Todos** - Documentation & tasks
3. **Proposals** - Validation workflow
4. **Collaboration** - Users, discussions, assignments
5. **Sessions** - Persistent memory
6. **Tools** - Auto-discovery & tracking
7. **Reviews** - Code & proposal quality
8. **Quality Gates** - Prevent degradation
9. **Prevention** - Lightweight checks (< 5ms)
10. **Maintenance** - Scheduled tasks
11. **Unified CLI** - Single interface

## 🎯 Key Features

### Prevention-First
- Block issues before they happen
- < 5ms overhead per request
- No expensive recovery

### Priority-Based
- 🔴 Urgent → 🟠 High → 🟡 Medium → 🟢 Low
- Auto-prioritization
- Focus on what matters

### Self-Improving
- Track performance
- Propose improvements
- Learn from failures

### Collaborative
- Role-based access
- Discussions & assignments
- Shared context

## 📊 Unified Interface

### One Command for Everything

```bash
ws status              # Dashboard
ws init <user>         # Initialize
ws propose <title>     # Quick proposal
ws todo                # List by priority
ws review <file>       # Code review
ws check               # All checks
ws maintain            # Maintenance
ws search <query>      # Search all
```

### Status Dashboard

```bash
./ws status
```

Shows:
- Complexity score
- Todos by priority
- Pending proposals
- Unresolved alerts
- Active tools
- Resource utilization

## 🔄 Integrated Workflows

### Feature Development

```bash
# 1. Propose
./ws propose "Add caching"

# 2. Implement
# ... code ...

# 3. Review
./ws review cache.py

# 4. Check quality
./ws check

# 5. Complete
python3 workspace_manager.py todo update 1 done
```

### Daily Routine

```bash
# Morning
./ws status
./ws todo

# During work
./ws check

# End of day
./ws maintain
```

## 📈 Priority System

### Auto-Prioritization

Proposals → Todos with automatic priority:
- **Critical impact** → Urgent
- **High impact** → High
- **Medium impact** → Medium
- **Low impact** → Low

### Priority View

```bash
./ws todo

# Output:
🔴 URGENT (2)
   [todo] #5: Fix security vulnerability
   [in_progress] #3: Database leak

🟠 HIGH (3)
   [todo] #7: Implement caching
   ...
```

## 🛡️ Quality & Prevention

### Automated Checks

```bash
./ws check
```

Runs:
1. Quality gate (pass/fail)
2. Prevention rules (block bad actions)
3. Proactive check (find issues)
4. System assessment (score + grade)

### Prevention Rules

- Size limits (< 1ms)
- Rate limits (< 1ms)
- Input validation (< 1ms)
- Guardrails (< 0.5ms)

**Total overhead**: < 5ms

## 🔍 Universal Search

```bash
./ws search "keyword"
```

Searches:
- Knowledge base
- Proposals
- Todos
- Wiki pages
- Discussions
- Sessions

## 📚 Documentation

- `SYSTEM_OVERVIEW.md` - Complete system guide
- `INTEGRATION_GUIDE.md` - Unified CLI & workflows
- `WORKSPACE_OVERVIEW.md` - Directory structure
- Individual guides for each system

## 🗄️ Database

**Single SQLite database**: `workspace_knowledge.db`

- 30+ tables
- Full-text search
- < 1MB size
- No server needed

## 🎓 Examples

### Initialize Workspace

```bash
./ws init alice
# ✓ User 'alice' created
# ✓ Session #1 started
# ✓ Discovered 6 tools
# ✓ Workspace ready
```

### Submit Proposal

```bash
./ws propose "Add Redis caching"
# Description: ...
# ✓ Proposal #4 submitted
# ✓ Validation: APPROVED (score: 85%)
# ✓ Converted to todo #3
```

### Check Status

```bash
./ws status
# Complexity: 31 (LOW)
# Todos: 5 total (1 urgent, 2 high)
# Proposals: 3 total (0 pending)
# Alerts: 0 unresolved
# Tools: 6 active
```

### Run Checks

```bash
./ws check
# 1. Quality Gate... ✓ PASS (3/3)
# 2. Prevention Rules... ✓ All clear
# 3. Proactive Check... ✓ All clear
# 4. System Assessment... Score: 100/100 (Grade: A)
```

## 🔧 Installation

```bash
# Make executable
chmod +x workspace_cli.py

# Create symlink
ln -s workspace_cli.py ws

# Initialize
./ws init your-name
```

## 📊 Metrics

### Current System
- **Complexity**: 31 (LOW)
- **Quality Score**: 100/100 (A)
- **Tools**: 6 active
- **Success Rate**: 100%
- **Overhead**: < 5ms

### Consolidation Benefits
- **Commands**: 11 → 1
- **Complexity**: High → Low
- **Learning curve**: Steep → Gentle
- **Efficiency**: 11 steps → 1 step

## 🎯 Best Practices

✅ Use `./ws` for everything  
✅ Check status daily  
✅ Prioritize ruthlessly  
✅ Run checks often  
✅ Search before creating  
✅ Maintain regularly  

## 🚀 Advanced Usage

### Custom Workflows

```bash
#!/bin/bash
# daily.sh

./ws status
./ws check
./ws maintain
./ws todo | grep "URGENT"
```

### Automation

```bash
# Cron
0 9 * * * cd /workspace && ./ws check

# Git hook
# .git/hooks/pre-commit
./ws check || exit 1
```

## 📈 Success Metrics

Track:
- Complexity trend
- Quality scores
- Task completion rate
- Prevention effectiveness
- Tool success rates

## 🔗 Integration

All systems share one database and work together:

```
Knowledge ←→ Proposals ←→ Todos
    ↓           ↓          ↓
Sessions ←→ Reviews ←→ Quality Gates
    ↓           ↓          ↓
Tools ←→ Prevention ←→ Maintenance
```

## 💡 Key Innovations

1. **Prevention-First** - Block issues before they happen
2. **Priority-Based** - Focus on what matters
3. **Self-Improving** - Learn and adapt
4. **Unified Interface** - One command for all
5. **Minimal Overhead** - < 5ms per request

## 🎉 Summary

Built a complete workspace intelligence system with:
- ✅ 11 integrated components
- ✅ 30+ database tables
- ✅ Prevention-first architecture
- ✅ Priority-based workflows
- ✅ Unified CLI interface
- ✅ < 5ms overhead
- ✅ Self-improving capabilities

**One command to rule them all**: `./ws`

## 📞 Quick Reference

```bash
./ws status      # Dashboard
./ws init        # Initialize
./ws propose     # Submit proposal
./ws todo        # List by priority
./ws review      # Code review
./ws check       # All checks
./ws maintain    # Maintenance
./ws search      # Search all
./ws help        # Show help
```

## 🏁 Get Started

```bash
./ws init your-name
./ws status
./ws help
```

**Welcome to your intelligent workspace!** 🚀
