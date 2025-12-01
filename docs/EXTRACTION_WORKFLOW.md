# Idea Extraction & Integration Workflow

**Quick reference for systematic project mining**

---

## 🚀 Quick Start (3 Commands)

```bash
# 1. Extract all ideas
./extract_all.sh

# 2. Review extracted ideas
python3 idea_extractor.py list

# 3. Integrate an idea
./integrate_idea.sh <idea_id>
```

---

## 📋 Complete Workflow

### Step 1: Extract Ideas

**Single project:**
```bash
python3 idea_extractor.py scan ./project
```

**All projects:**
```bash
./extract_all.sh
```

**Output:**
- 🟢 High reality (>=70%): Production-ready
- 🟡 Medium reality (50-69%): Needs validation
- 🔴 Low reality (<50%): Auto-skipped

---

### Step 2: Review Ideas

**List high-quality ideas (>=50% reality):**
```bash
python3 idea_extractor.py list
```

**By category:**
```bash
python3 idea_extractor.py list pattern
python3 idea_extractor.py list todo
python3 idea_extractor.py list documentation
```

**Include low-quality:**
```bash
python3 idea_extractor.py list-all
```

---

### Step 3: Check Duplicates

**Before integrating:**
```bash
python3 dedup_checker.py "Your idea title"
```

**Adjust sensitivity:**
```bash
python3 dedup_checker.py "Your idea title" 0.7  # 70% similarity
```

**Exit codes:**
- 0 = No duplicates (safe to proceed)
- 1 = Duplicates found (review needed)

---

### Step 4: Integrate Safely

**Automated workflow:**
```bash
./integrate_idea.sh <idea_id>
```

**What it does:**
1. Validates reality score
2. Checks for duplicates
3. Creates proposal
4. Runs quality checks
5. Prompts for confirmation

**Manual workflow:**
```bash
# 1. Check duplicates
python3 dedup_checker.py "idea title"

# 2. Create proposal
./ws propose "idea title"

# 3. Validate
./ws check
```

---

### Step 5: Track Progress

**View proposals:**
```bash
python3 proposal_system.py list
```

**View todos:**
```bash
./ws todo
```

**System status:**
```bash
./ws status
```

---

## 🛡️ Duplication Prevention

### 3-Layer Protection

**Layer 1: Database constraints**
- Automatic UNIQUE checks on key fields

**Layer 2: Similarity detection**
- 80% threshold by default
- Checks across: ideas, proposals, todos, wiki, knowledge

**Layer 3: Manual review**
- Integration script prompts on duplicates
- Search before create: `./ws search "keyword"`

---

## 📊 Reality Scoring

### What Gets Scored

- **100%**: Manual entries, documentation
- **90-100%**: Production code with tests
- **70-89%**: Working code, good structure
- **50-69%**: Incomplete but usable
- **<50%**: Mock/test/outdated (auto-skipped)

### Scoring Factors

**Positive (+):**
- Working code structure
- Real implementations
- Good documentation

**Negative (-):**
- Mock/simulation patterns
- Test/demo code
- Deprecated/outdated
- Minimal content

---

## 🎯 Best Practices

### Before Extraction
✅ Backup database: `cp workspace_knowledge.db workspace_knowledge.db.bak`  
✅ Check current state: `./ws status`  
✅ Note complexity score

### During Extraction
✅ Start with one project (test)  
✅ Review reality scores  
✅ Filter by category if needed

### During Integration
✅ Always check duplicates first  
✅ Use proposal workflow (not direct todo)  
✅ Run quality checks after each integration  
✅ Keep complexity LOW (<50)

### After Integration
✅ Update documentation  
✅ Run system check: `./ws check`  
✅ Verify status: `./ws status`  
✅ Archive source if from old project

---

## 🔧 Advanced Usage

### Batch Integration

