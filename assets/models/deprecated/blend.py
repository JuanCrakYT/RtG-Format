import bpy
from pathlib import Path
import re

# ============================================================
# CONFIGURATION
# ============================================================

OUTPUT_DIR = Path(
    r"C:\Users\User\Desktop\Created programs\Mine\Reverse Engineering\Roblox\RtG Format\assets\models"
)

# ============================================================
# PREPARE OUTPUT DIRECTORY
# ============================================================

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Get selected objects BEFORE changing selection
objects = list(bpy.context.selected_objects)

if not objects:
    raise Exception("No objects are selected.")

print("=" * 60)
print("RtG OBJ EXPORT")
print("=" * 60)
print(f"Output: {OUTPUT_DIR}")
print(f"Objects: {len(objects)}")
print()

# ============================================================
# EXPORT
# ============================================================

exported = 0
failed = 0

for obj in objects:

    # Ignore objects that aren't meshes
    if obj.type != 'MESH':
        print(f"[SKIP] {obj.name} - not a mesh")
        continue

    # Windows-invalid filename characters
    safe_name = re.sub(r'[<>:"/\\|?*]', '_', obj.name)

    # Prevent empty filenames
    if not safe_name.strip():
        safe_name = "Unnamed"

    filepath = OUTPUT_DIR / f"{safe_name}.obj"

    # Select only this object
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj

    try:
        bpy.ops.wm.obj_export(
            filepath=str(filepath),
            export_selected_objects=True
        )

        print(f"[OK]   {obj.name} -> {filepath.name}")
        exported += 1

    except Exception as error:
        print(f"[FAIL] {obj.name} -> {error}")
        failed += 1

# ============================================================
# FINISHED
# ============================================================

print()
print("=" * 60)
print("EXPORT FINISHED")
print("=" * 60)
print(f"Exported: {exported}")
print(f"Skipped/Failed: {failed}")
print(f"Location: {OUTPUT_DIR}")
print("=" * 60)
