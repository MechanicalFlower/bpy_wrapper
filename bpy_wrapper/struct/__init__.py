"""
`struct` is a collection of wrapper class.
"""

from .camera import Camera
from .collection import Collection
from .empty import Empty
from .scene import Scene

__all__ = [
    'Scene', 'Camera', 'Collection', 'Empty',
]
