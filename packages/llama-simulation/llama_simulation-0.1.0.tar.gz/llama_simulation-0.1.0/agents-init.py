"""Agent implementations for the simulation framework.

This package provides agent implementations for the simulation framework,
ranging from basic agents to specialized agents for different domains.
"""

from llama_simulation.agents.base import Agent
from llama_simulation.agents.policy import MLXActorCritic, MLXPolicyNetwork
from llama_simulation.agents.registry import (
    MLXPolicyAgent,
    create_agent,
    list_available_agents,
    register_agent,
)
from llama_simulation.agents.specialized import FederatedAgent, LLMAgent

__all__ = [
    "Agent",
    "MLXPolicyNetwork",
    "MLXActorCritic",
    "MLXPolicyAgent",
    "create_agent",
    "list_available_agents",
    "register_agent",
    "FederatedAgent",
    "LLMAgent",
]
