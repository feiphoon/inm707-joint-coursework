import pytest
import numpy as np
from maze import Maze, Cell, Step


@pytest.fixture(scope="function")
def fixture_default_maze():
    yield Maze()


@pytest.fixture(scope="function")
def fixture_default_maze_has_treasure():
    yield Maze(has_treasure=True)


@pytest.fixture(scope="function")
def fixture_custom10_maze():
    yield Maze(size=10)


class TestCellIntEnum:
    def test_cells(self):
        assert Cell.EMPTY == 0
        assert Cell.WALL == 1
        assert Cell.ENTRANCE == 2
        assert Cell.EXIT == 3
        assert Cell.TREASURE == 4
        assert Cell.UNTERRAFORMED == 5
        assert Cell.ERROR == 6
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
        assert result.size == 5
        assert result.has_treasure is False
        assert result.treasure_left == 0
        assert result.treasure_found == 0
        assert len(result.treasure_map) == 0
        assert result.maze.dtype == "int"
        assert result.maze.shape == (5, 5)
        assert result.position_agent == result.position_entrance
        assert result.position_entrance is not None
        assert result.position_exit is not None
        assert result.turns_elapsed == 0
        assert result.done is False
        # No walls are left unterraformed
        assert np.all(result.maze[:, :] != Cell.UNTERRAFORMED.value)

    def test_custom_maze(self, fixture_custom10_maze):
        result = fixture_custom10_maze
        assert result.maze_width == 10
        assert result.maze_height == 10
        assert result.size == 10
        assert result.has_treasure is False
        assert result.treasure_left == 0
        assert result.treasure_found == 0
        assert len(result.treasure_map) == 0
        assert result.maze.dtype == "int"
        assert result.maze.shape == (10, 10)
        assert result.position_agent == result.position_entrance
        assert result.position_entrance is not None
        assert result.position_exit is not None
        assert result.turns_elapsed == 0
        assert result.done is False
        # No walls are left unterraformed
        assert np.all(result.maze[:, :] != Cell.UNTERRAFORMED.value)


class TestTreasure:
    def test_default_maze_no_treasure(self, fixture_default_maze):
        result = fixture_default_maze
        assert result.has_treasure is False
        assert len(result.treasure_map) == 0
        assert result.treasure_left == 0
        assert result.treasure_found == 0
        assert np.all(result.maze[:, :] != Cell.TREASURE.value)

    def test_default_maze_yes_treasure(self, fixture_default_maze_has_treasure):
        result = fixture_default_maze_has_treasure
        assert result.has_treasure is True
        assert len(result.treasure_map) > 0
        assert result.treasure_left != 0
        assert result.treasure_found == 0
        assert Cell.TREASURE.value in result.maze[:, :]


class TestMazeCells:
    def test_default_maze_walls_left_right(self, fixture_default_maze):
        result = fixture_default_maze
        assert np.all(result.maze[:, 0] == Cell.WALL.value)
        assert np.all(result.maze[:, -1] == Cell.WALL.value)

    def test_default_maze_walls_top(self, fixture_default_maze):
        result = fixture_default_maze
        # This row 1 will have 1 entrance
        unique, *_ = np.unique(result.maze[1, :], return_counts=True)
        assert len(unique) == len(
            [Cell.EMPTY.value, Cell.WALL.value, Cell.ENTRANCE.value]
        )
        assert [Cell.EMPTY.value, Cell.WALL.value, Cell.ENTRANCE.value] in unique
        assert result.maze[1, :].tolist().count(Cell.ENTRANCE.value) == 1

    def test_default_maze_walls_bottom(self, fixture_default_maze):
        result = fixture_default_maze
        # This bottom wall will have 1 exit
        unique, *_ = np.unique(result.maze[-1, :], return_counts=True)
        assert len(unique) == len([Cell.WALL.value, Cell.EXIT.value])
        assert [Cell.WALL.value, Cell.EXIT.value] in unique
        assert (
            result.maze[-1, :].tolist().count(Cell.WALL.value) == result.maze_height - 1
        )
        assert result.maze[-1, :].tolist().count(Cell.EXIT.value) == 1


class TestMazeEntrance:
    def test_default_maze_entrance_before_after_reset(self, fixture_default_maze):
        # Given an initialised maze:
        result = fixture_default_maze

        # When we reset:
        result.reset()

        # Then we still get the same state in the row 1 wall -
        # apart from entrance MAY have a different position.
        unique, *_ = np.unique(result.maze[1, :], return_counts=True)
        assert len(unique) == len(
            [Cell.WALL.value, Cell.EMPTY.value, Cell.ENTRANCE.value]
        )
        assert [Cell.WALL.value, Cell.EMPTY.value, Cell.ENTRANCE.value] in unique
        assert result.maze[1, :].tolist().count(Cell.ENTRANCE.value) == 1

    def test_default_maze_agent_before_after_reset(self, fixture_default_maze):
        # Given an initialised maze:
        result = fixture_default_maze
        # And the agent is at the entrance:
        assert result.position_agent == result.position_entrance

        # When we reset:
        result.reset()

        # Then the agent and entrance positions are updated to be equal:
        assert result.position_agent == result.position_entrance
