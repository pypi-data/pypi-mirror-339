"""Base Environment module for the llama_simulation framework.

This module provides the abstract base class for all environments in
the simulation framework. It defines the interface that environments
must implement to interact with agents.
"""

import abc
from typing import Any, Dict, List, Optional, Tuple, Union

import mlx.core as mx
import numpy as np


class Environment(abc.ABC):
    """Abstract base class for all environments in the simulation framework.

    This class defines the interface that all environments must implement
    to interact with agents in the simulation.

    Attributes:
        id: Unique identifier for this environment.
        name: Human-readable name of this environment.
        state_dim: Dimension of the state space.
        action_dim: Dimension of the action space.
        num_agents: Number of agents in this environment.
        continuous_actions: Whether actions are continuous.
    """

    def __init__(
        self,
        id: Optional[str] = None,
        name: Optional[str] = None,
        state_dim: int = 0,
        action_dim: int = 0,
        num_agents: int = 1,
        continuous_actions: bool = False,
    ) -> None:
        """Initialize a new Environment.

        Args:
            id: Unique identifier for this environment.
                If None, a random UUID will be generated.
            name: Human-readable name of this environment.
                If None, a default name will be generated.
            state_dim: Dimension of the state space.
            action_dim: Dimension of the action space.
            num_agents: Number of agents in this environment.
            continuous_actions: Whether actions are continuous.
        """
        import uuid

        self.id = id or str(uuid.uuid4())
        self.name = name or f"Environment-{self.id[:8]}"
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.num_agents = num_agents
        self.continuous_actions = continuous_actions
        self.step_count = 0
        self.episode_count = 0
        self.metrics: Dict[str, List[float]] = {}

    @abc.abstractmethod
    def reset(self) -> Any:
        """Reset the environment to its initial state.

        Returns:
            Any: Initial observation.
        """
        self.step_count = 0
        self.episode_count += 1
        return None

    @abc.abstractmethod
    def step(self, actions: Union[Any, List[Any]]) -> Tuple[Any, Any, bool, Dict[str, Any]]:
        """Take a step in the environment.

        Args:
            actions: Action(s) to take.
                For multi-agent environments, this should be a list of actions.
                For single-agent environments, this can be a single action.

        Returns:
            Tuple[Any, Any, bool, Dict[str, Any]]:
                - observation: Next observation.
                - reward: Reward(s) received.
                - done: Whether the episode is done.
                - info: Additional information.
        """
        self.step_count += 1
        return None, None, False, {}

    def render(self, mode: str = "human") -> Optional[Any]:
        """Render the environment.

        Args:
            mode: Rendering mode.
                - "human": Render to the current display or terminal.
                - "rgb_array": Return an RGB array.
                - "ansi": Return a string (e.g., for text environments).

        Returns:
            Optional[Any]: Rendered frame depending on the mode.
        """
        return None

    def close(self) -> None:
        """Clean up the environment."""
        pass

    def get_agent_observation(self, agent_id: int, observation: Any) -> Any:
        """Get observation for a specific agent.

        For multi-agent environments, this method should return the specific
        observation for the given agent. For single-agent environments,
        this will typically just return the observation unchanged.

        Args:
            agent_id: ID of the agent.
            observation: Full observation from the environment.

        Returns:
            Any: Agent-specific observation.
        """
        if self.num_agents == 1 or agent_id == 0:
            return observation

        if isinstance(observation, list) and agent_id < len(observation):
            return observation[agent_id]

        if isinstance(observation, dict) and str(agent_id) in observation:
            return observation[str(agent_id)]

        return observation

    def seed(self, seed: Optional[int] = None) -> List[int]:
        """Set random seed for environment randomness.

        Args:
            seed: Random seed.

        Returns:
            List[int]: List of seeds used.
        """
        if seed is not None:
            np.random.seed(seed)
            mx.random.seed(seed)
        return [seed]

    def get_state(self) -> Dict[str, Any]:
        """Get the current state of the environment.

        Returns:
            Dict[str, Any]: Environment state dictionary.
        """
        return {
            "id": self.id,
            "name": self.name,
            "type": self.__class__.__name__,
            "state_dim": self.state_dim,
            "action_dim": self.action_dim,
            "num_agents": self.num_agents,
            "continuous_actions": self.continuous_actions,
            "step_count": self.step_count,
            "episode_count": self.episode_count,
            "metrics": self.metrics,
            "params": self._get_params(),
        }

    def set_state(self, state: Dict[str, Any]) -> None:
        """Set the environment state from a state dictionary.

        Args:
            state: State dictionary from get_state().
        """
        self.id = state["id"]
        self.name = state["name"]
        self.state_dim = state["state_dim"]
        self.action_dim = state["action_dim"]
        self.num_agents = state["num_agents"]
        self.continuous_actions = state["continuous_actions"]
        self.step_count = state["step_count"]
        self.episode_count = state["episode_count"]
        self.metrics = state["metrics"]
        self._set_params(state["params"])

    def _get_params(self) -> Dict[str, Any]:
        """Get environment-specific parameters.

        Returns:
            Dict[str, Any]: Environment parameters.
        """
        return {}

    def _set_params(self, params: Dict[str, Any]) -> None:
        """Set environment-specific parameters.

        Args:
            params: Environment parameters from _get_params().
        """
        pass

    def add_metric(self, name: str, value: float) -> None:
        """Add a metric value to the metrics history.

        Args:
            name: Name of the metric.
            value: Value of the metric.
        """
        if name not in self.metrics:
            self.metrics[name] = []
        self.metrics[name].append(value)

    def get_metrics(self) -> Dict[str, List[float]]:
        """Get all collected metrics.

        Returns:
            Dict[str, List[float]]: Dictionary of metric histories.
        """
        return self.metrics

    def get_metric_mean(self, name: str) -> float:
        """Get the mean of a metric.

        Args:
            name: Name of the metric.

        Returns:
            float: Mean value of the metric.
        """
        if name not in self.metrics or not self.metrics[name]:
            return 0.0

        return np.mean(self.metrics[name])
