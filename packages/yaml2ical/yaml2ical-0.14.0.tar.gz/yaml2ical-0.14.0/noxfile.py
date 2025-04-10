import nox


nox.options.error_on_external_run = True
nox.options.reuse_existing_virtualenvs = True
nox.options.sessions = ["tests-3", "linters"]


# Convenience wrapper for running the project
@nox.session(python="3")
def mkical(session):
    session.install(".")
    session.run("yaml2ical", "-y", "meetings/", "-i", "icals/", "-f")


# Note setting python this way seems to give us a target name without
# python specific suffixes while still allowing us to force a specific
# version using --force-python.
@nox.session(python="3")
def linters(session):
    # TODO: switch this line to 'session.install("--group", "test-linters")'
    session.install(".[test-linters]")
    session.run("flake8")


@nox.session(python="3")
def venv(session):
    # TODO: switch to 'session.install("-e", ".", "--group", "test-unit")'
    session.install("-e", ".[test-unit]")
    session.run(*session.posargs)


# This will attempt to run python3 tests by default.
@nox.session(python=["3"])
def tests(session):
    # TODO: switch to 'session.install("-e", ".", "--group", "test-unit")'
    session.install("-e", ".[test-unit]")
    session.run("stestr", "run", *session.posargs)
    session.run("stestr", "slowest")
