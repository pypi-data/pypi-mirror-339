"""SimulationLab module for orchestrating agent-environment simulations.

This module provides the core simulation functionality for running multi-agent
simulations in various environments. It handles the interaction between agents
and environments, metrics collection, and result visualization.
"""

import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

import mlx.core as mx
import numpy as np
import pandas as pd
from llama_simulation.agents.base import Agent
from llama_simulation.environments.base import Environment
from llama_simulation.utils.config import SimulationConfig
from loguru import logger
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn


@dataclass
class SimulationResult:
    """Container for simulation results.

    Attributes:
        metrics: Dictionary of metrics collected during simulation.
        agent_states: Final states of all agents.
        environment_state: Final state of the environment.
        execution_time: Total execution time in seconds.
        config: Configuration used for this simulation run.
    """

    metrics: Dict[str, Any]
    agent_states: List[Dict[str, Any]]
    environment_state: Dict[str, Any]
    execution_time: float
    config: SimulationConfig


class SimulationLab:
    """Core orchestration engine for running multi-agent simulations.

    This class manages the interaction between agents and environments,
    collects metrics, and provides tools for analyzing and visualizing results.

    Attributes:
        environment: The environment in which agents will operate.
        agents: List of agents participating in the simulation.
        config: Configuration for the simulation.
        console: Rich console for pretty printing.
    """

    def __init__(
        self,
        environment: Environment,
        agents: Optional[List[Agent]] = None,
        config: Optional[SimulationConfig] = None,
        metrics: Optional[List[str]] = None,
    ) -> None:
        """Initialize a new SimulationLab instance.

        Args:
            environment: The environment in which agents will operate.
            agents: List of agents participating in the simulation.
                If None, the environment's default agents will be used.
            config: Configuration for the simulation.
                If None, default configuration will be used.
            metrics: List of metrics to collect during simulation.
                If None, default metrics will be collected.
        """
        self.environment = environment
        self.agents = agents or []
        self.config = config or SimulationConfig()
        self.metrics = metrics or ["reward", "steps"]
        self.console = Console()

        # Set up logging
        log_level = os.environ.get("LLAMA_SIM_LOG_LEVEL", "INFO")
        logger.remove()
        logger.add(lambda msg: self.console.print(msg, end=""), level=log_level)

        # Set random seed for reproducibility
        seed = int(os.environ.get("LLAMA_SIM_SEED", "42"))
        np.random.seed(seed)
        mx.random.seed(seed)

        # Create results directory
        results_dir = os.environ.get("LLAMA_SIM_RESULT_DIR", "./results")
        self.results_dir = Path(results_dir)
        self.results_dir.mkdir(exist_ok=True, parents=True)

        logger.info(f"SimulationLab initialized with {len(self.agents)} agents")
        logger.info(f"Environment: {self.environment.__class__.__name__}")
        logger.info(f"Metrics: {self.metrics}")

    def run(
        self, episodes: int = 1, max_steps: int = 1000, render: bool = False
    ) -> SimulationResult:
        """Run simulation for specified number of episodes.

        Args:
            episodes: Number of episodes to run.
            max_steps: Maximum steps per episode.
            render: Whether to render the environment during simulation.

        Returns:
            SimulationResult: Results of the simulation.
        """
        start_time = time.time()
        all_metrics = {metric: [] for metric in self.metrics}

        logger.info(
            f"Starting simulation with {episodes} episodes, {max_steps} max steps per episode"
        )

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            TimeElapsedColumn(),
            console=self.console,
        ) as progress:
            episode_task = progress.add_task("Episodes", total=episodes)

            for episode in range(episodes):
                episode_metrics = self._run_episode(episode, max_steps, render, progress)

                # Collect metrics
                for metric, value in episode_metrics.items():
                    all_metrics[metric].append(value)

                progress.update(episode_task, advance=1)

        # Calculate final metrics
        final_metrics = {
            metric: np.mean(values) if values else 0 for metric, values in all_metrics.items()
        }

        # Get final states
        agent_states = [agent.get_state() for agent in self.agents]
        environment_state = self.environment.get_state()

        execution_time = time.time() - start_time
        logger.info(f"Simulation completed in {execution_time:.2f} seconds")

        # Create and return result
        result = SimulationResult(
            metrics=final_metrics,
            agent_states=agent_states,
            environment_state=environment_state,
            execution_time=execution_time,
            config=self.config,
        )

        return result

    def _run_episode(
        self, episode: int, max_steps: int, render: bool, progress: Progress
    ) -> Dict[str, float]:
        """Run a single episode of simulation.

        Args:
            episode: Current episode number.
            max_steps: Maximum steps for this episode.
            render: Whether to render the environment.
            progress: Progress bar for tracking.

        Returns:
            Dict[str, float]: Metrics collected during this episode.
        """
        # Reset environment and agents
        obs = self.environment.reset()
        for agent in self.agents:
            agent.reset()

        step_task = progress.add_task(f"Episode {episode} steps", total=max_steps)

        total_rewards = mx.zeros(len(self.agents))
        done = False
        step = 0

        episode_metrics = {}

        while not done and step < max_steps:
            # Get actions from all agents
            actions = []
            for i, agent in enumerate(self.agents):
                agent_obs = self.environment.get_agent_observation(i, obs)
                action = agent.act(agent_obs)
                actions.append(action)

            # Step environment
            next_obs, rewards, done, info = self.environment.step(actions)

            # Update agents
            for i, agent in enumerate(self.agents):
                agent_obs = self.environment.get_agent_observation(i, obs)
                agent_next_obs = self.environment.get_agent_observation(i, next_obs)
                agent_reward = rewards[i] if isinstance(rewards, list) else rewards
                agent_done = done
                agent_info = info.get(i, {}) if isinstance(info, dict) else {}

                agent.update(
                    agent_obs,
                    actions[i],
                    agent_reward,
                    agent_next_obs,
                    agent_done,
                    agent_info,
                )
                total_rewards = total_rewards.at[i].add(agent_reward)

            # Render if requested
            if render:
                self.environment.render()

            # Collect metrics
            if "metrics" in info:
                for metric, value in info["metrics"].items():
                    if metric in self.metrics:
                        if metric not in episode_metrics:
                            episode_metrics[metric] = []
                        episode_metrics[metric].append(value)

            obs = next_obs
            step += 1
            progress.update(step_task, advance=1)

        progress.remove_task(step_task)

        # Finalize episode metrics
        final_episode_metrics = {
            "reward": mx.mean(total_rewards).item(),
            "steps": step,
        }

        # Add environment-specific metrics
        for metric in self.metrics:
            if metric in episode_metrics:
                final_episode_metrics[metric] = np.mean(episode_metrics[metric])

        return final_episode_metrics

    def visualize(self, result: SimulationResult, output_path: Optional[str] = None) -> None:
        """Visualize simulation results.

        Args:
            result: Simulation result to visualize.
            output_path: Path to save visualizations.
                If None, visualizations will be saved to the default results directory.
        """
        import matplotlib.pyplot as plt
        import seaborn as sns

        output_path = output_path or self.results_dir / f"sim_result_{int(time.time())}"
        Path(output_path).mkdir(exist_ok=True, parents=True)

        # Set up plot style
        sns.set_theme(style="whitegrid")

        # Plot metrics
        fig, ax = plt.subplots(figsize=(10, 6))
        metrics_df = pd.DataFrame(result.metrics, index=[0])
        metrics_df.T.plot(kind="bar", ax=ax)
        ax.set_title("Simulation Metrics")
        ax.set_xlabel("Metric")
        ax.set_ylabel("Value")
        plt.tight_layout()
        plt.savefig(f"{output_path}/metrics.png")

        # Save results as CSV
        metrics_df.to_csv(f"{output_path}/metrics.csv", index=False)

        logger.info(f"Results visualized and saved to {output_path}")

        # Display results summary
        self.console.print("\n[bold]Simulation Results Summary:[/bold]")
        for metric, value in result.metrics.items():
            self.console.print(f"{metric}: {value:.4f}")
        self.console.print(f"Execution time: {result.execution_time:.2f} seconds")

    def run_federated_simulation(
        self,
        aggregation_method: str = "fedavg",
        client_optimizer: str = "sgd",
        local_epochs: int = 1,
        communication_rounds: Optional[int] = None,
        fraction_fit: float = 1.0,
    ) -> SimulationResult:
        """Run a federated learning simulation.

        Args:
            aggregation_method: Method for aggregating client updates.
            client_optimizer: Optimizer to use for client training.
            local_epochs: Number of local training epochs per round.
            communication_rounds: Number of communication rounds.
                If None, the environment's default will be used.
            fraction_fit: Fraction of clients to select per round.

        Returns:
            SimulationResult: Results of the federated learning simulation.
        """
        from llama_simulation.environments.federated.base import FederatedLearningEnv

        if not isinstance(self.environment, FederatedLearningEnv):
            raise TypeError("Environment must be a FederatedLearningEnv for federated simulation")

        # Configure environment
        if communication_rounds is not None:
            self.environment.communication_rounds = communication_rounds
        self.environment.fraction_fit = fraction_fit

        # Configure federated learning parameters
        self.environment.configure_federation(
            aggregation_method=aggregation_method,
            client_optimizer=client_optimizer,
            local_epochs=local_epochs,
        )

        # Run simulation
        result = self.run(episodes=1, max_steps=self.environment.communication_rounds)
        return result

    def run_ethical_evaluation(
        self, test_categories: Optional[List[str]] = None, difficulty: str = "standard"
    ) -> SimulationResult:
        """Run an ethical evaluation simulation.

        Args:
            test_categories: Categories of ethical tests to run.
                If None, all available categories will be used.
            difficulty: Difficulty level of the test cases.

        Returns:
            SimulationResult: Results of the ethical evaluation.
        """
        from llama_simulation.environments.ethical.base import EthicalTestEnv

        if not isinstance(self.environment, EthicalTestEnv):
            raise TypeError("Environment must be an EthicalTestEnv for ethical evaluation")

        # Configure environment
        self.environment.configure_test_cases(
            categories=test_categories,
            difficulty=difficulty,
        )

        # Run simulation
        result = self.run(episodes=1, max_steps=len(self.environment.test_cases))
        return result

    def generate_ethical_report(
        self, result: SimulationResult, output_path: Optional[str] = None
    ) -> str:
        """Generate a detailed ethical evaluation report.

        Args:
            result: Simulation result from an ethical evaluation.
            output_path: Path to save the report.
                If None, the report will be saved to the default results directory.

        Returns:
            str: Path to the generated report.
        """
        from llama_simulation.environments.ethical.base import EthicalTestEnv

        if not isinstance(self.environment, EthicalTestEnv):
            raise TypeError("Environment must be an EthicalTestEnv for ethical report generation")

        if output_path is None:
            output_path = self.results_dir / f"ethical_report_{int(time.time())}.pdf"

        report_path = self.environment.generate_report(result, output_path)
        logger.info(f"Ethical evaluation report saved to {report_path}")

        return report_path

    def save(self, path: Optional[str] = None) -> str:
        """Save the simulation state.

        Args:
            path: Path to save the simulation state.
                If None, the state will be saved to the default results directory.

        Returns:
            str: Path to the saved simulation state.
        """
        import pickle

        if path is None:
            path = self.results_dir / f"sim_state_{int(time.time())}.pkl"

        state = {
            "environment_state": self.environment.get_state(),
            "agent_states": [agent.get_state() for agent in self.agents],
            "config": self.config,
        }

        with open(path, "wb") as f:
            pickle.dump(state, f)

        logger.info(f"Simulation state saved to {path}")
        return str(path)

    @classmethod
    def load(cls, path: str) -> "SimulationLab":
        """Load simulation state from file.

        Args:
            path: Path to load the simulation state from.

        Returns:
            SimulationLab: Loaded simulation instance.
        """
        import pickle

        with open(path, "rb") as f:
            state = pickle.load(f)

        # Recreate environment and agents
        from llama_simulation.agents.registry import create_agent
        from llama_simulation.environments.registry import create_environment

        env_state = state["environment_state"]
        environment = create_environment(env_type=env_state["type"], **env_state["params"])
        environment.set_state(env_state)

        agents = []
        for agent_state in state["agent_states"]:
            agent = create_agent(agent_type=agent_state["type"], **agent_state["params"])
            agent.set_state(agent_state)
            agents.append(agent)

        # Create SimulationLab
        lab = cls(
            environment=environment,
            agents=agents,
            config=state["config"],
        )

        logger.info(f"Simulation loaded from {path}")
        return lab
