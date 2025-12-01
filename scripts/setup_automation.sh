#!/bin/bash
# Setup Automated Review, Study, and Reporting

WORKSPACE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Setting up automated workspace management..."
echo ""

# 1. Schedule automated tasks
echo "📅 Scheduling automated tasks..."
python3 "$WORKSPACE_DIR/automation_manager.py" schedule
echo "   ✓ Tasks scheduled"
echo ""

# 2. Create cron jobs
echo "⏰ Setting up cron jobs..."

# Daily report at 9 AM
DAILY_CRON="0 9 * * * cd $WORKSPACE_DIR && python3 automation_manager.py report daily >> automation.log 2>&1"

# Weekly report on Monday at 9 AM
WEEKLY_CRON="0 9 * * 1 cd $WORKSPACE_DIR && python3 automation_manager.py report weekly >> automation.log 2>&1"

# Monthly report on 1st at 9 AM
MONTHLY_CRON="0 9 1 * * cd $WORKSPACE_DIR && python3 automation_manager.py report monthly >> automation.log 2>&1"

# Health check every hour
HEALTH_CRON="0 * * * * cd $WORKSPACE_DIR && python3 automation_manager.py health >> health.log 2>&1"

# Maintenance every 6 hours
MAINTAIN_CRON="0 */6 * * * cd $WORKSPACE_DIR && python3 maintenance_system.py task run >> maintenance.log 2>&1"

# Proactive check every 4 hours
PROACTIVE_CRON="0 */4 * * * cd $WORKSPACE_DIR && python3 prevention_system.py proactive >> prevention.log 2>&1"

echo "   Suggested cron jobs:"
echo ""
echo "   # Daily automated report"
echo "   $DAILY_CRON"
echo ""
echo "   # Weekly automated report"
echo "   $WEEKLY_CRON"
echo ""
echo "   # Monthly automated report"
echo "   $MONTHLY_CRON"
echo ""
echo "   # Hourly health check"
echo "   $HEALTH_CRON"
echo ""
echo "   # Maintenance every 6 hours"
echo "   $MAINTAIN_CRON"
echo ""
echo "   # Proactive check every 4 hours"
echo "   $PROACTIVE_CRON"
echo ""

# 3. Offer to install cron jobs
read -p "Install these cron jobs? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # Backup existing crontab
    crontab -l > /tmp/crontab.backup 2>/dev/null || true
    
    # Add new jobs
    (crontab -l 2>/dev/null || true; echo ""; echo "# Workspace Automation"; \
     echo "$DAILY_CRON"; \
     echo "$WEEKLY_CRON"; \
     echo "$MONTHLY_CRON"; \
     echo "$HEALTH_CRON"; \
     echo "$MAINTAIN_CRON"; \
     echo "$PROACTIVE_CRON") | crontab -
    
    echo "   ✓ Cron jobs installed"
    echo "   ✓ Backup saved to /tmp/crontab.backup"
else
    echo "   ⊘ Skipped cron installation"
    echo "   → Add manually with: crontab -e"
fi

echo ""
echo "✅ Automation setup complete!"
echo ""
echo "Test with:"
echo "  python3 automation_manager.py health"
echo "  python3 automation_manager.py report daily"
echo ""
echo "View logs:"
echo "  tail -f automation.log"
echo "  tail -f health.log"
echo "  tail -f maintenance.log"
