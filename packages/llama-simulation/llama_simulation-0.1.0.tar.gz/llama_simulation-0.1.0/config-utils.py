"""Configuration utilities for llama_simulation.

This module provides configuration classes and utilities for managing
simulation configurations.
"""

import os
from dataclasses import dataclass, field
from typing import Any, Dict, List

import yaml


@dataclass
class SimulationConfig:
    """Configuration for simulation runs.

    Attributes:
        random_seed: Random seed for reproducibility.
        log_level: Logging level.
        results_dir: Directory for saving results.
        metrics: List of metrics to track.
        render: Whether to render the environment during simulation.
    """

    random_seed: int = 42
    log_level: str = "INFO"
    results_dir: str = "./results"
    metrics: List[str] = field(default_factory=lambda: ["reward", "steps"])
    render: bool = False
    max_episodes: int = 1000
    max_steps_per_episode: int = 1000
    checkpoint_frequency: int = 100
    device: str = "gpu"  # "cpu" or "gpu"

    def __post_init__(self):
        """Initialize derived attributes and create directories."""
        # Create results directory
        os.makedirs(self.results_dir, exist_ok=True)

    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary.

        Returns:
            Dict[str, Any]: Configuration as dictionary.
        """
        return {
            "random_seed": self.random_seed,
            "log_level": self.log_level,
            "results_dir": self.results_dir,
            "metrics": self.metrics,
            "render": self.render,
            "max_episodes": self.max_episodes,
            "max_steps_per_episode": self.max_steps_per_episode,
            "checkpoint_frequency": self.checkpoint_frequency,
            "device": self.device,
        }

    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> "SimulationConfig":
        """Create config from dictionary.

        Args:
            config_dict: Configuration dictionary.

        Returns:
            SimulationConfig: Configuration object.
        """
        return cls(**config_dict)

    def save(self, path: str) -> None:
        """Save configuration to YAML file.

        Args:
            path: Path to save the configuration.
        """
        with open(path, "w") as f:
            yaml.dump(self.to_dict(), f)

    @classmethod
    def load(cls, path: str) -> "SimulationConfig":
        """Load configuration from YAML file.

        Args:
            path: Path to load the configuration from.

        Returns:
            SimulationConfig: Loaded configuration.
        """
        with open(path, "r") as f:
            config_dict = yaml.safe_load(f)

        return cls.from_dict(config_dict)


def get_env_config(key: str, default: Any = None) -> Any:
    """Get configuration value from environment variable.

    Args:
        key: Environment variable key.
        default: Default value if the environment variable is not set.

    Returns:
        Any: Configuration value.
    """
    env_key = f"LLAMA_SIM_{key.upper()}"
    value = os.environ.get(env_key)

    if value is None:
        return default

    # Convert to appropriate type
    if isinstance(default, bool):
        return value.lower() in ("true", "1", "t", "yes", "y")
    elif isinstance(default, int):
        return int(value)
    elif isinstance(default, float):
        return float(value)
    elif isinstance(default, list):
        return value.split(",")
    else:
        return value
