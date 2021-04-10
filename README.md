# INM707-joint-coursework

## Coursework details:
### Task1:
Build an environment fit to be used for Task 1 and 2.

Documentation is found [here](MAZE.md) in a separate markdown doc.

### Task 2:

Individual submission, not found in this repo.

### Task3:
We studied A2C (Advantage Actor Critic) and A3C (Asynchronous Actor Critic) -
for the latter multiple environments were needed, and this led us to this package:

- https://stable-baselines3.readthedocs.io/en/master/

The above package has the algorithms implemented, which was useful to test-drive
our environment on, but we have made an attempt to have a version that could be
tweaked with hyperparameters.




## Setup

`git clone` this repo so you can run it locally.

This repo was written for Python 3.8.5. On Mac, please check your version:

```
python --version
```

### Setup to make `stable-baselines3` package available

Install this prerequisite:

```bash
brew install cmake openmpi
```

### Virtualenv

Having a virtual environment gives you a self-contained space to reproduce your project with the right versions of modules. `venv` is the simplest way toward this.

#### Create your new virtual environment

```
cd inm707-joint-coursework # Be in your project folder
python3 -m venv venv # Where venv is the name of your new environment
```

#### Start and set up your new environment

```
source venv/bin/activate
pip install -r requirements.txt # Install the required packages in your new environment
pip list # Optional: check what was installed in `venv`
```
#### Exit your environment

```
deactivate
```


## Contributing and development guidelines

### Good repo hygiene tips

- Don't push without a branch
- Don't merge without a quick review from the other person
- Write informative and succinct commit messages - so we can find stuff and follow logic!
- Many small logical, _passing/working_ commits are better than huge ones - use Github Desktop to stage individual lines
- Use `black` and `flake8` via `inv lint` to tidy up code - keep the reformatting commits separate from the actual code change ones :)

### Code formatting

Just run this:

```
inv lint
```

The packages run by this are as follows (if you want to run them individually).

#### `black`

Aggressive PEP 8 code reformatter.

https://pypi.org/project/black/
```
black . # In the folder you're in, or a particular file you want to format
```

#### `flake8`

Reports PEP 8 violations.

https://pypi.org/project/flake8/
```
flake8 . # In the folder you're in, or a particular file you want to report on
```

### Running tests

Run all types of tests
```
inv test
```
More details follow.

#### `doctest`

Run `doctest` on the docstring tests in `maze.py`.
```
python -m doctest maze.py -v
```

#### `pytest`

Run all `pytest` tests:
```
pytest
```

Run tests for a specific file, where `test_maze.py` is named to match the file you want to test, `maze.py`.
```
pytest tests/test_maze.py
```

Verbose mode with `-v`, is always optional but gives you more information about test results.
```
pytest -v tests/test_maze.py
```

Run a set of tests based on the test name (so you should always name your tests well!).
Here we want to only run tests whose names contain the keyword "error".
```
pytest -k error
# OR
pytest -v -k error
```

Run a group of tests. You need to have applied some Test Classes:
```
pytest tests/test_maze.py::TestBuildMaze
```

You can run a specific method inside a Test Class too:
```
pytest tests/test_maze.py::TestBuildMaze::test_build_maze
```

You can inspect how and in what order your fixtures are set up, by adding the `--setup-show` argument:
```
pytest -v --setup-show tests/test_maze.py
```


#### `pytest` AND `doctest`:

Run both together! The `-v` or verbosity option is not required, but makes it a lot more satisfying.
```
pytest -v --doctest-modules
```

### Recommended VSCode settings

On your machine, create a `.vscode` folder in the root of this repo and create a `settings.json` inside it.

Save the following into it:
```json
{
    "python.terminal.activateEnvironment": true,
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": false,
    "python.linting.flake8Enabled": true,
    "python.linting.flake8Args": [
        "--config",
        ".flake8"
    ],
    "python.formatting.provider": "black",
    "editor.formatOnSave": true,
    "python.pythonPath": "<path to your venv!>venv/bin/python3"
}
```
