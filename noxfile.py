import nox


@nox.session
def lint(session: nox.Session) -> None:
    session.install("poetry")
    session.run("poetry", "install")
    session.run("pre-commit", "run", "-a")


@nox.session
def test(session: nox.Session) -> None:
    session.install("poetry")
    session.run("poetry", "install")
    session.run("pytest")
