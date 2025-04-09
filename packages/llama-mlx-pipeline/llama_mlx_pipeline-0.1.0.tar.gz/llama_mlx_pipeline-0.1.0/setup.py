#!/usr/bin/env python3
"""
Llama Mlx Pipeline - Python package for LlamaSearch AI
"""

from setuptools import setup, find_packages

setup(
    name="llama_mlx_pipeline",
    version="0.1.0",
    description="A Local-First Data Extraction Pipeline powered by Apple MLX",
    long_description="""# llama-mlx-pipeline

A Local-First Data Extraction Pipeline powered by Apple MLX

## Installation

```bash
pip install -e .
```

## Usage

```python
from llama_mlx_pipeline import LlamaMlxPipelineClient

# Initialize the client
client = LlamaMlxPipelineClient(api_key="your-api-key")
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
git clone https://github.com/nikjois/llama-mlx-pipeline.git
cd llama-mlx-pipeline

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
    url="https://github.com/llamasearchai/llama-mlx-pipeline",
    project_urls={
        "Documentation": "https://github.com/llamasearchai/llama-mlx-pipeline",
        "Bug Tracker": "https://github.com/llamasearchai/llama-mlx-pipeline/issues",
        "Source Code": "https://github.com/llamasearchai/llama-mlx-pipeline",
    },
    packages='src.llama_mlx_pipeline',
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
