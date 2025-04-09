#!/usr/bin/env python3
"""
Llama Context - Python package for LlamaSearch AI
"""

from setuptools import setup, find_packages

setup(
    name="llama_context",
    version="0.1.0",
    description="[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)]() <!-- Add appropriate Python version support -->",
    long_description="""# llama-context

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)]() <!-- Add appropriate Python version support -->

## Installation

```bash
pip install -e .
```

## Usage

```python
from llama_context import LlamaContextClient

# Initialize the client
client = LlamaContextClient(api_key="your-api-key")
result = client.query("your query")
print(result)
```

## Features

- Fast and efficient
- Easy to use API
- Comprehensive documentation
- Asynchronous support

## Development

### Setup

```bash
# Clone the repository
git clone https://github.com/nikjois/llama-context.git
cd llama-context

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
    url="https://github.com/llamasearchai/llama-context",
    project_urls={
        "Documentation": "https://github.com/llamasearchai/llama-context",
        "Bug Tracker": "https://github.com/llamasearchai/llama-context/issues",
        "Source Code": "https://github.com/llamasearchai/llama-context",
    },
    packages='src.llama_context',
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
