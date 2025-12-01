# Proposal System Guide

Improvement proposal workflow with validation and conversion to todos.

## Workflow

```
Submit → Validate → Review → Approve/Reject → Convert to Todo
```

## 1. Setup Validation Criteria

Define what makes a good proposal:

```bash
# Add criteria (name, description, weight)
python3 proposal_system.py criteria add "impact" "Business/technical impact" 3
python3 proposal_system.py criteria add "effort" "Implementation effort" 2
python3 proposal_system.py criteria add "clarity" "Proposal clarity" 1
python3 proposal_system.py criteria add "alignment" "Goal alignment" 2

# List criteria
python3 proposal_system.py criteria list
```

**Weight**: Higher weight = more important (1-5 recommended)

## 2. Submit Proposals

```bash
python3 proposal_system.py submit \
  "<title>" \
  "<description>" \
  "[rationale]" \
  "[impact]" \
  "[effort]"

# Example
python3 proposal_system.py submit \
  "Add API documentation" \
  "Create comprehensive API docs for all packages" \
  "Improves developer experience and reduces support burden" \
  "high" \
  "medium"
```

**Impact levels**: low, medium, high, critical  
**Effort levels**: low, medium, high, very_high

## 3. Validate Proposals

Auto-validate against criteria:

```bash
python3 proposal_system.py validate <id>
```

**Scoring**:
- ≥70%: Auto-approved
- 50-69%: Needs revision
- <50%: Rejected

**Criteria scoring**:
- **Impact**: critical=10, high=9, medium=6, low=3
- **Effort**: low=10, medium=7, high=4, very_high=2
- **Clarity**: Based on description length and rationale
- **Alignment**: Default score (can be customized)

## 4. Review Proposals

Manual review (overrides auto-validation):

```bash
# Approve
python3 proposal_system.py review <id> approved "Looks good"

# Reject
python3 proposal_system.py review <id> rejected "Not aligned with goals"

# Request revision
python3 proposal_system.py review <id> needs_revision "Add more details"
```

## 5. Convert to Todos

Convert approved proposals to actionable todos:

```bash
python3 proposal_system.py convert <id>
```

**Auto-mapping**:
- Impact → Priority (critical→urgent, high→high, medium→medium, low→low)
- Title → Todo title
- Description → Todo description
- Category → Project

## 6. List & Track

```bash
# All proposals
python3 proposal_system.py list

# By status
python3 proposal_system.py list submitted
python3 proposal_system.py list approved
python3 proposal_system.py list rejected
python3 proposal_system.py list needs_revision
python3 proposal_system.py list converted
```

## Status Flow

```
submitted → (validate) → needs_revision/approved/rejected
                              ↓
                          (convert)
                              ↓
                            todo
```

## Example Workflow

```bash
# 1. Submit proposal
python3 proposal_system.py submit \
  "Implement caching layer" \
  "Add Redis caching to reduce database load by 60%" \
  "Current response time is 500ms, caching will reduce to 50ms" \
  "high" \
  "medium"

# 2. Auto-validate
python3 proposal_system.py validate 1
# Output: Score: 72% - APPROVED

# 3. Convert to todo
python3 proposal_system.py convert 1
# Output: Converted to todo #5

# 4. Check todo
python3 workspace_manager.py todo list
# [todo] #5: Implement caching layer (high)
```

## Tips

**Good proposals have**:
- Clear, specific title
- Detailed description (>100 chars)
- Strong rationale with metrics/benefits
- Realistic impact and effort estimates

**Bad proposals**:
- Vague: "Improve performance"
- No rationale: "Just do it"
- Unrealistic: "Rewrite everything" (effort:low)

## Integration

```python
# In Python code
from proposal_system import submit_proposal, auto_validate, convert_to_todo

# Submit
prop_id = submit_proposal("Title", "Description", "Rationale", "high", "low")

# Validate
result = auto_validate(prop_id)
if result['decision'] == 'approved':
    todo_id = convert_to_todo(prop_id)
```

## Database Tables

- **proposals**: All submitted proposals
- **reviews**: Review history
- **criteria**: Validation criteria
- **todos**: Converted todos (in workspace_knowledge.db)

## Benefits

✅ Structured improvement process  
✅ Objective validation criteria  
✅ Review history and audit trail  
✅ Automatic todo creation  
✅ Prevents low-quality tasks  
✅ Prioritization based on impact/effort
