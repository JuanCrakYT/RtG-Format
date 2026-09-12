"""
RtG-Format - Blender Model Exporter
===================================

Exportador automático de modelos de Road To Gramby's desde Blender.

ESTRUCTURA ESPERADA
-------------------

Modelo simple:

    Switch
    ├── Switch
    └── Point_2

Modelo con ramas:

    Switch
    ├── Switch
    ├── Input
    │   └── Point_1
    ├── Output
    │   └── Point_2
    └── Point_3

CONVENCIONES
------------

- El objeto raíz representa el nombre del modelo.
- El MESH cuyo nombre coincide con el modelo raíz es el modelo completo.
- Los demás MESH descendientes son ramas.
- Los EMPTY llamados Point_X representan LocalPoints.
- Un Point_X puede estar:
    - directamente bajo el modelo,
    - bajo una rama,
    - o bajo otro objeto intermedio.
- Los Empty NO se exportan a OBJ.
- Las ramas se exportan automáticamente dentro de "split/".
- El modelo completo se exporta como "<ModelName>.obj".
- El JSON se crea como "<ModelName>.json".

CENTRADO
--------

El modelo se centra según el bounding box real de toda su geometría.

IMPORTANTE:

Este script NO mueve los objetos originales de Blender.

El centrado solamente se aplica a la geometría temporal que se usa
para exportar los OBJ.

De esta forma puedes ejecutar el script muchas veces sin acumular
offsets en la escena original.

PUNTOS
------

Los puntos conservan su posición relativa al modelo.

Después de calcular el centro:

    PointFinal = PointWorld - ModelCenter

La rotación se obtiene de la orientación mundial del Empty.

RAMAS
-----

Cada MESH descendiente distinto del modelo principal se considera
una rama.

La rama se asocia con el Point_X más cercano.

Si no existe un punto razonablemente cercano:

    "NaN"

Ejemplo:

    "Branches": {
        "NaN": "./split/Input.obj",
        "2": "./split/Output.obj"
    }

IMPORTANTE
----------

Este script está pensado para ser ejecutado desde Blender.

No depende de una colección llamada "Geometry".

La relación entre modelo, ramas y puntos se basa en la jerarquía
de objetos de Blender.
"""

import bpy
import json
from pathlib import Path
from mathutils import Vector, Matrix


# ============================================================
# CONFIGURACIÓN
# ============================================================

# ------------------------------------------------------------
# Ruta de salida.
#
# Esta es la carpeta:
#
# RtG-Format/assets/models/
#
# ------------------------------------------------------------

OUTPUT_ROOT = Path(
    r"C:\Users\User\Desktop\Created programs\Mine\Reverse Engineering\Roblox\RtG Format\assets\models"
)


# ------------------------------------------------------------
# Distancia máxima para asociar una rama con un Point_X.
#
# 250 se dejó porque es el valor que actualmente tienes en
# el repositorio, pero ahora solamente funciona como seguridad.
#
# Puedes reducirlo posteriormente cuando conozcamos mejor la
# escala definitiva de los modelos.
# ------------------------------------------------------------

BRANCH_POINT_MAX_DISTANCE = 250.0


# ------------------------------------------------------------
# Nombre que deben tener los puntos.
#
# Ejemplos:
#
# Point_1
# Point_2
# Point_3
# ------------------------------------------------------------

POINT_PREFIX = "Point_"


# ============================================================
# UTILIDADES
# ============================================================

def is_point(obj):
    """
    Comprueba si un objeto es un Empty llamado Point_X.

    Solamente se aceptan IDs numéricos.

    Point_2  -> True
    Point_10 -> True
    Point_A -> False
    """

    if obj.type != "EMPTY":
        return False

    if not obj.name.startswith(POINT_PREFIX):
        return False

    point_id = obj.name[len(POINT_PREFIX):]

    return point_id.isdigit()


def get_point_id(obj):
    """
    Obtiene el ID del Point_X.

    Point_2 -> "2"
    Point_10 -> "10"
    """

    return obj.name[len(POINT_PREFIX):]


