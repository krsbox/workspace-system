# Tool Management Guide

**Complete tool management with discussions, administration, and helpers**

## 🚀 Quick Start

```bash
# Check tool health
./ws summary
python3 tool_cli.py health

# List all tools
python3 tool_cli.py list

# Get tool stats
python3 tool_cli.py stats <tool-name>
```

## 📋 Features Added

### 1. Discussion Support for Reviews

Add threaded discussions to any review:

```bash
# Add discussion comment
python3 tool_cli.py discuss add <review_id> <type> <user> <message>

# Example
python3 tool_cli.py discuss add 1 code_review alice "Needs more tests"

# List discussions
python3 tool_cli.py discuss list 1 code_review

# Resolve discussion
python3 tool_cli.py discuss resolve 1
```

**Via unified CLI:**
```bash
./ws discuss add 1 code_review alice "Great work!"
./ws discuss list 1 code_review
./ws discuss resolve 1
```

### 2. Tool Administration

Admin actions with full audit logging:

```bash
# Disable tool
python3 tool_cli.py admin disable <admin_user> <tool_id> <reason>

# Example
python3 tool_cli.py admin disable admin 1 "Security issue"

# Enable tool
python3 tool_cli.py admin enable admin 1

# Reset tool statistics
python3 tool_cli.py admin reset admin 1

# View admin logs
python3 tool_cli.py admin logs
```

**Via unified CLI:**
```bash
./ws admin disable admin 1 "Needs update"
./ws admin enable admin 1
./ws admin reset admin 1
./ws admin logs
```

### 3. Helper Utilities

Quick summaries and health checks:

```bash
# System summary
./ws summary

# Tool health
python3 tool_cli.py health

# Review summary
# (included in ws summary)
```

## 📊 Database Schema

### New Tables

**review_discussions**
- Threaded discussions on reviews
- Support for replies (parent_id)
- Resolved status tracking

**tool_admin_logs**
- Audit trail for admin actions
- Track who did what and when
- Includes reason/details

## 🔧 Integration

All features integrate with existing systems:

```
Tools Manager ←→ Tool Helpers
      ↓              ↓
Review Tools ←→ Discussions
      ↓              ↓
Quality Gate ←→ Admin Logs
```

## 💡 Use Cases

### Code Review Discussion

```bash
# Start review
./ws review myfile.py

# Add discussion
./ws discuss add 1 code_review alice "Line 42 needs refactoring"

# Reply to discussion
./ws discuss add 1 code_review bob "Agreed, will fix"

# Resolve when done
./ws discuss resolve 1
```

### Tool Administration

```bash
# Disable problematic tool
./ws admin disable admin 3 "Causing errors"

# Check logs
./ws admin logs

# Re-enable after fix
./ws admin enable admin 3
```

### Health Monitoring

```bash
# Daily check
./ws summary

# Output:
# Tools: {5: 'active', 1: 'disabled'}
# Avg Success Rate: 98.5%
# Reviews: {3: 'approved', 1: 'pending'}
# Avg Score: 92.0
```

## 🎯 Best Practices

✅ Add discussions to reviews for collaboration  
✅ Use admin logs to track changes  
✅ Check tool health regularly  
✅ Resolve discussions when addressed  
✅ Document reasons for admin actions  

## 📈 Metrics

Track:
- Discussion resolution rate
- Admin action frequency
- Tool health trends
- Review collaboration level

## 🔗 Related Systems

- **tools_manager.py** - Core tool management
- **review_tools.py** - Code/proposal reviews
- **tool_helpers.py** - Discussions & admin
- **workspace_cli.py** - Unified interface
- **tool_cli.py** - Dedicated tool CLI

## 🎉 Summary

Added comprehensive tool management:
- ✅ Discussion support for reviews
- ✅ Tool administration with audit logs
- ✅ Health summaries and utilities
- ✅ Integrated with unified CLI
- ✅ Dedicated tool CLI
- ✅ Full database schema

**Three ways to manage tools:**
1. `./ws` - Unified interface
2. `python3 tool_cli.py` - Dedicated CLI
3. Direct Python imports

Choose what works best for your workflow! 🚀
