"""Federated Learning environments for AI simulation.

This package provides environments for federated learning simulation,
enabling research on privacy-preserving collaborative machine learning.
"""

from llama_simulation.environments.federated.base import (
    FederatedClient,
    FederatedLearningEnv,
)

__all__ = ["FederatedClient", "FederatedLearningEnv"]
