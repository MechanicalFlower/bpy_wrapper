import abc

from ..blender import Blender
from ..struct import Scene


class Pipeline:
    """
    Each `Pipeline` take scene in input and
    setup the scene as intended by the pipeline.
    """
    def __init__(self, app: Blender, scene: Scene) -> None:
        self._app = app
        self._scene = scene

    @abc.abstractmethod
    def execute(self) -> Scene:
        raise NotImplementedError
