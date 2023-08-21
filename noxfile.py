import nox


@nox.session
def test(session: nox.Session) -> None:
    session.install("poetry")
    session.run("poetry", "install")
    session.run("pytest")
