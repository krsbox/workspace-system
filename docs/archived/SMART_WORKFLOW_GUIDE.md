# Smart Workflow Guide: No Bypass, Flaw Detection

**Date**: 2025-12-01  
**Status**: ✅ ENFORCED - Mandatory gates active  
**Philosophy**: Quality over speed, review over automation

---

## 🎯 Workflow Overview

```
Ideas → [GATE 1] → Proposals → [GATE 2] → Todos → Done
         Review              Discussion
         Required            Required
```

**No Bypass**: Every step must pass gates  
**Flaw Detection**: Automatic quality checks  
**Smart Handling**: Flawed improvements blocked

---

## 🚪 Gate 1: Idea → Proposal

### Requirements
1. **Reality score >= 50%** (quality threshold)
2. **Not already converted** (no duplicates)
3. **No critical flaws** (quality check)

### Flaw Detection
**Automatic checks:**
- Title length (min 10 chars)
- Description present (min 20 chars)
- No vague language (maybe, perhaps, might)
- Not marked as duplicate
- Not test/mock/demo code

### Commands

**Check if idea can become proposal:**
```bash
python3 smart_workflow.py check-idea <idea_id>
```

**Create proposal from idea:**
```bash
python3 smart_workflow.py idea-to-proposal <idea_id>
```

**Example:**
```bash
# Check first
python3 smart_workflow.py check-idea 100
# Output: ✓ Idea #100 ready to become proposal

# Create proposal
python3 smart_workflow.py idea-to-proposal 100
# Output: ✓ Proposal #8 created (needs review)
#         ⚠️  Warnings: Missing reality score or source context
```

---

## 🚪 Gate 2: Proposal → Todo

### Requirements (ALL MANDATORY)
1. **Proposal must be reviewed** (status: approved)
2. **Discussion must exist** (collaborative decision)
3. **No critical flaws** (quality check)
4. **Not already converted** (no duplicates)

### Flaw Detection
**Automatic checks:**
- All Gate 1 checks
- Proposal status (must be approved)
- Discussion exists
- Not already converted

### Commands

**Check if proposal can become todo:**
```bash
python3 smart_workflow.py check-proposal <proposal_id>
```

**Review proposal (required step):**
```bash
python3 smart_workflow.py review <proposal_id> <approve|reject|revise> [feedback]
```

**Convert proposal to todo:**
```bash
python3 smart_workflow.py proposal-to-todo <proposal_id>
```

**Example:**
```bash
# Try to convert without review (BLOCKED)
python3 smart_workflow.py proposal-to-todo 4
# Output: ✗ BLOCKED: Proposal not approved (status: submitted). Review required!

# Review and approve
python3 smart_workflow.py review 4 approve "Looks good"
# Output: ✓ Proposal #4 approved

# Check if ready
python3 smart_workflow.py check-proposal 4
# Output: ✓ Proposal #4 ready to convert

# Convert to todo
python3 smart_workflow.py proposal-to-todo 4
# Output: ✓ Todo #18 created from proposal
```

---

## 🛡️ Flaw Detection System

### Critical Flaws (BLOCK)
- Title too short (< 10 chars)
- Description missing or too short (< 20 chars)
- Marked as duplicate
- Reality score too low (< 50%)
- Already converted

### Warnings (ALLOW with warning)
- Title very long (> 200 chars)
- Contains vague language
- Missing context (reality/source)
- Contains test/mock/demo indicators

### Example Output
```bash
python3 smart_workflow.py idea-to-proposal 50
# Output: ✗ Flaws detected: Title too short (< 10 chars), Description missing
#         ⚠️  Warnings: Contains test/mock/demo indicators
```

---

## 🔄 Complete Workflow Example

### Scenario: Convert high-value idea to todo

**Step 1: Check idea**
```bash
python3 smart_workflow.py check-idea 100
# ✓ Idea #100 ready to become proposal
```

**Step 2: Create proposal**
```bash
python3 smart_workflow.py idea-to-proposal 100
# ✓ Proposal #8 created (needs review)
# ⚠️  Warnings: Missing reality score or source context
```

**Step 3: Try to convert (BLOCKED)**
```bash
python3 smart_workflow.py proposal-to-todo 8
# ✗ BLOCKED: Proposal not approved (status: needs_review). Review required!
```

**Step 4: Review proposal**
```bash
# View proposal details
python3 proposal_system.py review 8

# Approve
python3 smart_workflow.py review 8 approve "Good idea, approved"
# ✓ Proposal #8 approved
```

**Step 5: Ensure discussion exists**
```bash
# Discussion auto-created when proposal created
# Or manually create:
python3 collab_system.py create-discussion "Discussion: Proposal #8"
```

**Step 6: Check if ready**
```bash
python3 smart_workflow.py check-proposal 8
# ✓ Proposal #8 ready to convert
```

**Step 7: Convert to todo**
```bash
python3 smart_workflow.py proposal-to-todo 8
# ✓ Todo #19 created from proposal
```

**Step 8: Verify**
```bash
./ws status
# Todos: 19 total (0 urgent, 17 high)
```

---

## 🚨 Handling Flawed Improvements

### Scenario 1: Low Reality Score

**Problem**: Idea has reality score < 50%

