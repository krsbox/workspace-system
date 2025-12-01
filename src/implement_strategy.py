#!/usr/bin/env python3
"""Implementation Executor: Execute strategies systematically"""
import sqlite3
import subprocess
from pathlib import Path

DB_PATH = Path("/media/sunil-kr/workspace/workspace-system/workspace_knowledge.db")

def get_top_patterns(limit=20):
    """Get unique, high-quality patterns"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT DISTINCT title, id, reality_score 
        FROM ideas 
        WHERE category='pattern' AND reality_score >= 90
        ORDER BY reality_score DESC, id DESC
        LIMIT ?
    """, (limit,))
    patterns = c.fetchall()
    conn.close()
    return patterns

def get_critical_todos(limit=30):
    """Get actionable TODOs"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT title, id, source, reality_score
        FROM ideas
        WHERE category='todo' AND reality_score >= 80
        ORDER BY reality_score DESC
        LIMIT ?
    """, (limit,))
    todos = c.fetchall()
    conn.close()
    return todos

def check_duplicate(title):
    """Check if idea already exists"""
    result = subprocess.run(
        ['python3', 'dedup_checker.py', title],
        capture_output=True,
        text=True
    )
    return result.returncode != 0  # True if duplicates found

def create_proposal(title, description=""):
    """Create proposal via workspace CLI"""
    result = subprocess.run(
        ['./ws', 'propose', title],
        input=description,
        capture_output=True,
        text=True
    )
    return result.returncode == 0

def execute_phase1():
    """Execute Phase 1: Pattern Library Integration"""
    print("\n" + "="*60)
    print("EXECUTING PHASE 1: Pattern Library Integration")
    print("="*60 + "\n")
    
    patterns = get_top_patterns(20)
    print(f"📦 Found {len(patterns)} top patterns\n")
    
    integrated = 0
    skipped = 0
    
    for title, idea_id, reality in patterns[:10]:  # Start with top 10
        clean_title = title.replace('Pattern: class ', '')
        proposal_title = f"Integrate pattern: {clean_title}"
        
        print(f"Processing: {clean_title} (reality: {reality}%)")
        
        # Check duplicate
        if check_duplicate(proposal_title):
            print(f"  ⚠️  Duplicate found - skipping")
            skipped += 1
            continue
        
        # Create proposal
        description = f"High-quality pattern from extracted ideas (ID: {idea_id}, Reality: {reality}%)"
        if create_proposal(proposal_title, description):
            print(f"  ✓ Proposal created")
            integrated += 1
        else:
            print(f"  ✗ Failed to create proposal")
            skipped += 1
    
    print(f"\n✓ Phase 1 complete: {integrated} integrated, {skipped} skipped")
    return integrated, skipped

def execute_phase2_todos():
    """Execute Phase 2: Technical Debt Resolution"""
    print("\n" + "="*60)
    print("EXECUTING PHASE 2: Technical Debt Resolution")
    print("="*60 + "\n")
    
    todos = get_critical_todos(10)  # Start with top 10
    print(f"📋 Found {len(todos)} critical TODOs\n")
    
    integrated = 0
    skipped = 0
    
    for title, idea_id, source, reality in todos:
        clean_title = title[:60].strip()
        proposal_title = f"Resolve: {clean_title}"
        
        print(f"Processing: {clean_title[:50]}...")
        
        # Check duplicate
        if check_duplicate(proposal_title):
            print(f"  ⚠️  Duplicate found - skipping")
            skipped += 1
            continue
        
        # Create proposal
        description = f"Technical debt from {source} (ID: {idea_id}, Reality: {reality}%)"
        if create_proposal(proposal_title, description):
            print(f"  ✓ Proposal created")
            integrated += 1
        else:
            print(f"  ✗ Failed to create proposal")
            skipped += 1
    
    print(f"\n✓ Phase 2 complete: {integrated} integrated, {skipped} skipped")
    return integrated, skipped

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  implement_strategy.py phase1     - Pattern integration")
        print("  implement_strategy.py phase2     - TODO resolution")
        print("  implement_strategy.py all        - Execute all phases")
        sys.exit(1)
    
    phase = sys.argv[1]
    
    total_integrated = 0
    total_skipped = 0
    
    if phase in ['phase1', 'all']:
        i, s = execute_phase1()
        total_integrated += i
        total_skipped += s
    
    if phase in ['phase2', 'all']:
        i, s = execute_phase2_todos()
        total_integrated += i
        total_skipped += s
    
    print("\n" + "="*60)
    print("EXECUTION SUMMARY")
    print("="*60)
    print(f"  Integrated: {total_integrated}")
    print(f"  Skipped: {total_skipped}")
    print(f"  Success rate: {total_integrated/(total_integrated+total_skipped)*100:.1f}%")
    print("\nNext: Review proposals with './ws status' and './ws todo'")
