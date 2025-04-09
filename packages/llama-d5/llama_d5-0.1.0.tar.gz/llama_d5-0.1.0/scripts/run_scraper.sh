#!/bin/bash
# run_scraper.sh - Enhanced script to run the web scraper with proper arguments

# Ensure we're in the correct directory
cd "$(dirname "$0")"

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Default values
OUTPUT_DIR="output"
PDF_NAME="website_capture_$(date +%Y%m%d_%H%M%S).pdf"
DELETE_SCREENSHOTS=true
MAX_PARALLEL=2
HEADLESS=true
RETRIES=3
MAX_DEPTH=0
MAX_URLS=100

# Parse command line arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --url|--urls)
      URLS="$2"
      shift 2
      ;;
    --url-file)
      URL_FILE="$2"
      shift 2
      ;;
    --output-dir)
      OUTPUT_DIR="$2"
      shift 2
      ;;
    --pdf-name)
      PDF_NAME="$2"
      shift 2
      ;;
    --keep-screenshots)
      DELETE_SCREENSHOTS=false
      shift
      ;;
    --parallel)
      MAX_PARALLEL="$2"
      shift 2
      ;;
    --visible)
      HEADLESS=false
      shift
      ;;
    --retries)
      RETRIES="$2"
      shift 2
      ;;
    --max-depth)
      MAX_DEPTH="$2"
      shift 2
      ;;
    --max-urls)
      MAX_URLS="$2"
      shift 2
      ;;
    --proxy)
      PROXY="$2"
      shift 2
      ;;
    --help)
      echo "Llama Screenshot - Advanced web scraping tool"
      echo ""
      echo "Usage: $0 [options]"
      echo ""
      echo "Options:"
      echo "  --url, --urls URL      Comma-separated list of URLs to scrape"
      echo "  --url-file FILE        File containing URLs to scrape (one per line)"
      echo "  --output-dir DIR       Output directory (default: output)"
      echo "  --pdf-name NAME        Output PDF filename (default: website_capture_DATE.pdf)"
      echo "  --keep-screenshots     Keep screenshots after PDF creation"
      echo "  --parallel N           Maximum number of parallel browser instances (default: 2)"
      echo "  --visible              Run with browser visible (not headless)"
      echo "  --retries N            Maximum number of retries per URL (default: 3)"
      echo "  --max-depth N          Maximum depth for URL discovery (default: 0)"
      echo "  --max-urls N           Maximum number of URLs to process (default: 100)"
      echo "  --proxy URL            Proxy server to use (e.g., http://proxy:port)"
      echo "  --help                 Show this help message"
      exit 0
      ;;
    *)
      echo "Unknown parameter: $1"
      echo "Use --help for usage information."
      exit 1
      ;;
  esac
done

# Check if URLs were provided
if [ -z "$URLS" ] && [ -z "$URL_FILE" ]; then
  echo "Error: You must provide URLs to scrape with --url or --url-file"
  echo "Use --help for usage information."
  exit 1
fi

# Ensure output directory exists
mkdir -p "$OUTPUT_DIR"

# Build command arguments
CMD_ARGS=""

if [ ! -z "$URLS" ]; then
  CMD_ARGS="$CMD_ARGS --urls \"$URLS\""
fi

if [ ! -z "$URL_FILE" ]; then
  CMD_ARGS="$CMD_ARGS --url-file \"$URL_FILE\""
fi

CMD_ARGS="$CMD_ARGS --output-dir \"$OUTPUT_DIR\""
CMD_ARGS="$CMD_ARGS --pdf-name \"$PDF_NAME\""
CMD_ARGS="$CMD_ARGS --max-parallel $MAX_PARALLEL"
CMD_ARGS="$CMD_ARGS --retries $RETRIES"
CMD_ARGS="$CMD_ARGS --max-depth $MAX_DEPTH"
CMD_ARGS="$CMD_ARGS --max-urls $MAX_URLS"

if [ "$HEADLESS" = false ]; then
  CMD_ARGS="$CMD_ARGS --no-headless"
fi

if [ "$DELETE_SCREENSHOTS" = false ]; then
  CMD_ARGS="$CMD_ARGS --keep-screenshots"
fi

if [ ! -z "$PROXY" ]; then
  CMD_ARGS="$CMD_ARGS --proxy \"$PROXY\""
fi

# Print command summary
echo "Starting web scraping with the following settings:"
echo "- URLs: ${URLS:-"From file $URL_FILE"}"
echo "- Output directory: $OUTPUT_DIR"
echo "- PDF name: $PDF_NAME"
echo "- Delete screenshots: $DELETE_SCREENSHOTS"
echo "- Max parallel: $MAX_PARALLEL"
echo "- Headless: $HEADLESS"
echo "- Max retries: $RETRIES"
echo "- Max depth: $MAX_DEPTH"
echo "- Max URLs: $MAX_URLS"
if [ ! -z "$PROXY" ]; then
  echo "- Proxy: $PROXY"
fi

# Run the script
echo "Running command: python llama_screenshot.py $CMD_ARGS"
eval "python llama_screenshot.py $CMD_ARGS"

# Check if the script was successful
if [ $? -eq 0 ]; then
  echo "Successfully completed scraping and PDF generation!"
  echo "PDF saved to: $OUTPUT_DIR/$PDF_NAME"
else
  echo "An error occurred during the scraping process."
  exit 1
fi 