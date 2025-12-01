.PHONY: test lint format check install clean help

SHELL := /bin/bash

help:
	@echo "Available commands:"
	@echo "  make test      - Run tests"
	@echo "  make lint      - Run linter"
	@echo "  make format    - Format code"
	@echo "  make check     - Run all checks"
	@echo "  make install   - Install dependencies"
	@echo "  make clean     - Clean cache files"

test:
	@source .venv/bin/activate && pytest -v

lint:
	@source .venv/bin/activate && ruff check src/

format:
	@source .venv/bin/activate && black src/

check: test lint
	@echo "✓ All checks passed!"

install:
	@uv pip install -r requirements.txt

clean:
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	@echo "✓ Cleaned cache files"
