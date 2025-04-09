#!/usr/bin/env bash

# Set up colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${MAGENTA}"
echo "🦙🦙🦙🦙🦙🦙🦙🦙🦙🦙🦙🦙🦙🦙🦙🦙🦙🦙🦙🦙🦙🦙🦙🦙🦙🦙🦙🦙"
echo "🦙                                                    🦙"
echo "🦙       SUPREME LLAMA LAUNCHER                      🦙"
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

# Check if any arguments were provided
if [ $# -eq 0 ]; then
    # Run interactive mode if no arguments
    echo -e "${CYAN}Launching Supreme Llama Interface in interactive mode...${NC}"
    python -m llamadoc2pdf
else
    # Otherwise, pass all arguments to the command
    echo -e "${CYAN}Launching Supreme Llama Interface with arguments: $@${NC}"
    python -m llamadoc2pdf "$@"
fi

exit_code=$?

if [ $exit_code -eq 0 ]; then
    echo -e "\n${GREEN}👋 The Llama has completed its task successfully!${NC}"
else
    echo -e "\n${RED}😭 The Llama encountered an error (exit code: $exit_code)${NC}"
fi 