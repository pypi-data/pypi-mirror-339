# llama-mlx-pipeline

[![PyPI version](https://img.shields.io/pypi/v/llama_mlx_pipeline.svg)](https://pypi.org/project/llama_mlx_pipeline/)
[![License](https://img.shields.io/github/license/llamasearchai/llama-mlx-pipeline)](https://github.com/llamasearchai/llama-mlx-pipeline/blob/main/LICENSE)
[![Python Version](https://img.shields.io/pypi/pyversions/llama_mlx_pipeline.svg)](https://pypi.org/project/llama_mlx_pipeline/)
[![CI Status](https://github.com/llamasearchai/llama-mlx-pipeline/actions/workflows/llamasearchai_ci.yml/badge.svg)](https://github.com/llamasearchai/llama-mlx-pipeline/actions/workflows/llamasearchai_ci.yml)

**Llama MLX Pipeline (llama-mlx-pipeline)** provides tools and components for building efficient data processing pipelines, specifically optimized for Apple Silicon using the MLX framework. It focuses on tasks like data scraping, chunking, and feature extraction.

## Key Features

- **MLX Optimization:** Designed to leverage Apple's MLX framework for high performance on M-series chips.
- **Data Scraping:** Includes components for fetching data from various sources (`scraper.py`).
- **Data Chunking:** Provides utilities for splitting data into manageable chunks (`chunker.py`).
- **Feature Extraction:** Contains tools for extracting relevant features or information (`extractor.py`).
- **Pipeline Core:** A central module (`core.py`) likely orchestrates pipeline stages.
- **Configurable:** Supports configuration via `config.py`.

## Installation

```bash
pip install llama-mlx-pipeline
# Or install directly from GitHub for the latest version:
# pip install git+https://github.com/llamasearchai/llama-mlx-pipeline.git
```

## Usage

*(Usage examples demonstrating pipeline creation and execution will be added here.)*

```python
# Placeholder for Python client usage
# from llama_mlx_pipeline import PipelineBuilder, MLXConfig

# config = MLXConfig.load("path/to/config.yaml")
# builder = PipelineBuilder(config)

# pipeline = builder.add_scraper(source="web", url="...") \
#                   .add_chunker(size=512) \
#                   .add_extractor(model="bert-base") \
#                   .build()

# results = pipeline.run(input_data="...")
# print(results)
```

## Architecture Overview

```mermaid
graph TD
    A[Input Data Source] --> B{Scraper (scraper.py)};
    B --> C{Chunker (chunker.py)};
    C --> D{Extractor (extractor.py)};
    D --> E[Processed Output];

    F[Pipeline Orchestrator (core.py)] -- Manages --> B;
    F -- Manages --> C;
    F -- Manages --> D;

    G[Configuration (config.py)] -- Configures --> F;
    G -- Configures --> B;
    G -- Configures --> C;
    G -- Configures --> D;

    subgraph MLX Optimized Components
        direction LR
        B;
        C;
        D;
    end

    style F fill:#f9f,stroke:#333,stroke-width:2px
```

1.  **Input:** Data enters the pipeline.
2.  **Scraper:** Fetches or loads the initial data.
3.  **Chunker:** Splits data into smaller pieces.
4.  **Extractor:** Processes chunks to extract features or information.
5.  **Output:** The final processed data is produced.
6.  **Orchestrator:** The `core.py` module likely manages the flow and execution of these stages, configured by `config.py`.

## Configuration

*(Details on configuring pipeline stages, MLX settings, etc., will be added here.)*

## Development

### Setup

```bash
# Clone the repository
git clone https://github.com/llamasearchai/llama-mlx-pipeline.git
cd llama-mlx-pipeline

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
