"""Tests for the SimulationLab module."""

from pathlib import Path
from unittest import mock

import mlx.core as mx
import numpy as np
import pytest
from llama_simulation.agents.base import Agent
from llama_simulation.agents.policy import MLXPolicyNetwork
from llama_simulation.environments.base import Environment
from llama_simulation.simulation.lab import SimulationLab
from llama_simulation.utils.config import SimulationConfig


class MockAgent(Agent):
    """Mock agent for testing."""

    def __init__(self, action_dim=1, id=None, name=None):
        super().__init__(id=id, name=name)
        self.action_dim = action_dim
        self.action_history = []

    def act(self, observation):
        """Return a random action."""
        action = np.random.randint(0, self.action_dim)
        self.action_history.append(action)
        return action

    def _get_params(self):
        return {"action_dim": self.action_dim}

    def _set_params(self, params):
        self.action_dim = params.get("action_dim", self.action_dim)


class MockEnvironment(Environment):
    """Mock environment for testing."""

    def __init__(
        self,
        state_dim=4,
        action_dim=2,
        num_agents=1,
        max_steps=100,
        id=None,
        name=None,
    ):
        super().__init__(
            id=id,
            name=name,
            state_dim=state_dim,
            action_dim=action_dim,
            num_agents=num_agents,
        )
        self.max_steps = max_steps
        self.current_step = 0
        self.state = mx.zeros((state_dim,))

    def reset(self):
        """Reset the environment."""
        super().reset()
        self.current_step = 0
        self.state = mx.random.normal((self.state_dim,))
        return self.state

    def step(self, actions):
        """Take a step in the environment."""
        super().step(actions)

        # Convert actions to list if not already
        if not isinstance(actions, list):
            actions = [actions]

        # Simulate next state and reward
        self.state = mx.random.normal((self.state_dim,))
        rewards = mx.array([float(a) for a in actions])

        # Update state
        self.current_step += 1
        done = self.current_step >= self.max_steps

        # Prepare info
        info = {
            "current_step": self.current_step,
            "metrics": {
                "reward": float(mx.mean(rewards)),
                "steps": self.current_step,
            },
        }

        return self.state, rewards, done, info

    def _get_params(self):
        return {
            "state_dim": self.state_dim,
            "action_dim": self.action_dim,
            "num_agents": self.num_agents,
            "max_steps": self.max_steps,
        }

    def _set_params(self, params):
        self.state_dim = params.get("state_dim", self.state_dim)
        self.action_dim = params.get("action_dim", self.action_dim)
        self.num_agents = params.get("num_agents", self.num_agents)
        self.max_steps = params.get("max_steps", self.max_steps)


@pytest.fixture
def simulation_lab():
    """Create a simulation lab with mock environment and agents."""
    env = MockEnvironment(state_dim=4, action_dim=2, num_agents=2, max_steps=10)
    agents = [MockAgent(action_dim=2) for _ in range(2)]
    config = SimulationConfig()

    return SimulationLab(environment=env, agents=agents, config=config)


def test_simulation_lab_init():
    """Test SimulationLab initialization."""
    env = MockEnvironment()
    agents = [MockAgent()]
    config = SimulationConfig()

    lab = SimulationLab(environment=env, agents=agents, config=config)

    assert lab.environment == env
    assert lab.agents == agents
    assert lab.config == config
    assert len(lab.metrics) > 0
    assert lab.results_dir.exists()


def test_simulation_lab_run(simulation_lab):
    """Test running a simulation."""
    result = simulation_lab.run(episodes=2, max_steps=5)

    assert result is not None
    assert "reward" in result.metrics
    assert "steps" in result.metrics
    assert len(result.agent_states) == 2
    assert result.execution_time > 0


def test_simulation_lab_visualize(simulation_lab, tmp_path):
    """Test visualizing simulation results."""
    # Mock matplotlib to avoid display issues
    with mock.patch("matplotlib.pyplot.savefig"):
        result = simulation_lab.run(episodes=1, max_steps=5)
        output_path = str(tmp_path / "test_viz")
        simulation_lab.visualize(result, output_path=output_path)

        # Check that output files were created
        assert Path(f"{output_path}/metrics.png").exists()
        assert Path(f"{output_path}/metrics.csv").exists()


def test_simulation_lab_save_load(simulation_lab, tmp_path):
    """Test saving and loading a simulation."""
    # Run a simulation
    simulation_lab.run(episodes=1, max_steps=5)

    # Save state
    save_path = str(tmp_path / "test_save.pkl")
    simulation_lab.save(save_path)

    # Create registry mocks
    with mock.patch("llama_simulation.environments.registry.create_environment") as mock_create_env:
        with mock.patch("llama_simulation.agents.registry.create_agent") as mock_create_agent:
            # Set up mocks
            mock_create_env.return_value = simulation_lab.environment
            mock_create_agent.return_value = simulation_lab.agents[0]

            # Load simulation
            loaded_lab = SimulationLab.load(save_path)

            # Check that it loaded correctly
            assert loaded_lab.environment == simulation_lab.environment
            assert len(loaded_lab.agents) == len(simulation_lab.agents)
            assert loaded_lab.config == simulation_lab.config


def test_policy_network():
    """Test MLXPolicyNetwork functionality."""
    # Create policy network
    state_dim = 4
    action_dim = 2
    policy = MLXPolicyNetwork(state_dim=state_dim, action_dim=action_dim)

    # Test forward pass
    state = mx.random.normal((3, state_dim))
    logits = policy(state)

    assert logits.shape == (3, action_dim)

    # Test sampling
    actions = policy.sample(state)

    assert actions.shape == (3,)

    # Test deterministic action
    det_actions = policy.sample(state, deterministic=True)

    assert det_actions.shape == (3,)


def test_environment_interface():
    """Test Environment interface."""
    env = MockEnvironment(state_dim=4, action_dim=2, num_agents=2)

    # Test reset
    obs = env.reset()
    assert obs.shape == (4,)

    # Test step
    next_obs, rewards, done, info = env.step([0, 1])

    assert next_obs.shape == (4,)
    assert rewards.shape == (2,)
    assert isinstance(done, bool)
    assert "current_step" in info

    # Test get_agent_observation
    agent_obs = env.get_agent_observation(0, next_obs)
    assert agent_obs.shape == (4,)

    # Test get_state and set_state
    state = env.get_state()
    env.set_state(state)

    assert env.state_dim == 4
    assert env.action_dim == 2
    assert env.num_agents == 2


def test_agent_interface():
    """Test Agent interface."""
    agent = MockAgent(action_dim=3)

    # Test act
    obs = mx.random.normal((4,))
    action = agent.act(obs)

    assert 0 <= action < 3

    # Test update
    agent.update(
        observation=obs,
        action=action,
        reward=1.0,
        next_observation=mx.random.normal((4,)),
        done=False,
    )

    assert len(agent.history) == 1
    assert agent.stats["total_reward"] == 1.0

    # Test reset
    agent.reset()

    assert len(agent.history) == 0
    assert agent.stats["total_reward"] == 0.0

    # Test get_state and set_state
    state = agent.get_state()
    agent.set_state(state)

    assert agent.id == state["id"]
    assert agent.name == state["name"]


if __name__ == "__main__":
    # Run tests
    pytest.main(["-xvs", __file__])
