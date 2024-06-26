import nox

nox.options.sessions = ["lint", "typing", "tests"]
locations = ["noxfile.py", "setup.py", "digaws/", "tests/"]

lint_common_args = ["--max-line-length", "100"]
black_args = ["--line-length", "100"]
mypy_args = ["--ignore-missing-imports", "--install-types", "--non-interactive"]

pytest_args = ["--cov=digaws", "--cov-report=", "tests/"]
coverage_args = ["report", "--show-missing", "--fail-under=80"]


@nox.session()
def lint(session):
    args = session.posargs or locations
    session.install("pycodestyle", "flake8", "black")
    session.run("pycodestyle", *(lint_common_args + args))
    session.run("flake8", *(lint_common_args + args))
    session.run("black", "--check", *(black_args + args))


@nox.session()
def typing(session):
    args = session.posargs or locations
    session.install("mypy")
    session.run("mypy", *(mypy_args + args))


@nox.session()
def tests(session):
    args = session.posargs
    session.install("-r", "requirements_test.txt")
    session.run("pytest", *(pytest_args + args))
    session.run("coverage", *coverage_args)
