import bpy  # type: ignore

from bpy_wrapper import Blender, Scene


class TestScene:
    SCENE_NAME = "TestScene"

    def test_0001_create_scene(self, app: Blender) -> None:
        assert self.SCENE_NAME not in bpy.data.scenes

        # Create a scene wrapper
        scene = Scene(self.SCENE_NAME, app)

        # Create a scene
        scene.create()

        assert self.SCENE_NAME in bpy.data.scenes

    def test_0002_remove_scene(self, app: Blender) -> None:
        assert self.SCENE_NAME in bpy.data.scenes

        # Create a scene wrapper
        scene = Scene(self.SCENE_NAME, app)

        # Remove a scene
        scene.remove()

        assert self.SCENE_NAME not in bpy.data.scenes
