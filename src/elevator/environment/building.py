"""zero is the top floor
"""
# import numpy as np
import random

from collections import deque
import logging

# from collections import namedtuple
# from enum import Enum, unique


RATE_OF_PASSENGER_ARRIVAL_PER_TIMESTEP = 2
# IndexedStep = namedtuple("IndexedStep", "index delta_i delta_j")


# @unique
# class Action(Enum):
#     UP = IndexedStep(index=0, delta_i=-1, delta_j=0)
#     DOWN = IndexedStep(index=1, delta_i=1, delta_j=0)


# DISPLAY_DICT = {0: ".", 1: "X", 2: "L", 3: "E", 9: "A"}

# Observation = namedtuple("Observation", "distance_to_exit neighbours")

logging.basicConfig(level=logging.DEBUG)


class Building:
    def __init__(self, num_floors=2, max_num_passengers=4):
        """
        >>> b = Building(1, 2)
        >>> print(b.num_floors)
        1
        >>> print(b.num_passengers)
        2
        """
        assert type(num_floors) is int
        assert type(max_num_passengers) is int
        self.num_floors = num_floors + 1  # plus one for the ground floor
        self.max_num_passengers = max_num_passengers
        self.num_passengers_left = max_num_passengers
        # self.passenger_list = self._create_passengers()
        self._create_building()

    def _create_building(self):
        """Use this to create building"""
        # Not using this:
        # self.building = np.zeros([self.num_floors, self.num_passengers])

        # Note: Each passenger slot/place in deque on each floor is a slot to keep their wait time so far
        self.building = [
            deque(maxlen=self.max_num_passengers) for _ in range(self.num_floors + 1)
        ]

        # Pick a random floor
        for _ in range(1, RATE_OF_PASSENGER_ARRIVAL_PER_TIMESTEP + 1):
            rand_floor = random.choice(
                range(1, self.num_floors)
            )  # Skip the 0 floor. I might want to flip this so the top floor is 0? I don't know

            # Pick a passenger
            self.building[rand_floor].append(0)

            # Deduct passengers from number of passengers
            self.num_passengers_left -= 1

        # Scratch
        # next_passenger = self.passenger_list.pop()
        # # Put the passenger at that floor
        # self.building[rand_floor]...
        # call the lift?

    # def _create_passengers(self):
    #     generated_passengers = [
    #         _ / 10 for _ in random.sample(range(400, 1500), self.num_passengers)
    #     ]
    #     return generated_passengers

    def __repr__(self):
        return f"A Building with {self.num_floors} floors and {self.max_num_passengers} passengers. {self.building}"
