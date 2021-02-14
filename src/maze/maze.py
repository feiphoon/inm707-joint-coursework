import operator
from enum import Enum, IntEnum, unique
from random import randint, choice
import numpy as np


@unique
class Cell(IntEnum):
    EMPTY = 0
    WALL = 1
    ENTRANCE = 2
    EXIT = 3
    UNTRAVERSED = 4
    ERROR = 5


# Probably going to replace this later
@unique
class Step(Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)


# class CellDisplay(Enum):
#     CELL = "."
#     WALL = "X"
#     ENTRANCE = "."
#     EXIT = "E"
#     AGENT = "A"


CELL_DISPLAY_DICT = {0: ".", 1: "X", 2: ".", 3: "E", 4: "U", 5: "?", 9: "A"}


class Maze:
    def __init__(self, width=5, height=5):
        assert type(width) is int
        assert type(height) is int
        self.maze_width = width
        self.maze_height = height
        self.position_agent = None

        self.maze = np.full(
            (self.maze_width, self.maze_height), Cell.UNTRAVERSED.value, dtype=int
        )

        self._build_maze()

        # Turns or timesteps
        self.turns_elapsed = 0

    def _add_coord_tuples(self, coord, step):
        return tuple(map(operator.add, coord, step.value))

    def _build_maze(self):
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
        self.generation_start_neighbours = {}
        # self.generation_start_neighbours[Step.UP.name] = tuple(
        #     map(operator.add, self.generation_start_coords, Step.UP.value)
        # )
        # self.generation_start_neighbours[Step.DOWN.name] = tuple(
        #     map(operator.add, self.generation_start_coords, Step.DOWN.value)
        # )
        # self.generation_start_neighbours[Step.LEFT.name] = tuple(
        #     map(operator.add, self.generation_start_coords, Step.LEFT.value)
        # )
        # self.generation_start_neighbours[Step.RIGHT.name] = tuple(
        #     map(operator.add, self.generation_start_coords, Step.RIGHT.value)
        # )

        self.generation_start_neighbours[Step.UP.name] = self._add_coord_tuples(
            self.generation_start_coords, Step.UP
        )

        self.generation_start_neighbours[Step.DOWN.name] = self._add_coord_tuples(
            self.generation_start_coords, Step.DOWN
        )

        self.generation_start_neighbours[Step.LEFT.name] = self._add_coord_tuples(
            self.generation_start_coords, Step.LEFT
        )

        self.generation_start_neighbours[Step.RIGHT.name] = self._add_coord_tuples(
            self.generation_start_coords, Step.RIGHT
        )

        # Apply walls to surround starting point in the maze.
        for _ in self.generation_start_neighbours.values():
            self.maze[_] = Cell.WALL.value

        #
        # All border cells are obstacles.
        # self.maze[:, 0] = Cell.WALL.value
        # self.maze[:, -1] = Cell.WALL.value
        # self.maze[0, :] = Cell.WALL.value
        # self.maze[-1, :] = Cell.WALL.value

    def display(self, debug=False):
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


m = Maze()
m.display(debug=True)