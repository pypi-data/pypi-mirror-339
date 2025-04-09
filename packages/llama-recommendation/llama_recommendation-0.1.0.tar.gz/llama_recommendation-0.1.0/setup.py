#!/usr/bin/env python3
"""
Llama Recommendation - Python package for LlamaSearch AI
"""

from setuptools import setup, find_packages

setup(
    name="llama_recommendation",
    version="0.1.0",
    description="A privacy-preserving, multi-modal, graph-based recommendation system with causal and ethical components.",
    long_description="""# llama-recommendation

A privacy-preserving, multi-modal, graph-based recommendation system with causal and ethical components.

## Installation

```bash
pip install -e .
```

## Usage

```python
from llama_recommendation import LlamaRecommendationClient

# Initialize the client
client = LlamaRecommendationClient(api_key="your-api-key")
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
git clone https://github.com/nikjois/llama-recommendation.git
cd llama-recommendation

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
    url="https://github.com/llamasearchai/llama-recommendation",
    project_urls={
        "Documentation": "https://github.com/llamasearchai/llama-recommendation",
        "Bug Tracker": "https://github.com/llamasearchai/llama-recommendation/issues",
        "Source Code": "https://github.com/llamasearchai/llama-recommendation",
    },
    packages='src.llama_recommendation',
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
