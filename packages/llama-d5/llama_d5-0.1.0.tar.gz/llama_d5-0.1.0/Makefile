.PHONY: setup test run clean install

# Setup and install development dependencies
setup:
	pip install -e .

# Run tests
test:
	python -m pytest tests/

# Run the demo
run:
	bash scripts/run_demo.sh

# Clean up build artifacts and temporary files
clean:
	rm -rf output/ build/ dist/ *.egg-info/ .eggs/ .pytest_cache/ .coverage htmlcov/
	find . -type d -name "__pycache__" -exec rm -rf {} +

# Install in development mode
install:
	pip install -e .

# Show help
help:
	@echo "Available commands:"
	@echo "  make setup    - Install the package in development mode"
	@echo "  make test     - Run tests"
	@echo "  make run      - Run the demonstration script"
	@echo "  make clean    - Clean up temporary files and build artifacts" 