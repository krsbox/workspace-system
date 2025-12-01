# Prevention System Guide

**Prevention is better than cure** - Lightweight proactive measures with minimal overhead.

## Philosophy

- ✅ **Prevent** issues before they happen
- ✅ **Lightweight** checks (milliseconds, not seconds)
- ✅ **Proactive** monitoring (not reactive)
- ✅ **Early warnings** (before thresholds breach)
- ✅ **Guardrails** (hard boundaries)
- ❌ **No heavy recovery** processes
- ❌ **No expensive rollbacks**

## Components

### 1. Prevention Rules (Lightweight Checks)

Fast checks that prevent bad actions.

```bash
python3 prevention_system.py rule add <name> <type> <condition> <action>

# Examples
python3 prevention_system.py rule add "file-size-limit" "size_limit" '{"max_size": 1000000}' "block_upload"
python3 prevention_system.py rule add "api-rate-limit" "rate_limit" '{"component": "api", "max_per_minute": 100}' "throttle"
python3 prevention_system.py rule add "require-tests" "validation" '{"field": "tests", "pattern": ".+"}' "reject_commit"
```

**Rule Types**:
- **size_limit**: Prevent oversized files/data
- **rate_limit**: Prevent API abuse
- **dependency_check**: Ensure dependencies exist
- **validation**: Validate input patterns

**Overhead**: Low (< 1ms per check)

### 2. Guardrails (Hard Boundaries)

Absolute limits that cannot be crossed.

```bash
python3 prevention_system.py guardrail add <name> <type> <limit> [enforcement]

# Examples
python3 prevention_system.py guardrail add "max-memory" "memory" '{"max": 1024}'
python3 prevention_system.py guardrail add "min-coverage" "coverage" '{"min": 70}'
python3 prevention_system.py guardrail add "max-complexity" "complexity" '{"max": 10}'
```

**Enforcement**:
- **hard**: Block action (default)
- **soft**: Warn but allow

### 3. Early Warnings (Before Breach)

Alert before thresholds are breached.

```bash
python3 prevention_system.py warning check <component> <metric> <current> <threshold>

# Example
python3 prevention_system.py warning check "database" "connections" 85 100
# Warns at 80%, 90%, 95% of threshold
```

**Warning Levels**:
- 80% - Info
- 90% - Warning
- 95% - Critical

### 4. Proactive Checks (Periodic)

Lightweight system health checks.

```bash
python3 prevention_system.py proactive

# Checks:
# - Unresolved alerts
# - Pending proposals
# - Failing tools
# - Old sessions
```

**Overhead**: < 10ms total

## Usage Examples

### Prevent Large File Upload

```bash
# Add rule
python3 prevention_system.py rule add "file-limit" "size_limit" '{"max_size": 5000000}' "block"

# Check before upload
python3 prevention_system.py rule check '{"size": 6000000}'
# Output: ⚠️ Prevented 1 actions: file-limit: block
```

### Prevent API Abuse

```bash
# Add rate limit
python3 prevention_system.py rule add "api-limit" "rate_limit" '{"component": "api", "max_per_minute": 60}' "throttle"

# Automatic check on each API call
# Blocks if > 60 calls/minute
```

### Enforce Code Quality

```bash
# Add guardrail
python3 prevention_system.py guardrail add "min-tests" "coverage" '{"min": 80}'

# Check before commit
python3 prevention_system.py guardrail check "coverage" 75
# Output: 🚫 1 guardrail violations: min-tests: min_violated
```

### Early Warning System

```bash
# Monitor disk space
python3 prevention_system.py warning check "disk" "usage" 82 100
# Output: ⚠️ Warning at 80%: disk.usage at 82.0% of threshold

# Take action before it fills up
cleanup_old_files()
```

## Integration

### Pre-Commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

# Check prevention rules
python3 prevention_system.py rule check '{"description": "'"$COMMIT_MSG"'"}'

if [ $? -ne 0 ]; then
    echo "❌ Prevention rule failed"
    exit 1
fi
```

### API Middleware

```python
from prevention_system import check_prevention_rules

def api_middleware(request):
    # Check rate limits
    prevented = check_prevention_rules({
        "user": request.user,
        "endpoint": request.path
    })
    
    if prevented:
        return {"error": "Rate limit exceeded"}, 429
    
    return next()
```

### File Upload

```python
from prevention_system import check_guardrails

def upload_file(file):
    # Check size guardrail
    violations = check_guardrails("file_size", file.size)
    
    if violations:
        raise ValueError(f"File too large: {file.size}")
    
    save_file(file)
