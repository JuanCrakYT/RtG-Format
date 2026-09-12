"""
RtG-Format - Blender Model Exporter
===================================

Este script automatiza la preparación de modelos de Road To Gramby's
desde Blender.

Estructura esperada de un modelo:

    Switch
    ├── Geometry
    │   ├── Switch
    │   ├── Input
    │   └── Output
    │
    └── Points
        └── Point_2

Convenciones:

- El objeto raíz tiene el nombre del modelo.
- Los objetos de geometría están dentro de la colección/estructura del modelo.
- Los Empty de puntos se llaman:
      Point_1
      Point_2
      Point_3
      ...
- Las ramas son objetos de geometría distintos del modelo principal.
- La rama se asocia automáticamente al Point_X más cercano a su origen.
- Si una rama no tiene un Point_X cercano, se guarda como "NaN".

El script:

1. Encuentra los modelos.
2. Calcula el centro real de la geometría.
3. Reubica el origen del modelo en ese centro.
4. Mantiene los puntos en su posición relativa.
5. Deja la geometría con posición 0,0,0.
6. Lee los puntos y sus rotaciones.
7. Exporta los OBJ.
8. Genera/actualiza el JSON del modelo.

IMPORTANTE:
- Los Empty NO se exportan a OBJ.
- Este script modifica la escena actual de Blender.
- Haz una copia del .blend antes de ejecutarlo si quieres conservar
  las posiciones originales.
"""

import bpy
import json
import math
from pathlib import Path
from mathutils import Vector, Matrix


# ============================================================
# CONFIGURACIÓN
# ============================================================

# Carpeta donde se guardarán los modelos exportados.
#
# Ejemplo:
# RtG-Format/assets/models/
#
# Cambia esta ruta por la ubicación real de tu carpeta models.
OUTPUT_ROOT = Path(
    r"C:\Users\User\Desktop\Created programs\Mine\Reverse Engineering\Roblox\RtG Format\assets\models"
)


# Nombre de la colección que contiene los modelos.
#
# Ejemplo:
#
# Models
# ├── Switch
# ├── Tooth
# ├── Part
# └── ...
#
# Si no utilizas una colección "Models", puedes poner:
# MODELS_COLLECTION = None
#
# y el script buscará objetos raíz en la escena.
MODELS_COLLECTION = "Models"


# Distancia máxima para considerar que una rama pertenece
# a un Point_X.
#
# Si ninguna distancia es menor a este valor, la rama recibe
# "NaN".
#
# Ajusta este valor según la escala de tus modelos.
BRANCH_POINT_MAX_DISTANCE = 250.0


# Nombre de la colección de puntos.
POINTS_COLLECTION_NAME = "Points"


# Nombre de la colección de geometría.
GEOMETRY_COLLECTION_NAME = "Geometry"


# ============================================================
# UTILIDADES GENERALES
# ============================================================

def is_point_object(obj):
    """
    Devuelve True si el objeto es un Empty llamado Point_X.

    Ejemplos válidos:
        Point_1
        Point_2
        Point_10

    Ejemplos inválidos:
        Point
        point_2
        Connector
    """

    if obj.type != 'EMPTY':
        return False

    if not obj.name.startswith("Point_"):
        return False

    point_id = obj.name[6:]

    return point_id.isdigit()


def get_point_id(obj):
    """
    Extrae el ID numérico de Point_X.

    Point_2 -> "2"
    Point_10 -> "10"
    """

    return obj.name[6:]


def get_world_location(obj):
    """
    Devuelve la posición mundial del objeto.
    """

    return obj.matrix_world.translation.copy()


def get_world_rotation_euler(obj):
    """
    Devuelve la rotación mundial como Euler.

    Se utilizará para llenar:

        LocalPoints:
        {
            "2": [
                [x, y, z],
                [rx, ry, rz]
            ]
        }
    """

    return obj.matrix_world.to_euler().copy()


# ============================================================
# BÚSQUEDA DE PUNTOS
# ============================================================

