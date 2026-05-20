"""Render previews with a proper vermillion + aged wood material."""
import bpy
import math
import mathutils
from pathlib import Path

OUT_DIR = Path("/Users/songha/Documents/Projects/Website VMQTG - olddata/.claude/worktrees/determined-pike-f70772/mockup/khue-zoom-reveal")
GLB = OUT_DIR / "khue-van-cac.glb"

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=str(GLB))

mesh_objs = [o for o in bpy.data.objects if o.type == "MESH"]
for o in mesh_objs:
    print(f"[render] {o.name}", flush=True)

# Apply a warm vermillion-wood material (sRGB 0.78, 0.34, 0.20 ≈ #c75832, slightly darker than gate)
for mat in bpy.data.materials:
    if not mat.use_nodes:
        mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (0.62, 0.22, 0.12, 1)   # vermillion ~ c75832
        bsdf.inputs["Roughness"].default_value = 0.68
        if "Specular IOR Level" in bsdf.inputs:
            bsdf.inputs["Specular IOR Level"].default_value = 0.35
        elif "Specular" in bsdf.inputs:
            bsdf.inputs["Specular"].default_value = 0.35

# Lighting setup — 3-point, warm key
size = mathutils.Vector((0.6, 0.6, 1.0))
center = mathutils.Vector((0, 0, 0.5))

def add_light(name, kind, energy, loc, rot=(0,0,0), color=(1,1,1), area_size=1.5):
    bpy.ops.object.light_add(type=kind, location=loc)
    L = bpy.context.object
    L.name = name
    L.data.energy = energy
    L.data.color = color
    L.rotation_euler = rot
    if kind == "AREA":
        L.data.size = area_size

# Warm key from upper-right-front
add_light("Key",  "AREA", 500, ( 2.4,  -2.0, 2.6),
          (math.radians(45), 0, math.radians(35)),
          color=(1, 0.88, 0.78), area_size=2)
# Soft cool fill from left
add_light("Fill", "AREA", 180, (-2.4,  -1.0, 1.6),
          (math.radians(55), 0, math.radians(-35)),
          color=(0.78, 0.85, 1), area_size=2.5)
# Warm rim from back
add_light("Rim",  "AREA", 350, ( 0.5,   2.3, 2.0),
          (math.radians(60), math.radians(180), 0),
          color=(1, 0.7, 0.5), area_size=2)
# Ground bounce (warm)
add_light("Bounce", "AREA", 60, (0, 0, -0.5),
          (math.radians(180), 0, 0),
          color=(0.9, 0.7, 0.5), area_size=4)

# Warm dark world
world = bpy.data.worlds.get("World") or bpy.data.worlds.new("World")
bpy.context.scene.world = world
world.use_nodes = True
bg = world.node_tree.nodes["Background"]
bg.inputs[0].default_value = (0.08, 0.06, 0.045, 1)
bg.inputs[1].default_value = 0.3

cam_data = bpy.data.cameras.new("Camera")
cam = bpy.data.objects.new("Camera", cam_data)
bpy.context.collection.objects.link(cam)
bpy.context.scene.camera = cam
cam_data.lens = 50

scene = bpy.context.scene
scene.render.engine = "BLENDER_EEVEE"
scene.render.resolution_x = 1280
scene.render.resolution_y = 800
scene.render.film_transparent = False
scene.view_settings.view_transform = "Standard"
scene.view_settings.look = "Medium High Contrast"
try: scene.eevee.taa_render_samples = 64
except Exception: pass
try: scene.eevee.use_ssr = True
except Exception: pass

def look_at(obj, point):
    direction = point - obj.location
    rot_quat = direction.to_track_quat('-Z', 'Y')
    obj.rotation_euler = rot_quat.to_euler()

shots = [
    ("preview-front.png",   mathutils.Vector(( 0.0, -2.0, 0.7))),
    ("preview-3q.png",      mathutils.Vector(( 1.6, -1.6, 0.85))),
    ("preview-profile.png", mathutils.Vector(( 2.2,  0.0, 0.65))),
    ("preview-low.png",     mathutils.Vector(( 1.0, -1.8, 0.25))),
]
for name, loc in shots:
    cam.location = loc
    look_at(cam, center)
    scene.render.filepath = str(OUT_DIR / name)
    bpy.ops.render.render(write_still=True)
    print(f"[render] wrote {name}", flush=True)

print("[render] done", flush=True)
