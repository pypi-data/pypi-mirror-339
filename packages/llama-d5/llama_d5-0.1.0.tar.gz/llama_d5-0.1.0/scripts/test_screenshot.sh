#!/bin/bash
# test_screenshot.sh - Test screenshot functionality

# Ensure we have all dependencies
cd "$(dirname "$0")"
source venv/bin/activate

# Install any missing dependencies
pip install pillow playwright-stealth

# Ensure output directory exists
mkdir -p output

# Check if URL was provided
if [ $# -ne 1 ]; then
  echo "Usage: $0 <url>"
  echo "Example: $0 https://platform.openai.com/docs/overview"
  exit 1
fi

# Run the test script
echo "Running screenshot test for $1..."
python test_screenshot.py "$1"

# Check if it worked
if [ $? -eq 0 ]; then
  echo "Test completed successfully"
  # Show the screenshot (macOS only)
  if [[ "$OSTYPE" == "darwin"* ]]; then
    SCREENSHOT_FILE="output/$(echo "$1" | sed 's/[^a-zA-Z0-9]/_/g').png"
    if [ -f "$SCREENSHOT_FILE" ]; then
      open "$SCREENSHOT_FILE"
    fi
  fi
else
  echo "Test failed"
fi 