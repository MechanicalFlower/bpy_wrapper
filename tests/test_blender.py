from typing import Dict

import pytest

from bpy_wrapper import Blender


class TestBlender:
    @pytest.mark.parametrize('app_options', [
        {'do_reset': True},
        {'do_reset': False},
    ])
    def test_0001_create_app(self, app_options: Dict[str, bool]) -> None:
        Blender(**app_options)
