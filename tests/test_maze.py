import pytest
import numpy as np
from maze import Maze, Cell, Step


@pytest.fixture(scope="function")
def fixture_default_maze():
    yield Maze()


@pytest.fixture(scope="function")
def fixture_custom10_maze():
    yield Maze(10)


class TestCellIntEnum:
    def test_cells(self):
        assert Cell.EMPTY == 0
        assert Cell.WALL == 1
        assert Cell.ENTRANCE == 2
        assert Cell.EXIT == 3
        assert Cell.UNTRAVERSED == 4
        assert Cell.ERROR == 5
        assert Cell.AGENT == 9


class TestStepEnum:
    def test_steps(self):
        assert Step.UP.value == (-1, 0)
        assert Step.DOWN.value == (1, 0)
        assert Step.LEFT.value == (0, -1)
        assert Step.RIGHT.value == (0, 1)


class TestMaze:
    def test_default_maze(self, fixture_default_maze):
        result = fixture_default_maze
        assert result.maze_width == 5
        assert result.maze_height == 5
        assert result.maze.dtype == "int"
        assert result.maze.shape == (5, 5)
        assert result.position_agent == result.position_entrance
        assert result.position_entrance != None
        assert result.position_exit != None
        assert result.turns_elapsed == 0
        assert result.done == False
        # No walls are left untraversed
        assert np.all(result.maze[:, :] != Cell.UNTRAVERSED.value)

    def test_custom_maze(self, fixture_custom10_maze):
        result = fixture_custom10_maze
        assert result.maze_width == 10
        assert result.maze_height == 10
        assert result.maze.dtype == "int"
        assert result.maze.shape == (10, 10)
        assert result.position_agent == result.position_entrance
        assert result.position_entrance != None
        assert result.position_exit != None
        assert result.turns_elapsed == 0
        assert result.done == False
        # No walls are left untraversed
        assert np.all(result.maze[:, :] != Cell.UNTRAVERSED.value)


class TestMazeCells:
    def test_default_maze_walls_left_right(self, fixture_default_maze):
        result = fixture_default_maze
        assert np.all(result.maze[:, 0] == Cell.WALL.value)
        assert np.all(result.maze[:, -1] == Cell.WALL.value)

    def test_default_maze_walls_top(self, fixture_default_maze):
        result = fixture_default_maze
        # This top wall will have 1 entrance
        unique, *_ = np.unique(result.maze[0, :], return_counts=True)
        assert len(unique) == len([Cell.WALL.value, Cell.ENTRANCE.value])
        assert [Cell.WALL.value, Cell.ENTRANCE.value] in unique
        assert (
            result.maze[0, :].tolist().count(Cell.WALL.value) == result.maze_width - 1
        )
        assert result.maze[0, :].tolist().count(Cell.ENTRANCE.value) == 1

    def test_default_maze_walls_bottom(self, fixture_default_maze):
        result = fixture_default_maze
        # This top wall will have 1 exit
        unique, *_ = np.unique(result.maze[-1, :], return_counts=True)
        assert len(unique) == len([Cell.WALL.value, Cell.ENTRANCE.value])
        assert [Cell.WALL.value, Cell.EXIT.value] in unique
        assert (
            result.maze[-1, :].tolist().count(Cell.WALL.value) == result.maze_height - 1
        )
        assert result.maze[-1, :].tolist().count(Cell.EXIT.value) == 1
