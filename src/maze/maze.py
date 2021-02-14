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


CELL_DISPLAY_DICT = {0: ".", 1: "X", 2: ".", 3: "E", 4: "-", 5: "?", 9: "A"}


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

    def _count_surrounding_empty_cells(self, rand_nb_coords):
        """
        Make a useful surrounding cell function.
        Count the number of surrounding empty cells.
        """
        a = [
            self.maze[self._add_coord_tuples(rand_nb_coords, _)] == Cell.EMPTY.value
            for _ in list(Step)
        ]
        return sum(a)

    def _fill_in_walls(self):
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

    def _create_entrance_exit(self):
        # Create entrance (top of maze)
        for i in range(0, self.maze_width):
            # Check for first instance of the second row
            # (row[1]) having a clear empty cell.
            # If it does, we will put the entrance above it, on the border.
            if self.maze[1][i] == Cell.EMPTY.value:
                self.maze[0][i] = Cell.ENTRANCE.value
                break

        # Create exit (bottom of maze)
        for i in range(self.maze_width - 1, 0, -1):
            # Check for first instance of the second last row
            # (row[-2]) having a clear empty cell.
            # If it does, we will put the exit below it, on the border.
            if self.maze[self.maze_height - 2][i] == Cell.EMPTY.value:
                self.maze[self.maze_height - 1][i] = Cell.EXIT.value
                break

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
m.display()
