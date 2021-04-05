# Maze (& QMaze) environments


## Maze
The maze environment is produced by the `Maze` class in `maze.py`. It uses [Prim's algorithm](https://en.wikipedia.org/wiki/Prim%27s_algorithm) to generate the walls and create a solvable maze each time.

Provide the desired size (defaults to `5x5`), and it generates a maze that can take the following cell types. The result will have an entrance at the top and an exit at the bottom.

```python
@unique
class Cell(IntEnum):
    EMPTY = 0
    WALL = 1
    ENTRANCE = 2
    EXIT = 3
    TREASURE = 4
    UNTERRAFORMED = 5
    ERROR = 6
    AGENT = 9
```

```python
CELL_DISPLAY_DICT = {
    0: ".",
    1: "X",
    2: "I",
    3: "O",
    4: "-",
    5: "?",
    9: "A"
}
```

Generate and display the maze like so:

```bash
python maze.py
```

```python
m5 = Maze()
m5.display()
```

Output:

```bash
X I X X X
X . X . X
X . X . X
X . . . X
X X X O X
```

Or:

```python
m20 = Maze(20)
m20.display()
```

Output:
```bash
X I X X X X X X X X X X X X X X X X X X
X . . . X . X . . . X . . X X . X . X X
X X . X X . . . X X X . X X . . . . . X
X . . . X X . X X X X . . X X . X X X X
X . X . . . . . . . X . X X . . . . . X
X . X X . X . X X . . . . . . X X . X X
X . X . . X X X X . X . X X . X X X X X
X . X X . X . . . . X . . X . . X X . X
X . X . . X X . X . X . X X X X X . . X
X . X X . . X X X . X . . . . . . . X X
X . . X X . X X . . X . X X X . X X X X
X X X X X . X . . X X . X X . . . . . X
X . . . . . X X . X X X X X X . X . X X
X . X . X X X X . . . . . . X . X . . X
X X X X X X . X . X X . X . X X X X . X
X X . X . . . . . . X X X . . X X . . X
X . . . . X X . X . . . X X . . X X . X
X . X X . X X . X . X X X X X . . X X X
X . X . . X X . X . . . . . X X . . . X
X X X X X X X X X X X X X X X X X X O X
```

Adding a `debug=True` parameter to the display function (`display(debug=True)`) will print all instance (`self`)variables.

## QMaze

The `QMaze` class extends the `Maze` class and is found in `q_maze.py`.

It has a modification on top of `Maze` whereby it will return a state rather than an observation,
so it can be used to produce Q-values.
