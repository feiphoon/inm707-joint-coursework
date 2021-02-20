import pytest
from maze import Maze


class TestMaze:
    def test_default_maze(self):
        result = Maze()
        assert result.maze_width == 5
        assert result.maze_height == 5
        assert result.position_agent == result.position_entrance
        assert result.position_entrance != None
        assert result.position_exit != None
        assert result.turns_elapsed == 0
        assert result.done == False

    def test_custom_maze(self):
        result = Maze(size=10)
        assert result.maze_width == 10
        assert result.maze_height == 10
        assert result.position_agent == result.position_entrance
        assert result.position_entrance != None
        assert result.position_exit != None
        assert result.turns_elapsed == 0
        assert result.done == False
