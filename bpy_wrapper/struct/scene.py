import logging
import os
from typing import Any

import bpy  # type: ignore

from ..wrapper import Wrapper

logger = logging.getLogger(__file__)


class Scene(Wrapper):
    __import_model_funs = {
        ".dae": bpy.ops.wm.collada_import,
        ".3ds": bpy.ops.import_scene.autodesk_3ds,
        ".fbx": bpy.ops.import_scene.fbx,
        ".ply": bpy.ops.import_mesh.ply,
        ".obj": bpy.ops.import_scene.obj,
        ".stl": bpy.ops.import_mesh.stl,
        ".glb": bpy.ops.import_scene.gltf,
    }

    @property
    def bpy_scene(self) -> bpy.types.Scene:
        return bpy.data.scenes[self._name]

    @property
    def bpy_root_collection(self) -> bpy.types.Collection:
        return self.bpy_scene.collection

    def create(self, **kwargs: Any) -> 'Scene':
        bpy.data.scenes.new(name=self._name)
        return self.setup(**kwargs)

    def setup(self, **kwargs: Any) -> 'Scene':
        self.bpy_scene.render.engine = 'BLENDER_EEVEE'
        # self.bpy_scene.render.engine = 'CYCLES'
        # self.bpy_scene.render.image_settings.color_mode = 'RGBA'
        # self.bpy_scene.display.shading.type = 'MATERIAL'
        # self.bpy_scene.display.shading.light = 'FLAT'
        # self.bpy_scene.display.shading.color_type = 'TEXTURE'

        return self

    def remove(self) -> 'Scene':
        bpy.data.scenes.remove(self.bpy_scene)
        return self

    def set_active_camera(self, camera: bpy.types.Object) -> 'Scene':
        self.bpy_scene.camera = camera
        return self

    def with_model(self, input_file: str) -> 'Scene':
        if not os.path.isfile(input_file):
            logger.error("File not found: %s", input_file)
            raise FileNotFoundError

        extension = os.path.splitext(input_file)[1].lower()
        if extension not in self.__import_model_funs:
            logger.error("Unsupported input file extension: %s", extension)
            raise NotImplementedError

        self.__import_model_funs[extension](filepath=input_file)

        return self

    def render(self, output_dir: str, *, use_animation: bool = True) -> 'Scene':
        self.bpy_scene.render.filepath = os.path.join(output_dir, "")
        bpy.ops.render.render(
            animation=use_animation,
            write_still=(not use_animation),
            scene=self._name
        )
        return self
