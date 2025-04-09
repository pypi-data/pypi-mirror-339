# llama-integration

[![PyPI version](https://img.shields.io/pypi/v/llama_integration.svg)](https://pypi.org/project/llama_integration/)
[![License](https://img.shields.io/github/license/llamasearchai/llama-integration)](https://github.com/llamasearchai/llama-integration/blob/main/LICENSE)
[![Python Version](https://img.shields.io/pypi/pyversions/llama_integration.svg)](https://pypi.org/project/llama_integration/)
[![CI Status](https://github.com/llamasearchai/llama-integration/actions/workflows/llamasearchai_ci.yml/badge.svg)](https://github.com/llamasearchai/llama-integration/actions/workflows/llamasearchai_ci.yml)

**Llama Integration (llama-integration)** is a toolkit providing components for integrating LlamaSearch AI functionalities with external systems and managing common infrastructure tasks. It includes modules for API gateway implementation, routing, external provider interaction (e.g., OpenAI), API key management, data masking (HIPAA), and model routing/conversion (MLX, CoreML).

## Key Features

- **API Gateway:** Components for building or interacting with API gateways (`gateway-implementation.py`).
- **Routing:** Logic for routing requests, potentially based on model type or destination (`routing/`, `mlx-router.py`).
- **External Provider Integration:** Base classes and specific implementations for interacting with external AI providers like OpenAI (`base-provider.py`, `openai-provider.py`).
- **API Key Management:** Tools for managing API keys securely (`api-key-manager.py`).
- **Data Masking:** Utilities for masking sensitive data, specifically mentioning HIPAA compliance (`hipaa-masking.py`).
- **Model Conversion/Integration:** Support for CoreML conversion and Trusted Execution Environments (TEE) (`coreml-conversion.py`, `tee-integration.py`).
- **Core Module:** Orchestrates integration tasks (`core.py`).
- **Configuration:** Settings for endpoints, keys, routing rules, etc. (`config.py`).
- **Utilities:** Includes logging and other helper functions (`logging/`, `utils/`).

## Installation

```bash
pip install llama-integration
# Or install directly from GitHub for the latest version:
# pip install git+https://github.com/llamasearchai/llama-integration.git
```

## Usage

*(Usage examples demonstrating gateway configuration, provider interaction, data masking, etc., will be added here.)*

```python
# Placeholder for Python client usage
# from llama_integration import ApiGateway, DataMasker, OpenAIProvider

# # Example: Using the OpenAI Provider
# provider = OpenAIProvider(api_key="sk-...")
# response = provider.generate_completion(prompt="Translate to French: Hello World")
# print(response)

# # Example: Masking data
# masker = DataMasker(mode="hipaa")
# text = "Patient John Doe, DOB 01/01/1980, has diabetes."
# masked_text = masker.mask(text)
# print(masked_text) # Output: Patient [NAME], DOB [DATE], has diabetes.
```

## Architecture Overview

```mermaid
graph TD
    A[External Client / LlamaSearch Service] --> B{API Gateway / Router (gateway, routing, mlx-router)};
    B -- Routes to --> C{External Provider (e.g., OpenAI)};
    B -- Routes to --> D{Internal LlamaSearch Service};
    B -- Routes to --> E{TEE Integration (tee-integration)};

    subgraph Integration Components
        F[API Key Manager]
        G[Data Masker (HIPAA)]
        H[CoreML Converter]
        I[Logging]
        J[Utilities]
    end

    B -- Uses --> F;
    B -- Uses --> G; # Masking might happen at gateway
    B -- Uses --> H; # Conversion might be needed for routing
    B -- Uses --> I;
    B -- Uses --> J;

    K{Core Integration Module (core.py)} -- Manages --> B;
    K -- Manages --> F; K -- Manages --> G; K -- Manages --> H;

    L[Configuration (config.py)] -- Configures --> K;
    L -- Configures --> B;
    L -- Configures --> C;
    L -- Configures --> F;
    L -- Configures --> G;

    style B fill:#f9f,stroke:#333,stroke-width:2px
    style C fill:#ccf,stroke:#333,stroke-width:1px
    style D fill:#ccf,stroke:#333,stroke-width:1px
    style E fill:#ccf,stroke:#333,stroke-width:1px
```

1.  **Entry Point:** Requests come from external clients or other LlamaSearch services.
2.  **Gateway/Router:** The central component handles incoming requests, potentially applying routing rules, authentication (using API Key Manager), data masking, model conversion, or TEE interactions.
3.  **Backend Targets:** Requests are routed to appropriate internal LlamaSearch services or external providers (like OpenAI).
4.  **Supporting Modules:** Key management, masking, conversion, logging, and utilities support the gateway/router functionality.
5.  **Core/Config:** The core module manages these components based on the provided configuration.

## Configuration

*(Details on configuring API endpoints, routing rules, provider API keys, masking rules, TEE settings, logging levels, etc., will be added here.)*

## Development

### Setup

```bash
# Clone the repository
git clone https://github.com/llamasearchai/llama-integration.git
cd llama-integration

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
