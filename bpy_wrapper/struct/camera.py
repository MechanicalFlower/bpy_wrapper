from typing import Any, Dict, Optional, Tuple

import bpy  # type: ignore

from ..wrapper import ObjectWrapper


class Camera(ObjectWrapper):
    @property
    def bpy_camera(self) -> bpy.types.Camera:
        return bpy.data.cameras[self._name]

    def create(self, **kwargs: Any) -> 'Camera':
        cam = bpy.data.cameras.new(name=self._name)
        bpy.data.objects.new(self._name, cam)

        return self.setup(**kwargs)

    def setup(
        self, *,
        collection_to_link_to: Optional[bpy.types.Collection] = None,
        location: Tuple[float, float, float] = (0, 0, 0),
        data: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> 'Camera':
        if collection_to_link_to:
            collection_to_link_to.objects.link(self.bpy_object)

        self.bpy_object.location = location

        if data:
            for key, value in data.items():
                setattr(self.bpy_object.data, key, value)

        return self

    def remove(self) -> 'Camera':
        bpy.data.objects.remove(self.bpy_object)
        bpy.data.cameras.remove(self.bpy_camera)
        return self
