#!/usr/bin/env python3
"""Idea Extractor V2: Enhanced with AI-Human collaboration"""
import re
from pathlib import Path
from collections import Counter

DB_PATH = Path("/media/sunil-kr/workspace/workspace-system/workspace_knowledge.db")


def extract_with_context(project_path):
    """Extract ideas with rich context for better decision-making"""
    path = Path(project_path)
    ideas = []

    for py_file in path.rglob("*.py"):
        try:
            content = py_file.read_text(errors="ignore")
            lines = content.splitlines()

            # Extract with surrounding context
            for i, line in enumerate(lines):
                # TODOs with context
                if re.search(r"(TODO|FIXME|HACK|XXX):", line, re.I):
                    context_before = "\n".join(lines[max(0, i - 2) : i])
                    context_after = "\n".join(lines[i + 1 : min(len(lines), i + 3)])

                    ideas.append(
                        {
                            "source": f"{py_file.relative_to(path)}:{i+1}",
                            "title": line.strip()[:100],
                            "context": f"{context_before}\n>>> {line}\n{context_after}",
                            "category": "todo",
                            "type": "contextual",
                        }
                    )

                # Function/class definitions with docstrings
                if match := re.match(r"(def|class)\s+(\w+)", line):
                    kind, name = match.groups()
                    docstring = ""
                    if i + 1 < len(lines) and '"""' in lines[i + 1]:
                        docstring = lines[i + 1].strip()

                    ideas.append(
                        {
                            "source": str(py_file.relative_to(path)),
                            "title": f"{kind.title()}: {name}",
                            "context": docstring,
                            "category": "pattern",
                            "type": "definition",
                        }
                    )
        except:
            continue

    return ideas


def analyze_idea_value(idea):
    """AI analyzes idea value and suggests priority"""
    score = 50  # Base score

    title_lower = idea["title"].lower()
    context_lower = idea.get("context", "").lower()

    # High value indicators
    if any(word in title_lower for word in ["security", "critical", "urgent", "bug"]):
        score += 30
    if any(word in title_lower for word in ["performance", "optimize", "improve"]):
        score += 20
    if any(word in context_lower for word in ["important", "must", "required"]):
        score += 15

    # Low value indicators
    if any(word in title_lower for word in ["maybe", "consider", "nice to have"]):
        score -= 20
    if any(word in title_lower for word in ["test", "example", "demo"]):
        score -= 15

    # Determine priority
    if score >= 80:
        priority = "urgent"
    elif score >= 65:
        priority = "high"
    elif score >= 45:
        priority = "medium"
    else:
        priority = "low"

    return {
        "value_score": min(100, max(0, score)),
        "priority": priority,
        "reasoning": f"Score: {score} based on keywords and context",
    }


def suggest_integration_path(idea, value_analysis):
    """AI suggests how to integrate this idea"""

    if value_analysis["priority"] in ["urgent", "high"]:
        return {
            "path": "immediate_proposal",
            "steps": [
                "Create high-priority proposal",
                "Assign to current sprint",
                "Human review required",
            ],
            "automation_level": "ai_assisted",
        }

    elif idea["category"] == "pattern" and value_analysis["value_score"] >= 70:
        return {
            "path": "pattern_library",
            "steps": [
                "Check for duplicates",
                "Add to pattern catalog",
                "Auto-document",
            ],
            "automation_level": "ai_automated",
        }

    else:
        return {
            "path": "review_queue",
            "steps": ["Add to review queue", "Human prioritization", "Manual decision"],
            "automation_level": "human_primary",
        }


def extract_smart(project_path, auto_classify=True):
    """Smart extraction with AI classification"""
    print(f"\n🔍 Extracting from: {project_path}")

    ideas = extract_with_context(project_path)
    print(f"  Found {len(ideas)} raw ideas")

    if auto_classify:
        print("  🤖 AI analyzing...")
        for idea in ideas:
            value = analyze_idea_value(idea)
            path = suggest_integration_path(idea, value)

            idea["value_score"] = value["value_score"]
            idea["priority"] = value["priority"]
            idea["integration_path"] = path["path"]
            idea["automation_level"] = path["automation_level"]

    # Group by automation level
    by_level = Counter(i["automation_level"] for i in ideas if "automation_level" in i)

    print("\n  📊 Classification:")
    print(f"     AI Automated:  {by_level.get('ai_automated', 0):4} ideas")
    print(f"     AI Assisted:   {by_level.get('ai_assisted', 0):4} ideas")
    print(f"     Human Primary: {by_level.get('human_primary', 0):4} ideas")

    return ideas


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: idea_extractor_v2.py <project_path>")
        sys.exit(1)

    ideas = extract_smart(sys.argv[1])

    print(f"\n✓ Extraction complete: {len(ideas)} ideas with AI classification")
