# llama-vector

[![PyPI version](https://img.shields.io/pypi/v/llama_vector.svg)](https://pypi.org/project/llama_vector/)
[![License](https://img.shields.io/github/license/llamasearchai/llama-vector)](https://github.com/llamasearchai/llama-vector/blob/main/LICENSE)
[![Python Version](https://img.shields.io/pypi/pyversions/llama_vector.svg)](https://pypi.org/project/llama_vector/)
[![CI Status](https://github.com/llamasearchai/llama-vector/actions/workflows/llamasearchai_ci.yml/badge.svg)](https://github.com/llamasearchai/llama-vector/actions/workflows/llamasearchai_ci.yml)

**Llama Vector (llama-vector)** provides tools and abstractions for working with vector embeddings and vector stores within the LlamaSearch AI ecosystem. It facilitates the creation, indexing, querying, and quality assessment of vector representations of data.

## Key Features

- **Embedding Generation:** Tools to create vector embeddings from data (`embedding.py`).
- **Vector Indexing:** Components for building and managing vector indices (`index.py`).
- **Vector Querying:** Functionality to perform similarity searches and other queries on vector stores (`query.py`).
- **Vector Store Abstraction:** Interfaces with different vector database backends (`vector_store.py`).
- **Quality Assessment:** Tools to evaluate the quality of embeddings and search results (`quality.py`).
- **Core Module:** Central orchestration and management (`core.py`).
- **Configurable:** Allows specifying embedding models, vector stores, and other parameters (`config.py`).

## Installation

```bash
pip install llama-vector
# Or install directly from GitHub for the latest version:
# pip install git+https://github.com/llamasearchai/llama-vector.git
```

## Usage

*(Usage examples demonstrating embedding creation, indexing, and querying will be added here.)*

```python
# Placeholder for Python client usage
# from llama_vector import VectorClient, VectorConfig

# config = VectorConfig.load("config.yaml")
# client = VectorClient(config)

# # Create embeddings
# documents = ["doc1 content", "doc2 content"]
# client.add_documents(documents)

# # Query the vector store
# query_vector = client.embed_query("search query")
# results = client.search(query_vector, top_k=5)
# print(results)

# # Assess quality
# quality_metrics = client.assess_quality(ground_truth_data="...")
# print(quality_metrics)
```

## Architecture Overview

```mermaid
graph TD
    A[Input Data] --> B{Embedding Generator (embedding.py)};
    B --> C[Vector Embeddings];

    C --> D{Indexer (index.py)};
    D --> E{Vector Store Interface (vector_store.py)};
    E --> F[(Vector DB / Store)];

    G[Query] --> H{Query Processor (query.py)};
    H -- Needs Embeddings --> B;
    H --> E;
    E --> I[Search Results];

    J{Core Module (core.py)} -- Manages --> B;
    J -- Manages --> D;
    J -- Manages --> H;
    J -- Manages --> K;

    K[Quality Assessor (quality.py)] -- Evaluates --> E;
    K -- Evaluates --> I;
    K --> L[Quality Metrics];

    M[Configuration (config.py)] -- Configures --> J;
    M -- Configures --> B;
    M -- Configures --> E;
    N[Utilities (utils.py)] -- Used by --> B;
    N -- Used by --> D;
    N -- Used by --> H;
    N -- Used by --> K;

    style J fill:#f9f,stroke:#333,stroke-width:2px
    style F fill:#ccf,stroke:#333,stroke-width:1px
```

1.  **Embedding:** Input data is converted into vector embeddings.
2.  **Indexing:** Embeddings are indexed and stored using a vector store interface.
3.  **Querying:** User queries are embedded and used to search the vector store via the query processor.
4.  **Quality:** Tools assess the quality of the stored embeddings and search results.
5.  **Core/Config:** The core module orchestrates these steps, guided by configuration.

## Configuration

*(Details on configuring embedding models, vector store connections, indexing parameters, quality metrics, etc., will be added here.)*

## Development

### Setup

```bash
# Clone the repository
git clone https://github.com/llamasearchai/llama-vector.git
cd llama-vector

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
