#!/usr/bin/env bash
# This script demonstrates the web scraping functionality of llamadoc2pdf

# Set up colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== LlamaDoc2PDF Web Scraping Demonstration ===${NC}\n"

# Check if URL was provided
if [ -z "$1" ]; then
  echo -e "${YELLOW}Usage: $0 <url>${NC}"
  echo -e "${YELLOW}Example: $0 https://example.com${NC}"
  # Default to example.com if no URL is provided
  URL="https://example.com"
  echo -e "${YELLOW}No URL provided, using default: ${URL}${NC}\n"
else
  URL="$1"
fi

# Run the scraper
echo -e "${GREEN}Running the Supreme Llama Web Scraper on ${URL}...${NC}\n"
llamadoc2pdf scrape --url "$URL"

echo -e "\n${GREEN}Scraping demo completed!${NC}" 