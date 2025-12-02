# System Readiness: Idea Extraction & Integration

**Status**: Ready for systematic project mining  
**Date**: 2025-12-01  
**Goal**: Extract, validate, and integrate ideas without duplication

---

## 🎯 Current Capabilities

### ✅ What We Have

1. **Idea Extractor** (`idea_extractor.py`)
   - Reality scoring (0-100%)
   - Filters mock/test/outdated code
   - Extracts: TODOs, patterns, documentation
   - Database storage with warnings

2. **Workspace System** (11 integrated components)
   - Knowledge base, proposals, todos
   - Quality gates, prevention rules
   - Tools tracking, reviews
   - Single database (`workspace_knowledge.db`)

3. **Unified CLI** (`./ws`)
   - Status, check, maintain, search
   - Proposal workflow
   - Priority management

---

## 🔍 Phase 1: Extraction Strategy

### Target Projects
```bash
# Your available projects
/media/sunil-kr/workspace/projects/project/          # Main project
/media/sunil-kr/workspace/projects/projects-old/    # 21 archived projects
```

### Extraction Process

**Step 1: Scan with Reality Filter**
```bash
# Scan main project (reality >= 50%)
python3 idea_extractor.py scan ./project

# Scan archived projects
for dir in projects-old/*/; do
  python3 idea_extractor.py scan "$dir"
done
```

**Step 2: Review Extracted Ideas**
```bash
# High-quality ideas (>=70% reality)
python3 idea_extractor.py list

# All ideas including medium quality
python3 idea_extractor.py list-all
```

**Step 3: Categorize**
- 🟢 High reality (>=70%): Production-ready patterns
- 🟡 Medium reality (50-69%): Needs validation
- 🔴 Low reality (<50%): Skipped automatically

---

## 🏗️ Phase 2: Implementation Strategy

### Workflow: Idea → Proposal → Todo → Implementation

```
┌─────────────┐
│ Extract Idea│ (reality scored)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Validate    │ (check duplication)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Create      │ (./ws propose)
│ Proposal    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Auto-convert│ (proposal → todo)
│ to Todo     │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Implement   │ (with quality checks)
└─────────────┘
```

### Implementation Script

**Create**: `integrate_idea.sh`
```bash
#!/bin/bash
# Usage: ./integrate_idea.sh <idea_id>

IDEA_ID=$1

# 1. Get idea details
IDEA=$(python3 -c "
import sqlite3
conn = sqlite3.connect('workspace_knowledge.db')
c = conn.cursor()
c.execute('SELECT title, description, category, reality_score FROM ideas WHERE id=?', ($IDEA_ID,))
print(c.fetchone())
")

# 2. Check for duplicates (search existing)
./ws search "$IDEA"

# 3. If unique, create proposal
./ws propose "$IDEA"

# 4. Run quality checks
./ws check
```

---

## 🛡️ Phase 3: Duplication Prevention

### Multi-Layer Detection

**Layer 1: Database Constraints**
```sql
-- Already in schema
UNIQUE constraints on:
- wiki.title
- users.username
- tools.name
- quality_gates.name
- prevention_rules.name
```

**Layer 2: Search Before Create**
```bash
# Before adding idea
./ws search "<keyword>"

# Check knowledge base
python3 kb_manager.py search "<keyword>"

# Check proposals
python3 proposal_system.py list
```

**Layer 3: Similarity Detection**

Create: `dedup_checker.py`
```python
#!/usr/bin/env python3
import sqlite3
from difflib import SequenceMatcher

def similarity(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def find_duplicates(title, threshold=0.8):
    conn = sqlite3.connect('workspace_knowledge.db')
    c = conn.cursor()
    
    # Check across all sources
    sources = [
        ('ideas', 'SELECT id, title FROM ideas'),
        ('proposals', 'SELECT id, title FROM proposals'),
        ('todos', 'SELECT id, title FROM todos'),
        ('wiki', 'SELECT id, title FROM wiki'),
        ('knowledge', 'SELECT id, title FROM knowledge')
    ]
    
    duplicates = []
    for source, query in sources:
        c.execute(query)
        for row in c.fetchall():
            score = similarity(title, row[1])
            if score >= threshold:
                duplicates.append((source, row[0], row[1], score))
    
    conn.close()
    return duplicates

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: dedup_checker.py <title>")
        sys.exit(1)
    
    title = " ".join(sys.argv[1:])
    dupes = find_duplicates(title)
    
    if dupes:
        print(f"⚠️  Found {len(dupes)} similar items:")
        for source, id, text, score in dupes:
            print(f"  {score:.0%} - {source}#{id}: {text}")
    else:
        print("✓ No duplicates found")
```

