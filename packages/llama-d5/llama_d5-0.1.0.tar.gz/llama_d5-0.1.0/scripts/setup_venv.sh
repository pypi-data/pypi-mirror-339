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
echo "🦙       SUPREME LLAMA ENVIRONMENT SETUP             🦙"
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

# Install dependencies
echo -e "\n${YELLOW}Installing requirements...${NC}"
pip install -e .

# Install additional dependencies
echo -e "\n${YELLOW}Installing additional dependencies...${NC}"
pip install typer rich pydantic pydantic-settings python-dotenv cloudscraper beautifulsoup4 requests playwright markdown pillow img2pdf pytest

# Install Playwright browsers
echo -e "\n${YELLOW}Installing Playwright browsers...${NC}"
python -m playwright install chromium

# Make scripts executable
echo -e "\n${YELLOW}Making scripts executable...${NC}"
chmod +x scripts/launch_llama.sh
chmod +x scripts/run_demo.sh
chmod +x scripts/install.sh

echo -e "\n${GREEN}Environment setup complete!${NC}"
echo -e "${GREEN}To activate this environment in the future, run:${NC}"
echo -e "${CYAN}source $VENV_DIR/bin/activate${NC}"
echo -e "\n${GREEN}Would you like to run the Supreme Llama Interface now? [Y/n]${NC}"
read -r run_now
if [[ ! $run_now =~ ^[Nn]$ ]]; then
    echo -e "\n${MAGENTA}Launching Supreme Llama Interface...${NC}"
    python -m llamadoc2pdf.main
else
    echo -e "\n${GREEN}You can run the program later using:${NC}"
    echo -e "${CYAN}source $VENV_DIR/bin/activate${NC}"
    echo -e "${CYAN}python -m llamadoc2pdf.main${NC}"
fi 