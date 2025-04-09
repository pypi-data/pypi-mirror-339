"""Registry for agent implementations.

This module provides a registry of available agent implementations and
utilities for creating agent instances.
"""

import importlib
import inspect
from typing import Dict, Optional, Type

from llama_simulation.agents.base import Agent

# Registry of available agents
_AGENT_REGISTRY: Dict[str, Type[Agent]] = {}
_AGENT_DESCRIPTIONS: Dict[str, str] = {}


def register_agent(name: str, description: str = ""):
    """Register an agent class in the registry.

    This decorator registers an agent class in the global registry,
    making it available for use in simulations.

    Args:
        name: Name to register the agent under.
        description: Description of the agent.

    Returns:
        Callable: Decorator function.
    """

    def _register(cls):
        if not inspect.isclass(cls) or not issubclass(cls, Agent):
            raise TypeError(f"Class {cls.__name__} is not a subclass of Agent")

        _AGENT_REGISTRY[name] = cls
        _AGENT_DESCRIPTIONS[name] = description

        return cls

    return _register


def create_agent(agent_type: str, **kwargs) -> Agent:
    """Create an agent instance of the specified type.

    Args:
        agent_type: Type of agent to create.
        **kwargs: Additional keyword arguments to pass to the agent constructor.

    Returns:
        Agent: Created agent instance.

    Raises:
        ValueError: If the specified agent type is not found in the registry.
    """
    # Check if agent type is in the registry
    if agent_type not in _AGENT_REGISTRY:
        # Try to import agent
        try:
            module_path = f"llama_simulation.agents.{agent_type.lower()}"
            importlib.import_module(module_path)
        except ImportError:
            raise ValueError(f"Unknown agent type: {agent_type}")

    # Check again after potential import
    if agent_type not in _AGENT_REGISTRY:
        raise ValueError(f"Agent type {agent_type} not registered")

    # Create agent instance
    agent_cls = _AGENT_REGISTRY[agent_type]
    agent = agent_cls(**kwargs)

    return agent


def list_available_agents() -> Dict[str, str]:
    """List all available agents in the registry.

    Returns:
        Dict[str, str]: Dictionary mapping agent names to descriptions.
    """
    # Import built-in agents to ensure they are registered

    return _AGENT_DESCRIPTIONS


# Import and register basic agent types
from llama_simulation.agents.policy import MLXPolicyNetwork


@register_agent("MLXPolicyAgent", "Agent using MLX policy network")
class MLXPolicyAgent(Agent):
    """Agent using MLX policy network for decision making.

    Attributes:
        policy_network: MLX policy network.
    """

    def __init__(
        self,
        state_dim: int = 4,
        action_dim: int = 2,
        hidden_dims: list = [64, 64],
        continuous_actions: bool = False,
        id: Optional[str] = None,
        name: Optional[str] = None,
    ):
        """Initialize a new MLXPolicyAgent.

        Args:
            state_dim: Dimension of the state space.
            action_dim: Dimension of the action space.
            hidden_dims: Dimensions of hidden layers.
            continuous_actions: Whether actions are continuous.
            id: Unique identifier for this agent.
            name: Human-readable name of this agent.
        """
        super().__init__(id=id, name=name)

        self.state_dim = state_dim
        self.action_dim = action_dim
        self.hidden_dims = hidden_dims
        self.continuous_actions = continuous_actions

        # Create policy network
        self.policy_network = MLXPolicyNetwork(
            state_dim=state_dim,
            action_dim=action_dim,
            hidden_dims=hidden_dims,
            continuous=continuous_actions,
        )

    def act(self, observation):
        """Select an action based on the current observation.

        Args:
            observation: Current observation from the environment.

        Returns:
            Any: Selected action.
        """
        # Convert observation to array
        if not isinstance(observation, mx.array):
            observation = mx.array(observation)

        # Add batch dimension if needed
        if len(observation.shape) == 1:
            observation = observation.reshape(1, -1)

        # Get action from policy network
        action = self.policy_network.sample(observation)[0]

        # Convert to appropriate format
        if self.continuous_actions:
            action = action.tolist()
        else:
            action = int(action.item())

        return action

    def _get_params(self):
        """Get agent-specific parameters."""
        return {
            "state_dim": self.state_dim,
            "action_dim": self.action_dim,
            "hidden_dims": self.hidden_dims,
            "continuous_actions": self.continuous_actions,
        }

    def _set_params(self, params):
        """Set agent-specific parameters."""
        self.state_dim = params.get("state_dim", self.state_dim)
        self.action_dim = params.get("action_dim", self.action_dim)
        self.hidden_dims = params.get("hidden_dims", self.hidden_dims)
        self.continuous_actions = params.get("continuous_actions", self.continuous_actions)

        # Recreate policy network with new parameters
        self.policy_network = MLXPolicyNetwork(
            state_dim=self.state_dim,
            action_dim=self.action_dim,
            hidden_dims=self.hidden_dims,
            continuous=self.continuous_actions,
        )


# Import mx module
import mlx.core as mx
