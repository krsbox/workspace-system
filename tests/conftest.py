"""Pytest configuration and fixtures"""

import pytest
import sys
from pathlib import Path
import tempfile
import shutil


@pytest.fixture
def src_path():
    """Fixture: Path to src directory"""
    return Path(__file__).resolve().parents[1] / "src"


@pytest.fixture(autouse=True)
def add_src_to_path(src_path):
    """Fixture: Automatically add src to sys.path for all tests"""
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))
    yield
    if str(src_path) in sys.path:
        sys.path.remove(str(src_path))


@pytest.fixture
def temp_db():
    """Fixture: Temporary database file"""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = Path(f.name)
    yield db_path
    db_path.unlink(missing_ok=True)


@pytest.fixture
def temp_dir():
    """Fixture: Temporary directory"""
    temp_path = Path(tempfile.mkdtemp())
    yield temp_path
    shutil.rmtree(temp_path, ignore_errors=True)
