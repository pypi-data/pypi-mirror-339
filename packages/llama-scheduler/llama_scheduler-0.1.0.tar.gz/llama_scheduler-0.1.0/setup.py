#!/usr/bin/env python3
"""
Llama Scheduler - Python package for LlamaSearch AI
"""

from setuptools import setup, find_packages

setup(
    name="llama_scheduler",
    version="0.1.0",
    description="[![PyPI version](https://badge.fury.io/py/llama-scheduler.svg)](https://badge.fury.io/py/llama-scheduler)
[![Python Version](https://img.shields.io/pypi/pyversions/llama-scheduler.svg)](https://pypi.org/project/llama-scheduler/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/yourusername/llama-scheduler-pkg/actions/workflows/ci.yml/badge.svg)](https://github.com/yourusername/llama-scheduler-pkg/actions/workflows/ci.yml)",
    long_description="""# llama-scheduler

[![PyPI version](https://badge.fury.io/py/llama-scheduler.svg)](https://badge.fury.io/py/llama-scheduler)
[![Python Version](https://img.shields.io/pypi/pyversions/llama-scheduler.svg)](https://pypi.org/project/llama-scheduler/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/yourusername/llama-scheduler-pkg/actions/workflows/ci.yml/badge.svg)](https://github.com/yourusername/llama-scheduler-pkg/actions/workflows/ci.yml)

## Installation

```bash
pip install -e .
```

## Usage

```python
from llama_scheduler import LlamaSchedulerClient

# Initialize the client
client = LlamaSchedulerClient(api_key="your-api-key")
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
git clone https://github.com/nikjois/llama-scheduler.git
cd llama-scheduler

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
    url="https://github.com/llamasearchai/llama-scheduler",
    project_urls={
        "Documentation": "https://github.com/llamasearchai/llama-scheduler",
        "Bug Tracker": "https://github.com/llamasearchai/llama-scheduler/issues",
        "Source Code": "https://github.com/llamasearchai/llama-scheduler",
    },
    packages='src.llama_scheduler',
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