**Layer 4: Prevention Rules**
```bash
# Add to prevention_system.py
- Block duplicate titles (exact match)
- Warn on high similarity (>80%)
- Suggest merge instead of create
```

---

## 📋 Phase 4: Integration Checklist

### Before Integration
- [ ] Extract ideas with reality filter
- [ ] Review reality scores
- [ ] Check for duplicates
- [ ] Validate against existing system

### During Integration
- [ ] Create proposal (not direct todo)
- [ ] Run quality gate
- [ ] Check prevention rules
- [ ] Review code if applicable

### After Integration
- [ ] Update documentation
- [ ] Run system check
- [ ] Update complexity score
- [ ] Archive original if from old project

---

## 🚀 Quick Start Commands

### 1. Extract from All Projects
```bash
# Create extraction script
cat > extract_all.sh << 'EOF'
#!/bin/bash
echo "Extracting from main project..."
python3 idea_extractor.py scan ./project

echo "Extracting from archived projects..."
for dir in projects-old/*/; do
  echo "Scanning: $dir"
  python3 idea_extractor.py scan "$dir" 2>/dev/null
done

echo "✓ Extraction complete"
python3 idea_extractor.py list
EOF

chmod +x extract_all.sh
./extract_all.sh
```

### 2. Review & Prioritize
```bash
# High-quality ideas only
python3 idea_extractor.py list

# By category
python3 idea_extractor.py list pattern
python3 idea_extractor.py list todo
python3 idea_extractor.py list documentation
```

### 3. Integrate Safely
```bash
# Check for duplicates first
python3 dedup_checker.py "Your idea title"

# If unique, create proposal
./ws propose "Your idea title"

# Validate
./ws check
```

---

## 📊 Success Metrics

Track integration quality:

```bash
# Before extraction
./ws status  # Note: complexity, todos, proposals

# After integration
./ws status  # Compare metrics

# Quality maintained?
./ws check   # Should still pass (100/100)
```

**Target Goals:**
- Reality score: >=70% for all integrated ideas
- Duplication rate: <5%
- Quality score: Maintain 100/100
- Complexity: Keep LOW (<50)

---

## 🔧 Tools to Create

### 1. Deduplication Checker
```bash
# Create dedup_checker.py (see Phase 3)
chmod +x dedup_checker.py
```

### 2. Integration Helper
```bash
# Create integrate_idea.sh (see Phase 2)
chmod +x integrate_idea.sh
```

### 3. Batch Processor
```bash
# Process multiple ideas
cat > batch_integrate.sh << 'EOF'
#!/bin/bash
# Read idea IDs from file
while read id; do
  echo "Processing idea #$id..."
  ./integrate_idea.sh $id
  sleep 1
done < idea_ids.txt
EOF

chmod +x batch_integrate.sh
```

---

## 🎯 Next Steps

**Immediate Actions:**

1. **Create dedup checker**
   ```bash
   # Copy from Phase 3 above
   ```

2. **Extract from one project first** (test run)
   ```bash
   python3 idea_extractor.py scan ./project
   python3 idea_extractor.py list
   ```

3. **Manually integrate 1-2 ideas** (validate workflow)
   ```bash
   # Pick high-reality idea
   python3 dedup_checker.py "idea title"
   ./ws propose "idea title"
   ./ws check
   ```

4. **Scale up** (if workflow works)
   ```bash
   ./extract_all.sh
   # Review and integrate systematically
   ```

---

## ✅ System Ready

Your workspace is **ready for systematic idea extraction**:

- ✅ Extraction tool with reality scoring
- ✅ Duplication detection strategy
- ✅ Integration workflow defined
- ✅ Quality gates in place
- ✅ Prevention rules active
- ✅ Unified CLI for management

**Start with**: `python3 idea_extractor.py scan ./project`
