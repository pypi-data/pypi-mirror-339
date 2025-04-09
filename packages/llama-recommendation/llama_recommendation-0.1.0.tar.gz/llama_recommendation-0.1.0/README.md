# llama-recommendation

[![PyPI version](https://img.shields.io/pypi/v/llama_recommendation.svg)](https://pypi.org/project/llama_recommendation/)
[![License](https://img.shields.io/github/license/llamasearchai/llama-recommendation)](https://github.com/llamasearchai/llama-recommendation/blob/main/LICENSE)
[![Python Version](https://img.shields.io/pypi/pyversions/llama_recommendation.svg)](https://pypi.org/project/llama_recommendation/)
[![CI Status](https://github.com/llamasearchai/llama-recommendation/actions/workflows/llamasearchai_ci.yml/badge.svg)](https://github.com/llamasearchai/llama-recommendation/actions/workflows/llamasearchai_ci.yml)

**Llama Recommendation (llama-recommendation)** is an advanced and comprehensive toolkit within the LlamaSearch AI ecosystem for building sophisticated recommendation systems. It encompasses a wide range of techniques, including standard collaborative and content-based filtering, multimodal embeddings, graph-based recommendations, federated learning, causal inference, and ethical considerations like fairness and diversity.

## Key Features

- **Core Recommender:** Main recommendation logic and pipelines (`recommender.py`, `core.py`).
- **Candidate Generation:** Methods for generating potential recommendations (`recommendation_candidate.py`).
- **Filtering & Ranking:** Components for filtering candidates and ranking them for final presentation (`recommendation_filtering.py`, `recommendation_ranking.py`).
- **Multimodal Embeddings:** Support for creating and using embeddings from text, images, and potentially other modalities (`text_encoder.py`, `image_encoder.py`, `multimodal_encoder.py`, `embeddings.py`).
- **Graph-Based Methods:** Includes graph neural network approaches (GCN) and relation analysis (`graph_gcn.py`, `graph_relations.py`).
- **Federated Learning:** Components for privacy-preserving distributed model training (`federated_client.py`, `federated_server.py`, `federated_aggregation.py`).
- **Causal Inference:** Tools for uplift modeling and counterfactual analysis in recommendations (`causal_uplift.py`, `causal_counterfactual.py`).
- **Explainability:** Methods for explaining *why* certain recommendations are made (`recommendation_explanation.py`).
- **Ethics & Privacy:** Modules focused on fairness, diversity, privacy preservation, and ethical guidelines (`ethics_fairness.py`, `ethics_diversity.py`, `ethics_guidelines.py`, `privacy.py`).
- **Security:** Utilities for encryption and key management (`security_encryption.py`, `security_keys.py`).
- **Mobile Deployment:** Support for CoreML (`mobile_coreml.py`).
- **Utilities:** Helpers for data loading, configuration, and logging (`utils_data.py`, `utils_config.py`, `utils_logging.py`).

## Installation

```bash
pip install llama-recommendation
# Or install directly from GitHub for the latest version:
# pip install git+https://github.com/llamasearchai/llama-recommendation.git
```

## Usage

*(Usage examples demonstrating how to train models, generate recommendations using different techniques (e.g., federated, causal), and evaluate fairness will be added here.)*

```python
# Placeholder for Python client usage
# from llama_recommendation import Recommender, RecConfig

# config = RecConfig.load("config.yaml")
# recommender = Recommender(config)

# # Train a model (potentially federated)
# # recommender.train(training_data="...")

# # Get recommendations for a user
# user_id = "user123"
# recommendations = recommender.get_recommendations(user_id, context="product_page", top_k=10)

# print(f"Recommendations for {user_id}:")
# for rec in recommendations:
#     explanation = recommender.explain(rec)
#     print(f" - {rec.item_id} (Score: {rec.score:.3f}), Reason: {explanation}")

# # Evaluate fairness
# fairness_metrics = recommender.evaluate_fairness(test_data="...")
# print(f"Fairness Metrics: {fairness_metrics}")
```

## Architecture Overview

```mermaid
graph TD
    subgraph Input Data
        A[User Profiles]
        B[Item Catalog]
        C[Interaction History]
    end

    subgraph Feature Engineering & Embeddings
        D{Data Utils (utils_data.py)}
        E{Encoders (text, image, multimodal)}
        F{Embedding Store (embeddings.py)}
        A --> D; B --> D; C --> D;
        D --> E; E --> F;
    end

    subgraph Core Recommendation Pipeline
        G{Candidate Generation} --> H{Filtering}; H --> I{Ranking}; I --> J[Ranked Recommendations];
        F -- Input --> G;
    end

    subgraph Advanced Modules
        K{Federated Learning (Client/Server/Agg)};
        L{Causal Inference (Uplift/Counterfactual)};
        M{Graph Methods (GCN/Relations)};
        N{Explainability};
        O{Ethics & Privacy (Fairness/Diversity)};
        P{Security (Encryption/Keys)};
        Q{Mobile Export (CoreML)};
    end

    subgraph Orchestration & Config
        R{Core Recommender (recommender.py, core.py)};
        S[Configuration (config.py, utils_config.py)];
        T[Logging (utils_logging.py)];
    end

    R -- Manages --> G; R -- Manages --> H; R -- Manages --> I;
    R -- Uses --> E; R -- Uses --> F;
    R -- Integrates --> K; R -- Integrates --> L; R -- Integrates --> M;
    R -- Integrates --> N; R -- Integrates --> O; R -- Integrates --> P;
    R -- Integrates --> Q;
    S -- Configures --> R;
    T -- Logs from --> R;
    J --> U[Output to User/Application];

    style R fill:#f9f,stroke:#333,stroke-width:2px
    style F fill:#ccf,stroke:#333,stroke-width:1px

```

1.  **Data Input:** User, item, and interaction data is processed.
2.  **Feature Engineering/Embeddings:** Data is encoded into embeddings (potentially multimodal).
3.  **Core Pipeline:** Candidates are generated, filtered, and ranked.
4.  **Advanced Modules:** Federated learning, causal inference, graph methods, explainability, ethics, security, and mobile export components enhance or modify the core pipeline.
5.  **Orchestration:** The main recommender component manages the overall workflow, configured via settings.
6.  **Output:** Ranked and potentially explained/fair recommendations are provided.

## Configuration

*(Details on configuring data sources, embedding models, recommendation algorithms (collaborative, content, graph, federated), causal models, fairness metrics, privacy settings, etc., will be added here.)*

## Development

### Setup

```bash
# Clone the repository
git clone https://github.com/llamasearchai/llama-recommendation.git
cd llama-recommendation

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
