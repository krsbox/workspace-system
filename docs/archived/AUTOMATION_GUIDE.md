# Automation Guide

**Automated review, study, and reporting system**

## 🎯 Overview

The automation manager automatically:
- **Reviews** system state
- **Studies** trends and patterns
- **Concludes** with recommendations
- **Reports** findings
- **Schedules** recurring tasks

## 🚀 Quick Start

### Generate Report

```bash
# Daily report
python3 automation_manager.py report daily

# Weekly report
python3 automation_manager.py report weekly

# Monthly report
python3 automation_manager.py report monthly
```

### Quick Health Check

```bash
python3 automation_manager.py health

# Output:
# ✓ Database        260.0 KB
# ✓ Tools           6 active
# ✓ Quality         A grade
# ✓ Prevention      3 rules
```

### Setup Automation

```bash
chmod +x setup_automation.sh
./setup_automation.sh

# Installs cron jobs for:
# - Daily reports (9 AM)
# - Weekly reports (Monday 9 AM)
# - Monthly reports (1st 9 AM)
# - Hourly health checks
# - 6-hour maintenance
# - 4-hour proactive checks
```

## 📊 Automated Report

### What It Includes

**1. System Review**
- Current metrics (complexity, quality, tools, todos, alerts)
- Achievements (positive outcomes)
- Issues (items needing attention)

**2. Trend Analysis**
- Complexity trend (increasing/stable/decreasing)
- Quality trend (improving/stable/degrading)
- Usage patterns
- Insights and observations

**3. Conclusions & Recommendations**
- Overall status (excellent/healthy/needs_attention/critical)
- Key findings
- Specific recommendations
- Actionable items

### Example Report

```
======================================================================
AUTOMATED SYSTEM REPORT - DAILY
Generated: 2025-11-30 23:45:58
======================================================================

📊 SYSTEM REVIEW
----------------------------------------------------------------------

Metrics:
  • Complexity: 31
  • Quality Score: 100
  • Quality Grade: A
  • Tools Active: 6
  • Tool Success Rate: 100.0%
  • Todos Total: 2
  • Todos Urgent: 0
  • Alerts Unresolved: 0
  • Prevention Total: 2

✅ Achievements:
  • Maintained low complexity: 31
  • High quality maintained: A
  • High tool success rate: 100.0%
  • Prevented 2 issues this week

======================================================================
🔍 TREND ANALYSIS
----------------------------------------------------------------------

Trends:
  ➡️ Quality: stable

Patterns:
  • Most used tools: 1 tools account for majority of usage

======================================================================
🎯 CONCLUSIONS & RECOMMENDATIONS
----------------------------------------------------------------------

Overall Status: 🟢 EXCELLENT

Key Findings:
  • Achievements: 4 positive outcomes

Recommendations:
  1. Continue current practices

Action Items:
  1. Run: ./ws maintain

======================================================================
```

## 🔄 Automated Tasks

### Daily Tasks

**9:00 AM** - Daily Report
- System review
- Trend analysis
- Recommendations

**Every Hour** - Health Check
- Database status
- Tool availability
- Quality check
- Prevention status

**Every 4 Hours** - Proactive Check
- Find potential issues
- Early warnings
- Preventive measures

**Every 6 Hours** - Maintenance
- Run scheduled tasks
- Cleanup old data
- Optimize database

### Weekly Tasks

**Monday 9:00 AM** - Weekly Report
- Week-over-week comparison
- Trend analysis
- Performance review
- Recommendations

### Monthly Tasks

**1st 9:00 AM** - Monthly Report
- Month-over-month comparison
- Long-term trends
- Strategic recommendations
- Planning insights

## 🛠️ Components

### Auto Review

Automatically reviews:
- Complexity score
- Quality assessment
- Tool performance
- Todo status
- Alert count
- Prevention effectiveness

```bash
python3 automation_manager.py review
```

### Auto Study

Analyzes trends:
- Complexity trend
- Quality trend
- Usage patterns
- Completion rates

```bash
python3 automation_manager.py study
```

### Auto Conclude

Draws conclusions:
- Overall status
- Key findings
- Recommendations
- Action items

```bash
python3 automation_manager.py conclude
```

## 📈 Status Levels

### 🟢 Excellent
- No issues
- Quality score ≥ 90
- All systems healthy

### 🟢 Healthy
- ≤ 2 issues
- Quality score ≥ 80
- Minor attention needed

### 🟡 Needs Attention
- 3-5 issues
- Quality score ≥ 70
- Action required

### 🔴 Critical
- > 5 issues
- Quality score < 70
- Immediate action required

## 🔧 Setup

