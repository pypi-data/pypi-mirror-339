# llama-d5

[![PyPI version](https://img.shields.io/pypi/v/llama_d5.svg)](https://pypi.org/project/llama_d5/)
[![License](https://img.shields.io/github/license/llamasearchai/llama-d5)](https://github.com/llamasearchai/llama-d5/blob/main/LICENSE)
[![Python Version](https://img.shields.io/pypi/pyversions/llama_d5.svg)](https://pypi.org/project/llama_d5/)
[![CI Status](https://github.com/llamasearchai/llama-d5/actions/workflows/llamasearchai_ci.yml/badge.svg)](https://github.com/llamasearchai/llama-d5/actions/workflows/llamasearchai_ci.yml)

**Llama D5 (llama-d5)** is a document processing toolkit within the LlamaSearch AI ecosystem. It appears to focus on document conversion (potentially from various formats to PDF, indicated by `llamadoc2pdf`) and capturing document representations (like screenshots, suggested by `llama_screenshot`).

## Key Features

- **Document Conversion:** Includes components for converting document formats, possibly centered around PDF output (`llamadoc2pdf/`).
- **Document Capture:** Functionality to capture visual representations of documents, like screenshots (`llama_screenshot.py`).
- **Core Module:** Likely orchestrates the conversion and capture processes (`core.py`).
- **Configurable:** Supports configuration options (`config.py`).

## Installation

```bash
pip install llama-d5
# Or install directly from GitHub for the latest version:
# pip install git+https://github.com/llamasearchai/llama-d5.git
```

## Usage

*(Usage examples for document conversion and screenshot generation will be added here.)*

```python
# Placeholder for Python client usage
# from llama_d5 import DocProcessor, ConversionConfig

# config = ConversionConfig.load("config.yaml")
# processor = DocProcessor(config)

# # Convert a document to PDF
# pdf_path = processor.convert_to_pdf(input_file="document.docx")
# print(f"PDF saved to: {pdf_path}")

# # Take a screenshot
# screenshot_path = processor.take_screenshot(url="https://example.com", output_file="webpage.png")
# print(f"Screenshot saved to: {screenshot_path}")
```

## Architecture Overview

```mermaid
graph TD
    A[Input Document / URL] --> B{Core Processor (core.py)};
    B -- Conversion Task --> C{Document Converter (llamadoc2pdf/)};
    C --> D[Output PDF];
    B -- Capture Task --> E{Screenshot Tool (llama_screenshot.py)};
    E --> F[Output Image (Screenshot)];

    G[Configuration (config.py)] -- Configures --> B;
    G -- Configures --> C;
    G -- Configures --> E;

    style B fill:#f9f,stroke:#333,stroke-width:2px
```

1.  **Input:** Accepts a document file or URL.
2.  **Core Processor:** Manages the request and routes it to the appropriate tool.
3.  **Converter:** Handles conversion of input documents into PDF format.
4.  **Screenshot Tool:** Captures a visual representation (screenshot) of a document or webpage.
5.  **Output:** Produces either a PDF file or an image file.
6.  **Configuration:** Settings control the behavior of the conversion and capture tools.

## Configuration

*(Details on configuring input/output formats, screenshot resolution, conversion options, etc., will be added here.)*

## Development

### Setup

```bash
# Clone the repository
git clone https://github.com/llamasearchai/llama-d5.git
cd llama-d5

# Install in editable mode with development dependencies
pip install -e ".[dev]"
```

### Testing

```bash
pytest tests/
```

### Contributing

Contributions are welcome! Please refer to [CONTRIBUTING.md](CONTRIBUTING.md) and submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
