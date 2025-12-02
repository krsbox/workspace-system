"""Test imports for all src modules"""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))


class TestSrcImports(unittest.TestCase):
    """Test suite for src module imports"""

    def test_import_all_src_modules(self):
        """Smoke test: import all src modules to catch syntax/import errors."""
        failed = []
        for py_file in sorted(SRC_DIR.glob("*.py")):
            mod_name = py_file.stem
            try:
                __import__(mod_name)
            except Exception as e:
                failed.append((mod_name, type(e).__name__, str(e)[:100]))

        self.assertEqual(failed, [], f"Failed to import {len(failed)} modules: {failed}")

    def test_stdlib_imports_available(self):
        """Verify all stdlib modules used by the project are available."""
        stdlib_modules = [
            "collections",
            "contextlib",
            "datetime",
            "difflib",
            "json",
            "pathlib",
            "re",
            "shutil",
            "sqlite3",
            "subprocess",
            "sys",
        ]
        for mod_name in stdlib_modules:
            try:
                __import__(mod_name)
            except ImportError as e:
                self.fail(f"stdlib module '{mod_name}' not available: {e}")


if __name__ == "__main__":
    unittest.main()
