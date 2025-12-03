import os

import bpy

bpy.context.scene.render.image_settings.file_format = "PNG"
bpy.context.scene.render.image_settings.file_format = "PNG"

blend_dir = os.path.dirname(bpy.data.filepath)
texture_base_dir = os.path.join(blend_dir, "wood_floor_2k.blend", "textures")

for image in bpy.data.images:
    if image.filepath:
        filename = os.path.basename(image.filepath)
        possible_path = os.path.join(texture_base_dir, filename)
        if os.path.exists(possible_path):
            image.filepath = possible_path
            image.reload()
            print(f"Reloaded texture: {filename}")

bpy.context.scene.frame_start = 1
bpy.context.scene.frame_end = 100

bpy.ops.render.render(animation=True)
