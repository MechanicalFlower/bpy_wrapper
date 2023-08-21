import abc
from typing import Any

import bpy  # type: ignore

from .blender import Blender


class Wrapper:
    def __init__(self, name: str, app: Blender) -> None:
        self._name = name
        self._app = app

    @abc.abstractmethod
    def create(self, **kwargs: Any) -> 'Wrapper':
        raise NotImplementedError

    @abc.abstractmethod
    def setup(self, **kwargs: Any) -> 'Wrapper':
        raise NotImplementedError

    @abc.abstractmethod
    def remove(self) -> 'Wrapper':
        raise NotImplementedError


class ObjectWrapper(Wrapper):
    @property
    def bpy_object(self) ->  bpy.types.Object:
        return bpy.data.objects[self._name]

    def set_parent(self, parent: bpy.types.Object) -> 'ObjectWrapper':
        self.bpy_object.parent = parent
        return self

    def add_track_to(self, target: bpy.types.Object) -> 'ObjectWrapper':
        constraint = self.bpy_object.constraints.new(type='TRACK_TO')
        constraint.target = target
        return self