def find_points(model_root):
    """
    Busca todos los Point_X pertenecientes al modelo.

    El script busca:

        Model
        └── Points
            ├── Point_1
            ├── Point_2
            └── ...

    También permite que estén como hijos directos del modelo.
    """

    points = []

    # --------------------------------------------------------
    # Primero buscamos por descendencia.
    # --------------------------------------------------------

    for obj in bpy.data.objects:

        if not is_point_object(obj):
            continue

        # Comprueba si el objeto pertenece al modelo
        # recorriendo sus padres.
        parent = obj.parent

        while parent is not None:

            if parent == model_root:
                points.append(obj)
                break

            parent = parent.parent

    # --------------------------------------------------------
    # Ordenar numéricamente.
    # --------------------------------------------------------

    points.sort(
        key=lambda obj: int(get_point_id(obj))
    )

    return points


# ============================================================
# BÚSQUEDA DE GEOMETRÍA
# ============================================================

def find_geometry_objects(model_root):
    """
    Encuentra la geometría real del modelo.

    No incluye Empty/Points.

    Devuelve objetos MESH.

    También excluye cámaras, luces y otros objetos que puedan
    estar dentro de la escena.
    """

    geometry = []

    for obj in bpy.data.objects:

        if obj.type != 'MESH':
            continue

        parent = obj

        belongs_to_model = False

        while parent is not None:

            if parent == model_root:
                belongs_to_model = True
                break

            parent = parent.parent

        if belongs_to_model:
            geometry.append(obj)

    return geometry


# ============================================================
# CENTRADO DE GEOMETRÍA
# ============================================================

def calculate_geometry_center(objects):
    """
    Calcula el centro geométrico global de todos los vértices
    del modelo.

    Esto es importante:

    NO utilizamos simplemente object.location.

    Utilizamos los vértices reales de la geometría para encontrar
    dónde está físicamente el modelo.
    """

    world_vertices = []

    for obj in objects:

        if obj.type != 'MESH':
            continue

        matrix = obj.matrix_world

        for vertex in obj.data.vertices:

            world_position = matrix @ vertex.co

            world_vertices.append(world_position)

    if not world_vertices:
        return Vector((0.0, 0.0, 0.0))

    min_x = min(v.x for v in world_vertices)
    max_x = max(v.x for v in world_vertices)

    min_y = min(v.y for v in world_vertices)
    max_y = max(v.y for v in world_vertices)

    min_z = min(v.z for v in world_vertices)
    max_z = max(v.z for v in world_vertices)

    center = Vector((
        (min_x + max_x) / 2.0,
        (min_y + max_y) / 2.0,
        (min_z + max_z) / 2.0
    ))

    return center


def center_model_geometry(model_root, geometry_objects, points):
    """
    Centra toda la geometría según su bounding box real.

    IMPORTANTE:

    Primero guardamos las matrices de los puntos.

    Después movemos la geometría.

    Finalmente recalculamos las posiciones de los puntos
    relativas al nuevo centro.

    De esta manera el punto sigue exactamente en el mismo lugar
    relativo del modelo.
    """

    if not geometry_objects:
        return

    # --------------------------------------------------------
    # Guardar posiciones mundiales de los puntos.
    # --------------------------------------------------------

    point_world_matrices = {
        point: point.matrix_world.copy()
        for point in points
    }

    # --------------------------------------------------------
    # Calcular centro geométrico.
    # --------------------------------------------------------

    center = calculate_geometry_center(
        geometry_objects
    )

    print(
        f"[RtG] Centro calculado para {model_root.name}: "
        f"{center}"
    )

    # --------------------------------------------------------
    # Mover TODO el conjunto del modelo.
    #
    # En lugar de mover vértices individualmente, modificamos
    # las matrices de los objetos.
    # --------------------------------------------------------

    translation = MatrixTranslation(
        -center.x,
        -center.y,
        -center.z
    )

    for obj in geometry_objects:

        obj.matrix_world = (
            translation @ obj.matrix_world
        )

    # --------------------------------------------------------
    # Restaurar las posiciones relativas de los puntos.
    #
    # Los puntos no deben quedarse en su posición anterior.
    # También tienen que desplazarse con la geometría.
    # --------------------------------------------------------

    for point, old_matrix in point_world_matrices.items():

        point.matrix_world = (
            translation @ old_matrix
        )

    # --------------------------------------------------------
    # El root se mantiene en 0,0,0.
    # --------------------------------------------------------

    model_root.location = (
        0.0,
        0.0,
        0.0
    )


