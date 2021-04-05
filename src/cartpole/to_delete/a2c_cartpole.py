import math
import random

import gym
import numpy as np

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.distributions import Categorical

use_cuda = torch.cuda.is_available()
device = torch.device("cuda" if use_cuda else "cpu")

from baselines_multiprocessing import SubprocVecEnv

num_envs = 10
env_name = "CartPole-v0"


def make_env():
    def _thunk():
        env = gym.make(env_name)
        return env

    return _thunk


if __name__ == "__main__":
    envs = [make_env() for i in range(num_envs)]
    envs = SubprocVecEnv(envs)
    # env = gym.make(env_name)
