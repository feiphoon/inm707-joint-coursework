from maze import Maze
from random import random

# from collections import namedtuple

# Observation = namedtuple("Observation", "distance_to_prey neighbours")


class Minotaur:
    def __init__(self, environment: Maze) -> None:
        _available_cells = environment._find_empty_cells()
        self.position_minotaur = random.choice(_available_cells)
        self.rate_of_movement = 1  # probably not going to do anything with this tbh

    def step(self) -> None:
        pass
