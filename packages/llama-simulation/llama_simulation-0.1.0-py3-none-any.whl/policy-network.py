"""Policy network implementations using MLX for agent decision making.

This module provides MLX-based neural network policy implementations
for reinforcement learning agents in the simulation framework.
"""

from typing import Callable, List, Tuple, Union

import mlx.core as mx
import mlx.nn as nn
import numpy as np


class MLXPolicyNetwork(nn.Module):
    """Base policy network implementation using MLX.

    This class provides a base implementation of a policy network using
    MLX neural networks. It can be used for both discrete and continuous
    action spaces.

    Attributes:
        state_dim: Dimension of the state space.
        action_dim: Dimension of the action space.
        hidden_dims: Dimensions of hidden layers.
        activation: Activation function.
        continuous: Whether the action space is continuous.
    """

    def __init__(
        self,
        state_dim: int,
        action_dim: int,
        hidden_dims: List[int] = [64, 64],
        activation: Callable = nn.relu,
        continuous: bool = False,
    ) -> None:
        """Initialize a new MLXPolicyNetwork.

        Args:
            state_dim: Dimension of the state space.
            action_dim: Dimension of the action space.
            hidden_dims: Dimensions of hidden layers.
            activation: Activation function.
            continuous: Whether the action space is continuous.
        """
        super().__init__()

        self.state_dim = state_dim
        self.action_dim = action_dim
        self.hidden_dims = hidden_dims
        self.activation = activation
        self.continuous = continuous

        # Build layers
        layers = []
        prev_dim = state_dim

        for dim in hidden_dims:
            layers.append(nn.Linear(prev_dim, dim))
            layers.append(activation)
            prev_dim = dim

        self.feature_layers = nn.Sequential(*layers)

        if continuous:
            # For continuous actions, output mean and log_std
            self.mean_layer = nn.Linear(prev_dim, action_dim)
            self.log_std_layer = nn.Linear(prev_dim, action_dim)
        else:
            # For discrete actions, output logits
            self.action_layer = nn.Linear(prev_dim, action_dim)

    def __call__(self, state: mx.array) -> Union[mx.array, Tuple[mx.array, mx.array]]:
        """Forward pass of the policy network.

        Args:
            state: State tensor of shape (batch_size, state_dim).

        Returns:
            Union[mx.array, Tuple[mx.array, mx.array]]:
                For discrete actions: logits of shape (batch_size, action_dim).
                For continuous actions: tuple of (mean, log_std) each of shape (batch_size, action_dim).
        """
        features = self.feature_layers(state)

        if self.continuous:
            mean = self.mean_layer(features)
            log_std = self.log_std_layer(features)
            # Clamp log_std for numerical stability
            log_std = mx.clip(log_std, -20.0, 2.0)
            return mean, log_std
        else:
            logits = self.action_layer(features)
            return logits

    def sample(self, state: mx.array, deterministic: bool = False) -> mx.array:
        """Sample actions from the policy.

        Args:
            state: State tensor of shape (batch_size, state_dim).
            deterministic: Whether to sample deterministically
                (i.e., take the most likely action).

        Returns:
            mx.array: Sampled actions of shape (batch_size, action_dim).
        """
        if self.continuous:
            mean, log_std = self(state)

            if deterministic:
                return mean

            std = mx.exp(log_std)
            eps = mx.random.normal(mean.shape)
            actions = mean + eps * std
            return actions
        else:
            logits = self(state)

            if deterministic:
                return mx.argmax(logits, axis=-1)

            # Gumbel-softmax sampling
            eps = mx.random.uniform(logits.shape) + 1e-8
            gumbel = -mx.log(-mx.log(eps))
            actions = mx.argmax(logits + gumbel, axis=-1)
            return actions

    def evaluate(self, state: mx.array, action: mx.array) -> Tuple[mx.array, mx.array, mx.array]:
        """Evaluate actions given states.

        Args:
            state: State tensor of shape (batch_size, state_dim).
            action: Action tensor of shape (batch_size, action_dim) for continuous,
                or (batch_size,) for discrete.

        Returns:
            Tuple[mx.array, mx.array, mx.array]:
                log_prob: Log probability of the actions.
                entropy: Policy entropy.
                value: Value estimate (if the policy has a value head).
        """
        if self.continuous:
            mean, log_std = self(state)
            std = mx.exp(log_std)

            # Compute log probabilities
            action_shape = action.shape
            if len(action_shape) < len(mean.shape):
                action = action.reshape(*action_shape, 1)

            normal_dist = mx.random.normal(mean.shape)

            # Log probability of actions
            log_prob = (
                -0.5 * ((action - mean) / (std + 1e-8)) ** 2 - log_std - 0.5 * np.log(2 * np.pi)
            )
            log_prob = mx.sum(log_prob, axis=-1)

            # Entropy of the policy
            entropy = mx.sum(log_std + 0.5 * np.log(2 * np.pi * np.e), axis=-1)

            return log_prob, entropy, mx.zeros(log_prob.shape)  # No value estimate
        else:
            logits = self(state)
            log_prob = mx.log_softmax(logits, axis=-1)

            # Gather log_prob of selected actions
            if len(action.shape) == len(logits.shape) - 1:
                # If action is one-hot encoded
                action_indices = mx.argmax(action, axis=-1)
            else:
                # If action is an index
                action_indices = action

            # Using explicit indexing for gathering
            batch_indices = mx.arange(log_prob.shape[0])
            selected_log_probs = log_prob[batch_indices, action_indices]

            # Entropy: -sum(p * log(p))
            probs = mx.softmax(logits, axis=-1)
            entropy = -mx.sum(probs * log_prob, axis=-1)

            return (
                selected_log_probs,
                entropy,
                mx.zeros(selected_log_probs.shape),
            )  # No value estimate