def is_descendant(obj, root):
    """
    Comprueba si obj pertenece a la jerarquía de root.

    Esto permite encontrar puntos y MESH aunque tengan objetos
    intermedios entre ellos.
    """

    current = obj.parent

    while current is not None:

        if current == root:
            return True

        current = current.parent

    return False


def get_world_position(obj):
    """
    Devuelve la posición mundial del objeto.
    """

    return obj.matrix_world.translation.copy()


def get_world_rotation(obj):
    """
    Devuelve la rotación mundial como Euler.
    """

    return obj.matrix_world.to_euler().copy()


# ============================================================
# DESCUBRIR ELEMENTOS DEL MODELO
# ============================================================

def find_points(model_root):
    """
    Encuentra todos los Point_X que pertenecen al modelo.

    Los puntos pueden estar directamente debajo del modelo
    o debajo de cualquier objeto descendiente.
    """

    points = []

    for obj in bpy.data.objects:

        if not is_point(obj):
            continue

        if is_descendant(obj, model_root):
            points.append(obj)

    # Orden numérico:
    #
    # Point_1
    # Point_2
    # Point_10
    #
    # y no:
    #
    # Point_1
    # Point_10
    # Point_2

    points.sort(
        key=lambda obj: int(get_point_id(obj))
    )

    return points


def find_meshes(model_root):
    """
    Encuentra todos los MESH descendientes del modelo.
    """

    meshes = []

    for obj in bpy.data.objects:

        if obj.type != "MESH":
            continue

        if is_descendant(obj, model_root):
            meshes.append(obj)

    return meshes


def find_main_mesh(model_root, meshes):
    """
    Encuentra el MESH principal.

    El modelo completo debe llamarse igual que el objeto raíz.

    Ejemplo:

        Switch
        └── Switch

    Si no existe un MESH con ese nombre, se genera un error.
    """

    for mesh in meshes:

        if mesh.name == model_root.name:
            return mesh

    return None


# ============================================================
# CENTRADO GEOMÉTRICO
# ============================================================

def get_world_vertices(obj):
    """
    Obtiene los vértices del objeto en coordenadas mundiales.

    Se utiliza la matriz mundial completa para respetar:

    - Location
    - Rotation
    - Scale
    - Parenting
    """

    matrix = obj.matrix_world

    for vertex in obj.data.vertices:

        yield matrix @ vertex.co


def calculate_model_center(meshes):
    """
    Calcula el centro del bounding box de toda la geometría.

    El centro se obtiene a partir de los vértices reales.

    Esto es diferente de utilizar object.location.
    """

    vertices = []

    for obj in meshes:

        vertices.extend(
            get_world_vertices(obj)
        )

    if not vertices:

        return Vector((0.0, 0.0, 0.0))

    min_x = min(v.x for v in vertices)
    max_x = max(v.x for v in vertices)

    min_y = min(v.y for v in vertices)
    max_y = max(v.y for v in vertices)

    min_z = min(v.z for v in vertices)
    max_z = max(v.z for v in vertices)

    return Vector((
        (min_x + max_x) / 2.0,
        (min_y + max_y) / 2.0,
        (min_z + max_z) / 2.0
    ))


# ============================================================
# PUNTOS LOCALES
# ============================================================

def build_local_points(points, model_center):
    """
    Convierte los Point_X de Blender a LocalPoints.

    La posición queda relativa al centro geométrico del modelo.

    Ejemplo:

        Point_2 World:
            (105, 20, -8)

        Model Center:
            (100, 20, -10)

        Resultado:
            (5, 0, 2)
    """

    local_points = {}

    for point in points:

        world_location = get_world_position(point)

        local_location = (
            world_location - model_center
        )

        rotation = get_world_rotation(point)

        local_points[
            get_point_id(point)
        ] = [
            [
                clean_number(local_location.x),
                clean_number(local_location.y),
                clean_number(local_location.z)
            ],
            [
                clean_number(rotation.x),
                clean_number(rotation.y),
                clean_number(rotation.z)
            ]
        ]

    return local_points


