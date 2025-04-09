#!/usr/bin/env bash

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
echo "🦙       SUPREME LLAMA INSTALLATION                  🦙"
echo "🦙                                                    🦙"
echo "🦙🦙🦙🦙🦙🦙🦙🦙🦙🦙🦙🦙🦙🦙🦙🦙🦙🦙🦙🦙🦙🦙🦙🦙🦙🦙🦙🦙"
echo -e "${NC}\n"

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check if Python is installed
if ! command_exists python3; then
    echo -e "${RED}Python 3 is not installed. Please install Python 3 and try again.${NC}"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo -e "${GREEN}Using Python version: ${CYAN}$PYTHON_VERSION${NC}"

# Create virtual environment
echo -e "\n${YELLOW}Creating virtual environment...${NC}"
VENV_DIR="venv"

# Check if venv already exists
if [ -d "$VENV_DIR" ]; then
    echo -e "${YELLOW}Found existing virtual environment. Would you like to recreate it? [y/N]${NC}"
    read -r recreate
    if [[ $recreate =~ ^[Yy]$ ]]; then
        echo -e "${YELLOW}Removing existing virtual environment...${NC}"
        rm -rf "$VENV_DIR"
    else
        echo -e "${GREEN}Using existing virtual environment.${NC}"
    fi
fi

# Create venv if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv "$VENV_DIR"
    echo -e "${GREEN}Virtual environment created at: ${CYAN}$VENV_DIR${NC}"
fi

# Activate virtual environment
echo -e "\n${YELLOW}Activating virtual environment...${NC}"
source "$VENV_DIR/bin/activate"
echo -e "${GREEN}Virtual environment activated.${NC}"

# Upgrade pip
echo -e "\n${YELLOW}Upgrading pip...${NC}"
pip install --upgrade pip

# Install core dependencies
echo -e "\n${YELLOW}Installing core dependencies...${NC}"
pip install typer rich pydantic pydantic-settings python-dotenv

# Ask which features to install
echo -e "\n${YELLOW}Which features would you like to install?${NC}"
echo -e "1) ${CYAN}Minimal${NC} - Basic document conversion only"
echo -e "2) ${CYAN}Standard${NC} - Document conversion + Web scraping"
echo -e "3) ${CYAN}Complete${NC} - All features including AI integration"
echo -e "4) ${CYAN}Custom${NC} - Customize which features to install"

read -p "Enter your choice [1-4]: " feature_choice

case $feature_choice in
    1)
        # Minimal installation
        echo -e "\n${YELLOW}Installing minimal dependencies...${NC}"
        pip install pillow img2pdf markdown weasyprint
        ;;
    2)
        # Standard installation
        echo -e "\n${YELLOW}Installing standard dependencies...${NC}"
        pip install pillow img2pdf markdown weasyprint docx2pdf
        pip install cloudscraper playwright beautifulsoup4 requests
        
        # Install Playwright browsers
        echo -e "\n${YELLOW}Installing Playwright browsers...${NC}"
        python -m playwright install chromium
        ;;
    3)
        # Complete installation
        echo -e "\n${YELLOW}Installing all dependencies...${NC}"
        pip install pillow img2pdf markdown weasyprint docx2pdf reportlab pypdf
        pip install cloudscraper playwright beautifulsoup4 requests requests-html
        pip install playwright-stealth tf-playwright-stealth
        
        # Optional AI-related packages
        pip install openai llama-index-core llama-index-readers-playwright
        
        # Install Playwright browsers
        echo -e "\n${YELLOW}Installing Playwright browsers...${NC}"
        python -m playwright install chromium
        python -m playwright install-deps
        ;;
    4)
        # Custom installation
        echo -e "\n${YELLOW}Select which components to install:${NC}"
        
        # Document conversion
        read -p "Install document conversion tools (Pillow, img2pdf, Markdown, WeasyPrint)? [Y/n] " install_doc
        if [[ ! $install_doc =~ ^[Nn]$ ]]; then
            pip install pillow img2pdf markdown weasyprint
        fi
        
        # Office document support
        read -p "Install Office document support (docx2pdf)? [Y/n] " install_office
        if [[ ! $install_office =~ ^[Nn]$ ]]; then
            pip install docx2pdf
        fi
        
        # Web scraping
        read -p "Install web scraping tools (Playwright, BeautifulSoup, Cloudscraper)? [Y/n] " install_web
        if [[ ! $install_web =~ ^[Nn]$ ]]; then
            pip install cloudscraper playwright beautifulsoup4 requests
            
            # Install Playwright browsers
            echo -e "\n${YELLOW}Installing Playwright browsers...${NC}"
            python -m playwright install chromium
        fi
        
        # Advanced web scraping
        read -p "Install advanced web scraping tools (Playwright-stealth, TF-Playwright-stealth)? [Y/n] " install_adv_web
        if [[ ! $install_adv_web =~ ^[Nn]$ ]]; then
            pip install playwright-stealth tf-playwright-stealth
        fi
        
        # AI integration
        read -p "Install AI integration (OpenAI, LlamaIndex)? [y/N] " install_ai
        if [[ $install_ai =~ ^[Yy]$ ]]; then
            pip install openai llama-index-core llama-index-readers-playwright
        fi
        ;;
    *)
        echo -e "${RED}Invalid choice. Installing minimal dependencies.${NC}"
        pip install pillow img2pdf markdown
        ;;
esac

# Install the package in development mode
echo -e "\n${YELLOW}Installing LlamaDoc2PDF in development mode...${NC}"
pip install -e .

# Make scripts executable
echo -e "\n${YELLOW}Making scripts executable...${NC}"
chmod +x scripts/launch_llama.sh
chmod +x scripts/run_demo.sh
chmod +x scripts/install.sh

echo -e "\n${GREEN}Installation complete!${NC}"
echo -e "${GREEN}To activate this environment in the future, run:${NC}"
echo -e "${CYAN}source $VENV_DIR/bin/activate${NC}"
echo -e "\n${GREEN}Would you like to run the Supreme Llama Interface now? [Y/n]${NC}"
read -r run_now
if [[ ! $run_now =~ ^[Nn]$ ]]; then
    echo -e "\n${MAGENTA}Launching Supreme Llama Interface...${NC}"
    python -m llamadoc2pdf
else
    echo -e "\n${GREEN}You can run the program later using:${NC}"
    echo -e "${CYAN}source $VENV_DIR/bin/activate${NC}"
    echo -e "${CYAN}python -m llamadoc2pdf${NC}"
fi 