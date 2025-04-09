"""Command-line interface for llama_simulation.

This module provides a command-line interface for running simulations
and other utilities.
"""

from pathlib import Path
from typing import List, Optional

import typer
from llama_simulation import __version__
from llama_simulation.agents.registry import create_agent, list_available_agents
from llama_simulation.environments.registry import (
    create_environment,
    list_available_environments,
)
from llama_simulation.simulation.lab import SimulationLab
from llama_simulation.utils.config import SimulationConfig
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

app = typer.Typer(help="llama_simulation: A comprehensive AI simulation framework")
console = Console()


@app.command("run")
def run_simulation(
    environment: str = typer.Option(..., "--env", "-e", help="Environment to use"),
    agent: str = typer.Option(..., "--agent", "-a", help="Agent to use"),
    config_file: Optional[Path] = typer.Option(
        None, "--config", "-c", help="Path to configuration file"
    ),
    episodes: Optional[int] = typer.Option(
        None, "--episodes", "-n", help="Number of episodes to run"
    ),
    max_steps: Optional[int] = typer.Option(
        None, "--max-steps", "-s", help="Maximum steps per episode"
    ),
    render: bool = typer.Option(False, "--render", "-r", help="Render the environment"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Path to save results"),
    env_params: List[str] = typer.Option(
        [], "--env-param", help="Environment parameters (key=value)"
    ),
    agent_params: List[str] = typer.Option(
        [], "--agent-param", help="Agent parameters (key=value)"
    ),
):
    """Run a simulation with the specified environment and agent."""
    # Load configuration
    config = SimulationConfig()
    if config_file is not None:
        config = SimulationConfig.load(config_file)

    # Override config with command-line parameters
    if episodes is not None:
        config.max_episodes = episodes
    if max_steps is not None:
        config.max_steps_per_episode = max_steps
    if render:
        config.render = True

    # Parse environment parameters
    env_kwargs = {}
    for param in env_params:
        if "=" not in param:
            console.print(f"[yellow]Warning: Ignoring invalid parameter format: {param}[/yellow]")
            continue

        key, value = param.split("=", 1)
        env_kwargs[key] = _parse_value(value)

    # Parse agent parameters
    agent_kwargs = {}
    for param in agent_params:
        if "=" not in param:
            console.print(f"[yellow]Warning: Ignoring invalid parameter format: {param}[/yellow]")
            continue

        key, value = param.split("=", 1)
        agent_kwargs[key] = _parse_value(value)

    # Create environment and agent
    console.print(f"[bold blue]Creating environment: {environment}[/bold blue]")
    env = create_environment(environment, **env_kwargs)

    console.print(f"[bold blue]Creating agent: {agent}[/bold blue]")
    agent_instance = create_agent(agent, **agent_kwargs)

    # Create simulation lab
    lab = SimulationLab(
        environment=env,
        agents=[agent_instance],
        config=config,
    )

    # Run simulation
    console.print(
        f"[bold green]Running simulation for {config.max_episodes} episodes, "
        f"{config.max_steps_per_episode} steps per episode[/bold green]"
    )

    result = lab.run(
        episodes=config.max_episodes,
        max_steps=config.max_steps_per_episode,
        render=config.render,
    )

    # Save results
    if output is not None:
        output_path = output
        lab.visualize(result, output_path=str(output_path))
        console.print(f"[bold green]Results saved to {output_path}[/bold green]")
    else:
        # Display results summary
        console.print("\n[bold]Simulation Results:[/bold]")
        table = Table(title="Metrics")
        table.add_column("Metric")
        table.add_column("Value")

        for metric, value in result.metrics.items():
            table.add_row(metric, f"{value:.4f}")

        console.print(table)


@app.command("list")
def list_components(
    component_type: str = typer.Argument(..., help="Component type to list (environment, agent)")
):
    """List available components of the specified type."""
    if component_type.lower() in ("environment", "environments", "env"):
        environments = list_available_environments()

        table = Table(title="Available Environments")
        table.add_column("Name")
        table.add_column("Description")

        for env_name, env_desc in environments.items():
            table.add_row(env_name, env_desc)

        console.print(table)

    elif component_type.lower() in ("agent", "agents"):
        agents = list_available_agents()

        table = Table(title="Available Agents")
        table.add_column("Name")
        table.add_column("Description")

        for agent_name, agent_desc in agents.items():
            table.add_row(agent_name, agent_desc)

        console.print(table)

    else:
        console.print(f"[bold red]Unknown component type: {component_type}[/bold red]")
        console.print("Available component types: environment, agent")


@app.command("version")
def show_version():
    """Show the version of llama_simulation."""
    console.print(Panel(f"llama_simulation v{__version__}", title="Version"))


def _parse_value(value: str) -> any:
    """Parse a string value into the appropriate type."""
    # Try to parse as int
    try:
        return int(value)
    except ValueError:
        pass

    # Try to parse as float
    try:
        return float(value)
    except ValueError:
        pass

    # Try to parse as bool
    if value.lower() in ("true", "yes", "y", "1"):
        return True
    elif value.lower() in ("false", "no", "n", "0"):
        return False

    # Parse as string
    return value


if __name__ == "__main__":
    app()