**Create idea list:**
```bash
# Get IDs of high-reality ideas
python3 -c "
import sqlite3
conn = sqlite3.connect('workspace_knowledge.db')
c = conn.cursor()
c.execute('SELECT id FROM ideas WHERE reality_score >= 70 ORDER BY reality_score DESC')
for row in c.fetchall():
    print(row[0])
" > high_quality_ideas.txt
```

**Process batch:**
```bash
while read id; do
  echo "Processing #$id..."
  ./integrate_idea.sh $id
  sleep 2
done < high_quality_ideas.txt
```

### Custom Filters

**Extract only TODOs:**
```bash
python3 -c "
import sqlite3
conn = sqlite3.connect('workspace_knowledge.db')
c = conn.cursor()
c.execute('SELECT id, title, reality_score FROM ideas WHERE category=\"todo\" AND reality_score >= 70')
for row in c.fetchall():
    print(f'{row[0]:3} ({row[2]}%) - {row[1]}')
"
```

**Extract patterns only:**
```bash
python3 idea_extractor.py list pattern
```

### Merge Similar Ideas

**Find similar:**
```bash
python3 dedup_checker.py "idea title" 0.6  # Lower threshold
```

**Merge manually:**
```bash
# Update one idea with combined info
# Delete duplicate
python3 -c "
import sqlite3
conn = sqlite3.connect('workspace_knowledge.db')
c = conn.cursor()
c.execute('DELETE FROM ideas WHERE id=?', (ID_TO_DELETE,))
conn.commit()
"
```

---

## 📈 Success Metrics

### Track These

**Before extraction:**
```bash
./ws status
# Note: complexity, todos, proposals, quality score
```

**After integration:**
```bash
./ws status
# Compare metrics
```

**Quality maintained:**
```bash
./ws check
# Should still be 100/100 (Grade A)
```

### Target Goals

- ✅ Reality score: >=70% for integrated ideas
- ✅ Duplication rate: <5%
- ✅ Quality score: Maintain 100/100
- ✅ Complexity: Keep LOW (<50)
- ✅ Integration time: <2 min per idea

---

## 🚨 Troubleshooting

### "Duplicates found"
```bash
# Review duplicates
python3 dedup_checker.py "title"

# If false positive, lower threshold
python3 dedup_checker.py "title" 0.9

# Or force integration
./ws propose "title"  # Manual
```

### "Low reality score"
```bash
# Review the idea
python3 -c "
import sqlite3
conn = sqlite3.connect('workspace_knowledge.db')
c = conn.cursor()
c.execute('SELECT * FROM ideas WHERE id=?', (ID,))
print(c.fetchone())
"

# Check warnings
# Decide: integrate or skip
```

### "Quality check failed"
```bash
# See what failed
./ws check

# Fix issues
# Re-run check
```

---

## 📚 Command Reference

### Extraction
```bash
./extract_all.sh                          # Extract from all projects
python3 idea_extractor.py scan <path>     # Extract from one project
python3 idea_extractor.py list            # List ideas (>=50% reality)
python3 idea_extractor.py list-all        # List all ideas
python3 idea_extractor.py list <category> # Filter by category
```

### Duplication
```bash
python3 dedup_checker.py "<title>"        # Check duplicates (80%)
python3 dedup_checker.py "<title>" 0.7    # Custom threshold
./ws search "<keyword>"                   # Search workspace
```

### Integration
```bash
./integrate_idea.sh <id>                  # Automated integration
./ws propose "<title>"                    # Manual proposal
./ws check                                # Quality checks
./ws status                               # System status
```

### Management
```bash
./ws todo                                 # View todos
python3 proposal_system.py list           # View proposals
./ws maintain                             # Run maintenance
```

---

## ✅ Ready to Start

**Your system is ready!**

1. ✅ Extraction tool with reality scoring
2. ✅ Duplication checker (3 layers)
3. ✅ Integration workflow (automated)
4. ✅ Quality gates (prevention-first)
5. ✅ Unified management (./ws)

**Start now:**
```bash
./extract_all.sh
```
