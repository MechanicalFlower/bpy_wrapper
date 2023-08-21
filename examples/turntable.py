import logging
import math
import sys
from argparse import ArgumentParser, Namespace

from bpy_wrapper import (Blender, Camera, Collection, Empty, PipelineFactory,
                         Scene)


def parse_args() -> Namespace:
    if '--' in sys.argv:
        sys.argv = sys.argv[sys.argv.index('--'):]

    parser = ArgumentParser()
    parser.add_argument("-d", "--debug", action="store_true", dest="debug")
    parser.add_argument("-m", "--model", action="store", dest="input_file")
    parser.add_argument("-o", "--output", action="store", dest="output_dir")
    parser.add_argument("--psx", action="store_true", dest="is_psx")
    parser.add_argument("--test-mode", action="store_true", dest="test_mode_enabled", default=False)
    return parser.parse_args()


def start() -> None:
    args = parse_args()

    logging.basicConfig(format='[%(levelname)s] %(message)s', level=logging.DEBUG if args.debug else logging.WARNING)

    def run() -> None:
        app = Blender(do_reset=True)

        scene = (
            # TODO : render not work if scene is not named Scene
            Scene('Scene', app)
                .create()
                .with_model(args.input_file)
        )

        collection = (
            Collection('TurntableCollection', app)
                .create(collection_to_link_to=scene.bpy_root_collection)
        )

        if args.is_psx:
            scene = PipelineFactory.psxify(app, scene, collection)

        else:
            empty = (
                Empty('TurntableAxe', app)
                    .create(collection_to_link_to=collection.bpy_collection)
            )

            camera = (
                Camera('TurntableCamera', app)
                    .create(
                        location=(-5 * 1.2, 0, 1),
                        collection_to_link_to=collection.bpy_collection
                    )
                    .add_track_to(empty.bpy_object)
            )

            camera.set_parent(empty.bpy_object)
            scene.set_active_camera(camera.bpy_object)

            empty.bpy_object.rotation_mode = 'XYZ'

            scene.bpy_scene.frame_start = 1
            scene.bpy_scene.frame_end = 120

            empty.bpy_object.rotation_euler = (0, 0, 0)
            empty.bpy_object.keyframe_insert('rotation_euler', index=2 ,frame=1)

            empty.bpy_object.rotation_euler = (0, 0, math.radians(180))
            empty.bpy_object.keyframe_insert('rotation_euler', index=2 ,frame=60)

            empty.bpy_object.rotation_euler = (0, 0, math.radians(360))
            empty.bpy_object.keyframe_insert('rotation_euler', index=2 ,frame=120)

        scene.render(
            args.output_dir,
            use_animation=(not args.test_mode_enabled)
        )

    run()


if __name__ == "__main__":
    start()
