"""Environment implementations for the simulation framework.

This package provides environment implementations for the simulation framework,
ranging from basic environments to specialized environments for different domains.
"""

from llama_simulation.environments.base import Environment
from llama_simulation.environments.ethical import EthicalTestCase, EthicalTestEnv
from llama_simulation.environments.federated import (
    FederatedClient,
    FederatedLearningEnv,
)
from llama_simulation.environments.registry import (
    MockEnvironment,
    create_environment,
    list_available_environments,
    register_environment,
)

__all__ = [
    "Environment",
    "EthicalTestCase",
    "EthicalTestEnv",
    "FederatedClient",
    "FederatedLearningEnv",
    "MockEnvironment",
    "create_environment",
    "list_available_environments",
    "register_environment",
]
