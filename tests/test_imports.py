import importlib
import pathlib
import sys


ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def _top_level_py_modules():
    for p in ROOT.glob("*.py"):
        if p.name.startswith("test_"):
            continue
        if p.name == "setup.py":
            continue
        yield p.stem


def test_import_top_level_modules():
    """Smoke test: import each top-level module to catch syntax/import errors."""
    failed = []
    for name in _top_level_py_modules():
        try:
            importlib.import_module(name)
        except Exception as e:
            failed.append((name, repr(e)))

    assert not failed, f"Failed to import modules: {failed}"
