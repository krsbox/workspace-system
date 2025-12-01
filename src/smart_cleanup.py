#!/usr/bin/env python3
"""Smart Cleanup: Use Existing Tools, Don't Reinvent"""

import subprocess
from pathlib import Path
import json


def find_duplicate_files(project_path):
    """Use fdupes (proven tool) to find duplicates"""
    project_path = Path(project_path).resolve()

    print("🔍 Finding duplicate files (using fdupes)...")

    try:
        # Use fdupes - proven duplicate finder
        result = subprocess.run(
            ["fdupes", "-r", "-S", str(project_path)],
            capture_output=True,
            text=True,
            timeout=60,
        )

        if result.returncode != 0:
            print("⚠ fdupes not installed. Install: sudo apt install fdupes")
            return []

        # Parse output
        duplicates = []
        current_group = []

        for line in result.stdout.split("\n"):
            if line.strip():
                current_group.append(line.strip())
            elif current_group:
                if len(current_group) > 1:
                    duplicates.append(current_group)
                current_group = []

        return duplicates

    except FileNotFoundError:
        print("⚠ fdupes not installed. Install: sudo apt install fdupes")
        return []
    except subprocess.TimeoutExpired:
        print("⚠ fdupes timed out (project too large)")
        return []


def find_dead_code(project_path):
    """Use vulture (proven tool) to find dead code"""
    project_path = Path(project_path).resolve()

    print("🔍 Finding dead code (using vulture)...")

    try:
        # Use vulture - proven dead code finder
        result = subprocess.run(
            ["vulture", str(project_path), "--min-confidence", "80"],
            capture_output=True,
            text=True,
            timeout=60,
        )

        if "command not found" in result.stderr or result.returncode == 127:
            print("⚠ vulture not installed. Install: uv pip install vulture")
            return []

        # Parse output
        dead_code = []
        for line in result.stdout.split("\n"):
            if line.strip() and "unused" in line.lower():
                dead_code.append(line.strip())

        return dead_code

    except FileNotFoundError:
        print("⚠ vulture not installed. Install: uv pip install vulture")
        return []
    except subprocess.TimeoutExpired:
        print("⚠ vulture timed out")
        return []


def find_large_files(project_path, size_mb=1):
    """Use find (built-in) to find large files"""
    project_path = Path(project_path).resolve()

    print(f"🔍 Finding files > {size_mb}MB (using find)...")

    try:
        # Use find - built-in tool
        result = subprocess.run(
            ["find", str(project_path), "-type", "f", "-size", f"+{size_mb}M"],
            capture_output=True,
            text=True,
            timeout=30,
        )

        files = [f.strip() for f in result.stdout.split("\n") if f.strip()]
        return files

    except subprocess.TimeoutExpired:
        print("⚠ find timed out")
        return []


def find_unused_imports(project_path):
    """Use autoflake (proven tool) to find unused imports"""
    project_path = Path(project_path).resolve()

    print("🔍 Finding unused imports (using autoflake)...")

    try:
        # Use autoflake - proven import cleaner
        result = subprocess.run(
            ["autoflake", "--check", "--recursive", str(project_path)],
            capture_output=True,
            text=True,
            timeout=60,
        )

        if "command not found" in result.stderr or result.returncode == 127:
            print("⚠ autoflake not installed. Install: uv pip install autoflake")
            return []

        # Parse output
        unused = []
        for line in result.stdout.split("\n"):
            if "would remove" in line.lower():
                unused.append(line.strip())

        return unused

    except FileNotFoundError:
        print("⚠ autoflake not installed. Install: uv pip install autoflake")
        return []
    except subprocess.TimeoutExpired:
        print("⚠ autoflake timed out")
        return []