def clean_number(value):
    """
    Convierte valores numéricos de Blender a valores JSON limpios.

    Evita guardar cosas como:

        1.0000000000000002

    cuando realmente representan:

        1
    """

    value = float(value)

    if abs(value) < 1e-10:
        return 0

    rounded = round(value, 10)

    if rounded == int(rounded):
        return int(rounded)

    return rounded


# ============================================================
# RAMAS
# ============================================================

def find_nearest_point(branch, points):
    """
    Encuentra el Point_X más cercano a una rama.

    La posición utilizada es el origen del objeto MESH.

    Devuelve:

        point_id, distance

    o:

        "NaN", distance

    si no hay un punto dentro del límite configurado.
    """

    if not points:

        return "NaN", None

    branch_position = get_world_position(branch)

    nearest_point = None
    nearest_distance = float("inf")

    for point in points:

        point_position = get_world_position(point)

        distance = (
            branch_position - point_position
        ).length

        if distance < nearest_distance:

            nearest_distance = distance
            nearest_point = point

    if nearest_point is None:

        return "NaN", None

    if nearest_distance > BRANCH_POINT_MAX_DISTANCE:

        return "NaN", nearest_distance

    return (
        get_point_id(nearest_point),
        nearest_distance
    )


def build_branches(branches, points):
    """
    Construye el objeto Branches.

    Cada rama se asocia al Point_X más cercano.
    """

    result = {}

    for branch in branches:

        point_id, distance = find_nearest_point(
            branch,
            points
        )

        filename = f"{branch.name}.obj"

        result[point_id] = (
            f"./split/{filename}"
        )

        if distance is None:

            print(
                f"[RtG] Rama '{branch.name}' -> {point_id}"
            )

        else:

            print(
                f"[RtG] Rama '{branch.name}' -> "
                f"{point_id} "
                f"(distancia: {distance:.4f})"
            )

    return result


# ============================================================
# EXPORTACIÓN TEMPORAL
# ============================================================

def create_export_object(source_obj, model_center):
    """
    Crea un objeto temporal preparado para exportación.

    El objeto original NO se modifica.

    Toda la geometría se convierte a coordenadas mundiales
    y después se le resta el centro del modelo.

    Resultado:

        centro del modelo = 0,0,0
    """

    # --------------------------------------------------------
    # Copiar la malla.
    # --------------------------------------------------------

    mesh = source_obj.data.copy()

    export_obj = bpy.data.objects.new(
        f"__RtGExport_{source_obj.name}",
        mesh
    )

    # --------------------------------------------------------
    # Colocarlo temporalmente en la escena.
    # --------------------------------------------------------

    bpy.context.collection.objects.link(
        export_obj
    )

    # --------------------------------------------------------
    # Convertir cada vértice a coordenadas mundiales y después
    # aplicar el desplazamiento del centro.
    # --------------------------------------------------------

    world_matrix = source_obj.matrix_world

    for vertex in mesh.vertices:

        world_position = (
            world_matrix @ vertex.co
        )

        centered_position = (
            world_position - model_center
        )

        vertex.co = centered_position

    # --------------------------------------------------------
    # Resetear la transformación del objeto exportado.
    #
    # La geometría ya contiene la transformación completa.
    # --------------------------------------------------------

    export_obj.location = (
        0.0,
        0.0,
        0.0
    )

    export_obj.rotation_euler = (
        0.0,
        0.0,
        0.0
    )

    export_obj.scale = (
        1.0,
        1.0,
        1.0
    )

    return export_obj


