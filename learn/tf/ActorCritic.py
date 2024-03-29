from abc import ABC

import tensorflow as tf
from tensorflow.keras import layers
from typing import Any, List, Sequence, Tuple


class ActorCritic(tf.keras.Model, ABC):
    """Combined actor-critic network."""

    def __init__(
            self,
            num_actions: int,
            num_hidden_units: int):
        """Initialize."""
        super().__init__()

        self.common = layers.Dense(num_hidden_units, activation="relu")
        self.actor = layers.Dense(num_actions)
        self.critic = layers.Dense(1)

    def call(self, inputs: tf.Tensor) -> Tuple[tf.Tensor, tf.Tensor]:
        x = self.common(inputs)
        return self.actor(x), self.critic(x)
