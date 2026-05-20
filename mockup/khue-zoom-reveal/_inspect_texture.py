"""Inspect material + texture details inside the GLB."""
import bpy
from pathlib import Path

GLB = Path("/Users/songha/Documents/Projects/Website VMQTG - olddata/.claude/worktrees/determined-pike-f70772/mockup/khue-zoom-reveal/khue-van-cac.glb")
OUT_DIR = GLB.parent

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=str(GLB))

for mat in bpy.data.materials:
    print(f"[mat] {mat.name}  nodes={mat.use_nodes}", flush=True)
    if mat.use_nodes:
        for n in mat.node_tree.nodes:
            print(f"  node: {n.name}  type={n.type}", flush=True)
            if n.type == "TEX_IMAGE" and n.image:
                img = n.image
                print(f"     image: {img.name}  size={img.size[0]}x{img.size[1]}  packed={img.packed_file is not None}", flush=True)
                # Save the image to disk for inspection
                p = OUT_DIR / f"_tex_{img.name}.png"
                img.filepath_raw = str(p)
                img.file_format = "PNG"
                img.save()
                print(f"     saved to {p}", flush=True)

for img in bpy.data.images:
    if img.name != "Render Result":
        print(f"[img] {img.name} {img.size[0]}x{img.size[1]} packed={img.packed_file is not None}", flush=True)
