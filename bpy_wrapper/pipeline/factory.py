from ..blender import Blender
from ..struct import Collection, Scene
from .psx import PSXPipeline


class PipelineFactory:
    @staticmethod
    def psxify(app: Blender, scene: Scene, collection: Collection) -> Scene:
        return PSXPipeline(app, scene, collection).execute()
