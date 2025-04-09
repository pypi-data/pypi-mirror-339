# llama-distributed

[![PyPI version](https://img.shields.io/pypi/v/llama_distributed.svg)](https://pypi.org/project/llama_distributed/)
[![License](https://img.shields.io/github/license/llamasearchai/llama-distributed)](https://github.com/llamasearchai/llama-distributed/blob/main/LICENSE)
[![Python Version](https://img.shields.io/pypi/pyversions/llama_distributed.svg)](https://pypi.org/project/llama_distributed/)
[![CI Status](https://github.com/llamasearchai/llama-distributed/actions/workflows/llamasearchai_ci.yml/badge.svg)](https://github.com/llamasearchai/llama-distributed/actions/workflows/llamasearchai_ci.yml)

**Llama Distributed (llama-distributed)** is a toolkit within the LlamaSearch AI ecosystem designed for distributing tasks or packages across multiple nodes or environments. It likely aids in packaging applications and managing their deployment or execution in a distributed setting.

## Key Features

- **Package Distribution:** Core logic related to packaging and distributing Python applications or tasks (`package.py`).
- **Deployment Management (Potential):** May include tools for deploying packages to target environments.
- **Task Execution (Potential):** Could support running distributed tasks or parallel processing.
- **Core Module:** Manages the distribution process (`core.py`).
- **Configurable:** Allows specifying target environments, package details, and distribution methods (`config.py`).

## Installation

```bash
pip install llama-distributed
# Or install directly from GitHub for the latest version:
# pip install git+https://github.com/llamasearchai/llama-distributed.git
```

## Usage

*(Usage examples for packaging and distributing applications or tasks will be added here.)*

```python
# Placeholder for Python client usage
# from llama_distributed import Distributor, PackageConfig

# config = PackageConfig.load("config.yaml")
# distributor = Distributor(config)

# # Define package or task
# package_path = "/path/to/my_app"
# target_nodes = ["node1.example.com", "node2.example.com"]

# # Distribute the package
# distribution_job = distributor.distribute(
#     package_path=package_path,
#     targets=target_nodes,
#     options={'run_command': 'python main.py'}
# )
# print(f"Distribution job started: {distribution_job.id}")
```

## Architecture Overview

```mermaid
graph TD
    A[User / Build System] --> B{Core Distributor (core.py)};
    B --> C{Packaging Logic (package.py)};
    C --> D[Packaged Application / Task];
    B -- Uses --> E{Deployment / Execution Interface};
    E -- Deploys/Runs on --> F[Target Node 1];
    E -- Deploys/Runs on --> G[Target Node 2];
    E -- Deploys/Runs on --> H[...];

    I[Configuration (config.py)] -- Configures --> B;
    I -- Configures --> C;
    I -- Configures --> E;

    style B fill:#f9f,stroke:#333,stroke-width:2px
    style F fill:#ccf,stroke:#333,stroke-width:1px
    style G fill:#ccf,stroke:#333,stroke-width:1px
    style H fill:#ccf,stroke:#333,stroke-width:1px
```

1.  **Input:** User or a build system triggers the distribution process.
2.  **Core Distributor:** Manages the workflow based on configuration.
3.  **Packaging:** The application or task is packaged for distribution.
4.  **Deployment/Execution:** The packaged artifact is sent to target nodes and potentially executed.
5.  **Targets:** Represents the remote machines or environments where the package is distributed.
6.  **Configuration:** Defines the package source, target nodes, deployment methods, execution commands, etc.

## Configuration

*(Details on configuring source packages, target node addresses/credentials, distribution protocols (SSH, etc.), post-deployment commands, etc., will be added here.)*

## Development

### Setup

```bash
# Clone the repository
git clone https://github.com/llamasearchai/llama-distributed.git
cd llama-distributed

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
