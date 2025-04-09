#!/usr/bin/env python3
"""
Llama Find - Python package for LlamaSearch AI
"""

from setuptools import setup, find_packages

setup(
    name="llama_find",
    version="0.1.0",
    description="[![PyPI version](https://badge.fury.io/py/llamafind.svg)](https://badge.fury.io/py/llamafind)
[![Python Version](https://img.shields.io/pypi/pyversions/llamafind.svg)](https://pypi.org/project/llamafind/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/yourusername/llamafind-pkg/actions/workflows/ci.yml/badge.svg)](https://github.com/yourusername/llamafind-pkg/actions/workflows/ci.yml)
[![Documentation Status](https://img.shields.io/badge/docs-latest-blue.svg)](https://yourusername.github.io/llamafind-pkg)",
    long_description="""# llama-find

[![PyPI version](https://badge.fury.io/py/llamafind.svg)](https://badge.fury.io/py/llamafind)
[![Python Version](https://img.shields.io/pypi/pyversions/llamafind.svg)](https://pypi.org/project/llamafind/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/yourusername/llamafind-pkg/actions/workflows/ci.yml/badge.svg)](https://github.com/yourusername/llamafind-pkg/actions/workflows/ci.yml)
[![Documentation Status](https://img.shields.io/badge/docs-latest-blue.svg)](https://yourusername.github.io/llamafind-pkg)

## Installation

```bash
pip install -e .
```

## Usage

```python
from llama_find import LlamaFindClient

# Initialize the client
client = LlamaFindClient(api_key="your-api-key")
result = client.query("your query")
print(result)
```

## Features

- Fast and efficient
- Easy to use API
- Comprehensive documentation
- Built-in caching

## Development

### Setup

```bash
# Clone the repository
git clone https://github.com/nikjois/llama-find.git
cd llama-find

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
    url="https://github.com/llamasearchai/llama-find",
    project_urls={
        "Documentation": "https://github.com/llamasearchai/llama-find",
        "Bug Tracker": "https://github.com/llamasearchai/llama-find/issues",
        "Source Code": "https://github.com/llamasearchai/llama-find",
    },
    packages='src.llama_find',
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
