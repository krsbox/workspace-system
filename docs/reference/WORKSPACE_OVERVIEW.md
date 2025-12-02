# Workspace Overview

**Location:** `/media/sunil-kr/workspace/projects`  
**Last Updated:** 2025-11-30

## Directory Structure

```
/media/sunil-kr/workspace/projects/
├── project/              # Active consolidated project
├── projects-old/         # Archive of 22+ old projects
├── artifacts/            # Saved artifacts and demos
└── my-project.code-workspace
```

## Active Project: `project/`

**Type:** Python development workflow intelligence/automation project  
**Status:** Active development (merge in progress)  
**Package Manager:** uv  

### Key Components

- **packages/** - Multiple devflow packages:
  - devflow-wiki
  - devflow-intelligence
  - devflow-shared-tools
  - devflow-tracker

- **scripts/** - Automation scripts:
  - review_analyzer.py
  - version_manager.py
  - consolidation_manager.py
  - workflow_automation.py
  - knowledge_db.py
  - And 20+ more

- **docs/** - Comprehensive documentation:
  - Architectural improvements
  - Workspace structure
  - Git workflow guides
  - Refactoring guides

- **data/** - Knowledge bases and reports:
  - system_catalog.json
  - knowledge.db
  - review reports
  - dashboards

- **tests/** - Test suite
- **.github/** - GitHub workflows, issue templates, PR templates
- **.gemini/** - Gemini AI chat logs
- **.amazonq/** - Amazon Q rules and CLI todo lists

### Notable Features

- Git repository with active merge
- Pre-commit hooks
- Docker support
- Makefile for automation
- Shell scripts for preview, nightly, and latest builds
- Extensive tooling (code review toolkit)

## Archive: `projects-old/`

Contains 22+ archived projects that were consolidated into the current `project/`:

### Major Archived Projects

1. **ai-orchestra** (2 versions) - AI provider orchestration system
2. **coding-tools-wrapper** (2 versions) - Node.js coding tools
3. **my-project** (2 versions) - Workflow automation with AI
4. **unified-devflow** (2 versions) - Unified development workflow
5. **unified-project** (2 versions) - Consolidated project attempts
6. **devflow-ecosystem** (2 versions) - TypeScript/Node.js ecosystem
7. **devflow-complete** (2 versions) - Complete devflow implementation
8. **coding-agent** - AI coding agent with Gemini integration
9. **dev-refactor** (3 versions) - Refactoring tools
10. **new_project** - Generic project template
11. **fast-review-tool** - Fast code review tool
12. **todo-automator** - TODO automation system

### Characteristics of Old Projects

- Multiple duplicates (versions with "(2)" suffix)
- Mix of Node.js/TypeScript and Python
- Fragmented functionality
- Shell script heavy
- Less organized structure

## Artifacts: `artifacts/`

- **Codemap HTML** - Saved webpage about Progressive Build Methodology
- **ssh** - SSH key file
- **python-demo/** - Python demo project with uv

## Evolution

The current `project/` appears to be the result of consolidating functionality from multiple projects in `projects-old/`, creating a unified Python-based development workflow intelligence system with better organization and modern tooling.

## Key Differences: Old vs Current

| Aspect | projects-old | project (current) |
|--------|-------------|-------------------|
| Language | Mixed (Node.js, Python, Shell) | Python-focused |
| Organization | Fragmented, duplicated | Unified, well-structured |
| Package Management | npm, yarn, pip | uv |
| Structure | Flat, scattered | Modular (packages/) |
| Documentation | Scattered | Comprehensive (docs/) |
| Tooling | Basic | Advanced (pre-commit, CI/CD) |
| Status | Archived | Active development |
