# Team Discussion Guide

Your workspace has **three discussion channels** that work together for optimal collaboration:

## 🏢 1. Built-in Workspace Discussions (Internal Coordination)

Your system has a native discussion database with 8 active conversations about architecture, AI team coordination, and toolchain decisions.

### Current Discussions
```
#1: Should we use TypeScript?
#2-5: Pattern discussions (class design)
#6: UV Toolchain Migration & Pre-commit Fix
#7: Kiro AI Assistant - Introduction
#8: Gemini AI - Joining the Team
```

### Using Workspace Discussions

**View all discussions:**
```bash
./ws collab list-discussions
```

**Add a comment to discussion #7 (Kiro):**
```bash
./ws collab comment 7 "Your comment here"
```

**Start a new discussion:**
```bash
./ws collab create-discussion "Discussion Title" "Description"
```

**Why use this?**
- ✅ Integrated with workspace database
- ✅ AI team can read/respond to discussions
- ✅ Context preserved across sessions
- ✅ Searchable discussion history
- ✅ No external dependency

---

## 🌐 2. GitHub Discussions (Public & Team Visibility)

For broader visibility and easier team collaboration.

### Enable GitHub Discussions
1. Go to: https://github.com/krsbox/workspace-system/settings
2. Scroll to "Features" section
3. Check the box for "Discussions"
4. Set up categories (Q&A, Ideas, Announcements, etc.)

### Access Discussions
- **Web**: https://github.com/krsbox/workspace-system/discussions
- **CLI**: Use GitHub CLI if installed (`gh discussion list`)

**Why use this?**
- ✅ Public visibility for contributors
- ✅ Threaded conversations
- ✅ Voting/marking answers
- ✅ Category organization
- ✅ GitHub-native integration

---

## 🎯 3. GitHub Issues (Problem Tracking)

Already available at: https://github.com/krsbox/workspace-system/issues

### Creating Issues
```bash
git issue create --title "Bug: Prevention checks too slow" --body "Description..."
```

Or via web: https://github.com/krsbox/workspace-system/issues/new

**Why use this?**
- ✅ Bug tracking and fixes
- ✅ Feature requests with discussion
- ✅ Labels, assignments, milestones
- ✅ Automatic linking to PRs

---

## 📊 Recommended Workflow

### Use Workspace Discussions For:
- 🤖 **AI Team Coordination** (Copilot, Kiro, Gemini conversations)
- 🔧 **Internal Architecture Decisions** (system design, patterns)
- 📝 **Session-based Knowledge** (ephemeral discussions, brainstorming)
- ⚡ **Real-time Collaboration** (immediate team feedback)

### Use GitHub Discussions For:
- 💡 **Feature Ideas** (crowdsourced input from community)
- ❓ **Q&A** (user questions about usage)
- 📢 **Announcements** (releases, major updates)
- 📚 **Knowledge Base** (permanent documentation discussions)

### Use GitHub Issues For:
- 🐛 **Bugs** (reproducible problems)
- ✨ **Feature Requests** (user-requested enhancements)
- 📋 **Tasks** (tracked to-do items)

---

## 🚀 Getting Started

### Step 1: Enable GitHub Discussions
Go to your repository settings and enable Discussions feature.

### Step 2: Create Categories (Optional)
Common categories:
- 💬 **Q&A** - Questions about usage
- 💡 **Ideas** - Feature proposals
- 📢 **Announcements** - Important updates
- 🔬 **Research** - Technical exploration

### Step 3: Link to README
Add to your README.md:
```markdown
## 💬 Discussion & Support

- **Workspace Discussions**: Internal AI team coordination (database-native)
- **GitHub Discussions**: Community questions and ideas
- **GitHub Issues**: Bug reports and feature requests
```

### Step 4: Start Conversations
Begin with introductory discussions about:
- Project vision and goals
- Architecture decisions
- AI team roles and responsibilities
- Contribution guidelines

---

## 📋 Current AI Team Discussions

Your workspace database already tracks:

| # | Topic | Status |
|---|-------|--------|
| #7 | Kiro AI Assistant Introduction | 🔄 Open |
| #8 | Gemini AI - Joining the Team | 🔄 Open |
| #6 | UV Toolchain Migration | 🔄 Open |
| #1 | TypeScript Consideration | 🔄 Open |

These can be referenced in your GitHub Discussions under an "AI Team" category!

---

## 🔗 Integration Ideas

### Sync Workspace → GitHub
Create a script to periodically sync important workspace discussions to GitHub:
```bash
#!/bin/bash
# future enhancement: auto-post significant workspace discussions
# to GitHub Discussions for visibility
```

### GitHub → Workspace Tracking
Link GitHub discussions in workspace:
```python
# in collab_system.py
def link_github_discussion(github_url, workspace_discussion_id):
    """Link a GitHub discussion to workspace discussion"""
    pass
```

---

## 📞 Quick Commands

```bash
# View workspace discussions
./ws collab list-discussions

# Add comment to workspace discussion #7
./ws collab comment 7 "Your response"

# Create new workspace discussion
./ws collab create-discussion "AI Team Sync" "Weekly coordination"

# View GitHub issues
open https://github.com/krsbox/workspace-system/issues

# View GitHub discussions (after enabling)
open https://github.com/krsbox/workspace-system/discussions
```

---

## ✅ Checklist

- [ ] Enable GitHub Discussions in repository settings
- [ ] Create discussion categories
- [ ] Link discussion guide to README
- [ ] Start introductory GitHub discussion
- [ ] Migrate key workspace discussions to GitHub (if needed)
- [ ] Set up discussion templates (optional)

---

**Repository**: https://github.com/krsbox/workspace-system  
**Current Branch**: copilot  
**Last Updated**: December 2, 2025
