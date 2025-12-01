# Tools System Guide

Comprehensive tool management with auto-discovery, execution tracking, reviews, and self-improvement.

## Overview

The tools system provides:
- **Auto-discovery** - Find tools automatically
- **Registry** - Central tool catalog
- **Execution tracking** - Usage stats and performance
- **Reviews** - Code and proposal quality checks
- **Self-improvement** - Propose and track enhancements
- **Health monitoring** - System health checks

## Tools Manager

### Auto-Discovery

Automatically find and register tools:

```bash
python3 tools_manager.py discover
# Discovers: *.py, *.sh files
```

### Register Tool

```bash
python3 tools_manager.py tool register <name> <type> <command> [description]

# Example
python3 tools_manager.py tool register "git-status" "shell" "git status -s" "Quick git status"
```

**Types**: python, shell, binary, script

### List Tools

```bash
python3 tools_manager.py tool list [category]

# All tools
python3 tools_manager.py tool list

# By category
python3 tools_manager.py tool list "auto-discovered"
```

### Execute Tool

```bash
python3 tools_manager.py tool execute <name> [args]

# Example
python3 tools_manager.py tool execute kb_manager "list"
```

**Tracks**:
- Success/failure
- Runtime
- Output
- Error messages

### Tool Statistics

```bash
python3 tools_manager.py tool stats <name>

# Shows:
# - Usage count
# - Success rate
# - Average runtime
# - Failure count
```

## Review Tools

### Auto Code Review

```bash
python3 review_tools.py review <file_path>

# Example
python3 review_tools.py review kb_manager.py
```

**Checks**:
- Line length (>120 chars)
- TODO/FIXME comments
- Missing docstrings
- Hardcoded credentials
- Code style issues

**Severity levels**: critical, warning, info

### Proposal Review

```bash
python3 review_tools.py proposal <proposal_id>

# Checks:
# - Title length
# - Description quality
# - Rationale strength
# - Impact/effort defined
```

### View Review

```bash
python3 review_tools.py show <review_id>
```

### Review Templates

```bash
# Create template
python3 review_tools.py template create "security" '["Check auth", "Validate input"]'

# List templates
python3 review_tools.py template list
```

## Self-Improvement

### Propose Improvement

```bash
python3 tools_manager.py improve propose <tool_name> <type> <description>

# Types: performance, feature, bugfix, security, usability

# Example
python3 tools_manager.py improve propose kb_manager "performance" "Add query caching"
```

### List Improvements

```bash
# All improvements
python3 tools_manager.py improve list

# By status
python3 tools_manager.py improve list proposed
python3 tools_manager.py improve list implemented
```

### Implement Improvement

```bash
python3 tools_manager.py improve implement <improvement_id>
```

## Health Monitoring

### Check Health

```bash
python3 tools_manager.py health status

# Shows:
# - Overall health (healthy/degraded/unhealthy)
# - Component status
# - Health percentage
```

## Integration Examples

### 1. Tool Discovery + Execution

```bash
# Discover all tools
python3 tools_manager.py discover

# Execute discovered tool
python3 tools_manager.py tool execute session_manager "session list alice"

# Check stats
python3 tools_manager.py tool stats session_manager
```

### 2. Code Review + Discussion

```bash
# Review code
python3 review_tools.py review new_feature.py

# If issues found, start discussion
python3 collab_system.py discuss start "Code review findings" "alice"
python3 collab_system.py discuss comment 1 "bob" "Found 3 security issues"
```

### 3. Proposal Review + Validation

```bash
# Submit proposal
python3 proposal_system.py submit "Add caching" "Redis caching layer" "Improve performance"

# Review quality
python3 review_tools.py proposal 1

# If approved, validate
python3 proposal_system.py validate 1

# Convert to todo
python3 proposal_system.py convert 1
```

### 4. Self-Improvement Workflow

```bash
# Tool fails frequently
python3 tools_manager.py tool stats problematic_tool
# Shows: 60% success rate

# Propose improvement
python3 tools_manager.py improve propose problematic_tool "bugfix" "Fix timeout handling"

# Implement fix
# ... make changes ...

# Mark as implemented
python3 tools_manager.py improve implement 1

# Verify improvement
python3 tools_manager.py tool stats problematic_tool
# Shows: 95% success rate
```

## Python API

### Tools Manager

```python
from tools_manager import (
    register_tool, list_tools, execute_tool,
    get_tool_stats, propose_improvement,
    discover_tools, run_health_check
)

# Register
tool_id = register_tool("my-tool", "python", "python3 my_tool.py")

# Execute
result = execute_tool("my-tool", args="--verbose")
if result['success']:
    print(result['output'])

# Stats
stats = get_tool_stats("my-tool")
print(f"Success rate: {stats['success_rate']}%")

# Discover
discovered = discover_tools()
```

### Review Tools

```python
from review_tools import (
    auto_review_code, review_proposal_quality,
    get_review, create_template
)

# Review code
review_id = auto_review_code("my_file.py")
review, comments = get_review(review_id)

# Review proposal
review_id, score = review_proposal_quality(proposal_id)
```

## Auto-Healing

The system can self-heal:

1. **Detect issues** - Health checks find problems
2. **Propose fixes** - Auto-generate improvement proposals
3. **Track implementation** - Monitor fix effectiveness
4. **Learn** - Improve detection and fixes over time

```bash
# Health check detects issue
python3 tools_manager.py health status
# Component: database - unhealthy

# System proposes fix
python3 tools_manager.py improve propose database "bugfix" "Optimize connection pool"

# Implement and verify
python3 tools_manager.py improve implement 1
python3 tools_manager.py health status
# Component: database - healthy
```

## Best Practices

✅ **Run discovery regularly** - Find new tools  
✅ **Review before merging** - Use auto-review  
✅ **Track tool performance** - Monitor stats  
✅ **Propose improvements** - Document ideas  
✅ **Health checks** - Run periodically  

## Tool Categories

- **auto-discovered**: Auto-found tools
- **core**: Essential system tools
- **review**: Code/proposal review tools
- **automation**: Workflow automation
- **monitoring**: Health and metrics
- **custom**: User-defined tools

## Metrics Tracked

Per tool:
- Usage count
- Success/failure rate
- Average runtime
- Error patterns
- Last execution time

System-wide:
- Total tools
- Active tools
- Health status
- Improvement proposals
- Review completion rate

## Future Enhancements

Proposed improvements in the system:
1. Query caching for kb_manager
2. JSON export for session_manager
3. Parallel tool execution
4. ML-based code review
5. Auto-fix suggestions
6. Performance profiling
7. Dependency tracking
8. Version management

Check improvement proposals:
```bash
python3 tools_manager.py improve list proposed
```
