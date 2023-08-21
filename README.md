<div align="center">

# `bpy_wrapper`

![Blender Version](https://img.shields.io/badge/blender-3.6-fb7d01?logo=blender&logoColor=white)
![Python Version](https://img.shields.io/badge/python-3.10-0a7bbc?logo=python&logoColor=white)
![license](https://img.shields.io/badge/license-GPL_v3.0-green?logo=open-source-initiative&logoColor=white)

Blender API wrapper for easy scripting

</div>

## Usage

### Use as package

Some examples are present in the repository, to try it, run :
```shell
python examples/<example_name>.py
```

### Use as addon

To install the addon, run :
```shell
git clone https://github.com/MechanicalFlower/bpy_wrapper.git
cd bpy_wrapper
pip install poetry
poetry install --only=build
poetry run bpy-addon-build
```

And you can now run :
```shell
blender <project_name>.blend --python examples/<example_name>.py
```

## Examples

### Turntable

Use this to create 360 pictures of your model.

Supported extensions: `.3ds`, `.fbx`, `.ply`, `.obj`, `.stl`, `.glb`.

```shell
turntable --model ./t_pose.glb --output render/t_pose/ --test-mode
```
```shell
blender empty.blend --python examples/turntable.py -- --model ./t_pose.glb --output render/t_pose/ --test-mode
```

Output folder will be created if it does not exist.

## References

- [Turntable script](https://github.com/innosoft-pro/blender-turntable) by [innosoft-pro](https://github.com/innosoft-pro)
- [PSX pipeline](https://github.com/DreliasJackCarter/PSXifyBlender2.8) by [DreliasJackCarter](https://github.com/DreliasJackCarter)
- [Blender API wrapper](https://github.com/keunhong/brender) by [keunhong](https://github.com/keunhong)
