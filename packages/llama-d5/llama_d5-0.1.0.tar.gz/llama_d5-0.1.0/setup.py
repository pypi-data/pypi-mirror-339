#!/usr/bin/env python3
"""
Llama D5 - Python package for LlamaSearch AI
"""

from setuptools import setup, find_packages

setup(
    name="llama_d5",
    version="0.1.0",
    description="A comprehensive document and web page conversion toolkit powered by Llama AI.",
    long_description="""# llama-d5

A comprehensive document and web page conversion toolkit powered by Llama AI.

## Installation

```bash
pip install -e .
```

## Usage

```python
from llama_d5 import LlamaD5Client

# Initialize the client
client = LlamaD5Client(api_key="your-api-key")
result = client.query("your query")
print(result)
```

## Features

- Fast and efficient
- Easy to use API
- Comprehensive documentation
- Asynchronous support
- Built-in caching

## Development

### Setup

```bash
# Clone the repository
git clone https://github.com/nikjois/llama-d5.git
cd llama-d5

# Install development dependencies
pip install -e ".[dev]"
```

### Testing

```bash
pytest
```

## License

MIT

## Author

Nik Jois (nikjois@llamasearch.ai)
""",
    long_description_content_type="text/markdown",
    author="Nik Jois",
    author_email="nikjois@llamasearch.ai",
    url="https://github.com/llamasearchai/llama-d5",
    project_urls={
        "Documentation": "https://github.com/llamasearchai/llama-d5",
        "Bug Tracker": "https://github.com/llamasearchai/llama-d5/issues",
        "Source Code": "https://github.com/llamasearchai/llama-d5",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
)
