# Define the Poetry command
POETRY := poetry

# Project directories
SRC_DIR := src
TEST_DIR := tests

# Main script to run
MAIN_SCRIPT := $(SRC_DIR)/main.py

# Poetry setup
.PHONY: setup
setup:
		$(POETRY) install
		@echo "Project dependencies installed."

# Run the application
.PHONY: run
run:
		$(POETRY) run python $(MAIN_SCRIPT)

# Run tests (assuming you have tests in the TEST_DIR)
.PHONY: test
test:
		$(POETRY) run pytest $(TEST_DIR)

# Lint the code
.PHONY: lint
lint:
		$(POETRY) run pylint $(SRC_DIR) $(TEST_DIR)

# Format the code
.PHONY: format
format:
		$(POETRY) run black $(SRC_DIR) $(TEST_DIR)

# Add dependencies
.PHONY: add
add:
		-$(POETRY) add $(DEP)

# Add dev dependencies
.PHONY: add-dev
add-dev:
		-$(POETRY) add --dev $(DEP)

# Update dependencies
.PHONY: update
update:
		$(POETRY) update

# Clean up temporary files
.PHONY: clean
clean:
		find . -type f -name '*.pyc' -delete
		find . -type d -name '__pycache__' -delete
		@echo "Cleaned up."

# Build package
.PHONY: build
build:
		$(POETRY) build

# Publish package
.PHONY: publish
publish:
		$(POETRY) publish

# Help command to list available targets
.PHONY: help
help:
		@echo "Available commands:"
		@echo "  make setup     - Install project dependencies using Poetry"
		@echo "  make run       - Run the main script"
		@echo "  make test      - Run tests with pytest"
		@echo "  make lint      - Run pylint on the project"
		@echo "  make format    - Format code with black"
		@echo "  make add DEP=<package> - Add a dependency to pyproject.toml"
		@echo "  make add-dev DEP=<package> - Add a development dependency to pyproject.toml"
		@echo "  make update    - Update dependencies"
		@echo "  make clean     - Remove pyc files and __pycache__ directories"
		@echo "  make build     - Build the project"
		@echo "  make publish   - Publish package to PyPI"
		@echo "  make help      - Show this help message"

# This ensures that these targets are always executed
.PHONY: all
all: setup run