```

### Monitoring Loop

```bash
# Run every 5 minutes
*/5 * * * * cd /workspace && python3 prevention_system.py proactive
```

## Prevention vs Recovery

| Aspect | Prevention | Recovery |
|--------|-----------|----------|
| **Timing** | Before issue | After issue |
| **Cost** | Low (< 1ms) | High (seconds/minutes) |
| **Impact** | None | Downtime/data loss |
| **Complexity** | Simple checks | Complex rollbacks |
| **User Experience** | Seamless | Disruptive |

## Best Practices

✅ **Add rules early** - Before problems occur  
✅ **Keep checks fast** - < 1ms per rule  
✅ **Use guardrails** - For critical limits  
✅ **Monitor warnings** - Act at 80%, not 100%  
✅ **Run proactive checks** - Every 5-10 minutes  
✅ **Review stats** - Track what's prevented  

❌ Don't add expensive checks  
❌ Don't ignore early warnings  
❌ Don't bypass guardrails  
❌ Don't wait for 100% threshold  

## Common Prevention Rules

### File Operations
```bash
# Max file size
python3 prevention_system.py rule add "file-size" "size_limit" '{"max_size": 10000000}' "block"

# Required metadata
python3 prevention_system.py rule add "file-metadata" "validation" '{"field": "metadata", "pattern": ".+"}' "reject"
```

### API Protection
```bash
# Rate limiting
python3 prevention_system.py rule add "api-rate" "rate_limit" '{"component": "api", "max_per_minute": 100}' "throttle"

# Authentication required
python3 prevention_system.py rule add "auth-required" "dependency_check" '{"requires": "auth_token"}' "reject"
```

### Code Quality
```bash
# Test coverage
python3 prevention_system.py guardrail add "coverage" "coverage" '{"min": 80}'

# Code complexity
python3 prevention_system.py guardrail add "complexity" "complexity" '{"max": 10}'

# Documentation
python3 prevention_system.py rule add "docs-required" "validation" '{"field": "docstring", "pattern": ".{50,}"}' "reject"
```

### Resource Limits
```bash
# Memory
python3 prevention_system.py guardrail add "memory" "memory" '{"max": 2048}'

# CPU
python3 prevention_system.py guardrail add "cpu" "cpu" '{"max": 80}'

# Connections
python3 prevention_system.py guardrail add "connections" "connections" '{"max": 100}'
```

## Monitoring Dashboard

```bash
# Quick status
python3 prevention_system.py stats

# Output:
# Prevention Statistics:
#   Total prevented: 156
#   Recent (7d): 23
#   Active rules: 8
#   Active guardrails: 5
#   Pending warnings: 2
```

## Python API

```python
from prevention_system import (
    check_prevention_rules,
    check_guardrails,
    check_early_warning,
    proactive_check
)

# Check rules
prevented = check_prevention_rules({"size": 5000000})
if prevented:
    raise ValueError("Action prevented")

# Check guardrails
violations = check_guardrails("memory", 2048)
if violations:
    alert_admin()

# Early warning
warning = check_early_warning("disk", "usage", 85, 100)
if warning and warning['level'] >= 90:
    cleanup_disk()

# Proactive check
issues = proactive_check()
if issues:
    notify_team(issues)
```

## Performance

All checks are designed for minimal overhead:

- **Prevention rules**: < 1ms each
- **Guardrails**: < 0.5ms each
- **Early warnings**: < 2ms each
- **Proactive check**: < 10ms total

**Total overhead per request**: < 5ms

## Benefits

🚀 **Fast** - Millisecond checks  
🛡️ **Effective** - Prevent issues before they happen  
💰 **Cheap** - No expensive recovery  
📊 **Trackable** - Know what was prevented  
🔄 **Proactive** - Find issues early  
✨ **Simple** - Easy to add rules

## Example Workflow

```bash
# 1. Add prevention rules
python3 prevention_system.py rule add "size-limit" "size_limit" '{"max_size": 1000000}' "block"

# 2. User tries to upload large file
# System checks rules automatically
prevented = check_prevention_rules({"size": 2000000})
# Result: Prevented (< 1ms)

# 3. User uploads smaller file
prevented = check_prevention_rules({"size": 500000})
# Result: Allowed (< 1ms)

# 4. Monitor stats
python3 prevention_system.py stats
# Total prevented: 1 (saved recovery time: ~30s)
```

## Recovery Avoided

By preventing issues:
- ❌ No rollbacks needed
- ❌ No data corruption
- ❌ No downtime
- ❌ No user impact
- ❌ No expensive fixes

✅ Issues never happen!