### Manual Setup

```bash
# 1. Make executable
chmod +x automation_manager.py
chmod +x setup_automation.sh

# 2. Run setup
./setup_automation.sh

# 3. Test
python3 automation_manager.py health
python3 automation_manager.py report daily
```

### Cron Jobs

```bash
# Edit crontab
crontab -e

# Add jobs:
0 9 * * * cd /workspace && python3 automation_manager.py report daily
0 9 * * 1 cd /workspace && python3 automation_manager.py report weekly
0 9 1 * * cd /workspace && python3 automation_manager.py report monthly
0 * * * * cd /workspace && python3 automation_manager.py health
0 */6 * * * cd /workspace && python3 maintenance_system.py task run
0 */4 * * * cd /workspace && python3 prevention_system.py proactive
```

### View Logs

```bash
# Automation logs
tail -f automation.log

# Health logs
tail -f health.log

# Maintenance logs
tail -f maintenance.log

# Prevention logs
tail -f prevention.log
```

## 📊 Metrics Tracked

### System Metrics
- Complexity score
- Quality score & grade
- Tool count & success rate
- Todo count & urgency
- Alert count
- Prevention effectiveness

### Trend Metrics
- Complexity trend
- Quality trend
- Usage patterns
- Completion rates

### Performance Metrics
- Database size
- Response times
- Resource utilization
- Success rates

## 🎯 Use Cases

### Daily Standup

```bash
# Morning routine
python3 automation_manager.py report daily

# Review:
# - What was achieved yesterday
# - What needs attention today
# - Any blockers or issues
```

### Weekly Review

```bash
# Monday morning
python3 automation_manager.py report weekly

# Review:
# - Week's progress
# - Trends and patterns
# - Adjust priorities
```

### Monthly Planning

```bash
# Start of month
python3 automation_manager.py report monthly

# Review:
# - Month's achievements
# - Long-term trends
# - Strategic planning
```

### Continuous Monitoring

```bash
# Automated via cron
# - Hourly health checks
# - 4-hour proactive checks
# - 6-hour maintenance

# View status anytime:
python3 automation_manager.py health
```

## 🔍 Troubleshooting

### No Reports Generated

```bash
# Check if automation is scheduled
python3 automation_manager.py schedule

# Check cron jobs
crontab -l | grep automation

# Check logs
tail -f automation.log
```

### Health Check Fails

```bash
# Check database
ls -lh workspace_knowledge.db

# Check permissions
chmod 644 workspace_knowledge.db

# Reinitialize if needed
python3 automation_manager.py health
```

### Reports Not Actionable

```bash
# Ensure all systems are initialized
./ws init your-name

# Run manual checks
./ws check
./ws status

# Generate fresh report
python3 automation_manager.py report daily
```

## 💡 Best Practices

✅ **Review daily reports** - Start day with automated report  
✅ **Act on recommendations** - Don't ignore action items  
✅ **Monitor trends** - Watch for degradation  
✅ **Keep logs** - Rotate but keep history  
✅ **Adjust schedules** - Tune frequency as needed  

## 🚀 Advanced Usage

### Custom Reports

```python
from automation_manager import auto_review, auto_study, auto_conclude

# Custom analysis
review = auto_review()
study = auto_study()
conclusion = auto_conclude(review, study)

# Custom formatting
print(f"Status: {conclusion['overall_status']}")
for rec in conclusion['recommendations']:
    print(f"→ {rec}")
```

### Integration with Notifications

```bash
# Email daily report
python3 automation_manager.py report daily | mail -s "Daily Report" you@example.com

# Slack notification
python3 automation_manager.py health | slack-cli send "#workspace"

# Discord webhook
curl -X POST webhook-url -d "$(python3 automation_manager.py health)"
```

### Custom Schedules

```bash
# Every 2 hours
0 */2 * * * cd /workspace && python3 automation_manager.py health

# Business hours only (9 AM - 5 PM)
0 9-17 * * * cd /workspace && python3 automation_manager.py health

# Weekdays only
0 9 * * 1-5 cd /workspace && python3 automation_manager.py report daily
```

## 📈 Benefits

🤖 **Fully Automated** - No manual intervention  
📊 **Data-Driven** - Based on actual metrics  
🔍 **Trend-Aware** - Spots patterns early  
💡 **Actionable** - Clear recommendations  
⏰ **Timely** - Regular scheduled reviews  
📝 **Documented** - All reports saved  

## 🎉 Summary

The automation manager provides:
- Automated system review
- Trend analysis
- Actionable recommendations
- Scheduled reporting
- Continuous monitoring

**Set it up once, benefit forever!** 🚀