def MatrixTranslation(x, y, z):
    """
    Crea una matriz 4x4 de traslación.
    """
    return Matrix.Translation(
        Vector((x, y, z))
    )


# ============================================================
# NORMALIZACIÓN FINAL DE LA ESCENA
# ============================================================

def reset_model_position(model_root):
    """
    Asegura que el objeto raíz esté en:

        0, 0, 0

    No toca las coordenadas locales de la geometría.
    """

    model_root.location = (
        0.0,
        0.0,
        0.0
    )


# ============================================================
# ASOCIACIÓN DE RAMAS
# ============================================================

def find_nearest_point(branch, points):
    """
    Busca el Point_X más cercano al origen de una rama.

    Devuelve:

        ("2", distance)

    o:

        ("NaN", distance)

    cuando no hay un punto suficientemente cercano.
    """

    if not points:
        return "NaN", None

    branch_location = get_world_location(branch)

    nearest_point = None
    nearest_distance = float("inf")

    for point in points:

        point_location = get_world_location(point)

        distance = (
            branch_location - point_location
        ).length

        if distance < nearest_distance:

            nearest_distance = distance
            nearest_point = point

    if (
        nearest_point is None
        or nearest_distance > BRANCH_POINT_MAX_DISTANCE
    ):
        return "NaN", nearest_distance

    return (
        get_point_id(nearest_point),
        nearest_distance
    )


def classify_branches(model_root, geometry_objects, points):
    """
    Separa:

        - Modelo principal
        - Ramas

    El objeto cuyo nombre coincide con el modelo raíz
    se considera el modelo completo.

    Ejemplo:

        Switch
        ├── Switch   -> modelo principal
        ├── Input    -> rama
        └── Output   -> rama

    Resultado:

        Main:
            Switch

        Branches:
            Input
            Output
    """

    main_object = None
    branches = []

    for obj in geometry_objects:

        if obj.name == model_root.name:
            main_object = obj
        else:
            branches.append(obj)

    return main_object, branches


# ============================================================
# EXPORTACIÓN OBJ
# ============================================================

def export_object_as_obj(obj, output_path):
    """
    Exporta un objeto individual como OBJ.

    Los Empty no pasan por aquí, por lo que Point_X jamás
    termina dentro del archivo OBJ.
    """

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    # --------------------------------------------------------
    # Guardar selección actual.
    # --------------------------------------------------------

    previous_selection = [
        obj
        for obj in bpy.context.selected_objects
    ]

    previous_active = bpy.context.view_layer.objects.active

    # --------------------------------------------------------
    # Limpiar selección.
    # --------------------------------------------------------

    bpy.ops.object.select_all(
        action='DESELECT'
    )

    # --------------------------------------------------------
    # Seleccionar únicamente el objeto.
    # --------------------------------------------------------

    obj.select_set(True)

    bpy.context.view_layer.objects.active = obj

    # --------------------------------------------------------
    # Exportar.
    #
    # Blender 4.x utiliza:
    # bpy.ops.wm.obj_export
    # --------------------------------------------------------

    bpy.ops.wm.obj_export(
        filepath=str(output_path),
        export_selected_objects=True,
        apply_modifiers=True,
        export_materials=True,
        export_uv=True
    )

    # --------------------------------------------------------
    # Restaurar selección anterior.
    # --------------------------------------------------------

    bpy.ops.object.select_all(
        action='DESELECT'
    )

    for selected in previous_selection:

        if selected.name in bpy.data.objects:
            selected.select_set(True)

    bpy.context.view_layer.objects.active = previous_active


# ============================================================
# CONSTRUCCIÓN DE LOCALPOINTS
# ============================================================

