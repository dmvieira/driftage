from spade.container import Container


def pytest_unconfigure(config):
    container = Container()
    container.stop()