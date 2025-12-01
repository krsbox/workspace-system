# Session Manager Guide

Track conversations, context, and state between sessions for persistent memory.

## Why Sessions?

Users forget what they discussed. Sessions provide:
- **Conversation history** - Full message log
- **Context persistence** - Remember what you were working on
- **State tracking** - Variables, settings, current focus
- **Bookmarks** - Mark important moments
- **Search** - Find past discussions

## Quick Start

```bash
# Start session
python3 session_manager.py session start <user> [title]

# Resume last active session
python3 session_manager.py session resume <user>

# End session
python3 session_manager.py session end <session_id>
```

## 1. Sessions

### Start Session
```bash
python3 session_manager.py session start alice "Refactoring project"
# Output: Started session #1
```

### Resume Session
```bash
# Resumes last active session or creates new one
python3 session_manager.py session resume alice
# Output: Resumed session #2
```

### List Sessions
```bash
python3 session_manager.py session list alice
# Shows: 🟢 active, ⚫ ended
```

### Session Summary
```bash
python3 session_manager.py session summary 1
# Shows: messages, bookmarks, state vars
```

## 2. Messages (Conversation History)

### Add Message
```bash
python3 session_manager.py msg add <session_id> <role> <content>

# Examples
python3 session_manager.py msg add 1 user "How do I setup the project?"
python3 session_manager.py msg add 1 assistant "Run: pip install -r requirements.txt"
```

**Roles**: user, assistant, system

### List Messages
```bash
python3 session_manager.py msg list 1
# Shows conversation history
```

### Search Messages
```bash
python3 session_manager.py msg search alice "setup"
# Searches across all user's sessions
```

## 3. State (Session Variables)

Persist any data between interactions.

### Set State
```bash
python3 session_manager.py state set <session_id> <key> <value>

# Examples
python3 session_manager.py state set 1 "current_file" "main.py"
python3 session_manager.py state set 1 "line_number" "42"
python3 session_manager.py state set 1 "todos" '["fix bug", "add tests"]'
```

### Get State
```bash
python3 session_manager.py state get 1 current_file
# Output: current_file = main.py
```

### List All State
```bash
python3 session_manager.py state list 1
# Shows all key-value pairs
```

## 4. Bookmarks

Mark important moments to return to later.

### Add Bookmark
```bash
python3 session_manager.py bookmark add <session_id> <title> [description]

python3 session_manager.py bookmark add 1 "Found the bug" "Memory leak in parser.py line 156"
```

### List Bookmarks
```bash
python3 session_manager.py bookmark list 1
# Output: 📌 Found the bug: Memory leak in parser.py line 156
```

## Use Cases

### 1. Multi-Day Projects
```bash
# Day 1
python3 session_manager.py session start alice "API Refactor"
python3 session_manager.py state set 1 "phase" "planning"
python3 session_manager.py msg add 1 user "Starting API refactor"

# Day 2 (resume)
python3 session_manager.py session resume alice
python3 session_manager.py state get 1 phase
# Continue where you left off
```

### 2. Context Switching
```bash
# Working on feature A
python3 session_manager.py state set 1 "current_feature" "auth"
python3 session_manager.py state set 1 "files" '["auth.py", "user.py"]'

# Switch to bug fix
python3 session_manager.py session end 1
python3 session_manager.py session start alice "Bug fix #123"

# Return to feature A
python3 session_manager.py session resume alice
python3 session_manager.py state list 1
# All context restored
```

### 3. Knowledge Capture
```bash
# During exploration
python3 session_manager.py msg add 1 user "What does this function do?"
python3 session_manager.py msg add 1 assistant "It parses config files..."
python3 session_manager.py bookmark add 1 "Config parser explanation"

# Later, search for it
python3 session_manager.py msg search alice "config"
```

### 4. Collaboration Handoff
```bash
# Alice's session
python3 session_manager.py state set 1 "next_steps" '["review PR", "update docs"]'
python3 session_manager.py bookmark add 1 "Handoff to Bob" "Ready for review"

# Bob can view session summary
python3 session_manager.py session summary 1
python3 session_manager.py msg list 1
```

## Integration with Other Systems

### With Proposals
```python
# Track proposal discussion in session
session_id = start_session("alice", "Proposal #5 Discussion")
add_message(session_id, "user", "Reviewing caching proposal")
set_state(session_id, "proposal_id", 5)
```

### With Todos
```python
# Track todo progress
set_state(session_id, "current_todo", 3)
set_state(session_id, "progress", 75)
add_bookmark(session_id, "Todo 75% complete")
```

### With Wiki
```python
# Document findings in wiki, reference in session
add_message(session_id, "assistant", "Documented in wiki/architecture")
set_state(session_id, "wiki_pages", ["architecture", "setup"])
```

## Python API

```python
from session_manager import (
    start_session, resume_session, end_session,
    add_message, get_messages, search_messages,
    set_state, get_state, get_all_state,
    add_bookmark, list_bookmarks,
    get_session_summary
)

# Start or resume
session_id, is_new = resume_session("alice")

# Track conversation
add_message(session_id, "user", "Hello")
add_message(session_id, "assistant", "Hi! How can I help?")

# Save context
set_state(session_id, "working_on", "feature-x")

# Bookmark important moment
add_bookmark(session_id, "Breakthrough", "Found the solution!")

# End when done
end_session(session_id)
```

## Best Practices

✅ **Start sessions with descriptive titles**  
✅ **Set state for important variables**  
✅ **Bookmark key decisions/findings**  
✅ **End sessions when switching context**  
✅ **Search before asking repeated questions**  

❌ Don't create too many sessions (use resume)  
❌ Don't forget to end sessions  
❌ Don't store sensitive data in state  

## Database Schema

- **sessions**: Session metadata
- **session_messages**: Conversation history
- **session_state**: Key-value state
- **session_bookmarks**: Important moments

All in `workspace_knowledge.db`

## Benefits

🧠 **Persistent Memory** - Never forget context  
🔍 **Searchable History** - Find past discussions  
📌 **Bookmarks** - Quick access to key moments  
🔄 **Resume Anywhere** - Pick up where you left off  
👥 **Collaboration** - Share context with team  
📊 **Analytics** - Track what you work on
