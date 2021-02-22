import operator
from enum import Enum, IntEnum, unique
from random import randint, choice
import numpy as np
from typing import List
from collections import namedtuple

from datetime import datetime

# import logging


# dt_now = datetime.now()
# dt_str = dt_now.strftime("%Y%m%d-%H%M%S")
# LOG_PATH = f"logs/{dt_str}.log"

# with open(LOG_PATH, "w") as f:
#     f.write(dt_now.strftime("%c"))

# logging.basicConfig(filename=LOG_PATH, filemode="a", level=logging.DEBUG)
# logger = logging.getLogger()

# logger.addHandler(logging.FileHandler(LOG_PATH, "a"))
# print = logger.debug

# TODO: Observations - maybe only neighbours
#Observation = namedtuple("Observation", "distance_to_exit neighbours")


@unique
class Cell(IntEnum):
    EMPTY = 0
    WALL = 1
    ENTRANCE = 2
    EXIT = 3
    UNTRAVERSED = 4
    ERROR = 5
    AGENT = 9


# TODO: Probably going to replace this later as Action
@unique
class Step(Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)


CELL_DISPLAY_DICT = {0: ".", 1: "X", 2: "I", 3: "O", 4: "-", 5: "?", 9: "A"}


class Maze:
    def __init__(self, size: int = 5) -> None:
        """
        Maze can only be square for now.
        """
        assert type(size) is int
        self.maze_width = size
        self.maze_height = size
        self.position_agent = None
        self.position_entrance = None
        self.position_exit = None
        self.time_elapsed = 0

        self.maze = np.full(
            (self.maze_width, self.maze_height), Cell.UNTRAVERSED.value, dtype=int
        )

        self._build_maze()

        self.position_agent = self.position_entrance

        # Turns or timesteps
        self.turns_elapsed = 0
        # logger.debug(self.display(debug=True))

        # Make a done state for Maze
        self.done = False

    def _find_empty_cells(self) -> List[tuple]:
        # Gives us two arrays of indices - first array
        # for row and second for column indices.
        # E.g. array([1, 3]), array([2, 4])
        cell_indices_arrays = np.where(self.maze == Cell.EMPTY.value)

        # Zip these together to give a list of tuples of coordinates
        # E.g. [(1, 2), (3, 4)]
        return list(zip(cell_indices_arrays[0], cell_indices_arrays[1]))

    def _add_coord_tuples(self, coord: tuple, step: Step) -> tuple:
        return tuple(map(operator.add, coord, step.value))

    def _count_surrounding_empty_cells(self, rand_nb_coords: tuple) -> int:
        """
        Make a useful surrounding cell function.
        Count the number of surrounding empty cells.
        """
        a = [
            self.maze[self._add_coord_tuples(rand_nb_coords, _)] == Cell.EMPTY.value
            for _ in list(Step)
        ]
        return sum(a)

    def _fill_in_walls(self) -> None:
        """
        Convert untraversed cells, left in gaps, to walls.
        """
        # Set all border cells as walls.
        self.maze[:, 0] = Cell.WALL.value
        self.maze[:, -1] = Cell.WALL.value
        self.maze[0, :] = Cell.WALL.value
        self.maze[-1, :] = Cell.WALL.value

        # Fill in untraversed gaps
        for i in range(0, self.maze_height):
            for j in range(0, self.maze_width):
                if self.maze[i][j] == Cell.UNTRAVERSED.value:
                    self.maze[i][j] = Cell.WALL.value

    def _create_entrance_exit(self) -> None:
        # Create entrance (top of maze)
        for i in range(0, self.maze_width):
            # Check for first instance of the second row
            # (row[1]) having a clear empty cell.
            # If it does, we will put the entrance above it, on the border.
            if self.maze[1][i] == Cell.EMPTY.value:
                self.maze[0][i] = Cell.ENTRANCE.value
                self.position_entrance = (0, i)
                break

        # Create exit (bottom of maze)
        for i in range(self.maze_width - 1, 0, -1):
            # Check for first instance of the second last row
            # (row[-2]) having a clear empty cell.
            # If it does, we will put the exit below it, on the border.
            if self.maze[self.maze_height - 2][i] == Cell.EMPTY.value:
                self.maze[self.maze_height - 1][i] = Cell.EXIT.value
                self.position_exit = (self.maze_height - 1, i)
                break

    def _build_maze(self) -> None:
        """Following Randomised Prim's algorithm:
        https://en.wikipedia.org/wiki/Maze_generation_algorithm#Randomized_Prim's_algorithm
        With help from:
        https://medium.com/swlh/fun-with-python-1-maze-generator-931639b4fb7e
        """
        # Pick starting coordinates to build maze.
        # The starting point cannot be on the edge of the maze,
        # so that we have space for neighbours (-1),
        # and don't forget zero-indexing (-1). That gives us -2.
        # Immutable.
        self.generation_start_coords = (
            randint(1, self.maze_height - 2),
            randint(1, self.maze_width - 2),
        )

        self.maze[self.generation_start_coords] = Cell.EMPTY.value

        # Get coordinates of neighbours directly,
        # above, below, left and right of the starting point.
        self.generation_start_neighbours = []

        self.generation_start_neighbours.append(
            self._add_coord_tuples(self.generation_start_coords, Step.UP)
        )

        self.generation_start_neighbours.append(
            self._add_coord_tuples(self.generation_start_coords, Step.DOWN)
        )

        self.generation_start_neighbours.append(
            self._add_coord_tuples(self.generation_start_coords, Step.LEFT)
        )

        self.generation_start_neighbours.append(
            self._add_coord_tuples(self.generation_start_coords, Step.RIGHT)
        )

        # Apply walls to surround starting point in the maze.
        for _ in self.generation_start_neighbours:
            self.maze[_] = Cell.WALL.value

        while len(self.generation_start_neighbours) != 0:
            # Pick a random wall
            rand_nb_coords = choice(self.generation_start_neighbours)

            # Check if it is a left wall
            if rand_nb_coords[1] != 0:
                if (
                    self.maze[self._add_coord_tuples(rand_nb_coords, Step.LEFT)]
                    == Cell.UNTRAVERSED.value
                    and self.maze[self._add_coord_tuples(rand_nb_coords, Step.RIGHT)]
                    == Cell.EMPTY.value
                ):
                    # Find the number of surrounding cells
                    if self._count_surrounding_empty_cells(rand_nb_coords) < 2:
                        # Denote the new path
                        self.maze[rand_nb_coords] = Cell.EMPTY.value

                        # Mark the new walls
                        # Upper cell
                        if rand_nb_coords[0] != 0:
                            if (
                                self.maze[
                                    self._add_coord_tuples(rand_nb_coords, Step.UP)
                                ]
                                != Cell.EMPTY.value
                            ):
                                self.maze[
                                    self._add_coord_tuples(rand_nb_coords, Step.UP)
                                ] = Cell.WALL.value
                            if (
                                self._add_coord_tuples(rand_nb_coords, Step.UP)
                                not in self.generation_start_neighbours
                            ):
                                self.generation_start_neighbours.append(
                                    self._add_coord_tuples(rand_nb_coords, Step.UP)
                                )

                        # Bottom cell
                        if rand_nb_coords[0] != self.maze_height - 1:
                            if (
                                self.maze[
                                    self._add_coord_tuples(rand_nb_coords, Step.DOWN)
                                ]
                                != Cell.EMPTY.value
                            ):
                                self.maze[
                                    self._add_coord_tuples(rand_nb_coords, Step.DOWN)
                                ] = Cell.WALL.value
                            if (
                                self._add_coord_tuples(rand_nb_coords, Step.DOWN)
                                not in self.generation_start_neighbours
                            ):
                                self.generation_start_neighbours.append(
                                    self._add_coord_tuples(rand_nb_coords, Step.DOWN)
                                )

                        # Leftmost cell
                        if rand_nb_coords[1] != 0:
                            if (
                                self.maze[
                                    self._add_coord_tuples(rand_nb_coords, Step.LEFT)
                                ]
                                != Cell.EMPTY.value
                            ):
                                self.maze[
                                    self._add_coord_tuples(rand_nb_coords, Step.LEFT)
                                ] = Cell.WALL.value
                            if (
                                self._add_coord_tuples(rand_nb_coords, Step.LEFT)
                                not in self.generation_start_neighbours
                            ):
                                self.generation_start_neighbours.append(
                                    self._add_coord_tuples(rand_nb_coords, Step.LEFT)
                                )

                    # Delete wall
                    for _ in self.generation_start_neighbours:
                        if _ == rand_nb_coords:
                            self.generation_start_neighbours.remove(_)

                    continue

            # Check if it is an upper wall
            if rand_nb_coords[0] != 0:
                if (
                    self.maze[self._add_coord_tuples(rand_nb_coords, Step.UP)]
                    == Cell.UNTRAVERSED.value
                    and self.maze[self._add_coord_tuples(rand_nb_coords, Step.DOWN)]
                    == Cell.EMPTY.value
                ):

                    if self._count_surrounding_empty_cells(rand_nb_coords) < 2:
                        # Denote the new path
                        self.maze[rand_nb_coords] = Cell.EMPTY.value

                        # Mark the new walls
                        # Upper cell
                        if rand_nb_coords[0] != 0:
                            if (
                                self.maze[
                                    self._add_coord_tuples(rand_nb_coords, Step.UP)
                                ]
                                != Cell.EMPTY.value
                            ):
                                self.maze[
                                    self._add_coord_tuples(rand_nb_coords, Step.UP)
                                ] = Cell.WALL.value
                            if (
                                self._add_coord_tuples(rand_nb_coords, Step.UP)
                                not in self.generation_start_neighbours
                            ):
                                self.generation_start_neighbours.append(
                                    self._add_coord_tuples(rand_nb_coords, Step.UP)
                                )

                        # Leftmost cell
                        if rand_nb_coords[1] != 0:
                            if (
                                self.maze[
                                    self._add_coord_tuples(rand_nb_coords, Step.LEFT)
                                ]
                                != Cell.EMPTY.value
                            ):
                                self.maze[
                                    self._add_coord_tuples(rand_nb_coords, Step.LEFT)
                                ] = Cell.WALL.value
                            if (
                                self._add_coord_tuples(rand_nb_coords, Step.LEFT)
                                not in self.generation_start_neighbours
                            ):
                                self.generation_start_neighbours.append(
                                    self._add_coord_tuples(rand_nb_coords, Step.LEFT)
                                )

                        # Rightmost cell
                        if rand_nb_coords[1] != self.maze_width - 1:
                            if (
                                self.maze[
                                    self._add_coord_tuples(rand_nb_coords, Step.RIGHT)
                                ]
                                != Cell.EMPTY.value
                            ):
                                self.maze[
                                    self._add_coord_tuples(rand_nb_coords, Step.RIGHT)
                                ] = Cell.WALL.value
                            if (
                                self._add_coord_tuples(rand_nb_coords, Step.RIGHT)
                                not in self.generation_start_neighbours
                            ):
                                self.generation_start_neighbours.append(
                                    self._add_coord_tuples(rand_nb_coords, Step.RIGHT)
                                )

                    # Delete wall
                    for _ in self.generation_start_neighbours:
                        if _ == rand_nb_coords:
                            self.generation_start_neighbours.remove(_)

                    continue

            # Check the bottom wall
            if rand_nb_coords[0] != self.maze_height - 1:
                if (
                    self.maze[self._add_coord_tuples(rand_nb_coords, Step.DOWN)]
                    == Cell.UNTRAVERSED.value
                    and self.maze[self._add_coord_tuples(rand_nb_coords, Step.UP)]
                    == Cell.EMPTY.value
                ):
                    if self._count_surrounding_empty_cells(rand_nb_coords) < 2:
                        # Denote the new path
                        self.maze[rand_nb_coords] = Cell.EMPTY.value

                        # Mark the new walls
                        if rand_nb_coords[0] != self.maze_height - 1:
                            if (
                                self.maze[
                                    self._add_coord_tuples(rand_nb_coords, Step.DOWN)
                                ]
                                != Cell.EMPTY.value
                            ):
                                self.maze[
                                    self._add_coord_tuples(rand_nb_coords, Step.DOWN)
                                ] = Cell.WALL.value
                            if (
                                self._add_coord_tuples(rand_nb_coords, Step.DOWN)
                                not in self.generation_start_neighbours
                            ):
                                self.generation_start_neighbours.append(
                                    self._add_coord_tuples(rand_nb_coords, Step.DOWN)
                                )
                        if rand_nb_coords[1] != 0:
                            if (
                                self.maze[
                                    self._add_coord_tuples(rand_nb_coords, Step.LEFT)
                                ]
                                != Cell.EMPTY.value
                            ):
                                self.maze[
                                    self._add_coord_tuples(rand_nb_coords, Step.LEFT)
                                ] = Cell.WALL.value
                            if (
                                self._add_coord_tuples(rand_nb_coords, Step.LEFT)
                                not in self.generation_start_neighbours
                            ):
                                self.generation_start_neighbours.append(
                                    self._add_coord_tuples(rand_nb_coords, Step.LEFT)
                                )
                        if rand_nb_coords[1] != self.maze_width - 1:
                            if (
                                self.maze[
                                    self._add_coord_tuples(rand_nb_coords, Step.RIGHT)
                                ]
                                != Cell.EMPTY.value
                            ):
                                self.maze[
                                    self._add_coord_tuples(rand_nb_coords, Step.RIGHT)
                                ] = Cell.WALL.value
                            if (
                                self._add_coord_tuples(rand_nb_coords, Step.RIGHT)
                                not in self.generation_start_neighbours
                            ):
                                self.generation_start_neighbours.append(
                                    self._add_coord_tuples(rand_nb_coords, Step.RIGHT)
                                )

                    # Delete wall
                    for _ in self.generation_start_neighbours:
                        if _ == rand_nb_coords:
                            self.generation_start_neighbours.remove(_)

                    continue

            # Check the right wall
            if rand_nb_coords[1] != self.maze_width - 1:
                if (
                    self.maze[self._add_coord_tuples(rand_nb_coords, Step.RIGHT)]
                    == Cell.UNTRAVERSED.value
                    and self.maze[self._add_coord_tuples(rand_nb_coords, Step.LEFT)]
                    == Cell.EMPTY.value
                ):

                    if self._count_surrounding_empty_cells(rand_nb_coords) < 2:
                        # Denote the new path
                        self.maze[rand_nb_coords] = Cell.EMPTY.value

                        # Mark the new walls
                        if rand_nb_coords[1] != self.maze_width - 1:
                            if (
                                self.maze[
                                    self._add_coord_tuples(rand_nb_coords, Step.RIGHT)
                                ]
                                != Cell.EMPTY.value
                            ):
                                self.maze[
                                    self._add_coord_tuples(rand_nb_coords, Step.RIGHT)
                                ] = Cell.WALL.value
                            if (
                                self._add_coord_tuples(rand_nb_coords, Step.RIGHT)
                                not in self.generation_start_neighbours
                            ):
                                self.generation_start_neighbours.append(
                                    self._add_coord_tuples(rand_nb_coords, Step.RIGHT)
                                )
                        if rand_nb_coords[0] != self.maze_height - 1:
                            if (
                                self.maze[
                                    self._add_coord_tuples(rand_nb_coords, Step.DOWN)
                                ]
                                != Cell.EMPTY.value
                            ):
                                self.maze[
                                    self._add_coord_tuples(rand_nb_coords, Step.DOWN)
                                ] = Cell.WALL.value
                            if (
                                self._add_coord_tuples(rand_nb_coords, Step.DOWN)
                                not in self.generation_start_neighbours
                            ):
                                self.generation_start_neighbours.append(
                                    self._add_coord_tuples(rand_nb_coords, Step.DOWN)
                                )
                        if rand_nb_coords[0] != 0:
                            if (
                                self.maze[
                                    self._add_coord_tuples(rand_nb_coords, Step.UP)
                                ]
                                != Cell.EMPTY.value
                            ):
                                self.maze[
                                    self._add_coord_tuples(rand_nb_coords, Step.UP)
                                ] = Cell.WALL.value
                            if (
                                self._add_coord_tuples(rand_nb_coords, Step.UP)
                                not in self.generation_start_neighbours
                            ):
                                self.generation_start_neighbours.append(
                                    self._add_coord_tuples(rand_nb_coords, Step.UP)
                                )

                    # Delete wall
                    for _ in self.generation_start_neighbours:
                        if _ == rand_nb_coords:
                            self.generation_start_neighbours.remove(_)

                    continue

            # Delete the wall from the list anyway
            for _ in self.generation_start_neighbours:
                if _ == rand_nb_coords:
                    self.generation_start_neighbours.remove(_)

        # self.display()

        # Now some cells that will be untraversed, left in gaps.
        # Convert them to walls
        self._fill_in_walls()
        # self.display()
        self._create_entrance_exit()
        # self.display()

    def display(self, debug: bool = False) -> None:
        show_maze = self.maze.copy()

        # Place agent in show maze if it's been initialised
        if self.position_agent is not None:
            show_maze[self.position_agent[0], self.position_agent[1]] = Cell.AGENT.value

        show_maze_repr = ""

        for row in range(self.maze_width):
            line = ""
            for col in range(self.maze_height):
                string_repr = CELL_DISPLAY_DICT.get(
                    show_maze[row, col], CELL_DISPLAY_DICT[5]
                )
                line += "{0:2}".format(string_repr)
            show_maze_repr += line + "\n"

        print(show_maze_repr)
        if debug:
            print(vars(self))

    def reset(self):
        # Start entrance and the agent at the same place
        self._create_entrance_exit()
        # Update position_agent to position_entrance
        self.position_agent = self.position_entrance

        self.turns_elapsed = 0

        observations = self._calculate_observations()
        
        return observations

        self.done = False


    def _calculate_observations(self):
        """This function helps construct the observations
        by calculating the agent's position,so the agent
        can decide on next the steps to take """
        relative_coordinates = tuple(map(operator.sub,self.position_exit, self.position_agent))
    
        surroundings = self.maze[ self.position_agent[0] -1: self.position_agent[0] +2,
                                     self.position_agent[1] -1: self.position_agent[1] +2]

       # obs ={'relative_coordinates':relative_coordinates,
              # 'surroundings': surroundings}

        #Observation = namedtuple('Observation',obs.keys())
        Observation = namedtuple('Observation',["relative_coordinates","surroundings"])
        
        return Observation(relative_coordinates,surroundings)
        
    

    def step(self, action: Step)->(list, int, bool):
        """This function helps us calculate the position
        of the agent ,the immediate rewards based on the
        action and the observations """
        # At every timestep, the agent receives a negative reward
        reward = -1
        _bump = False
        
        # calculate the next position based on the action
        
        next_position = self._add_coord_tuples(self.position_agent, action)

    
        # If the agent bumps into a wall, it doesn't move
        if self.maze[next_position] == Cell.WALL.value:
            _bump = True
        else:
            self.position_agent = next_position

        # calculate reward
        current_cell_type = self.maze[self.position_agent]
        if current_cell_type == Cell.WALL.value:
            reward -= 20

        if current_cell_type == 3:
            reward += self.size**2
            
        if _bump:
            reward -= 5
        
        # calculate observations
        observations = self._calculate_observations()

        
        # update time
        self.turns_elapsed += 1
        #TODO i am not sure here time_elapsed works

        #Verify termination state
        
        #self.done = False
        
        if self.turns_elapsed == self.time_elapsed:
            done = True

        if self.position_agent == self.position_exit:
            done = True   


        return observations, reward, self.done



m = Maze()

m.display(debug=True)
m.step(Step.DOWN)
m.display(debug=True)
m.step(Step.LEFT)
m.display(debug=True)
#print(m._find_empty_cells())
# TODO:
# Make sure the agent can step in different directions correctly
# Make sure the rewards are correct
# Make sure the done state is correct
# Make sure that the timesteps elapsed is correct

#  m.step(Step.UP)
# m.display(debug=True)

#  m.step(Step.DOWN)
# m.display(debug=True)

#  m.step(Step.LEFT)
# m.display(debug=True)

#  m.step(Step.RIGHT)
# m.display(debug=True)