**Detection**:
```bash
python3 smart_workflow.py check-idea 25
# ✗ Idea #25 NOT ready: Reality score too low (35% < 50%)
```

**Solution**:
- Review idea manually
- If valuable, use force flag (not recommended)
- Or improve idea quality first

---

### Scenario 2: Missing Description

**Problem**: Proposal has no description

**Detection**:
```bash
python3 smart_workflow.py idea-to-proposal 30
# ✗ Flaws detected: Description missing or too short
```

**Solution**:
- Add description manually
- Update proposal in database
- Re-run conversion

---

### Scenario 3: Not Reviewed

**Problem**: Trying to convert unreviewed proposal

**Detection**:
```bash
python3 smart_workflow.py proposal-to-todo 5
# ✗ BLOCKED: Proposal not approved (status: submitted). Review required!
```

**Solution**:
```bash
# Review first
python3 smart_workflow.py review 5 approve "Reviewed and approved"

# Then convert
python3 smart_workflow.py proposal-to-todo 5
```

---

### Scenario 4: No Discussion

**Problem**: Proposal has no discussion

**Detection**:
```bash
python3 smart_workflow.py check-proposal 6
# ✗ Proposal #6 NOT ready: No discussion found. Discussion required!
```

**Solution**:
```bash
# Create discussion
python3 collab_system.py create-discussion "Discussion: Proposal #6"

# Or discussion auto-created when proposal created
# Check discussions:
python3 collab_system.py discussions
```

---

### Scenario 5: Already Converted

**Problem**: Trying to convert same proposal twice

**Detection**:
```bash
python3 smart_workflow.py proposal-to-todo 4
# ✗ BLOCKED: Already converted to todo
```

**Solution**:
- Check existing todo
- No action needed (duplicate prevention working)

---

## 📊 Workflow Statistics

### Check Current State
```bash
# Proposals by status
python3 -c "
import sqlite3
conn = sqlite3.connect('workspace_knowledge.db')
c = conn.cursor()
c.execute('SELECT status, COUNT(*) FROM proposals GROUP BY status')
for status, count in c.fetchall():
    print(f'{status}: {count}')
"

# Todos by priority
./ws todo

# Discussions
python3 collab_system.py discussions
```

---

## 🎯 Best Practices

### DO
✅ Always check before converting  
✅ Review proposals before approval  
✅ Ensure discussions exist  
✅ Fix flaws when detected  
✅ Use proper workflow (no bypass)  
✅ Track progress with snapshots

### DON'T
❌ Skip review step  
❌ Bypass gates with force flag  
❌ Ignore flaw warnings  
❌ Convert without discussion  
❌ Rush through workflow  
❌ Ignore quality checks

---

## 🔧 Advanced Usage

### Batch Processing with Gates

```bash
# Get approved proposals ready to convert
python3 -c "
import sqlite3
conn = sqlite3.connect('workspace_knowledge.db')
c = conn.cursor()
c.execute('''SELECT id, title FROM proposals 
    WHERE status='approved' 
    ORDER BY id''')
for prop_id, title in c.fetchall():
    print(f'{prop_id}: {title[:60]}')
"

# Convert each (gates will check)
for id in 8 9 10; do
  python3 smart_workflow.py proposal-to-todo $id
done
```

### Bulk Review

```bash
# Review multiple proposals
for id in 5 6 7; do
  python3 smart_workflow.py review $id approve "Batch approved"
done
```

### Quality Report

```bash
# Check all proposals
python3 -c "
import sqlite3
conn = sqlite3.connect('workspace_knowledge.db')
c = conn.cursor()
c.execute('SELECT id, title, status FROM proposals')
for prop_id, title, status in c.fetchall():
    print(f'Proposal #{prop_id}: {status}')
    # Check if ready
    import subprocess
    result = subprocess.run(
        ['python3', 'smart_workflow.py', 'check-proposal', str(prop_id)],
        capture_output=True, text=True
    )
    print(f'  {result.stdout.strip()}')
"
```

---

## 📈 Success Metrics

### Quality Maintained
- ✅ All proposals reviewed
- ✅ All todos from approved proposals
- ✅ Discussions for all proposals
- ✅ No flawed improvements
- ✅ No bypassed gates

### Workflow Compliance
- ✅ 100% gate compliance
- ✅ 0% bypass rate
- ✅ Flaw detection active
- ✅ Quality checks passing

---

## ✅ Summary

### Workflow Enforced
- **Gate 1**: Idea → Proposal (quality check)
- **Gate 2**: Proposal → Todo (review + discussion)
- **No Bypass**: All gates mandatory
- **Flaw Detection**: Automatic quality checks

### Commands
```bash
# Check
smart_workflow.py check-idea <id>
smart_workflow.py check-proposal <id>

# Convert
smart_workflow.py idea-to-proposal <id>
smart_workflow.py proposal-to-todo <id>

# Review
smart_workflow.py review <id> <approve|reject|revise> [feedback]
```

### Result
- ✅ Quality over speed
- ✅ Review over automation
- ✅ Collaboration over solo
- ✅ Smart over flawed

---

**🛡️ SMART WORKFLOW ACTIVE - NO BYPASS, QUALITY ENFORCED!**
