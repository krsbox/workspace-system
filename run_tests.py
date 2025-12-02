#!/usr/bin/env python3
"""Simple test runner using unittest (no external dependencies)"""
import sys
import unittest
from pathlib import Path

# Add src to path
SRC_DIR = Path(__file__).resolve().parents[0] / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

# Add tests to path
TESTS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(TESTS_DIR))


def run_tests():
    """Run all tests in the tests/ directory"""
    loader = unittest.TestLoader()
    suite = loader.discover(str(TESTS_DIR), pattern="test_*.py")
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(run_tests())
