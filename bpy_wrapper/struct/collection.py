import logging
from typing import Any, Optional

import bpy  # type: ignore

from ..wrapper import Wrapper

logger = logging.getLogger(__file__)


class Collection(Wrapper):
    @property
    def bpy_collection(self) -> bpy.types.Collection:
        return bpy.data.collections[self._name]

    def create(self, **kwargs: Any) -> 'Collection':
        logger.debug("Checking if %s exists", self._name)

        if self._name in bpy.data.collections:
            logger.debug("%s already exists", self._name)

        else:
            logger.debug("%s does not exist", self._name)

            logger.debug("Create %s", self._name)
            bpy.ops.collection.create(name=self._name)

        return self.setup(**kwargs)

    def setup(
        self, *,
        collection_to_link_to: Optional[bpy.types.Collection] = None,
        **kwargs: Any
    ) -> 'Collection':
            if collection_to_link_to:
                collection_to_link_to.children.link(self.bpy_collection)
            return self

    def replace(self, new_collection: 'Collection') -> 'Collection':
        obj = [o for o in self.bpy_collection.objects]

        collection_to_link_to = bpy.data.collections[new_collection._name]
        while obj:
            # Relink everything from the collection
            collection_to_link_to.objects.link(obj.pop())

        return self

    def clean(self) -> 'Collection':
        obj = [o for o in self.bpy_collection.objects]

        while obj:
            # Removing everything from the collection
            bpy.data.objects.remove(obj.pop())

        return self

    def remove(self) -> 'Collection':
        bpy.data.collections.remove(self.bpy_collection)
        return self

    def set_visibility(self, show: bool) -> 'Collection':
        self.bpy_collection.hide_render = (not show)
        return self
