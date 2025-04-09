#!/usr/bin/env bash
# This script demonstrates the funcionality of llamadoc2pdf

# Set up colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${MAGENTA}"
echo "🦙🦙🦙🦙🦙🦙🦙🦙🦙🦙🦙🦙🦙🦙🦙🦙🦙🦙🦙🦙🦙🦙🦙🦙🦙🦙🦙🦙"
echo "🦙                                                    🦙"
echo "🦙       SUPREME LLAMA DEMO                          🦙"
echo "🦙                                                    🦙"
echo "🦙🦙🦙🦙🦙🦙🦙🦙🦙🦙🦙🦙🦙🦙🦙🦙🦙🦙🦙🦙🦙🦙🦙🦙🦙🦙🦙🦙"
echo -e "${NC}\n"

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo -e "${YELLOW}Activating virtual environment...${NC}"
    source venv/bin/activate
    echo -e "${GREEN}Virtual environment activated.${NC}"
else
    echo -e "${YELLOW}No virtual environment found. Running with system Python.${NC}"
fi

# Check if required directories exist
if [ ! -d "examples" ]; then
    echo -e "${YELLOW}Creating examples directory...${NC}"
    mkdir -p examples
fi

if [ ! -d "output" ]; then
    echo -e "${YELLOW}Creating output directory...${NC}"
    mkdir -p output
fi

# Create a demo markdown file if it doesn't exist
if [ ! -f "examples/demo.md" ]; then
    echo -e "${YELLOW}Creating demo markdown file...${NC}"
    cat > examples/demo.md << 'EOF'
# LlamaDoc2PDF Demo

This is a demonstration of the Supreme Llama PDF converter capabilities.

## Features

- Convert Markdown to PDF
- Convert HTML to PDF
- Convert text files to PDF
- Convert images to PDF
- Web scraping with screenshots
- AI-enhanced document processing

## Code Example

```python
from llamadoc2pdf import ConversionEngine, InputSource, ConversionOptions

# Initialize engine
engine = ConversionEngine()

# Convert a file
result = engine.convert("document.md", "output.pdf")

# Print result
print(f"Conversion successful: {result.success}")
```

## Table Example

| Feature | Status | Notes |
|---------|--------|-------|
| Markdown | ✅ | Full support |
| Images | ✅ | JPEG, PNG, GIF |
| Office | ⚠️ | Requires LibreOffice |
| Web | ✅ | Uses Playwright |

## Image Example

![Llama](https://upload.wikimedia.org/wikipedia/commons/thumb/b/b9/Llama_lying_down.jpg/320px-Llama_lying_down.jpg)
EOF
fi

# Create a demo text file if it doesn't exist
if [ ! -f "examples/demo.txt" ]; then
    echo -e "${YELLOW}Creating demo text file...${NC}"
    cat > examples/demo.txt << 'EOF'
SUPREME LLAMA TEXT FILE DEMO
===========================

This is a simple text file that will be converted to PDF.

Features:
- Plain text conversion
- Formatting preserved
- Monospaced font

Example code:
  def hello_world():
      print("Hello from the Supreme Llama!")

----------------------------------------
End of demo file
EOF
fi

# Run the demo
echo -e "\n${CYAN}Converting markdown to PDF...${NC}"
python -m llamadoc2pdf convert examples/demo.md --output output/demo_md.pdf --verbose

echo -e "\n${CYAN}Converting text file to PDF...${NC}"
python -m llamadoc2pdf convert examples/demo.txt --output output/demo_txt.pdf --verbose

# Check if a URL was provided as argument
if [ $# -gt 0 ]; then
    URL="$1"
    echo -e "\n${CYAN}Scraping URL: $URL${NC}"
    python -m llamadoc2pdf scrape "$URL" --output output/scrape_output --format both
else
    echo -e "\n${CYAN}Running super conversion on all example files...${NC}"
    python -m llamadoc2pdf super-convert examples/* --output output/super_convert --verbose
fi

echo -e "\n${GREEN}Demo completed! Check the output directory for results.${NC}"
echo -e "${CYAN}Output files:${NC}"
ls -la output/ 