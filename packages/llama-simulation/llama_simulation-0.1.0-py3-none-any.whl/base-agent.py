"""Base Agent module for the llama_simulation framework.

This module provides the abstract base classes for implementing agents
that interact with simulation environments. It includes the core Agent class
and utilities for policy-based agents using MLX neural networks.
"""

import abc
from typing import Optional


class Agent(abc.ABC):
    """Abstract base class for all agents in the simulation framework.

    This class defines the interface that all agents must implement to
    interact with environments in the simulation.

    Attributes:
        id: Unique identifier for this agent.
        name: Human-readable name of this agent.
    """

    def __init__(self, id: Optional[str] = None, name: Optional[str] = None) -> None:
        """Initialize a new Agent.

        Args:
            id: Unique identifier for this agent.
                If None, a random UUID will be generated.
            name: Human-readable name of this agent.
                If None, a default name will be generated.
        """
        import uuid

        self.id = id or str(uuid.uuid4())
        self.name = name or f
