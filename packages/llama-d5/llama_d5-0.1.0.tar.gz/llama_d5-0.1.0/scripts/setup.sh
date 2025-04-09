#!/bin/bash
# setup.sh - Enhanced setup script with all necessary dependencies

echo "Setting up Llama Screenshot tool with all enhancements..."

# Create virtual environment if not exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install core dependencies with error handling
echo "Installing dependencies..."
pip install --upgrade pip

# Core requirements
REQUIREMENTS=(
    "playwright>=1.30.0"
    "playwright-stealth>=0.1.0"
    "aiohttp>=3.8.3"
    "beautifulsoup4>=4.11.1"
    "bs4"
    "img2pdf>=0.4.4"
    "rich>=13.0.0"
    "fake-useragent>=1.1.1"
    "cloudscraper>=1.2.60"
    "pikepdf>=6.2.5"
    "pillow>=9.4.0"
    "requests>=2.28.2"
    "numpy>=1.24.2"
    "pypdf2>=2.12.1"
)

for req in "${REQUIREMENTS[@]}"; do
    echo "Installing $req..."
    pip install "$req" || {
        echo "Error installing $req. Trying to continue with other dependencies."
    }
done

# Install Playwright browsers
echo "Installing Playwright browsers..."
playwright install chromium
playwright install firefox
playwright install webkit

# Install Playwright dependencies
echo "Installing Playwright system dependencies..."
playwright install-deps

# Create necessary directories
mkdir -p output
mkdir -p output/debug

# Make scripts executable
chmod +x run_scraper.sh

# Test the installation
echo "Testing the installation..."
python -c "
import sys
try:
    # Core dependencies
    import playwright
    import aiohttp
    import bs4
    import img2pdf
    import rich
    import fake_useragent
    import cloudscraper
    import pikepdf
    from PIL import Image, ImageStat
    import requests
    import numpy
    
    print('All dependencies installed successfully!')
except ImportError as e:
    print(f'Missing dependency: {e}')
    sys.exit(1)
"

if [ $? -eq 0 ]; then
    echo "Setup completed successfully!"
    echo ""
    echo "To run the tool, use:"
    echo "./run_scraper.sh --urls \"https://example.com\" --pdf-name \"output.pdf\""
    echo ""
    echo "For more options, use:"
    echo "./run_scraper.sh --help"
else
    echo "Some dependencies could not be installed. Please check the error messages above."
    exit 1
fi
