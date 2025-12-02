# Quality Gate Guide

Prevent system degradation with assessments, quality gates, and automated monitoring.

## Overview

Quality gates ensure:
- **No degradation** - Metrics stay above thresholds
- **Consistent quality** - Code and proposals meet standards
- **Early detection** - Catch issues before they spread
- **Automated enforcement** - Gates block bad changes
- **Continuous improvement** - Track trends over time

## Quality Metrics

### Record Metric

```bash
python3 quality_gate.py metric <component> <name> <value> <threshold>

# Examples
python3 quality_gate.py metric "api" "response_time" 0.5 1.0
python3 quality_gate.py metric "database" "query_time" 0.1 0.5
python3 quality_gate.py metric "cache" "hit_rate" 95 80
```

**Automatic**:
- Tracks trends (improving/stable/degrading)
- Alerts on degradation
- Pass/fail status

### Common Metrics

**Performance**:
- response_time (seconds)
- throughput (requests/sec)
- memory_usage (MB)
- cpu_usage (%)

**Quality**:
- success_rate (%)
- error_rate (%)
- test_coverage (%)
- code_quality_score (0-100)

**Reliability**:
- uptime (%)
- availability (%)
- failure_rate (%)

## Quality Gates

### Create Gate

```bash
python3 quality_gate.py gate create <name> '<rules_json>'

# Example: Pre-commit gate
python3 quality_gate.py gate create "pre-commit" '[
  {"type": "metric", "component": "code", "metric": "test_coverage", "threshold": 80},
  {"type": "tool_success_rate", "tool": "linter", "min_rate": 95},
  {"type": "review_score", "min_score": 70}
]'
```

**Rule Types**:

1. **metric** - Check component metric
   ```json
   {"type": "metric", "component": "api", "metric": "response_time", "threshold": 1.0}
   ```

2. **tool_success_rate** - Check tool reliability
   ```json
   {"type": "tool_success_rate", "tool": "kb_manager", "min_rate": 90}
   ```

3. **review_score** - Check review quality
   ```json
   {"type": "review_score", "min_score": 75}
   ```

### Execute Gate

```bash
python3 quality_gate.py gate execute <name>

# Example
python3 quality_gate.py gate execute "pre-commit"
# Output: ✓ PASS or ✗ FAIL
```

**Returns**:
- Status (pass/fail)
- Passed/failed rule counts
- Details for each rule

### List Gates

```bash
python3 quality_gate.py gate list
# Shows: 🟢 enabled, ⚫ disabled
```

## Assessments

Comprehensive quality evaluation.

### Run Assessment

```bash
python3 quality_gate.py assess <type> <target>

# System assessment
python3 quality_gate.py assess system "workspace"

# Tool assessment
python3 quality_gate.py assess tool "kb_manager"
```

**Assessment Types**:
- **system**: Overall system health
- **tool**: Individual tool quality
- **component**: Specific component
- **project**: Project quality

**Output**:
- Score (0-100)
- Grade (A-F)
- Findings (issues found)
- Recommendations (how to improve)

### Grading Scale

- **A (90-100)**: Excellent
- **B (80-89)**: Good
- **C (70-79)**: Acceptable
- **D (60-69)**: Needs improvement
- **F (<60)**: Failing

## Degradation Detection

### Automatic Alerts

System automatically detects:
- Metrics falling below thresholds
- Degrading trends (values decreasing over time)
- Tool failure rate increases
- Review score drops

### View Alerts

```bash
# Active alerts
python3 quality_gate.py alerts

# Resolved alerts
python3 quality_gate.py alerts resolved
```

**Severity**:
- 🔴 **Critical**: Value < 50% of threshold
- 🟡 **Warning**: Value below threshold but > 50%

### Resolve Alert

```python
from quality_gate import resolve_alert
resolve_alert(alert_id)
```

## Integration Examples

### 1. Pre-Commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

# Run quality gate
python3 quality_gate.py gate execute "pre-commit"

if [ $? -ne 0 ]; then
    echo "❌ Quality gate failed. Commit blocked."
    exit 1
fi

echo "✅ Quality gate passed"
```

### 2. CI/CD Pipeline

```yaml
# .github/workflows/quality.yml
- name: Quality Gate
  run: |
    python3 quality_gate.py gate execute "deployment"
    if [ $? -ne 0 ]; then
      echo "Deployment blocked by quality gate"
      exit 1
    fi
