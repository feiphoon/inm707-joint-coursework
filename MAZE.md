# Maze environment

The maze environment is produced by the `Maze` class in `maze.py`. It uses [Prim's algorithm](https://en.wikipedia.org/wiki/Prim%27s_algorithm) to generate the walls and create a solvable maze each time.

Provide the desired width and height (defaults to `5x5`), and it generates a maze that can take the following cell types. The result will have an entrance at the top and an exit at the bottom.

```python
@unique
class Cell(IntEnum):
    EMPTY = 0
    WALL = 1
    ENTRANCE = 2
    EXIT = 3
    UNTRAVERSED = 4
    ERROR = 5
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
m20 = Maze(20,20)
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
