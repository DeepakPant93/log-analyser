# Default target
.PHONY: help
help: ## Show this help
	@echo "Available commands:";
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-22s %s\n", $$1, $$2}'

.PHONY: venv
venv: ## Create a Python 3.12 virtual environment using uv
	uv venv -p 3.12 .venv

.PHONY: setup
setup: venv ## Create venv and install dependencies
	uv pip install -e .

.PHONY: activate
activate: ## Activate virtual environment (Fish shell compatible)
	@echo "To activate the virtual environment:"
	@echo "  source .venv/bin/activate.fish  # For Fish shell"
	@echo "  source .venv/bin/activate       # For Bash/Zsh"

.PHONY: install
install: bake ## Install the app locally (editable)
	uv pip install -e .

.PHONY: bake
bake: ## Build the app/package using uv
	uv build

.PHONY: run
run: ## Run the CLI (use ARGS="..." to pass arguments)
	log-analyser $(ARGS)

.PHONY: check
check: ## Quick check the CLI is available
	log-analyser --help | head -n 20 | cat

.PHONY: lint
lint: ## Run Ruff lint
	ruff check . --fix

.PHONY: test
test: ## Run tests
	pytest

.PHONY: clean
clean: ## Remove build artifacts
	rm -rf dist build *.egg-info **/__pycache__ .pytest_cache .coverage

