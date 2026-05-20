"""Convert FBX → GLB and report scene stats.

Run headless via:
    /Applications/Blender.app/Contents/MacOS/Blender --background --python _convert.py
"""
import bpy
import sys
import os
import math
from pathlib import Path

SRC = "/Users/songha/Downloads/d9d2bc1afb734a16ad54ddc90dc05ab1.fbx"
OUT_DIR = Path("/Users/songha/Documents/Projects/Website VMQTG - olddata/.claude/worktrees/determined-pike-f70772/mockup/khue-zoom-reveal")
OUT_GLB = OUT_DIR / "khue-van-cac.glb"

def log(msg):
    print(f"[convert] {msg}", flush=True)

# Wipe default scene
bpy.ops.wm.read_factory_settings(use_empty=True)

# Import FBX
log(f"importing {SRC}")
bpy.ops.import_scene.fbx(filepath=SRC)

# Clear all parent hierarchies (keep world transform), so transform_apply bakes correctly
bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
# Delete any non-mesh leftovers (empties used as parents)
for o in list(bpy.data.objects):
    if o.type != "MESH":
        bpy.data.objects.remove(o, do_unlink=True)

# Stats
mesh_objs = [o for o in bpy.data.objects if o.type == "MESH"]
total_verts = sum(len(o.data.vertices) for o in mesh_objs)
total_faces = sum(len(o.data.polygons) for o in mesh_objs)
total_tris  = sum(sum(len(p.vertices) - 2 for p in o.data.polygons) for o in mesh_objs)
materials = list(bpy.data.materials)
images = list(bpy.data.images)

log(f"meshes: {len(mesh_objs)}")
log(f"verts:  {total_verts:,}")
log(f"faces:  {total_faces:,}")
log(f"tris:   {total_tris:,}")
log(f"mats:   {len(materials)}")
log(f"imgs:   {len(images)}  -> {[i.name for i in images]}")

# Compute overall bounding box (world)
import mathutils
min_co = mathutils.Vector(( math.inf,)*3)
max_co = mathutils.Vector((-math.inf,)*3)
for o in mesh_objs:
    for v in o.bound_box:
        world = o.matrix_world @ mathutils.Vector(v)
        for i in range(3):
            if world[i] < min_co[i]: min_co[i] = world[i]
            if world[i] > max_co[i]: max_co[i] = world[i]
size = max_co - min_co
log(f"bbox min: {tuple(round(x,3) for x in min_co)}")
log(f"bbox max: {tuple(round(x,3) for x in max_co)}")
log(f"size:     {tuple(round(x,3) for x in size)}")

# Center and normalize: shift to origin (XY centered, Z bottom = 0), scale to fit 1×1×1 box
if mesh_objs:
    bpy.ops.object.select_all(action="DESELECT")
    for o in mesh_objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = mesh_objs[0]
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

    # Recompute bbox in world coords after apply
    min_co = mathutils.Vector(( math.inf,)*3)
    max_co = mathutils.Vector((-math.inf,)*3)
    for o in mesh_objs:
        for v in o.bound_box:
            world = o.matrix_world @ mathutils.Vector(v)
            for i in range(3):
                if world[i] < min_co[i]: min_co[i] = world[i]
                if world[i] > max_co[i]: max_co[i] = world[i]
    size_now = max_co - min_co
    longest = max(size_now.x, size_now.y, size_now.z)
    s = 1.0 / longest if longest > 0 else 1.0

    # 1) Scale first
    for o in mesh_objs:
        o.scale = (s, s, s)
    bpy.ops.object.select_all(action="DESELECT")
    for o in mesh_objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = mesh_objs[0]
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

    # 2) Recompute bbox in scaled coordinates
    min_co = mathutils.Vector(( math.inf,)*3)
    max_co = mathutils.Vector((-math.inf,)*3)
    for o in mesh_objs:
        for v in o.bound_box:
            world = o.matrix_world @ mathutils.Vector(v)
            for i in range(3):
                if world[i] < min_co[i]: min_co[i] = world[i]
                if world[i] > max_co[i]: max_co[i] = world[i]
    center = (min_co + max_co) / 2
    bottom_z = min_co.z

    # 3) Shift so XY centered, Z bottom = 0
    for o in mesh_objs:
        o.location.x -= center.x
        o.location.y -= center.y
        o.location.z -= bottom_z
    bpy.ops.object.transform_apply(location=True, rotation=False, scale=False)

    # Verify
    min_co = mathutils.Vector(( math.inf,)*3)
    max_co = mathutils.Vector((-math.inf,)*3)
    for o in mesh_objs:
        for v in o.bound_box:
            world = o.matrix_world @ mathutils.Vector(v)
            for i in range(3):
                if world[i] < min_co[i]: min_co[i] = world[i]
                if world[i] > max_co[i]: max_co[i] = world[i]
    log(f"after normalize: bbox min={tuple(round(x,3) for x in min_co)} max={tuple(round(x,3) for x in max_co)}")
    log(f"scale used: {s:.5f}")

# Export GLB with Draco
log(f"exporting GLB → {OUT_GLB}")
bpy.ops.export_scene.gltf(
    filepath=str(OUT_GLB),
    export_format="GLB",
    export_apply=True,
    export_yup=True,
    export_draco_mesh_compression_enable=True,
    export_draco_mesh_compression_level=6,
    export_draco_position_quantization=14,
    export_draco_normal_quantization=10,
    export_draco_texcoord_quantization=12,
    export_animations=True,
    export_lights=False,
    export_cameras=False,
)

# Final size
size_kb = OUT_GLB.stat().st_size / 1024
log(f"GLB size: {size_kb:.1f} KB")
log("done")
