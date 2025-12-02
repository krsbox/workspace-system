# Welcome to Workspace Intelligence System Wiki

**Your complete guide to the workspace management system with prevention-first architecture**

---

## 🚀 Quick Navigation

### Getting Started
- **[Quick Start](README.md)** - Get up and running in 5 minutes
- **[Installation & Setup](SETUP.md)** - Detailed installation guide
- **[First Steps](#first-steps)** - Your first commands

### Core Documentation
- **[System Overview](docs/reference/SYSTEM_OVERVIEW.md)** - Complete system architecture
- **[Architecture](ARCHITECTURE_OVERVIEW.txt)** - Technical design details
- **[Structure Guide](STRUCTURE.md)** - Directory organization

### AI Team & Collaboration
- **[AI Team](AI_TEAM.md)** - Meet Copilot, Kiro, and Gemini
- **[Discussion Guide](.github/DISCUSSION_GUIDE.md)** - 3-channel collaboration system
- **[Copilot Instructions](.github/copilot-instructions.md)** - AI agent patterns

### Developer Resources
- **[Developer Quick Reference](.github/DEVELOPER_QUICK_REFERENCE.md)** - Common patterns & workflows
- **[Testing Guide](TESTING.md)** - Test suite & quality checks
- **[Contributing](#contributing)** - How to contribute

---

## 📚 Documentation Index

### 🎯 User Guides

**Daily Workflows**
- [Proposal System](docs/PROPOSAL_SYSTEM_GUIDE.md) - Submit and validate proposals
- [Wiki Manager](WIKI_MANAGER_GUIDE.md) - Manage documentation
- [Tool Features](docs/TOOL_FEATURES_SUMMARY.md) - Available tools overview

**Collaboration**
- [Human-AI Collaboration](docs/HUMAN_AI_COLLABORATION.md) - Working with AI assistants
- [Discussion Channels](.github/DISCUSSION_GUIDE.md) - Where to ask what
- [Issue Templates](.github/ISSUE_TEMPLATE/) - Bug reports, features, tasks

### 🔧 Technical Guides

**System Components**
- [Quality Gates](docs/archived/QUALITY_GATE_GUIDE.md) - Automated quality checks
- [Prevention System](docs/archived/PREVENTION_GUIDE.md) - Block issues before they happen
- [Automation](docs/archived/AUTOMATION_GUIDE.md) - Workflow automation
- [Session Management](docs/archived/SESSION_MANAGER_GUIDE.md) - Persistent memory

**Development**
- [Integration Guide](docs/archived/INTEGRATION_GUIDE.md) - System integration
- [Implementation Guide](docs/archived/IMPLEMENTATION_GUIDE.md) - Feature implementation
- [Smart Workflow](docs/archived/SMART_WORKFLOW_GUIDE.md) - Intelligent workflows

### 📖 Reference

**Project Documentation**
- [System Readiness](docs/reference/SYSTEM_READINESS.md) - Production readiness checklist
- [Workspace Overview](docs/reference/WORKSPACE_OVERVIEW.md) - Directory structure
- [Index](INDEX.md) - Complete file index

**Analysis & Reports**
- [Analysis Report](ANALYSIS_REPORT.md) - System analysis
- [Optimization Summary](docs/OPTIMIZATION_SUMMARY.md) - Performance optimizations
- [Evolution Summary](docs/EVOLUTION_SUMMARY.md) - System evolution history

---

## 🎓 First Steps

### 1. Initialize Your Workspace

```bash
# Clone repository
git clone https://github.com/krsbox/workspace-system.git
cd workspace-system

# Initialize
./ws init your-name
```

### 2. Check Status

```bash
./ws status
```

You'll see:
- Complexity score
- Todos by priority
- Pending proposals
- Active tools
- Quality metrics

### 3. Run Quality Checks

```bash
./ws check
```

Runs:
- Quality gate (pass/fail)
- Prevention rules
- Proactive checks
- System assessment

### 4. Explore Commands

```bash
./ws help
```

Available commands:
- `status` - Dashboard
- `init` - Initialize
- `propose` - Submit proposal
- `todo` - List tasks
- `review` - Code review
- `check` - Quality checks
- `maintain` - Maintenance
- `search` - Search all

---

## 💡 Key Features

### Prevention-First Architecture
Block issues before they happen with < 5ms overhead:
- Size limits
- Rate limits
- Input validation
- Guardrails

### Priority-Based Workflows
Auto-prioritization system:
- 🔴 **Urgent** - Critical impact
- 🟠 **High** - High impact
- 🟡 **Medium** - Medium impact
- 🟢 **Low** - Low impact

### Self-Improving System
- Track performance metrics
- Propose improvements automatically
- Learn from failures
- Continuous optimization

### Unified Interface
One command for everything:
```bash
./ws <command>
```

---

## 🤖 AI Team Collaboration

### Three AI Assistants

**Copilot** (GitHub)
- Code generation & refactoring
- Pattern recognition
- Tooling & automation

**Kiro** (AWS)
- Cloud operations
- Code reviews
- Quality assurance

**Gemini** (Google)
- Complex reasoning
- Multimodal understanding
- Problem-solving

### Collaboration Channels

| Channel | Purpose | Access |
|---------|---------|--------|
| **Workspace Discussions** | AI coordination, architecture | `./ws collab list-discussions` |
| **GitHub Discussions** | Feature ideas, Q&A, public | [GitHub Discussions](https://github.com/krsbox/workspace-system/discussions) |
| **GitHub Issues** | Bug reports, tasks | [GitHub Issues](https://github.com/krsbox/workspace-system/issues) |

---

## 🔍 Common Tasks

### Submit a Proposal

```bash
./ws propose "Add caching layer"
# Follow prompts for description
# Auto-validated and converted to todo
```

### Review Code

```bash
./ws review src/my_module.py
# Get quality score, suggestions, and recommendations
```

### Search Documentation

```bash
./ws search "prevention"
# Searches knowledge base, proposals, todos, wiki, discussions
```

### Run Maintenance

```bash
./ws maintain
# Cleanup, optimization, health checks
```

---

## 📊 System Metrics

### Current Status
- **Complexity**: 31 (LOW)
- **Quality Score**: 100/100 (Grade A)
- **Active Tools**: 6
- **Success Rate**: 100%
- **Overhead**: < 5ms

### Components
- **11 Integrated Systems**
- **30+ Database Tables**
- **Single SQLite Database**
- **Unified CLI Interface**

---

## 🛠️ Development

### Project Structure

```
workspace-system/
├── src/                    # Source code
│   ├── workspace_cli.py    # Main CLI
│   ├── quality_gate.py     # Quality checks
│   ├── prevention_system.py # Prevention rules
│   └── ...
├── tests/                  # Test suite
├── docs/                   # Documentation
│   ├── guides/            # User guides
│   ├── reference/         # Technical reference
│   └── archived/          # Historical docs
├── .github/               # GitHub infrastructure
│   ├── workflows/         # GitHub Actions
│   ├── ISSUE_TEMPLATE/    # Issue templates
│   └── DISCUSSION_TEMPLATES/ # Discussion templates
└── workspace_knowledge.db # SQLite database
```

### Running Tests

```bash
# All tests
pytest

# With coverage
pytest --cov=src

# Specific test
pytest tests/test_schema.py
```

### Code Quality

```bash
# Linting
ruff check src/

# Formatting
ruff format src/

# Type checking
mypy src/
```

---

## 🤝 Contributing

### How to Contribute

1. **Start a Discussion** - Share your idea
2. **Submit Proposal** - Use `./ws propose`
3. **Create Issue** - Use GitHub issue templates
4. **Submit PR** - Follow PR template checklist

### Guidelines

- Follow existing code patterns
- Add tests for new features
- Update documentation
- Run quality checks before PR
- Use semantic commit messages

### Code Review Process

1. Automated checks (GitHub Actions)
2. AI review (Kiro)
3. Human review (maintainers)
4. Merge to main

---

## 📞 Quick Reference

### Essential Commands

```bash
./ws status      # Dashboard
./ws init        # Initialize
./ws propose     # Submit proposal
./ws todo        # List tasks
./ws review      # Code review
./ws check       # Quality checks
./ws maintain    # Maintenance
./ws search      # Search all
./ws help        # Show help
```

### File Locations

- **Database**: `workspace_knowledge.db`
- **CLI**: `src/workspace_cli.py`
- **Config**: `pyproject.toml`
- **Tests**: `tests/`
- **Docs**: `docs/`

### Important Links

- [GitHub Repository](https://github.com/krsbox/workspace-system)
- [GitHub Discussions](https://github.com/krsbox/workspace-system/discussions)
- [GitHub Issues](https://github.com/krsbox/workspace-system/issues)
- [Latest Release](https://github.com/krsbox/workspace-system/releases)

---

## 🎯 Best Practices

✅ **Use `./ws` for everything** - Single unified interface  
✅ **Check status daily** - Stay informed  
✅ **Prioritize ruthlessly** - Focus on what matters  
✅ **Run checks often** - Catch issues early  
✅ **Search before creating** - Avoid duplication  
✅ **Maintain regularly** - Keep system healthy  

---

## 📈 Success Metrics

### Track Your Progress

- Complexity trend (aim for LOW)
- Quality scores (aim for A grade)
- Task completion rate
- Prevention effectiveness
- Tool success rates

### View Metrics

```bash
./ws status        # Current snapshot
./ws check         # Quality assessment
./ws maintain      # Health report
```

---

## 🔗 Related Resources

### External Documentation
- [Python Best Practices](https://docs.python-guide.org/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [GitHub Actions Guide](https://docs.github.com/en/actions)

### Community
- [GitHub Discussions](https://github.com/krsbox/workspace-system/discussions) - Ask questions
- [GitHub Issues](https://github.com/krsbox/workspace-system/issues) - Report bugs
- [AI Team Guide](AI_TEAM.md) - AI collaboration

---

## 💬 Need Help?

### Where to Ask

**Quick Questions**: [GitHub Discussions Q&A](https://github.com/krsbox/workspace-system/discussions/categories/q-a)  
**Feature Ideas**: [GitHub Discussions Ideas](https://github.com/krsbox/workspace-system/discussions/categories/ideas)  
**Bug Reports**: [GitHub Issues](https://github.com/krsbox/workspace-system/issues/new?template=bug_report.yml)  
**AI Coordination**: `./ws collab create-discussion`

### Documentation Issues

Found a problem in the docs? [Open a documentation issue](https://github.com/krsbox/workspace-system/issues/new?template=docs_improvement.yml)

---

**Welcome to your intelligent workspace!** 🚀

*Last updated: December 2, 2025*
