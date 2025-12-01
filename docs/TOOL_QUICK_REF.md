# Tool Management Quick Reference

## 🚀 Commands

### Discussion Support
```bash
# Add discussion to review
./ws discuss add <review_id> <type> <user> <message>
./tool discuss add 1 code_review alice "Needs tests"

# List discussions
./ws discuss list <review_id> <type>
./tool discuss list 1 code_review

# Resolve discussion
./ws discuss resolve <id>
./tool discuss resolve 1
```

### Tool Administration
```bash
# Disable tool
./ws admin disable <user> <tool_id> <reason>
./tool admin disable admin 3 "Security issue"

# Enable tool
./ws admin enable <user> <tool_id>
./tool admin enable admin 3

# Reset statistics
./ws admin reset <user> <tool_id>
./tool admin reset admin 3

# View audit logs
./ws admin logs
./tool admin logs
```

### Health & Monitoring
```bash
# System summary
./ws summary

# Tool health
./tool health

# Tool statistics
./tool stats <name>

# List tools
./tool list [category]
```

## 📊 Example Workflow

### Code Review with Discussion
```bash
# 1. Start review
./ws review myfile.py

# 2. Team discusses
./ws discuss add 1 code_review alice "Line 42 needs refactoring"
./ws discuss add 1 code_review bob "Agreed, will fix"

# 3. Check discussions
./ws discuss list 1 code_review

# 4. Resolve when done
./ws discuss resolve 1
```

### Tool Management
```bash
# 1. Check health
./tool health

# 2. Disable problematic tool
./ws admin disable admin 3 "Causing errors"

# 3. Check logs
./ws admin logs

# 4. Re-enable after fix
./ws admin enable admin 3

# 5. Verify
./tool stats tool_name
```

## 🎯 Two Ways to Access

**Unified CLI** (`./ws`)
- Part of complete workspace system
- Integrated with all features
- Use for general workflow

**Tool CLI** (`./tool`)
- Dedicated tool management
- More detailed tool operations
- Use for tool-specific tasks

Both work identically for tool commands!

## 📁 Files

- `tool_helpers.py` - Core functions
- `tool_cli.py` - Dedicated CLI
- `workspace_cli.py` - Unified CLI
- `TOOL_MANAGEMENT_GUIDE.md` - Full guide
- `TOOL_FEATURES_SUMMARY.md` - Implementation details

## ✨ Key Features

✅ Threaded discussions on reviews  
✅ Full admin audit trail  
✅ Tool health monitoring  
✅ Dual CLI interface  
✅ Complete integration  

Ready to use! 🚀
