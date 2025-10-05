
cd /home/kuonji/python_project
mkdir -p src/first_app tests
# ---------- README ----------
cat > README.md << 'EOF'
# first_app
A tiny demo package.
EOF
# ---------- pyproject.toml ----------
cat > pyproject.toml << 'EOF'
[build-system]
requires = ["setuptools>=68", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "first_app"
version = "0.1.0"
description = "Tiny demo package"
readme = "README.md"
requires-python = ">=3.11"
authors = [{ name = "Your Name" }]

[tool.setuptools]
package-dir = {"" = "src"}

[tool.setuptools.packages.find]
where = ["src"]

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
python_functions = ["test_*"]

[tool.ruff]
target-version = "py311"

[tool.ruff.lint]
# I: import sorting/formatting；
extend-select = ["I"]

[tool.ruff.format]
quote-style = "preserve"
EOF


cat > src/first_app/__init__.py << 'EOF'
__all__ = ["hello"]
EOF

cat > src/first_app/main.py << 'EOF'
import sys


def hello() -> str:
    return f"hello from {sys.version}"


if __name__ == "__main__":
    print(hello())
EOF

# ---------- test ----------
cat > tests/test_main.py << 'EOF'
from first_app.main import hello


def test_hello_contains_prefix_and_version():
    s = hello()
    assert s.startswith("hello from ")
    assert "." in s
EOF

# ---------- Makefile ----------
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
make venv
make deps
make install
make lint-fix  
make lint
make test
make build
make run



