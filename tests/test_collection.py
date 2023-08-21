import bpy  # type: ignore

from bpy_wrapper import Blender, Collection, Scene


class TestCollection:
    COLLECTION_NAME = "TestCollection"

    def test_0001_create_collection(self, app: Blender, scene: Scene) -> None:
        assert self.COLLECTION_NAME not in bpy.data.collections

        # Create a collection wrapper
        collection = Collection(self.COLLECTION_NAME, app)

        # Create a collection
        collection.create(collection_to_link_to=scene.bpy_root_collection)

        assert self.COLLECTION_NAME in bpy.data.collections

    def test_0002_remove_collection(self, app: Blender) -> None:
        assert self.COLLECTION_NAME in bpy.data.collections

        # Create a collection wrapper
        collection = Collection(self.COLLECTION_NAME, app)

        # Remove the collection
        collection.remove()

        assert self.COLLECTION_NAME not in bpy.data.collections