```

### 3. Continuous Monitoring

```bash
# Monitor metrics every hour
*/60 * * * * cd /workspace && python3 quality_gate.py metric "api" "response_time" $(get_response_time) 1.0
```

### 4. Assessment Reports

```bash
# Daily assessment
0 9 * * * cd /workspace && python3 quality_gate.py assess system "workspace" > daily_report.txt
```

## Standard Gates

### Pre-Commit Gate

Runs before code commit:
- Test coverage ≥ 80%
- Linter success ≥ 95%
- Review score ≥ 70

### Deployment Gate

Runs before deployment:
- All tests passing
- No critical security issues
- Performance metrics within limits
- Tool success rate ≥ 95%

### Merge Gate

Runs before PR merge:
- Code review approved
- All checks passing
- No degradation alerts
- Documentation updated

## Python API

```python
from quality_gate import (
    record_metric, get_metric_trend,
    create_gate, execute_gate,
    run_assessment, get_alerts
)

# Record metric
record_metric("api", "response_time", 0.5, 1.0)

# Check trend
trend = get_metric_trend("api", "response_time")
if trend == "degrading":
    alert_team()

# Execute gate
result = execute_gate("pre-commit")
if result['status'] == "fail":
    block_commit()

# Run assessment
assessment = run_assessment("system", "workspace")
if assessment['grade'] in ['D', 'F']:
    trigger_review()

# Check alerts
alerts = get_alerts(resolved=False)
if len(alerts) > 0:
    notify_maintainers()
```

## Best Practices

✅ **Define clear thresholds** - Based on requirements  
✅ **Monitor trends** - Not just current values  
✅ **Automate gates** - In CI/CD and hooks  
✅ **Regular assessments** - Weekly or daily  
✅ **Act on alerts** - Don't ignore warnings  
✅ **Review and adjust** - Thresholds may need tuning  

❌ Don't set unrealistic thresholds  
❌ Don't ignore degradation trends  
❌ Don't bypass gates without review  
❌ Don't let alerts pile up  

## Metrics to Track

### Code Quality
- Test coverage
- Code complexity
- Duplication
- Documentation coverage

### Performance
- Response time
- Throughput
- Memory usage
- CPU usage

### Reliability
- Success rate
- Error rate
- Uptime
- MTBF (Mean Time Between Failures)

### Security
- Vulnerability count
- Security score
- Dependency issues
- Credential leaks

## Example Workflow

```bash
# 1. Developer makes changes
git add .

# 2. Pre-commit gate runs
python3 quality_gate.py gate execute "pre-commit"
# ✓ PASS

# 3. Commit allowed
git commit -m "Add feature"

# 4. CI runs deployment gate
python3 quality_gate.py gate execute "deployment"
# ✗ FAIL - Performance degraded

# 5. Fix issues
optimize_code()

# 6. Record new metrics
python3 quality_gate.py metric "api" "response_time" 0.3 1.0

# 7. Re-run gate
python3 quality_gate.py gate execute "deployment"
# ✓ PASS

# 8. Deploy
deploy_to_production()

# 9. Monitor
python3 quality_gate.py assess system "production"
# Score: 95/100 (Grade: A)
```

## Preventing Degradation

1. **Set baselines** - Record current metrics
2. **Define gates** - Create quality rules
3. **Automate checks** - Run gates automatically
4. **Monitor trends** - Watch for degradation
5. **Alert early** - Catch issues before they spread
6. **Fix quickly** - Address alerts promptly
7. **Assess regularly** - Weekly system assessments
8. **Improve continuously** - Raise thresholds over time

## Dashboard View

```bash
# Quick health check
python3 quality_gate.py assess system "workspace"

# Output:
# Score: 95/100 (Grade: A)
# 
# Findings:
#   • All metrics within thresholds
#   • No degradation alerts
#   • Tool success rate: 98%
# 
# Recommendations:
#   → Continue current practices
```

## Benefits

🛡️ **Prevent degradation** - Catch issues early  
📊 **Track quality** - Metrics over time  
🚫 **Block bad changes** - Automated gates  
🔍 **Early detection** - Trends and alerts  
📈 **Continuous improvement** - Raise standards  
🤖 **Automated enforcement** - No manual checks
