"""
Based on Lab4 code
"""

from random import choice
import numpy as np

from maze import Action


class EGreedyPolicy:
    def __init__(self, epsilon: float, decay: float) -> None:
        self.epsilon = self._check_valid_epsilon(epsilon)
        self.starting_epsilon = self.epsilon
        self.stopping_epsilon = 0.1
        self.decay = self._check_valid_decay(decay)

    @staticmethod
    def _check_valid_epsilon(epsilon: float) -> float:
        if type(epsilon) != float:
            raise Exception("Float type required for epsilon value.")
        if (epsilon < 0) or (epsilon == 1):
            raise Exception("Epsilon value must be from 0 to 1 exclusive.")
        return epsilon

    @staticmethod
    def _check_valid_decay(decay: float) -> float:
        if type(decay) != float:
            raise Exception("Float type required for decay value.")
        if (decay < 0) or (decay == 1):
            raise Exception("Decay value must be from 0 to 1 exclusive.")
        return decay

    def __call__(self, state: int, q_value_store: np.ndarray) -> Action:

        # Create a factor of randomness -
        # draw a number [0.0, 1.0) from a uniform distribution
        # against a specified epsilon.
        is_greedy = np.random.uniform() > self.epsilon

        # If greedy true, pick the largest q_value for the state
        if is_greedy:
            action_index = np.argmax(q_value_store[state])

        else:
            # We sample a random action by index, from available actions.
            sampled_action = choice(list(Action))
            action_index = sampled_action.value.index

        # This points to the index property/fetches the index of the action.
        # Yeah I refuse to make a dictionary just for this,
        # so this is what it's come to. We want this to return Action.DIRECTION.
        # This covers the action_index returned by all parts of the if-else just above.
        for _ in list(Action):
            if _.value.index == action_index:
                action_to_take = _

        return action_to_take

    def update_epsilon(self) -> None:
        """
        Update epsilon by product of decay, until epsilon
        is not larger than the stopping epsilon limit.
        """
        if self.epsilon > self.stopping_epsilon:
            self.epsilon = self.epsilon * self.decay

    def reset(self) -> None:
        self.epsilon = self.starting_epsilon
