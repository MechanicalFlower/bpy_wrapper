import logging
from time import sleep

import bpy  # type: ignore
import mathutils  # type: ignore

from ..blender import Blender
from ..struct import Camera, Collection, Scene
from .pipeline import Pipeline

logger = logging.getLogger(__file__)


class PSXPipeline(Pipeline):
    def __init__(self, app: Blender, scene: Scene, collection: Collection) -> None:
        super().__init__(app, scene)

        self._collection = collection
        self._psx_collection = (
            Collection('PSXCollection', self._app)
                .create(collection_to_link_to=self._scene.bpy_root_collection)
        )

        # PSX grid width resolution
        self.psx_render_width = 160
        # PSX grid height resolution
        self.psx_render_height = 120

        # Delay in seconds between each frame rendering, seems to prevent some glitches
        self.delay_between_frames = 0.1
        # Delay between objects calculation in the same frame
        self.delay_between_objects = 0.1

        # Relative distance from PSX camera
        self.depth = 0.2
        # PSX camera FOV, set it manually to fit the original camera
        self.psx_camera_scale = 1.33

    def _create_whole_fake_scene(self) -> Scene:
        """Get concerned collection and duplicate every objects inside into a dedicated new collection."""
        logger.debug("Start creating whole fake scene")

        try:
            # Deselect everything
            bpy.context.active_object.select_set(False)
            logger.debug("Deselecting active objects")
        except Exception:
            # TODO more granular exception and move logger to debug
            logger.exception("Nothing was selected")

        for object_to_psxify in self._collection.bpy_collection.all_objects:
            logger.debug("Checking if %s could be PSXified", object_to_psxify.name)

            if object_to_psxify.type == 'MESH':
                logger.debug("%s is a mesh", object_to_psxify.name)

                psxified_object = object_to_psxify.copy()
                psxified_object.data = object_to_psxify.data.copy()
                psxified_object.name = object_to_psxify.name + '.PSXified'
                psxified_object.animation_data_clear()
                psxified_object.rotation_euler = (0.0, 0.0, 0.0)
                psxified_object.location = (0.0, 0.0, 0.0)
                psxified_object.scale = (1.0, 1.0, 1.0)
                psxified_object.parent = None
                psxified_object.constraints.clear()
                psxified_object.vertex_groups.clear()

                self._psx_collection.bpy_collection.objects.link(psxified_object)

            else:
                logger.debug("%s is not a mesh", object_to_psxify.name)

        # Create PSX camera
        self._psx_camera = (
            Camera('PSXCamera', self._app)
                .create(
                    data={'type': 'ORTHO', 'ortho_scale': self.psx_camera_scale},
                    collection_to_link_to=self._psx_collection.bpy_collection
                )
        )

        # Set active camera
        self._scene.set_active_camera(self._psx_camera.bpy_object)

        # Hide original collection
        self._collection.set_visibility(False)

        logger.debug("Finish creating whole fake scene")

        return self._scene

    def _psxify_collection(self, camera: Camera, collection: Collection, scene: Scene) -> None:
        for obj in collection.bpy_collection.all_objects:
            if obj.type == 'MESH' and not obj.name.endswith('.PSXified'):
                target_object = scene.bpy_scene.objects[f'{obj.name}.PSXified']

                dg: bpy.types.Depsgraph = bpy.context.evaluated_depsgraph_get()
                mesh: bpy.types.Mesh = obj.evaluated_get(dg).to_mesh()

                logger.debug("Snapping %s from %s coordinates...", target_object.name, obj.name)
                for vertex, target_vertex in zip(mesh.vertices, target_object.data.vertices):
                    abs_pos = obj.matrix_world @ vertex.co
                    target_vertex.co = self._psxify_coords(camera, abs_pos, scene)

                logger.debug("%s snapped", target_object.name)
                sleep(self.delay_between_objects)

    def _psxify_coords(self, camera: Camera, coord: mathutils.Vector, scene: Scene) -> mathutils.Vector:
        """
        Inspired from world_to_camera_view() function and Komojo script.
        Steps:
        - Get coordinates of given vertice as seen from camera
        - Calculates its X,Y as % position in camera,
        - Rounding the coords to snap it on a low res grid
        - Scaling and arranging the final output
        """
        # Get vertice coord from camera POV
        co_local = camera.bpy_object.matrix_world.normalized().inverted() @ coord

        # Z remains the same (distance of vertice from camera center)
        z = co_local.z

        frame = [v for v in camera.bpy_object.data.view_frame(scene=scene.bpy_scene)[:3]]

        # Calculate to frame corners location
        if camera.bpy_object.data.type != 'ORTHO':
            if z == 0.0:
                return mathutils.Vector((0.5, 0.5, 0.0))
            else:
                frame = [-(v / (v.z / z)) for v in frame]

        # Get the four camera corner coords
        min_x, max_x = frame[2].x, frame[1].x
        min_y, max_y = frame[1].y, frame[0].y

        # Calculate X,Y of vertice as percentage position on screen
        x = (co_local.x - min_x) / (max_x - min_x) - 0.5 # -0.5 to center it
        y = (co_local.y - min_y) / (max_y - min_y) - 0.5 # -0.5 to center it

        # Snapping vertex to desired PSX resolution by rounding coords
        x = -(int)(x * self.psx_render_width) / self.psx_render_width
        y = -(int)(y * self.psx_render_height) / self.psx_render_height

        # Stretch X coord to adapt it to the camera frame
        x *= (self.psx_render_width / self.psx_render_height)

        # Fixes the "behind the camera"glitch:
        # When o get behind camera, the PSX mesh teleports at opposite side of axis, causing
        # visual glitch.
        # Solution: when they get behind the camera (= positive side), they stay at the same axis side
        if z > 0.0:
            x = -x
            y = -y

        # Depth scaling from camera
        z *= self.depth

        return mathutils.Vector((x, y, z))

    def update_handler(self, scene: bpy.types.Scene, depsgraph: bpy.types.Depsgraph) -> None:
        """Called every time the frame changes."""
        sleep(self.delay_between_frames)
        self._psxify_collection(self._psx_camera, self._psx_collection, self._scene)

    def execute(self) -> Scene:
        # Set a callback to update the transform when the frame changes
        bpy.app.handlers.frame_change_post.clear()  # Warning: This might also delete other callbacks
        bpy.app.handlers.frame_change_post.append(self.update_handler)

        self._create_whole_fake_scene()
        self._psxify_collection(self._psx_camera, self._psx_collection, self._scene)

        return self._scene
