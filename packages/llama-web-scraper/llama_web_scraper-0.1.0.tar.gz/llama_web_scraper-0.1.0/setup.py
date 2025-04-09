#!/usr/bin/env python3
"""
Llama Web Scraper - Python package for LlamaSearch AI
"""

from setuptools import setup, find_packages

setup(
    name="llama_web_scraper",
    version="0.1.0",
    description="A robust and versatile web scraping and analysis system powered by cutting-edge Language Models (LLMs) and advanced scraping techniques.",
    long_description="""# llama-web-scraper

A robust and versatile web scraping and analysis system powered by cutting-edge Language Models (LLMs) and advanced scraping techniques.

## Installation

```bash
pip install -e .
```

## Usage

```python
from llama_web_scraper import LlamaWebScraperClient

# Initialize the client
client = LlamaWebScraperClient(api_key="your-api-key")
result = client.query("your query")
print(result)
```

## Features

- Fast and efficient
- Easy to use API
- Comprehensive documentation

## Development

### Setup

```bash
# Clone the repository
git clone https://github.com/nikjois/llama-web-scraper.git
cd llama-web-scraper

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
    url="https://github.com/llamasearchai/llama-web-scraper",
    project_urls={
        "Documentation": "https://github.com/llamasearchai/llama-web-scraper",
        "Bug Tracker": "https://github.com/llamasearchai/llama-web-scraper/issues",
        "Source Code": "https://github.com/llamasearchai/llama-web-scraper",
    },
    packages='src.llama_web_scraper',
    package_dir={"": "src"},
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
