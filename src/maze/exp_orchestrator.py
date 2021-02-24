import numpy as np

from exp_runner import run_single_exp
from maze import Maze


def run_experiments(envir, policy, number_exp):

    all_rewards = []

    for n in range(number_exp):

        final_reward = run_single_exp(envir, policy)
        all_rewards.append(final_reward)

    max_reward = max(all_rewards)
    mean_reward = np.mean(all_rewards)
    var_reward = np.std(all_rewards)

    return all_rewards, max_reward, mean_reward, var_reward