def export_mesh_object(source_obj, output_path, model_center):
    """
    Exporta un único MESH sin modificar el original.

    Se crea una copia temporal, se centra y posteriormente
    se elimina.
    """

    export_obj = create_export_object(
        source_obj,
        model_center
    )

    # --------------------------------------------------------
    # Guardar selección actual.
    # --------------------------------------------------------

    old_selection = list(
        bpy.context.selected_objects
    )

    old_active = (
        bpy.context.view_layer.objects.active
    )

    # --------------------------------------------------------
    # Limpiar selección.
    # --------------------------------------------------------

    bpy.ops.object.select_all(
        action="DESELECT"
    )

    export_obj.select_set(True)

    bpy.context.view_layer.objects.active = (
        export_obj
    )

    # --------------------------------------------------------
    # Crear carpeta.
    # --------------------------------------------------------

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    # --------------------------------------------------------
    # Exportar OBJ.
    # --------------------------------------------------------

    bpy.ops.wm.obj_export(
        filepath=str(output_path),
        export_selected_objects=True,
        apply_modifiers=True,
        export_materials=True,
        export_uv=True
    )

    # --------------------------------------------------------
    # Eliminar objeto temporal.
    # --------------------------------------------------------

    bpy.data.objects.remove(
        export_obj,
        do_unlink=True
    )

    bpy.data.meshes.remove(
        export_obj.data,
        do_unlink=True
    )

    # --------------------------------------------------------
    # Restaurar selección.
    # --------------------------------------------------------

    bpy.ops.object.select_all(
        action="DESELECT"
    )

    for obj in old_selection:

        if obj.name in bpy.data.objects:

            obj.select_set(True)

    if old_active is not None:

        if old_active.name in bpy.data.objects:

            bpy.context.view_layer.objects.active = (
                old_active
            )


# ============================================================
# JSON
# ============================================================

def build_json(model_name, local_points, branches):
    """
    Construye el JSON de RtG-Format.

    Mantiene la estructura actual del repositorio.
    """

    return [
        {
            "RtG-Format": {

                "RtG-Format Data": {
                    "Release Date": "",
                    "Creator": "JuanCrakYT",
                    "Notes": "",
                    "Extra Files": []
                },

                "RtG-Preview": {

                    "Size": {
                        "default": 1
                    },

                    "Default Branch":
                        f"./{model_name}.obj"
                },

                "Page": {}
            },

            "Name": model_name,

            "Description": "",

            "LocalPoints": local_points,

            "Branches": branches
        }
    ]


def save_json(model_directory, model_name, data):
    """
    Guarda <ModelName>.json.
    """

    json_path = (
        model_directory /
        f"{model_name}.json"
    )

    with open(
        json_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )

    print(
        f"[RtG] JSON: {json_path}"
    )


# ============================================================
# PROCESAR MODELO
# ============================================================

