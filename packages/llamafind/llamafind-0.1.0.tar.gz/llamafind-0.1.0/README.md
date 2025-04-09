# llama-find

[![PyPI version](https://img.shields.io/pypi/v/llama_find.svg)](https://pypi.org/project/llama_find/)
[![License](https://img.shields.io/github/license/llamasearchai/llama-find)](https://github.com/llamasearchai/llama-find/blob/main/LICENSE)
[![Python Version](https://img.shields.io/pypi/pyversions/llama_find.svg)](https://pypi.org/project/llama_find/)
[![CI Status](https://github.com/llamasearchai/llama-find/actions/workflows/llamasearchai_ci.yml/badge.svg)](https://github.com/llamasearchai/llama-find/actions/workflows/llamasearchai_ci.yml)

**Llama Find (llama-find)** is a sophisticated search and information retrieval toolkit within the LlamaSearch AI ecosystem. It provides agents capable of querying multiple underlying search engines, processing results, and delivering synthesized information through a unified API. It includes support for MLX optimizations.

## Key Features

- **Agent-Based Search:** Utilizes intelligent agents to manage search queries.
- **Multi-Engine Support:** Integrates with various search backends (defined in `search_engines/`).
- **API Access:** Exposes functionality through a comprehensive API (`api.py`).
- **Web Interface (Optional):** Includes components for a basic web server (`web_server.py`).
- **MLX Compatibility:** Offers potential performance benefits on compatible hardware (`mlx_compat.py`).
- **Caching:** Implements caching (`cache/`) to improve response times.
- **Configurable:** Allows customization via configuration files (`config.py`, `config/`).

## Installation

```bash
pip install llama-find
# Or install directly from GitHub for the latest version:
# pip install git+https://github.com/llamasearchai/llama-find.git
```

## Usage

*(Usage examples for the API client or web interface will be added here based on the final implementation.)*

```python
# Placeholder for Python client usage
# from llama_find import FinderClient

# client = FinderClient(config_path="path/to/config.yaml")
# results = client.search("your query here", engine="auto")
# print(results)
```

## Architecture Overview

```mermaid
graph TD
    A[User / Client Application] --> B{API Layer (api.py / web_server.py)};
    B --> C{Search Agent (agents/)};
    C --> D[Core Processing (core.py)];
    D --> E{Search Engine Interface};
    E --> F[Search Engine 1];
    E --> G[Search Engine 2];
    E --> H[...];
    F --> I((External Search Service));
    G --> I;
    D --> J[Cache System (cache/)];
    D --> K[MLX Compatibility Layer (mlx_compat.py)];
    B --> L[Configuration (config.py, config/)];
    C --> L;
    D --> L;

    style D fill:#f9f,stroke:#333,stroke-width:2px
    style J fill:#ccf,stroke:#333,stroke-width:1px
```

1.  **Entry Point:** Users or client applications interact via the API or web server.
2.  **API Layer:** Handles incoming requests and routes them.
3.  **Search Agent:** Manages the query lifecycle and interacts with core components.
4.  **Core Processing:** Orchestrates the search, potentially leveraging MLX and caching.
5.  **Search Engine Interface:** Abstracts interactions with different backend search engines.
6.  **Cache/Config:** Caching improves speed; configuration allows customization.

## Configuration

*(Details on configuring search engines, API keys, caching, etc., will be added here.)*

## Development

### Setup

```bash
# Clone the repository
git clone https://github.com/llamasearchai/llama-find.git
cd llama-find

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
