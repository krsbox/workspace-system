# 🎯 Reality-Aware Idea Extraction Guide

**Enhanced with mock/simulation detection and consistency validation**

---

## 🚨 Reality Scoring System

### Strength of Reality (0-100%)

**🟢 High Reality (70-100%)**
- Working production code
- Complete implementations
- Real business logic
- Actual data processing

**🟡 Medium Reality (50-69%)**
- Partial implementations
- Some mock/test elements
- Older but functional code
- Documentation-heavy

**🔴 Low Reality (<50%)**
- Mock/simulation code
- Test fixtures
- Deprecated/obsolete code
- Incomplete stubs
- **AUTOMATICALLY SKIPPED**

---

## 🔍 Detection Mechanisms

### Mock/Simulation Detection (-30%)
Triggers on:
- File/path contains: `mock`, `fake`, `stub`, `dummy`, `test_data`
- Code contains: `simulation`, `example`, `demo`, `sample`
- Alert: ⚠️ MOCK/SIMULATION detected

### Outdated Code Detection (-20%)
Triggers on:
- Keywords: `deprecated`, `obsolete`, `old`, `legacy`
- Python 2 syntax
- Comments: `TODO remove`, `FIXME outdated`
- Alert: ⚠️ OUTDATED code detected

### Working Code Indicators (+10%)
Checks for:
- Function definitions: `def function()`
- Class definitions: `class ClassName`
- Imports: `import module`
- Main block: `if __name__ == "__main__"`
- Alert: ✓ Working code structure

### Test Code Detection (-20%)
Triggers on:
- File names: `test_*.py`, `*_test.py`
- Imports: `unittest`, `pytest`
- Functions: `def test_*()`
- Alert: ⚠️ TEST code (not production)

### Minimal Code Detection (-30%)
Triggers on:
- File size < 100 characters
- Alert: ⚠️ Minimal/incomplete code

---

## 📊 Extraction Strategy

### Priority 1: TODOs from Working Code
```python
# Extract TODO/FIXME/HACK/NOTE from reality >= 50%
# These are actionable items from real code
```

**Example Output**:
```
🟢 #123 [todo] 100% - # TODO: Add caching layer
    ✓ Working code structure
```

### Priority 2: Class Patterns
```python
# Extract unique class definitions from reality >= 70%
# These are proven architectural patterns
```

**Example Output**:
```
🟢 #456 [pattern] 90% - Pattern: class DatabaseManager
    ✓ Working code structure
```

### Priority 3: Documentation
```python
# Extract README files (reality = 80%)
# These provide context and architecture
```

**Example Output**:
```
🟡 #789 [documentation] 80% - Documentation: README.md
    ✓ Documentation
```

---

## 🎯 Usage

### Scan Project (Reality-Aware)
```bash
python3 idea_extractor.py scan projects-old/ai-orchestra
```

**Output**:
```
✓ Found 16738 ideas
  🟢 High reality (>=70%): 16611
  🟡 Medium reality (50-69%): 127
  🔴 Low reality (<50%): 0 (skipped)
✓ Added 16738 ideas to database
```

### List Ideas (Filtered by Reality)
```bash
# Only show reality >= 50%
python3 idea_extractor.py list

# Show specific category
python3 idea_extractor.py list todo
python3 idea_extractor.py list pattern
python3 idea_extractor.py list documentation

# Show ALL (including low reality)
python3 idea_extractor.py list-all
```

### Add Manual Idea
```bash
python3 idea_extractor.py add "Implement feature X"
# Automatically assigned 100% reality (manual entry)
```

---

## ⚠️ Warnings System

### Common Warnings

**✓ Working code structure**
- Good sign - real implementation detected
- High confidence in extraction

**⚠️ MOCK/SIMULATION detected**
- Code may not reflect production reality
- Use with caution

**⚠️ OUTDATED code detected**
- May use deprecated patterns
- Verify before implementing

**⚠️ TEST code (not production)**
- Test fixtures, not real logic
- Extract patterns, not implementations

**⚠️ Minimal/incomplete code**
- Stub or placeholder
- May lack full context

**✓ Documentation**
- README or docs file
- Provides context

---

## 🎯 Best Practices

### DO ✅
- Focus on ideas with reality >= 70%
- Read warnings before implementing
- Verify outdated code is still relevant
- Extract patterns from working code
- Use TODOs as actionable items

### DON'T ❌
- Implement mock/simulation code directly
- Ignore outdated warnings
- Trust test code as production patterns
- Skip reality score checks
- Assume all extracted ideas are valid

---

## 📊 Example Workflow

### 1. Scan Multiple Projects
```bash
for project in projects-old/*; do
    python3 idea_extractor.py scan "$project"
done
```

### 2. Review High-Reality TODOs
```bash
python3 idea_extractor.py list todo | grep "🟢"
```

### 3. Extract Patterns
```bash
python3 idea_extractor.py list pattern | head -20
```

### 4. Create Proposals
```bash
# For high-reality ideas
./ws propose "Implement caching (from ai-orchestra)"
```

### 5. Track Implementation
```bash
./ws todo
./ws check
```

---

## 🔍 Reality Score Examples

### 100% Reality
```python
# Real production code
class DatabaseManager:
    def __init__(self, connection_string):
        self.conn = sqlite3.connect(connection_string)
    
    def execute(self, query):
        return self.conn.execute(query)
```
✓ Working code structure  
✓ Complete implementation  
✓ Real business logic

### 60% Reality
```python
# Older code with some issues
# TODO: Update to Python 3
class OldManager:
    def process(self):
        # FIXME: This is deprecated
        pass
```
⚠️ OUTDATED code detected  
✓ Working code structure

### 30% Reality (SKIPPED)
```python
# Mock for testing
class MockDatabase:
    def fake_query(self):
        return "test_data"
```
⚠️ MOCK/SIMULATION detected  
⚠️ TEST code (not production)

---

## 📈 Statistics

### From ai-orchestra Scan
- Total ideas: 16,738
- High reality (>=70%): 16,611 (99.2%)
- Medium reality (50-69%): 127 (0.8%)
- Low reality (<50%): 0 (0%)

### Breakdown by Category
- TODOs: 3,239 actionable items
- Patterns: 13,000+ class definitions
- Documentation: 499 files

---

## 🎯 Success Criteria

### Quality Extraction
- [ ] Reality score >= 50% for all extracted ideas
- [ ] Warnings reviewed and understood
- [ ] Mock/simulation code filtered out
- [ ] Outdated code flagged
- [ ] Working code prioritized

### Consistency
- [ ] Extract from working code only
- [ ] Verify patterns are production-ready
- [ ] Check TODOs are still relevant
- [ ] Validate against current standards

---

## 🚀 Next Steps

1. **Scan all projects**: Extract ideas from 22+ projects
2. **Review high-reality**: Focus on 70%+ ideas
3. **Create proposals**: Convert best ideas to proposals
4. **Implement**: Track with todos and quality gates
5. **Validate**: Ensure consistency with current system

---

**Remember**: Reality score is your guide to code quality and relevance!

**Command**: `python3 idea_extractor.py list todo | grep "🟢"`
