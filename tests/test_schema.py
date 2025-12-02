"""Test database schema and utilities"""

import sys
from pathlib import Path

# Ensure `src` is on sys.path before importing project modules
SRC_DIR = Path(__file__).resolve().parents[1] / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

import sqlite3
import tempfile
import unittest

import schema  # noqa: E402
import db_utils  # noqa: E402


class TestSchema(unittest.TestCase):
    """Test suite for database schema"""

    def test_schema_tables_defined(self):
        """Verify all schema tables are defined."""
        self.assertTrue(schema.TABLES, "No tables defined in schema")

        expected_tables = [
            "knowledge",
            "wiki",
            "todos",
            "progress",
            "proposals",
            "reviews",
            "users",
            "discussions",
            "tools",
            "tool_executions",
        ]

        for table_name in expected_tables:
            self.assertIn(table_name, schema.TABLES, f"Missing table definition: {table_name}")

    def test_schema_table_syntax(self):
        """Verify SQL table definitions are valid."""
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            db_path = f.name

        try:
            conn = sqlite3.connect(db_path)
            c = conn.cursor()

            for table_name, sql in schema.TABLES.items():
                try:
                    c.execute(sql)
                except sqlite3.OperationalError as e:
                    self.fail(f"Invalid SQL for table '{table_name}': {e}")

            conn.commit()
            conn.close()
        finally:
            Path(db_path).unlink(missing_ok=True)

    def test_db_utils_context_manager(self):
        """Verify db_utils.get_db() context manager works."""
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            db_path = f.name

        try:
            # Monkey-patch DB_PATH for testing
            original_db_path = db_utils.DB_PATH
            db_utils.DB_PATH = Path(db_path)

            # Initialize database
            conn = sqlite3.connect(db_path)
            c = conn.cursor()
            c.execute("CREATE TABLE test (id INTEGER PRIMARY KEY, value TEXT)")
            conn.commit()
            conn.close()

            # Test context manager
            try:
                with db_utils.get_db() as conn:
                    self.assertIsNotNone(conn, "get_db() returned None")
                    self.assertIsInstance(
                        conn, sqlite3.Connection, "get_db() did not return Connection"
                    )
            finally:
                db_utils.DB_PATH = original_db_path
        finally:
            Path(db_path).unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
