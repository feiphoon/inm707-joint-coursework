"""Implementing epsilon-greedy policy"""

from matplotlib import pyplot as plt
import numpy as np
import random

# from sarsa import Sarsa
# from q_maze import QMaze, Action


class E_greedy_policy:
    def __init__(self, epsilon, decay):

        self.epsilon = epsilon
        self.epsilon_start = epsilon
        self.decay = decay

    # Python has a set of built-in methods and __call__ is one of them.
    # The __call__ method enables Python programmers to write classes where the instances
    # behave like functions and can be called like a function.
    def __call__(self, state, q_values):

        is_greedy = random.random() > self.epsilon

        if is_greedy:
            # we select a greedy action by getting the max q_values from the grid
            action_index = np.argmax(q_values[state])
        else:
            # else we get a random choice from action
            action_index = random.choice(list(Action)).value.index

        selected_action = None
        for a in list(Action):
            if a.value.index == action_index:
                selected_action = a
        return selected_action

    def update_epsilon(self):
        self.epsilon = self.epsilon * self.decay

    def reset(self):
        self.epsilon = self.epsilon_start
