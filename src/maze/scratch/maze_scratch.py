class Step(Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)


"u"
Cell.UNTRAVERSED.value

"c"
Cell.EMPTY.value

"w"
Cell.WALL.value


walls
self.generation_start_neighbours


maze[rand_wall[0]][rand_wall[1]]
self.maze[rand_nb_coords]

[rand_nb_coords[0], rand_nb_coords[1] - 1]
self._add_coord_tuples(rand_nb_coords, Step.LEFT)
maze[rand_wall[0]][rand_wall[1] - 1]
self.maze[self._add_coord_tuples(rand_nb_coords, Step.LEFT)]


[
    rand_nb_coords[0],
    rand_nb_coords[1] + 1,
]
self._add_coord_tuples(rand_nb_coords, Step.RIGHT)
maze[rand_wall[0]][rand_wall[1] + 1]
self.maze[self._add_coord_tuples(rand_nb_coords, Step.RIGHT)]


[rand_nb_coords[0] - 1, rand_nb_coords[1]]
self._add_coord_tuples(rand_nb_coords, Step.UP)
maze[rand_wall[0] - 1][rand_wall[1]]
self.maze[self._add_coord_tuples(rand_nb_coords, Step.UP)]


[rand_nb_coords[0] + 1, rand_nb_coords[1]]
self._add_coord_tuples(rand_nb_coords, Step.DOWN)
maze[rand_wall[0] + 1][rand_wall[1]]
self.maze[self._add_coord_tuples(rand_nb_coords, Step.DOWN)]

_[0] == rand_nb_coords[0] and _[1] == rand_nb_coords[1]
_ == rand_nb_coords

width
self.maze_width

height
self.maze_height

while self.generation_start_neighbours:
    # Pick a random wall
    rand_nb_coords = self.generation_start_neighbours[
        int(random.random() * len(self.generation_start_neighbours)) - 1
    ]

    # Check if it is a left wall
    if rand_nb_coords[1] != 0:
        if (
            self.maze[self._add_coord_tuples(rand_nb_coords, Step.LEFT)]
            == Cell.UNTRAVERSED.value
            and self.maze[self._add_coord_tuples(rand_nb_coords, Step.RIGHT)]
            == Cell.UNTRAVERSED.value
        ):
            # Find the number of surrounding cells
            s_cells = surroundingCells(rand_nb_coords)

            if s_cells < 2:
                # Denote the new path
                self.maze[rand_nb_coords] = Cell.UNTRAVERSED.value

                # Mark the new walls
                # Upper cell
                if rand_nb_coords[0] != 0:
                    if (
                        self.maze[self._add_coord_tuples(rand_nb_coords, Step.UP)]
                        != Cell.UNTRAVERSED.value
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
                        self.maze[self._add_coord_tuples(rand_nb_coords, Step.DOWN)]
                        != Cell.UNTRAVERSED.value
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
                        self.maze[self._add_coord_tuples(rand_nb_coords, Step.LEFT)]
                        != Cell.UNTRAVERSED.value
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
            == Cell.UNTRAVERSED.value
        ):

            s_cells = surroundingCells(rand_nb_coords)
            if s_cells < 2:
                # Denote the new path
                self.maze[rand_nb_coords] = Cell.UNTRAVERSED.value

                # Mark the new walls
                # Upper cell
                if rand_nb_coords[0] != 0:
                    if (
                        self.maze[self._add_coord_tuples(rand_nb_coords, Step.UP)]
                        != Cell.UNTRAVERSED.value
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
                        self.maze[self._add_coord_tuples(rand_nb_coords, Step.LEFT)]
                        != Cell.UNTRAVERSED.value
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
                        self.maze[self._add_coord_tuples(rand_nb_coords, Step.RIGHT)]
                        != Cell.UNTRAVERSED.value
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
            == Cell.UNTRAVERSED.value
        ):

            s_cells = surroundingCells(rand_nb_coords)
            if s_cells < 2:
                # Denote the new path
                self.maze[rand_nb_coords] = Cell.UNTRAVERSED.value

                # Mark the new walls
                if rand_nb_coords[0] != self.maze_height - 1:
                    if (
                        self.maze[self._add_coord_tuples(rand_nb_coords, Step.DOWN)]
                        != Cell.UNTRAVERSED.value
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
                        self.maze[self._add_coord_tuples(rand_nb_coords, Step.LEFT)]
                        != Cell.UNTRAVERSED.value
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
                        self.maze[self._add_coord_tuples(rand_nb_coords, Step.RIGHT)]
                        != Cell.UNTRAVERSED.value
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
            == Cell.UNTRAVERSED.value
        ):

            s_cells = surroundingCells(rand_nb_coords)
            if s_cells < 2:
                # Denote the new path
                self.maze[rand_nb_coords] = Cell.UNTRAVERSED.value

                # Mark the new walls
                if rand_nb_coords[1] != self.maze_width - 1:
                    if (
                        self.maze[self._add_coord_tuples(rand_nb_coords, Step.RIGHT)]
                        != Cell.UNTRAVERSED.value
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
                        self.maze[self._add_coord_tuples(rand_nb_coords, Step.DOWN)]
                        != Cell.UNTRAVERSED.value
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
                        self.maze[self._add_coord_tuples(rand_nb_coords, Step.UP)]
                        != Cell.UNTRAVERSED.value
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

printMaze(maze)