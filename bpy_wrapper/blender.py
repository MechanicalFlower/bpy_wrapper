import bpy  # type: ignore

from .utils.singleton import Singleton


class Blender(metaclass=Singleton):
    def __init__(self, *, do_reset: bool = True):
        # Import default scene and settings.
        # bpy.ops.wm.read_factory_settings()

        if do_reset:
            # Clear data.
            for bpy_data_iter in (
                bpy.data.objects,
                bpy.data.meshes,
                bpy.data.cameras,
                bpy.data.materials,
                bpy.data.collections,
            ):
                for id_data in bpy_data_iter:
                    bpy_data_iter.remove(id_data, do_unlink=True)

    def close(self, background: bool) -> None:
        if not background:
            bpy.ops.wm.quit_blender()
