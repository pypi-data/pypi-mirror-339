#!/usr/bin/env bash
# This script sets up a Python virtual environment using uv and installs dependencies

# Ensure uv is installed
if ! command -v uv &> /dev/null; then
    echo "uv is not installed, installing now..."
    curl -sSf https://astral.sh/uv/install.sh | bash
    # Reload shell to use uv
    exec "$SHELL"
fi

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment with uv..."
    uv venv .venv
fi

# Activate the virtual environment
source .venv/bin/activate

# Install dependencies with uv
echo "Installing dependencies with uv..."
uv pip install -r requirements.txt

# Install development dependencies if --dev flag is provided
if [ "$1" == "--dev" ]; then
    echo "Installing development dependencies..."
    uv pip install -r requirements-dev.txt
fi

echo "Setup complete! Activate the virtual environment with: source .venv/bin/activate" 