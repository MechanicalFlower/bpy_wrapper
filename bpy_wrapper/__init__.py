from .blender import Blender
from .pipeline import PipelineFactory
from .struct import Camera, Collection, Empty, Scene

__all__ = [
    'Blender', 'Scene', 'Camera', 'Collection',
    'Empty', 'PipelineFactory',
]

__author__ = "Florian Vazelle"
__email__ = "florian.vazelle@vivaldi.net"
__version__ = "0.1.0"

# To use this package as addon, we define some required variables and methods

bl_info = {
    "name": "bpy_wrapper",
    "blender": (3, 6, 0),
    "category": "Object",
}

def register() -> None:
    print("Hello World")

def unregister() -> None:
    print("Goodbye World")

__addon_enabled__ = True