class MLXActorCritic(nn.Module):
    """Actor-Critic policy network implementation using MLX.

    This class provides an implementation of an actor-critic policy network
    using MLX neural networks. It combines a policy network with a value network.

    Attributes:
        state_dim: Dimension of the state space.
        action_dim: Dimension of the action space.
        hidden_dims: Dimensions of hidden layers.
        activation: Activation function.
        continuous: Whether the action space is continuous.
        shared_network: Whether to use a shared feature extractor.
    """

    def __init__(
        self,
        state_dim: int,
        action_dim: int,
        hidden_dims: List[int] = [64, 64],
        activation: Callable = nn.relu,
        continuous: bool = False,
        shared_network: bool = True,
    ) -> None:
        """Initialize a new MLXActorCritic.

        Args:
            state_dim: Dimension of the state space.
            action_dim: Dimension of the action space.
            hidden_dims: Dimensions of hidden layers.
            activation: Activation function.
            continuous: Whether the action space is continuous.
            shared_network: Whether to use a shared feature extractor.
        """
        super().__init__()

        self.state_dim = state_dim
        self.action_dim = action_dim
        self.hidden_dims = hidden_dims
        self.activation = activation
        self.continuous = continuous
        self.shared_network = shared_network

        if shared_network:
            # Shared feature extractor
            self.feature_extractor = self._build_network(state_dim, hidden_dims, activation)
            feature_dim = hidden_dims[-1]

            # Actor head
            if continuous:
                self.mean_layer = nn.Linear(feature_dim, action_dim)
                self.log_std_layer = nn.Linear(feature_dim, action_dim)
            else:
                self.action_layer = nn.Linear(feature_dim, action_dim)

            # Critic head
            self.value_layer = nn.Linear(feature_dim, 1)
        else:
            # Separate networks for actor and critic
            self.actor = MLXPolicyNetwork(
                state_dim=state_dim,
                action_dim=action_dim,
                hidden_dims=hidden_dims,
                activation=activation,
                continuous=continuous,
            )

            # Critic network
            critic_layers = []
            prev_dim = state_dim

            for dim in hidden_dims:
                critic_layers.append(nn.Linear(prev_dim, dim))
                critic_layers.append(activation)
                prev_dim = dim

            critic_layers.append(nn.Linear(prev_dim, 1))
            self.critic = nn.Sequential(*critic_layers)

    def _build_network(
        self, input_dim: int, hidden_dims: List[int], activation: Callable
    ) -> nn.Sequential:
        """Build a neural network with the given architecture.

        Args:
            input_dim: Input dimension.
            hidden_dims: Dimensions of hidden layers.
            activation: Activation function.

        Returns:
            nn.Sequential: Neural network.
        """
        layers = []
        prev_dim = input_dim

        for dim in hidden_dims:
            layers.append(nn.Linear(prev_dim, dim))
            layers.append(activation)
            prev_dim = dim

        return nn.Sequential(*layers)

    def __call__(
        self, state: mx.array
    ) -> Tuple[Union[mx.array, Tuple[mx.array, mx.array]], mx.array]:
        """Forward pass of the actor-critic network.

        Args:
            state: State tensor of shape (batch_size, state_dim).

        Returns:
            Tuple[Union[mx.array, Tuple[mx.array, mx.array]], mx.array]:
                - For discrete actions: (logits, value) where logits has shape (batch_size, action_dim).
                - For continuous actions: ((mean, log_std), value) where mean and log_std have shape
                  (batch_size, action_dim).
                - value has shape (batch_size, 1).
        """
        if self.shared_network:
            features = self.feature_extractor(state)
            value = self.value_layer(features)

            if self.continuous:
                mean = self.mean_layer(features)
                log_std = self.log_std_layer(features)
                # Clamp log_std for numerical stability
                log_std = mx.clip(log_std, -20.0, 2.0)
                return (mean, log_std), value
            else:
                logits = self.action_layer(features)
                return logits, value
        else:
            if self.continuous:
                mean, log_std = self.actor(state)
                value = self.critic(state)
                return (mean, log_std), value
            else:
                logits = self.actor(state)
                value = self.critic(state)
                return logits, value

    def sample(self, state: mx.array, deterministic: bool = False) -> Tuple[mx.array, mx.array]:
        """Sample actions from the policy and get value estimates.

        Args:
            state: State tensor of shape (batch_size, state_dim).
            deterministic: Whether to sample deterministically
                (i.e., take the most likely action).

        Returns:
            Tuple[mx.array, mx.array]:
                - actions: Sampled actions of shape (batch_size, action_dim) for continuous,
                  or (batch_size,) for discrete.
                - value: Value estimates of shape (batch_size, 1).
        """
        action_output, value = self(state)

        if self.continuous:
            mean, log_std = action_output

            if deterministic:
                actions = mean
            else:
                std = mx.exp(log_std)
                eps = mx.random.normal(mean.shape)
                actions = mean + eps * std
        else:
            logits = action_output

            if deterministic:
                actions = mx.argmax(logits, axis=-1)
            else:
                # Gumbel-softmax sampling
                eps = mx.random.uniform(logits.shape) + 1e-8
                gumbel = -mx.log(-mx.log(eps))
                actions = mx.argmax(logits + gumbel, axis=-1)

        return actions, value

    def evaluate(self, state: mx.array, action: mx.array) -> Tuple[mx.array, mx.array, mx.array]:
        """Evaluate actions given states.

        Args:
            state: State tensor of shape (batch_size, state_dim).
            action: Action tensor of shape (batch_size, action_dim) for continuous,
                or (batch_size,) for discrete.

        Returns:
            Tuple[mx.array, mx.array, mx.array]:
                log_prob: Log probability of the actions.
                entropy: Policy entropy.
                value: Value estimate.
        """
        action_output, value = self(state)

        if self.continuous:
            mean, log_std = action_output
            std = mx.exp(log_std)

            # Compute log probabilities
            action_shape = action.shape
            if len(action_shape) < len(mean.shape):
                action = action.reshape(*action_shape, 1)

            # Log probability of actions
            log_prob = (
                -0.5 * ((action - mean) / (std + 1e-8)) ** 2 - log_std - 0.5 * np.log(2 * np.pi)
            )
            log_prob = mx.sum(log_prob, axis=-1)

            # Entropy of the policy
            entropy = mx.sum(log_std + 0.5 * np.log(2 * np.pi * np.e), axis=-1)
        else:
            logits = action_output
            log_prob = mx.log_softmax(logits, axis=-1)

            # Gather log_prob of selected actions
            if len(action.shape) == len(logits.shape) - 1:
                # If action is one-hot encoded
                action_indices = mx.argmax(action, axis=-1)
            else:
                # If action is an index
                action_indices = action

            # Using explicit indexing for gathering
            batch_indices = mx.arange(log_prob.shape[0])
            selected_log_probs = log_prob[batch_indices, action_indices]
            log_prob = selected_log_probs

            # Entropy: -sum(p * log(p))
            probs = mx.softmax(logits, axis=-1)
            entropy = -mx.sum(probs * log_prob, axis=-1)

        return log_prob, entropy, value
