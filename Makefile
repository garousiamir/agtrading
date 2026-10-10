.PHONY: install test lint migrate

UV ?= uv

install:
	$(UV) sync --frozen

test:
	$(UV) run --frozen pytest

lint:
	$(UV) run --frozen ruff check .
	$(UV) run --frozen ruff format --check .

migrate:
	$(UV) run --frozen python scripts/migrate.py