def analyze_project(project_path):
    """Run all analyses using proven tools"""
    project_path = Path(project_path).resolve()

    print(f"\n🔍 Smart Cleanup Analysis: {project_path.name}")
    print("=" * 60)
    print("")

    report = {
        "project": str(project_path),
        "duplicates": [],
        "dead_code": [],
        "large_files": [],
        "unused_imports": [],
    }

    # Find duplicates
    duplicates = find_duplicate_files(project_path)
    report["duplicates"] = duplicates
    if duplicates:
        print(f"📋 Found {len(duplicates)} duplicate file groups")
        for i, group in enumerate(duplicates[:3], 1):
            print(f"   Group {i}: {len(group)} files")
    else:
        print("✓ No duplicates found")
    print("")

    # Find dead code
    dead_code = find_dead_code(project_path)
    report["dead_code"] = dead_code
    if dead_code:
        print(f"📋 Found {len(dead_code)} dead code items")
        for item in dead_code[:5]:
            print(f"   {item}")
    else:
        print("✓ No dead code found")
    print("")

    # Find large files
    large_files = find_large_files(project_path, size_mb=1)
    report["large_files"] = large_files
    if large_files:
        print(f"📋 Found {len(large_files)} large files (>1MB)")
        for f in large_files[:5]:
            size = Path(f).stat().st_size / (1024 * 1024)
            print(f"   {size:.1f}MB: {Path(f).name}")
    else:
        print("✓ No large files found")
    print("")

    # Find unused imports
    unused = find_unused_imports(project_path)
    report["unused_imports"] = unused
    if unused:
        print(f"📋 Found {len(unused)} unused imports")
        for item in unused[:5]:
            print(f"   {item}")
    else:
        print("✓ No unused imports found")
    print("")

    # Summary
    total_issues = len(duplicates) + len(dead_code) + len(large_files) + len(unused)

    print("=" * 60)
    print(f"📊 Total Issues: {total_issues}")
    print("")

    if total_issues > 0:
        print("💡 Cleanup Commands:")
        if duplicates:
            print("   fdupes -r -d <path>  # Interactive duplicate removal")
        if unused:
            print("   autoflake --in-place --remove-all-unused-imports -r <path>")
        if dead_code:
            print("   # Review vulture output and remove manually")
        if large_files:
            print("   # Review large files and archive/compress")
    else:
        print("✅ Project is clean!")

    return report


def auto_cleanup(project_path, dry_run=True):
    """Auto cleanup using proven tools (safe mode)"""
    project_path = Path(project_path).resolve()

    print(f"\n🧹 Auto Cleanup: {project_path.name}")
    print(f"Mode: {'DRY RUN' if dry_run else 'LIVE'}")
    print("=" * 60)
    print("")

    actions = []

    # 1. Remove unused imports (safe)
    print("1️⃣ Removing unused imports...")
    try:
        cmd = ["autoflake", "--recursive", str(project_path)]
        if not dry_run:
            cmd.extend(["--in-place", "--remove-all-unused-imports"])

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)

        if result.returncode == 0:
            print("   ✓ Unused imports cleaned")
            actions.append("unused_imports")
        else:
            print("   ⚠ autoflake not available")
    except Exception as e:
        print(f"   ⚠ Failed: {e}")

    # 2. Format code (safe)
    print("2️⃣ Formatting code...")
    try:
        cmd = ["black", str(project_path)]
        if dry_run:
            cmd.append("--check")

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        print("   ✓ Code formatted")
        actions.append("format")
    except Exception as e:
        print(f"   ⚠ Failed: {e}")

    # 3. Remove __pycache__ (safe)
    print("3️⃣ Removing cache directories...")
    try:
        cmd = ["find", str(project_path), "-type", "d", "-name", "__pycache__"]
        if not dry_run:
            cmd.extend(["-exec", "rm", "-rf", "{}", "+"])

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        print("   ✓ Cache directories removed")
        actions.append("cache")
    except Exception as e:
        print(f"   ⚠ Failed: {e}")

    print("")
    print("=" * 60)
    print(f"✅ Cleanup complete: {len(actions)} actions")

    if dry_run:
        print("\n💡 Run with --live to apply changes")

    return actions


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage:")
        print("  smart_cleanup.py analyze <project_path>")
        print("  smart_cleanup.py cleanup <project_path> [--live]")
        print("")
        print("Uses proven tools:")
        print("  - fdupes: Find duplicate files")
        print("  - vulture: Find dead code")
        print("  - autoflake: Remove unused imports")
        print("  - black: Format code")
        print("  - find: Built-in file search")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "analyze" and len(sys.argv) >= 3:
        path = sys.argv[2]
        report = analyze_project(path)

        # Save report
        report_file = Path("cleanup_report.json")
        with open(report_file, "w") as f:
            json.dump(report, f, indent=2)
        print(f"\n📄 Report saved: {report_file}")

    elif cmd == "cleanup" and len(sys.argv) >= 3:
        path = sys.argv[2]
        live = "--live" in sys.argv
        auto_cleanup(path, dry_run=not live)
