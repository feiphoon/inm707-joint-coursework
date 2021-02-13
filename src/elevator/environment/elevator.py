"""zero is the ground floor
And maybe elevator doesn't need to know what floor it's on. It's the environment/states?
"""
import numpy as np
from collections import deque


class Elevator:
    def __init__(self, capacity=1, num_floors=num_floors):
        assert type(num_floors) is int
        assert type(capacity) is int
        self.capacity = capacity
        self.num_floors = num_floors + 1  # plus one for ground floor
        self._create_elevator()

    def _create_elevator(self):
        """Use this to create elevator"""
        # Build elevator shaft
        floor_numbers = list(range(self.num_floors))
        # self.elevator = np.array(floor_numbers).reshape(self.num_floors, 1)
        self.elevator = [deque(maxlen=self.capacity) for _ in floor_numbers]

    def __repr__(self):
        return f"An Elevator with {self.capacity} capacity. \n {self.elevator}"
