
cd ~/python_project

cat > Makefile << 'EOF'
SHELL := /bin/bash
VENV := .venv/bin

.PHONY: help clean clean-venv venv deps install test lint lint-fix build run

help:
	@echo "Targets:"
	@echo "  venv        Create .venv if missing"
	@echo "  deps        Install dev deps (ruff, pytest, build)"
	@echo "  install     Editable install of project"
	@echo "  lint        Ruff lint"
	@echo "  lint-fix    Ruff lint with --fix"
	@echo "  test        Run pytest"
	@echo "  build       Build wheel and sdist"
	@echo "  run         Run entrypoint (python -m first_app.main)"
	@echo "  clean       Remove build/dist/__pycache__"
	@echo "  clean-venv  Remove .venv"

clean:
	rm -rf build dist .pytest_cache .ruff_cache
	find . -type d -name "__pycache__" -exec rm -rf {} +

clean-venv:
	rm -rf .venv

venv:
	test -d .venv || python3.11 -m venv .venv
	@echo "venv ready."

deps: venv
	$(VENV)/python -m pip install -U pip
	$(VENV)/pip install ruff pytest build

install: venv
	$(VENV)/pip install -e .

lint: venv
	$(VENV)/ruff check .

lint-fix: venv
	$(VENV)/ruff check . --fix

test: venv install
	$(VENV)/pytest -q

build: clean venv install
	$(VENV)/python -m build

run: venv install
	$(VENV)/python -m first_app.main
EOF
