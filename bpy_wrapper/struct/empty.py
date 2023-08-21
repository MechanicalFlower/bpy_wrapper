from typing import Any, Optional, Tuple

import bpy  # type: ignore

from ..wrapper import ObjectWrapper


class Empty(ObjectWrapper):
    def create(self, **kwargs: Any) -> 'Empty':
        bpy.data.objects.new(self._name, None)
        return self.setup(**kwargs)

    def setup(
        self, *,
        location: Tuple[float, float, float] = (0, 0, 0),
        collection_to_link_to: Optional[bpy.types.Collection] = None,
        **kwargs: Any,
    ) -> 'Empty':
        if collection_to_link_to:
            collection_to_link_to.objects.link(self.bpy_object)

        self.bpy_object.empty_display_size = 1
        self.bpy_object.empty_display_type = 'PLAIN_AXES'

        return self

    def remove(self) -> 'Empty':
        bpy.data.objects.remove(self.bpy_object)
        return self
