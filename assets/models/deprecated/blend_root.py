import bpy

root = bpy.data.objects.get("Switch")
mesh = bpy.data.objects.get("Switch")

# Como Blender no puede distinguirlos por nombre usando get(),
# buscamos el root y el MESH por tipo.
roots = [
    obj for obj in bpy.context.scene.objects
    if obj.name == "Switch" and obj.parent is None
]

meshes = [
    obj for obj in bpy.context.scene.objects
    if obj.name == "Switch" and obj.type == "MESH"
]

if roots and meshes:
    root = roots[0]
    mesh = meshes[0]

    if mesh != root:
        mesh.parent = root
        print("✓ Switch MESH parentado al root Switch.")
    else:
        print("✓ El Switch ya es el MESH root.")

else:
    print("✗ No se pudo encontrar la estructura de Switch.")