"""Registry for environment implementations.

This module provides a registry of available environment implementations and
utilities for creating environment instances.
"""

import importlib
import inspect
from typing import Dict, Optional, Type

from llama_simulation.environments.base import Environment

# Registry of available environments
_ENVIRONMENT_REGISTRY: Dict[str, Type[Environment]] = {}
_ENVIRONMENT_DESCRIPTIONS: Dict[str, str] = {}


def register_environment(name: str, description: str = ""):
    """Register an environment class in the registry.

    This decorator registers an environment class in the global registry,
    making it available for use in simulations.

    Args:
        name: Name to register the environment under.
        description: Description of the environment.

    Returns:
        Callable: Decorator function.
    """

    def _register(cls):
        if not inspect.isclass(cls) or not issubclass(cls, Environment):
            raise TypeError(f"Class {cls.__name__} is not a subclass of Environment")

        _ENVIRONMENT_REGISTRY[name] = cls
        _ENVIRONMENT_DESCRIPTIONS[name] = description

        return cls

    return _register


def create_environment(env_type: str, **kwargs) -> Environment:
    """Create an environment instance of the specified type.

    Args:
        env_type: Type of environment to create.
        **kwargs: Additional keyword arguments to pass to the environment constructor.

    Returns:
        Environment: Created environment instance.

    Raises:
        ValueError: If the specified environment type is not found in the registry.
    """
    # Check if environment type is in the registry
    if env_type not in _ENVIRONMENT_REGISTRY:
        # Try to import environment
        try:
            module_path = f"llama_simulation.environments.{env_type.lower()}"
            importlib.import_module(module_path)
        except ImportError:
            raise ValueError(f"Unknown environment type: {env_type}")

    # Check again after potential import
    if env_type not in _ENVIRONMENT_REGISTRY:
        raise ValueError(f"Environment type {env_type} not registered")

    # Create environment instance
    env_cls = _ENVIRONMENT_REGISTRY[env_type]
    env = env_cls(**kwargs)

    return env


def list_available_environments() -> Dict[str, str]:
    """List all available environments in the registry.

    Returns:
        Dict[str, str]: Dictionary mapping environment names to descriptions.
    """
    # Import built-in environments to ensure they are registered

    return _ENVIRONMENT_DESCRIPTIONS


# Import and register the FederatedLearningEnv environment
from llama_simulation.environments.federated.base import FederatedLearningEnv

register_environment(
    "FederatedLearningEnv",
    "Environment for simulating federated learning scenarios with MLX acceleration",
)(FederatedLearningEnv)


# Import and register a MockEnvironment for testing
@register_environment("MockEnvironment", "Simple environment for testing")
class MockEnvironment(Environment):
    """Simple environment for testing purposes.

    This environment provides a basic implementation for testing
    agents and simulation components.
    """

    def __init__(
        self,
        state_dim: int = 4,
        action_dim: int = 2,
        num_agents: int = 1,
        max_steps: int = 100,
        id: Optional[str] = None,
        name: Optional[str] = None,
    ):
        """Initialize a new MockEnvironment.

        Args:
            state_dim: Dimension of the state space.
            action_dim: Dimension of the action space.
            num_agents: Number of agents in this environment.
            max_steps: Maximum steps before episode termination.
            id: Unique identifier for this environment.
            name: Human-readable name of this environment.
        """
        super().__init__(
            id=id,
            name=name,
            state_dim=state_dim,
            action_dim=action_dim,
            num_agents=num_agents,
        )

        self.max_steps = max_steps
        self.current_step = 0

        try:
            import mlx.core as mx

            self.state = mx.zeros((state_dim,))
        except ImportError:
            import numpy as np

            self.state = np.zeros((state_dim,))

    def reset(self):
        """Reset the environment to its initial state."""
        super().reset()

        self.current_step = 0

        try:
            import mlx.core as mx

            self.state = mx.random.normal((self.state_dim,))
        except ImportError:
            import numpy as np

            self.state = np.random.normal(size=(self.state_dim,))

        return self.state

    def step(self, actions):
        """Take a step in the environment."""
        super().step(actions)

        # Convert actions to list if not already
        if not isinstance(actions, list):
            actions = [actions]

        # Simulate next state and reward
        try:
            import mlx.core as mx

            self.state = mx.random.normal((self.state_dim,))
            rewards = mx.array([float(a) for a in actions])
        except ImportError:
            import numpy as np

            self.state = np.random.normal(size=(self.state_dim,))
            rewards = np.array([float(a) for a in actions])

        # Update state
        self.current_step += 1
        done = self.current_step >= self.max_steps

        # Prepare info
        info = {
            "current_step": self.current_step,
            "metrics": {
                "reward": float(sum(rewards)) / len(rewards),
                "steps": self.current_step,
            },
        }

        return self.state, rewards, done, info

    def _get_params(self):
        """Get environment-specific parameters."""
        return {
            "state_dim": self.state_dim,
            "action_dim": self.action_dim,
            "num_agents": self.num_agents,
            "max_steps": self.max_steps,
        }

    def _set_params(self, params):
        """Set environment-specific parameters."""
        self.state_dim = params.get("state_dim", self.state_dim)
        self.action_dim = params.get("action_dim", self.action_dim)
        self.num_agents = params.get("num_agents", self.num_agents)
        self.max_steps = params.get("max_steps", self.max_steps)
