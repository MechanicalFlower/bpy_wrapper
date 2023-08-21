from typing import Generator

import pytest

from bpy_wrapper import Blender, Scene


@pytest.fixture(scope="session")
def app() -> Blender:
    return Blender()


@pytest.fixture(scope="function")
def scene(app: Blender) -> Generator[Scene, None, None]:
    scene = Scene('FixtureScene', app)
    scene.create()
    yield scene
    scene.remove()
