"""
Based on MC Control code in INM707 Lab4 by Dr Michael Garcia Ortiz:
- using Q Values for SARSA learning
- then modify to Q Learning
"""
import numpy as np

from q_maze import QMaze, Action
from fei_e_greedy_policy import EGreedyPolicy


class Sarsa:
    def __init__(
        self, policy: EGreedyPolicy, environment: QMaze, gamma: float, alpha: float
    ) -> None:
        # Discount factor
        self.gamma = self._check_valid_gamma(gamma)

        # Learning rate or memory rate
        self.alpha = self._check_valid_alpha(alpha)

        # Derived from environment Maze
        self.env_size = environment.size

        # Derived from environment QMaze
        self.coord_to_index_state = environment.coord_to_index_state

        self.q_value_store = np.zeros(
            (self.env_size * self.env_size, len(list(Action)))
        )

    @staticmethod
    def _check_valid_alpha(alpha: float) -> float:
        if type(alpha) != float:
            raise Exception("Float type required for alpha value.")
        if (alpha < 0) or (alpha == 1):
            raise Exception("Alpha value must be from 0 to 1 exclusive.")
        return alpha

    @staticmethod
    def _check_valid_gamma(gamma: float) -> float:
        if type(gamma) != float:
            raise Exception("Float type required for gamma value.")
        if (gamma < 0) or (gamma == 1):
            raise Exception("Gamma value must be from 0 to 1 exclusive.")
        return gamma

    def update_q_values(
        self,
        current_state: int,
        next_action: int,
        next_reward: int,
        next_state: int,
        next_next_action: int,
    ) -> None:
        # actions here are the Action.index values
        # TODO: double-check this formula is absolutely correct (for SARSA)
        self.q_value_store[current_state, next_action] += self.alpha * (
            next_reward
            + self.gamma * (self.q_value_store[next_state, next_next_action])
            - self.q_value_store[current_state, next_action]
        )

    def display_q_values(self) -> np.ndarray:
        """
        Based on INM707 Lab4 code by Dr Michael Garcia Ortiz.
        This is only to gather all the q-values, work out what is the max Q-value
        for each cell and display them.
        """
        q_value_display_matrix = np.zeros((self.env_size, self.env_size))

        for i in range(self.env_size):
            for j in range(self.env_size):
                _state = self.coord_to_index_state[i, j]
                q_value_display_matrix[i, j] = max(self.q_value_store[_state])

        return q_value_display_matrix