def build_local_points(points):
    """
    Convierte los Empty Point_X al formato esperado por
    los JSON de RtG-Format.

    Ejemplo:

        Point_2
        Location = (5, 0, 2)
        Rotation = (0, 0, 0)

    produce:

        "LocalPoints": {
            "2": [
                [5, 0, 2],
                [0, 0, 0]
            ]
        }
    """

    local_points = {}

    for point in points:

        point_id = get_point_id(point)

        location = get_world_location(point)
        rotation = get_world_rotation_euler(point)

        local_points[point_id] = [
            [
                float(location.x),
                float(location.y),
                float(location.z)
            ],
            [
                float(rotation.x),
                float(rotation.y),
                float(rotation.z)
            ]
        ]

    return local_points


# ============================================================
# CONSTRUCCIÓN DE BRANCHES
# ============================================================

def build_branches(branches, points, model_directory):
    """
    Construye el objeto JSON "Branches".

    Las ramas se asocian automáticamente con el Point_X
    más cercano.

    Si no hay punto cercano:

        "NaN"

    Ejemplo:

        {
            "NaN": "./split/input.obj",
            "2": "./split/output.obj"
        }
    """

    result = {}

    for branch in branches:

        point_id, distance = find_nearest_point(
            branch,
            points
        )

        # ----------------------------------------------------
        # Determinar nombre del archivo.
        # ----------------------------------------------------

        filename = (
            f"{branch.name}.obj"
        )

        # ----------------------------------------------------
        # Exportar dentro de split/.
        # ----------------------------------------------------

        split_directory = (
            model_directory / "split"
        )

        output_path = (
            split_directory / filename
        )

        export_object_as_obj(
            branch,
            output_path
        )

        # ----------------------------------------------------
        # Ruta relativa utilizada por RtG-Preview.
        # ----------------------------------------------------

        relative_path = (
            f"./split/{filename}"
        )

        result[point_id] = relative_path

        print(
            f"[RtG] Rama '{branch.name}' "
            f"-> {point_id} "
            f"(distancia: {distance})"
        )

    return result


# ============================================================
# GENERACIÓN DEL JSON
# ============================================================

