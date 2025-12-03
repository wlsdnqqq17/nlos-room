import math
import os
import platform
import random
from pathlib import Path

import bpy

FILE_PATH = Path("/Users/jinwoo/Documents/work/room")
system = platform.system()
print(system)
if system == "Linux":
    os.environ["CUDA_VISIBLE_DEVICES"] = "1"
FILE_PATH = Path(__file__).parent

TOTAL_FRAMES = 320
FRAME_STEP = 20
MOVE_SPEED = 1.0

for obj in bpy.data.objects:
    obj.hide_viewport = False
bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete()


def add_cube(name, loc, scale, hide=False):
    bpy.ops.mesh.primitive_cube_add(size=2, location=loc)
    obj = bpy.context.active_object
    obj.scale = scale
    obj.name = name
    obj.hide_viewport = hide
    return obj


add_cube("floor", (2, 0, 0), (5, 0.1, 5))
add_cube("ceiling", (2, -2, 0), (5, 0.1, 5), hide=True)
add_cube("inner wall", (3.5, -1, 0), (3.5, 1, 0.1))
add_cube("wall1", (2, -1, 5), (5, 1, 0.1))
add_cube("wall2", (2, -1, -5), (5, 1, 0.1))
add_cube("wall3", (7, -1, 0), (0.1, 1, 5))
add_cube("wall4", (-3, -1, 0), (0.1, 1, 5))

bpy.ops.object.camera_add(location=(-1, -1, -2))
bpy.ops.object.camera_add(location=(-1, -1, -1.5))
cam = bpy.context.active_object
cam.rotation_euler = (0, -2.14675, 3.14159)
cam.rotation_euler = (math.radians(0), math.radians(-109), math.radians(180))
bpy.context.scene.camera = cam

bpy.ops.object.light_add(type="POINT", location=(2, -1.9, 2.5))
bpy.context.object.data.energy = 200

bpy.ops.import_scene.fbx(filepath=str(FILE_PATH / "Walking.fbx"))
walker = bpy.context.active_object
walker.name = "walker"

anim = walker.animation_data
if anim and anim.action:
    track = anim.nla_tracks.new()
    strip = track.strips.new("walk_cycles", 1, action=anim.action)
    strip.repeat = 11
    anim.action = None

bpy.ops.object.empty_add(location=(0, 0, 0))
controller = bpy.context.active_object
controller.name = "Walker_Controller"

walker.parent = controller
walker.location = (0, 0, 0)

walker.rotation_euler = (math.radians(0), math.radians(-90), math.radians(180))
current_x = 0.5
current_z = 2.5
current_angle = 0.0

controller.location = (current_x, 0, current_z)
controller.rotation_euler = (0, 0, 0)
controller.keyframe_insert(data_path="location", frame=1)
controller.keyframe_insert(data_path="rotation_euler", frame=1)


frame = 1
while frame < TOTAL_FRAMES:
    valid_move = False
    attempt = 0

    while not valid_move:
        attempt += 1

        turn = random.uniform(math.radians(-45), math.radians(45))

        if attempt > 10:
            dx_center = 3.5 - current_x
            dz_center = 2.5 - current_z
            target_angle = math.atan2(dz_center, dx_center)
            temp_angle = target_angle + random.uniform(-0.2, 0.2)
        else:
            temp_angle = current_angle + turn

        dx = math.cos(temp_angle) * MOVE_SPEED
        dz = math.sin(temp_angle) * MOVE_SPEED

        next_x = current_x + dx
        next_z = current_z + dz

        if 0.5 < next_x < 6.5 and 0.5 < next_z < 4.5:
            valid_move = True
            current_x = next_x
            current_z = next_z
            current_angle = temp_angle
        if attempt > 50:
            valid_move = True

    frame += FRAME_STEP
    if frame > TOTAL_FRAMES:
        break

    controller.location = (current_x, 0, current_z)

    controller.rotation_euler = (0, -current_angle, 0)

    controller.keyframe_insert(data_path="location", frame=frame)
    controller.keyframe_insert(data_path="rotation_euler", frame=frame)

scene = bpy.context.scene

scene.render.engine = "CYCLES"

preferences = bpy.context.preferences
cycles_prefs = preferences.addons["cycles"].preferences

if system == "Linux":
    cycles_prefs.compute_device_type = "CUDA"

    cycles_prefs.get_devices()
    found_gpu = False

    for device in cycles_prefs.devices:
        if device.type == "CUDA" or device.type == "OPTIX":
            device.use = True
            found_gpu = True
            print(f"Using GPU: {device.name}")
        else:
            device.use = False
            print(f"Not using GPU: {device.name}")

scene.cycles.device = "GPU"
scene.cycles.samples = 128
scene.cycles.use_denoising = True

scene.render.resolution_x = 256
scene.render.resolution_y = 256
scene.render.resolution_percentage = 100

scene.render.image_settings.file_format = "FFMPEG"
scene.render.ffmpeg.format = "MPEG4"
scene.render.ffmpeg.codec = "H264"
scene.render.ffmpeg.constant_rate_factor = "MEDIUM"
scene.render.ffmpeg.audio_codec = "NONE"

scene.render.filepath = str(FILE_PATH / "output.mp4")
scene.frame_start = 1
scene.frame_end = TOTAL_FRAMES

print(f"Start Rendering to {FILE_PATH}...")
bpy.ops.render.render(animation=True)
print("Render Finished!")

blend_file_path = FILE_PATH / "saved_scene.blend"
bpy.ops.wm.save_mainfile(filepath=str(blend_file_path))

bpy.ops.object.camera_add(location=(2, -10, 0))
cam = bpy.context.active_object
cam.rotation_euler = (math.radians(90), 0, 0)
bpy.context.scene.camera = cam
cam.data.lens = 23

if "ceiling" in bpy.data.objects:
    bpy.data.objects["ceiling"].hide_render = True

scene.render.filepath = str(FILE_PATH / "output_top.mp4")
print(f"Start Rendering to {FILE_PATH / 'output_top.mp4'}...")
bpy.ops.render.render(animation=True)
print(f"Render Finished to {FILE_PATH / 'output_top.mp4'}!")
