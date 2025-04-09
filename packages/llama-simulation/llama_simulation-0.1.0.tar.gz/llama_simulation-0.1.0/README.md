# llama-simulator

[![PyPI version](https://img.shields.io/pypi/v/llama_simulator.svg)](https://pypi.org/project/llama_simulator/)
[![License](https://img.shields.io/github/license/llamasearchai/llama-simulator)](https://github.com/llamasearchai/llama-simulator/blob/main/LICENSE)
[![Python Version](https://img.shields.io/pypi/pyversions/llama_simulator.svg)](https://pypi.org/project/llama_simulator/)
[![CI Status](https://github.com/llamasearchai/llama-simulator/actions/workflows/llamasearchai_ci.yml/badge.svg)](https://github.com/llamasearchai/llama-simulator/actions/workflows/llamasearchai_ci.yml)

**Llama Simulator (llama-simulator)** is a framework within the LlamaSearch AI ecosystem for running simulations. It allows defining simulation environments and agents that interact within those environments, useful for testing algorithms, reinforcement learning, or modeling complex systems.

## Key Features

- **Simulation Environments:** Provides or allows defining various simulation environments (`environments/`).
- **Agent Definitions:** Supports creating agents with specific behaviors to operate within environments (`agents/`).
- **Simulation Core:** Manages the simulation loop, agent interactions, and environment updates (`core.py`).
- **Command-Line Interface:** Offers tools to configure and run simulations via CLI (`cli.py`).
- **Configurable:** Allows setting up simulation parameters, environments, agents, and logging (`config.py`).

## Installation

```bash
pip install llama-simulator
# Or install directly from GitHub for the latest version:
# pip install git+https://github.com/llamasearchai/llama-simulator.git
```

## Usage

### Command-Line Interface (CLI)

*(CLI usage examples for running specific simulations will be added here.)*

```bash
llama-simulator run --config simulation_config.yaml --environment TradingEnv --agent QLearningAgent
```

### Python Client / Embedding

*(Python usage examples for programmatically setting up and running simulations will be added here.)*

```python
# Placeholder for Python client usage
# from llama_simulator import SimulationRunner, SimulationConfig
# from my_envs import CustomEnvironment
# from my_agents import HeuristicAgent

# config = SimulationConfig.load("config.yaml")
# runner = SimulationRunner(config)

# # Setup simulation
# environment = CustomEnvironment()
# agent = HeuristicAgent()
# runner.setup(environment, [agent])

# # Run the simulation
# results = runner.run_simulation(steps=1000)
# print(f"Simulation finished. Final score: {results['final_score']}")
```

## Architecture Overview

```mermaid
graph TD
    A[User / CLI (cli.py)] --> B{Simulation Core (core.py)};
    B -- Loads --> C{Simulation Environment (environments/)};
    B -- Loads --> D{Agent(s) (agents/)};
    B -- Manages --> E[Simulation Loop];
    E -- Updates --> C;
    E -- Gets Actions --> D;
    D -- Acts On --> C;
    C -- Provides State/Reward --> D;
    E --> F[Simulation Results / Logs];

    G[Configuration (config.py)] -- Configures --> B;
    G -- Configures --> C;
    G -- Configures --> D;

    style B fill:#f9f,stroke:#333,stroke-width:2px
    style C fill:#ccf,stroke:#333,stroke-width:1px
    style D fill:#ccf,stroke:#333,stroke-width:1px
```

1.  **Interface:** User configures and starts the simulation via the CLI or programmatically.
2.  **Core:** Loads the specified environment and agent(s) based on configuration.
3.  **Simulation Loop:** The core manages the main loop, stepping through time.
4.  **Interaction:** In each step, agents perceive the environment state, decide on actions, and act upon the environment.
5.  **Environment Update:** The environment state changes based on agent actions and internal dynamics.
6.  **Results:** The simulation produces logs, metrics, or final state information.
7.  **Configuration:** Defines the environment, agents, simulation length, parameters, etc.

## Configuration

*(Details on configuring simulation environments, agent parameters, simulation runtime settings, logging, etc., will be added here.)*

## Development

### Setup

```bash
# Clone the repository
git clone https://github.com/llamasearchai/llama-simulator.git
cd llama-simulator

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