def build_json(model_name, local_points, branches):
    """
    Genera el contenido JSON siguiendo la estructura utilizada
    actualmente por RtG-Format.
    """

    data = [
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

    return data


def save_json(model_name, model_directory, data):
    """
    Guarda <ModelName>.json dentro de la carpeta del modelo.
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
        f"[RtG] JSON guardado: {json_path}"
    )


# ============================================================
# PROCESAMIENTO DE UN MODELO
# ============================================================

def process_model(model_root):
    """
    Procesa completamente un modelo.

    Ejemplo:

        Switch
        ├── Switch
        ├── Input
        ├── Output
        └── Point_2

    """

    model_name = model_root.name

    print("")
    print("=" * 60)
    print(
        f"[RtG] Procesando modelo: {model_name}"
    )
    print("=" * 60)

    # --------------------------------------------------------
    # Crear carpeta del modelo.
    # --------------------------------------------------------

    model_directory = (
        OUTPUT_ROOT /
        model_name
    )

    model_directory.mkdir(
        parents=True,
        exist_ok=True
    )

    # --------------------------------------------------------
    # Buscar puntos.
    # --------------------------------------------------------

    points = find_points(
        model_root
    )

    print(
        f"[RtG] Puntos encontrados: "
        f"{len(points)}"
    )

    for point in points:

        print(
            f"    - {point.name}"
        )

    # --------------------------------------------------------
    # Buscar geometría.
    # --------------------------------------------------------

    geometry_objects = (
        find_geometry_objects(
            model_root
        )
    )

    print(
        f"[RtG] Objetos de geometría: "
        f"{len(geometry_objects)}"
    )

    for obj in geometry_objects:

        print(
            f"    - {obj.name}"
        )

    if not geometry_objects:

        print(
            "[RtG] ERROR: "
            "No se encontró geometría."
        )

        return

    # --------------------------------------------------------
    # Centrar la geometría.
    #
    # Esto debe suceder ANTES de exportar y ANTES de leer
    # las posiciones finales de los puntos.
    # --------------------------------------------------------

    center_model_geometry(
        model_root,
        geometry_objects,
        points
    )

    # --------------------------------------------------------
    # Garantizar posición raíz 0,0,0.
    # --------------------------------------------------------

    reset_model_position(
        model_root
    )

    # --------------------------------------------------------
    # Separar modelo principal de ramas.
    # --------------------------------------------------------

    main_object, branches = (
        classify_branches(
            model_root,
            geometry_objects,
            points
        )
    )

    if main_object is None:

        print(
            f"[RtG] ADVERTENCIA: "
            f"no existe un objeto llamado "
            f"'{model_name}'."
        )

        return

    # --------------------------------------------------------
    # Exportar modelo completo.
    #
    # Este es el archivo:

    #     Switch/Switch.obj
    # --------------------------------------------------------

    main_output = (
        model_directory /
        f"{model_name}.obj"
    )

    export_object_as_obj(
        main_object,
        main_output
    )

    print(
        f"[RtG] Modelo principal exportado: "
        f"{main_output}"
    )

    # --------------------------------------------------------
    # Construir LocalPoints.
    #
    # IMPORTANTE:
    # Esto se hace DESPUÉS del centrado.
    # --------------------------------------------------------

    local_points = build_local_points(
        points
    )

    # --------------------------------------------------------
    # Construir Branches.
    # --------------------------------------------------------

    branches_json = build_branches(
        branches,
        points,
        model_directory
    )

    # --------------------------------------------------------
    # Crear JSON.
    # --------------------------------------------------------

    json_data = build_json(
        model_name,
        local_points,
        branches_json
    )

    # --------------------------------------------------------
    # Guardarlo.
    # --------------------------------------------------------

    save_json(
        model_name,
        model_directory,
        json_data
    )

    print(
        f"[RtG] Modelo '{model_name}' terminado."
    )


# ============================================================
# ENCONTRAR MODELOS
# ============================================================

def find_model_roots():
    """
    Encuentra los objetos raíz que representan modelos.

    Si existe la colección "Models", únicamente se procesa
    su contenido.

    De esta manera puedes tener:

        Models
        ├── Switch
        ├── Tooth
        ├── Part
        └── ...

    """

    if MODELS_COLLECTION:

        collection = bpy.data.collections.get(
            MODELS_COLLECTION
        )

        if collection is None:

            print(
                f"[RtG] ADVERTENCIA: "
                f"no existe la colección "
                f"'{MODELS_COLLECTION}'."
            )

            return []

        # ----------------------------------------------------
        # Solamente objetos que no tienen padre dentro de la
        # colección.
        # ----------------------------------------------------

        roots = []

        for obj in collection.objects:

            if obj.parent is None:
                roots.append(obj)

        return roots

    # --------------------------------------------------------
    # Alternativa:
    # objetos raíz de toda la escena.
    # --------------------------------------------------------

    return [
        obj
        for obj in bpy.context.scene.objects
        if obj.parent is None
    ]


# ============================================================
# EJECUCIÓN PRINCIPAL
# ============================================================

def main():
    """
    Punto de entrada del script.
    """

    print("")
    print("=" * 60)
    print("RtG-Format Blender Exporter")
    print("=" * 60)

    # --------------------------------------------------------
    # Comprobar carpeta de salida.
    # --------------------------------------------------------

    if not OUTPUT_ROOT.exists():

        print(
            f"[RtG] ERROR: "
            f"La carpeta de salida no existe:\n"
            f"{OUTPUT_ROOT}"
        )

        return

    # --------------------------------------------------------
    # Encontrar modelos.
    # --------------------------------------------------------

    models = find_model_roots()

    if not models:

        print(
            "[RtG] No se encontraron modelos."
        )

        return

    print(
        f"[RtG] Modelos encontrados: "
        f"{len(models)}"
    )

    # --------------------------------------------------------
    # Procesarlos uno por uno.
    # --------------------------------------------------------

    for model in models:

        process_model(model)

    print("")
    print("=" * 60)
    print("RtG-Format: proceso terminado")
    print("=" * 60)


# ============================================================
# EJECUTAR
# ============================================================

if __name__ == "__main__":
    main()