def process_model(model_root):
    """
    Procesa un modelo completo.
    """

    model_name = model_root.name

    print("")
    print("=" * 70)
    print(
        f"[RtG] Procesando: {model_name}"
    )
    print("=" * 70)

    # --------------------------------------------------------
    # Buscar geometría.
    # --------------------------------------------------------

    meshes = find_meshes(
        model_root
    )

    if not meshes:

        print(
            "[RtG] ERROR: "
            "No se encontró geometría MESH."
        )

        return False

    # --------------------------------------------------------
    # Encontrar modelo principal.
    # --------------------------------------------------------

    main_mesh = find_main_mesh(
        model_root,
        meshes
    )

    if main_mesh is None:

        print(
            f"[RtG] ERROR: "
            f"No existe un MESH llamado "
            f"'{model_name}'."
        )

        return False

    # --------------------------------------------------------
    # Encontrar puntos.
    # --------------------------------------------------------

    points = find_points(
        model_root
    )

    print(
        f"[RtG] MESH encontrados: {len(meshes)}"
    )

    print(
        f"[RtG] Points encontrados: {len(points)}"
    )

    # --------------------------------------------------------
    # Calcular centro.
    # --------------------------------------------------------

    model_center = calculate_model_center(
        meshes
    )

    print(
        f"[RtG] Centro geométrico: "
        f"{tuple(round(v, 6) for v in model_center)}"
    )

    # --------------------------------------------------------
    # Preparar carpeta del modelo.
    # --------------------------------------------------------

    model_directory = (
        OUTPUT_ROOT /
        model_name
    )

    split_directory = (
        model_directory /
        "split"
    )

    model_directory.mkdir(
        parents=True,
        exist_ok=True
    )

    # --------------------------------------------------------
    # Crear "split/" automáticamente.
    #
    # Incluso si actualmente no hay ramas, la carpeta queda
    # preparada para futuros modelos.
    # --------------------------------------------------------

    split_directory.mkdir(
        parents=True,
        exist_ok=True
    )

    # --------------------------------------------------------
    # Exportar modelo completo.
    # --------------------------------------------------------

    main_output = (
        model_directory /
        f"{model_name}.obj"
    )

    export_mesh_object(
        main_mesh,
        main_output,
        model_center
    )

    print(
        f"[RtG] Principal: {main_output}"
    )

    # --------------------------------------------------------
    # Encontrar ramas.
    #
    # Todo MESH excepto el MESH principal es una rama.
    # --------------------------------------------------------

    branches = [
        mesh
        for mesh in meshes
        if mesh != main_mesh
    ]

    # --------------------------------------------------------
    # Construir Branches.
    # --------------------------------------------------------

    branches_json = build_branches(
        branches,
        points
    )

    # --------------------------------------------------------
    # Exportar cada rama.
    # --------------------------------------------------------

    for branch in branches:

        branch_output = (
            split_directory /
            f"{branch.name}.obj"
        )

        export_mesh_object(
            branch,
            branch_output,
            model_center
        )

    # --------------------------------------------------------
    # Construir LocalPoints DESPUÉS de calcular el centro.
    # --------------------------------------------------------

    local_points = build_local_points(
        points,
        model_center
    )

    # --------------------------------------------------------
    # Construir JSON.
    # --------------------------------------------------------

    json_data = build_json(
        model_name,
        local_points,
        branches_json
    )

    # --------------------------------------------------------
    # Guardar JSON.
    # --------------------------------------------------------

    save_json(
        model_directory,
        model_name,
        json_data
    )

    print(
        f"[RtG] Terminado: {model_name}"
    )

    return True


# ============================================================
# DETECCIÓN DE MODELOS
# ============================================================

def find_models():
    """
    Encuentra los objetos raíz de la escena que representan
    modelos RtG.

    Un modelo es un objeto sin parent que contiene al menos
    un MESH descendiente.

    Esto permite colocar varios modelos en una misma escena.
    """

    models = []

    for obj in bpy.context.scene.objects:

        if obj.parent is not None:
            continue

        if obj.type == "MESH":

            # Un objeto MESH raíz también puede ser un modelo.
            models.append(obj)

            continue

        descendants = [
            child
            for child in bpy.context.scene.objects
            if is_descendant(child, obj)
        ]

        has_mesh = any(
            child.type == "MESH"
            for child in descendants
        )

        if has_mesh:

            models.append(obj)

    return models


# ============================================================
# MAIN
# ============================================================

def main():
    """
    Punto de entrada.
    """

    print("")
    print("=" * 70)
    print("RtG-Format Blender Exporter")
    print("=" * 70)

    # --------------------------------------------------------
    # Comprobar salida.
    # --------------------------------------------------------

    OUTPUT_ROOT.mkdir(
        parents=True,
        exist_ok=True
    )

    # --------------------------------------------------------
    # Buscar modelos.
    # --------------------------------------------------------

    models = find_models()

    if not models:

        print(
            "[RtG] ERROR: "
            "No se encontraron modelos."
        )

        return

    print(
        f"[RtG] Modelos encontrados: {len(models)}"
    )

    # --------------------------------------------------------
    # Procesar cada modelo.
    # --------------------------------------------------------

    successful = 0

    for model in models:

        try:

            if process_model(model):

                successful += 1

        except Exception as error:

            print(
                f"[RtG] ERROR procesando "
                f"'{model.name}': {error}"
            )

    # --------------------------------------------------------
    # Resumen.
    # --------------------------------------------------------

    print("")
    print("=" * 70)
    print(
        f"[RtG] Finalizado: "
        f"{successful}/{len(models)} modelos"
    )
    print("=" * 70)


# ============================================================
# EJECUCIÓN
# ============================================================

if __name__ == "__main__":
    main()
