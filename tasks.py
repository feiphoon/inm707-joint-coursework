from invoke import task


@task
def test(c):
    c.run("pytest -v --doctest-modules", pty=True)


@task
def lint(c):
    c.run("python -m flake8 src/.", pty=True)
    c.run("python -m flake8 tests/.", pty=True)
    c.run("python -m black --check .", pty=True)
