from maze import Maze
from q_maze import QMaze, Action
import numpy as np
from e_greedy_pol import eps_policy, E_greedy_policy


"""Sarsa Implementation is an on-policy algorithm for learning
 a Markov decision process policy. The Q values update
 depending on the current stage of the  Agent and the  Agent
 actions taken based on the policy.
 
 source https://en.wikipedia.org/wiki/State–action–reward–state–action"""


class Qlearning:
    def __init__(self, policy, env, gamma, alpha):
        self.policy = policy
        self.gamma = gamma
        self.alpha = alpha

        self.size_maze = env.size
        self.coord_to_index_state = env.coord_to_index_state

        self.q_values = np.zeros(self.size_maze * self.size_maze, len(list(Action)))

    def update_Qlearning(
        self, state_current, action_next, reward_next, state_next, action_next_next
    ):

        self.q_values[state_current, action_next] = self.q_values[
            state_current, action_next
        ] + self.alpha * (
            reward_next
            + self.gamma * self.q_values[state_current, action_next_next]
            - self.q_values
        )

    def new_values(self):

        value_grid = np.zeros((self.size_maze, self.size_maze))

        for i in range(self.size_maze):
            for j in range(self.size_maze):

                s = self.coord_to_index_state[i, j]

                value_grid[i, j] = max(self.q_values[s])

        return value_grid


epolicy = E_greedy_policy(1, 0.999)
qlearning = Qlearning(epolicy, QMaze, 0.9, 0.1)

s = Maze.reset()
done = False


# We Update the epsilon after each action
while not done:
    action = epolicy(s, qlearning.q_values)
    state_next, r, done = QMaze.step(Action)
    action_next = epolicy(state_next, qlearning.q_values)
