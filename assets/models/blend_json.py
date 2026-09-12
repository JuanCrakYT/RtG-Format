"""
RtG-Format - Blender Model Exporter
===================================

Exportador automático de modelos de Road To Gramby's desde Blender.

ESTRUCTURA DE BLENDER
---------------------

Modelo simple:

    Model
    └── Model

Modelo con ramas:

    Switch
    ├── Switch
    ├── input
    │   └── start
    └── output
        ├── start
        └── Point_2

REGLAS
------

ROOT
----

El objeto raíz representa el modelo.

El MESH cuyo nombre coincide con el nombre del root es el modelo
completo.

Ejemplo:

    Switch
    └── Switch

BRANCHES
--------

Todo MESH descendiente distinto del MESH principal es una rama.

Ejemplo:

    Switch
    ├── Switch
    ├── input
    └── output

El resultado será:

    Switch.obj
    split/input.obj
    split/output.obj

START
-----

Cada rama debe tener un Empty llamado exactamente:

    start

Ese Empty representa el origen de montaje de la rama.

Ejemplo:

    output
    ├── start
    └── Point_2

La posición y rotación de "start" se guardan en:

    "Branches Start"

POINTS
------

Los puntos son Empty llamados:

    Point_1
    Point_2
    Point_3
    ...

Un Point_X pertenece a la rama dentro de cuya jerarquía se encuentre.

Ejemplo:

    output
    ├── start
    └── Point_2

significa:

    "2": "./split/output.obj"

Si una rama no tiene Point_X:

    "NaN": "./split/input.obj"

Si una rama tiene más de un Point_X:

    ERROR

CENTRADO
--------

El modelo completo se centra usando únicamente la geometría del
MESH principal.

El centro del modelo completo pasa a ser:

    0,0,0

La escena original de Blender NO se modifica.

MODELO PRINCIPAL
----------------

Switch.obj se exporta en coordenadas centradas respecto al centro
geométrico del modelo completo.

RAMAS
------

Las ramas NO utilizan el centro global como origen.

Cada rama se exporta tomando su Empty "start" como origen.

Es decir:

    rama/start = 0,0,0

y su geometría se expresa relativa a ese start.

Esto permite colocar posteriormente la rama usando:

    "Branches Start"

JSON
----

Se conserva la información existente del JSON.

El script actualiza:

    LocalPoints
    Branches
    Branches Start
    Default Branch

La estructura final es:

    "LocalPoints": {
        "2": [
            [x,y,z],
            [rx,ry,rz]
        ]
    },

    "Branches": {
        "NaN": "./split/input.obj",
        "2": "./split/output.obj"
    },

    "Branches Start": {
        "./split/input.obj": [
            [x,y,z],
            [rx,ry,rz]
        ],
        "./split/output.obj": [
            [x,y,z],
            [rx,ry,rz]
        ]
    },

    "Default Branch": [
        "./Switch.obj"
    ]

IMPORTANTE
----------

Los Empty nunca se exportan.

El script no modifica la posición, rotación ni escala de los
objetos originales de Blender.
"""


# ============================================================
# IMPORTACIONES
# ============================================================

import bpy
import json

from pathlib import Path

from mathutils import Vector, Matrix


# ============================================================
# CONFIGURACIÓN
# ============================================================

# ------------------------------------------------------------
# Carpeta donde se encuentran los modelos de RtG-Format.
# ------------------------------------------------------------

OUTPUT_ROOT = Path(
    r"C:\Users\User\Desktop\Created programs\Mine\Reverse Engineering\Roblox\RtG Format\assets\models"
)


# ------------------------------------------------------------
# Nombre utilizado para los Empty de puntos.
# ------------------------------------------------------------

POINT_PREFIX = "Point_"


# ------------------------------------------------------------
# Nombre exacto del Empty de montaje de una rama.
# ------------------------------------------------------------

START_NAME = "start"


# ============================================================
# UTILIDADES
# ============================================================

def clean_number(value):
    """
    Limpia valores flotantes provenientes de Blender.

    Evita cosas como:

        0.000000000001

    y produce:

        0
    """

    value = float(value)

    if abs(value) < 1e-10:
        return 0

    value = round(value, 10)

    if value == int(value):
        return int(value)

    return value


def vector_to_list(vector):
    """
    Convierte un Vector de Blender a una lista JSON.
    """

    return [
        clean_number(vector.x),
        clean_number(vector.y),
        clean_number(vector.z)
    ]


def rotation_to_list(euler):
    """
    Convierte una rotación Euler de Blender a una lista JSON.

    La salida es:

        [x, y, z]
    """

    return [
        clean_number(euler.x),
        clean_number(euler.y),
        clean_number(euler.z)
    ]


# ============================================================
# IDENTIFICAR POINT_X
# ============================================================

def is_point(obj):
    """
    Comprueba si un objeto es un Empty Point_X.

    Ejemplos:

        Point_1 -> True
        Point_2 -> True
        Point_25 -> True

        Point -> False
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
    """

    return obj.name[len(POINT_PREFIX):]


# ============================================================
# JERARQUÍA
# ============================================================

def is_descendant(obj, root):
    """
    Devuelve True si obj pertenece a la jerarquía de root.
    """

    current = obj.parent

    while current is not None:

        if current == root:
            return True

        current = current.parent

    return False


def get_descendant_meshes(root):
    """
    Obtiene todos los MESH descendientes del modelo.
    """

    meshes = []

    for obj in bpy.context.scene.objects:

        if obj.type != "MESH":
            continue

        if is_descendant(obj, root):

            meshes.append(obj)

    return meshes


def get_descendant_points(root):
    """
    Obtiene todos los Point_X descendientes del modelo.
    """

    points = []

    for obj in bpy.context.scene.objects:

        if not is_point(obj):
            continue

        if is_descendant(obj, root):

            points.append(obj)

    points.sort(
        key=lambda obj: int(get_point_id(obj))
    )

    return points


def get_direct_children(root):
    """
    Devuelve únicamente hijos directos.
    """

    return [
        obj
        for obj in bpy.context.scene.objects
        if obj.parent == root
    ]


# ============================================================
# MODELO PRINCIPAL
# ============================================================

def find_main_mesh(model_root, meshes):
    """
    Encuentra el MESH cuyo nombre coincide con el modelo raíz.

    Ejemplo:

        Switch
        └── Switch

    """

    matches = [
        mesh
        for mesh in meshes
        if mesh.name == model_root.name
    ]

    if len(matches) == 0:

        raise RuntimeError(
            f"No existe un MESH principal llamado "
            f"'{model_root.name}'."
        )

    if len(matches) > 1:

        raise RuntimeError(
            f"Existen múltiples MESH llamados "
            f"'{model_root.name}'."
        )

    return matches[0]


# ============================================================
# RAMAS
# ============================================================

def find_branches(main_mesh, meshes):
    """
    Todo MESH distinto del principal es una rama.
    """

    return [
        mesh
        for mesh in meshes
        if mesh != main_mesh
    ]


# ============================================================
# START DE RAMA
# ============================================================

def find_branch_start(branch):
    """
    Busca el Empty llamado exactamente "start" dentro de una rama.

    Ejemplo:

        output
        ├── start
        └── Point_2

    Devuelve:

        start

    """

    starts = []

    for obj in bpy.context.scene.objects:

        if obj.type != "EMPTY":
            continue

        if obj.name != START_NAME:
            continue

        if is_descendant(obj, branch):

            starts.append(obj)

    if len(starts) == 0:

        raise RuntimeError(
            f"La rama '{branch.name}' "
            f"no tiene un Empty llamado 'start'."
        )

    if len(starts) > 1:

        raise RuntimeError(
            f"La rama '{branch.name}' "
            f"tiene múltiples Empty llamados 'start'."
        )

    return starts[0]


# ============================================================
# POINT DE RAMA
# ============================================================

def find_branch_point(branch):
    """
    Busca el Point_X perteneciente a la rama.

    Una rama puede tener:

        0 Point_X -> NaN
        1 Point_X -> ID
        >1 Point_X -> ERROR
    """

    points = []

    for obj in bpy.context.scene.objects:

        if not is_point(obj):
            continue

        if is_descendant(obj, branch):

            points.append(obj)

    points.sort(
        key=lambda obj: int(get_point_id(obj))
    )

    if len(points) == 0:

        return "NaN"

    if len(points) > 1:

        point_names = ", ".join(
            point.name
            for point in points
        )

        raise RuntimeError(
            f"La rama '{branch.name}' "
            f"tiene varios puntos: {point_names}"
        )

    return get_point_id(points[0])


# ============================================================
# GEOMETRÍA EVALUADA
# ============================================================

def evaluated_mesh(obj):
    """
    Obtiene una copia evaluada de la malla.

    Esto incluye la geometría resultante de los modificadores.
    """

    depsgraph = bpy.context.evaluated_depsgraph_get()

    evaluated = obj.evaluated_get(
        depsgraph
    )

    mesh = evaluated.to_mesh(
        preserve_all_data_layers=True,
        depsgraph=depsgraph
    )

    return evaluated, mesh


# ============================================================
# CENTRO DEL MODELO COMPLETO
# ============================================================

def calculate_main_center(main_mesh):
    """
    Calcula el centro del bounding box del MESH completo.

    Se utilizan los vértices reales del modelo principal.
    """

    evaluated, mesh = evaluated_mesh(
        main_mesh
    )

    try:

        world_matrix = (
            evaluated.matrix_world.copy()
        )

        vertices = [
            world_matrix @ vertex.co
            for vertex in mesh.vertices
        ]

    finally:

        evaluated.to_mesh_clear()

    if not vertices:

        raise RuntimeError(
            f"El MESH '{main_mesh.name}' "
            f"no contiene vértices."
        )

    min_x = min(
        vertex.x
        for vertex in vertices
    )

    max_x = max(
        vertex.x
        for vertex in vertices
    )

    min_y = min(
        vertex.y
        for vertex in vertices
    )

    max_y = max(
        vertex.y
        for vertex in vertices
    )

    min_z = min(
        vertex.z
        for vertex in vertices
    )

    max_z = max(
        vertex.z
        for vertex in vertices
    )

    return Vector((
        (min_x + max_x) / 2.0,
        (min_y + max_y) / 2.0,
        (min_z + max_z) / 2.0
    ))


# ============================================================
# LOCALPOINTS
# ============================================================

def build_local_points(points, model_center):
    """
    Genera LocalPoints respecto al centro del modelo completo.
    """

    result = {}

    for point in points:

        world_position = (
            point.matrix_world.translation.copy()
        )

        local_position = (
            world_position - model_center
        )

        rotation = (
            point.matrix_world.to_euler().copy()
        )

        point_id = get_point_id(point)

        result[point_id] = [
            vector_to_list(local_position),
            rotation_to_list(rotation)
        ]

    return result


# ============================================================
# BRANCHES START
# ============================================================

def build_branches_start(branches, model_center):
    """
    Genera "Branches Start".

    Cada rama se coloca mediante su Empty "start".

    La posición queda expresada respecto al centro del modelo.

    Ejemplo:

        output/start
            World = (100, 20, 50)

        Model Center
            = (100, 19.25, 50)

        Resultado:

            [0, 0.75, 0]
    """

    result = {}

    for branch in branches:

        start = find_branch_start(
            branch
        )

        world_position = (
            start.matrix_world.translation.copy()
        )

        local_position = (
            world_position - model_center
        )

        rotation = (
            start.matrix_world.to_euler().copy()
        )

        branch_path = (
            f"./split/{branch.name}.obj"
        )

        result[branch_path] = [
            vector_to_list(local_position),
            rotation_to_list(rotation)
        ]

    return result


# ============================================================
# PREPARAR MALLA PRINCIPAL
# ============================================================

def create_main_export_mesh(main_mesh, model_center):
    """
    Crea una malla temporal del modelo principal.

    Toda la transformación mundial se hornea en los vértices.

    Después se resta model_center.

    Resultado:

        centro geométrico = 0,0,0
    """

    evaluated, source_mesh = evaluated_mesh(
        main_mesh
    )

    try:

        world_matrix = (
            evaluated.matrix_world.copy()
        )

        vertices = [
            world_matrix @ vertex.co
            - model_center
            for vertex in source_mesh.vertices
        ]

        faces = [
            tuple(polygon.vertices)
            for polygon in source_mesh.polygons
        ]

        mesh = bpy.data.meshes.new(
            f"__RtGMain_{main_mesh.name}"
        )

        mesh.from_pydata(
            [
                tuple(vertex)
                for vertex in vertices
            ],
            [],
            faces
        )

        mesh.update()

        obj = bpy.data.objects.new(
            f"__RtGMain_{main_mesh.name}",
            mesh
        )

        bpy.context.scene.collection.objects.link(
            obj
        )

        return obj

    finally:

        evaluated.to_mesh_clear()


# ============================================================
# PREPARAR MALLA DE RAMA
# ============================================================

def create_branch_export_mesh(branch, start):
    """
    Crea una malla temporal de una rama.

    La diferencia importante respecto al modelo principal:

    La rama utiliza "start" como su origen.

    Por lo tanto:

        start = 0,0,0

    dentro del OBJ exportado.

    Se utiliza la inversa de la matriz mundial de start para
    convertir la geometría mundial al espacio local del start.
    """

    evaluated, source_mesh = evaluated_mesh(
        branch
    )

    try:

        branch_world = (
            evaluated.matrix_world.copy()
        )

        start_world = (
            start.matrix_world.copy()
        )

        # ----------------------------------------------------
        # Transformación que convierte world-space a
        # start-space.
        # ----------------------------------------------------

        world_to_start = (
            start_world.inverted()
        )

        vertices = []

        for vertex in source_mesh.vertices:

            world_position = (
                branch_world @ vertex.co
            )

            local_position = (
                world_to_start @ world_position
            )

            vertices.append(
                local_position
            )

        faces = [
            tuple(polygon.vertices)
            for polygon in source_mesh.polygons
        ]

        mesh = bpy.data.meshes.new(
            f"__RtGBranch_{branch.name}"
        )

        mesh.from_pydata(
            [
                tuple(vertex)
                for vertex in vertices
            ],
            [],
            faces
        )

        mesh.update()

        obj = bpy.data.objects.new(
            f"__RtGBranch_{branch.name}",
            mesh
        )

        bpy.context.scene.collection.objects.link(
            obj
        )

        # ----------------------------------------------------
        # El objeto temporal ya está en el sistema de
        # coordenadas del start.
        # ----------------------------------------------------

        obj.location = (
            0.0,
            0.0,
            0.0
        )

        obj.rotation_euler = (
            0.0,
            0.0,
            0.0
        )

        obj.scale = (
            1.0,
            1.0,
            1.0
        )

        return obj

    finally:

        evaluated.to_mesh_clear()


# ============================================================
# EXPORTAR OBJ
# ============================================================

def export_temp_obj(temp_obj, output_path):
    """
    Exporta un objeto temporal como OBJ.
    """

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    old_selection = list(
        bpy.context.selected_objects
    )

    old_active = (
        bpy.context.view_layer.objects.active
    )

    try:

        bpy.ops.object.select_all(
            action="DESELECT"
        )

        temp_obj.select_set(
            True
        )

        bpy.context.view_layer.objects.active = (
            temp_obj
        )

        bpy.ops.wm.obj_export(
            filepath=str(output_path),
            export_selected_objects=True,
            export_materials=True,
            export_uv=True
        )

    finally:

        mesh = temp_obj.data

        bpy.data.objects.remove(
            temp_obj,
            do_unlink=True
        )

        if mesh.users == 0:

            bpy.data.meshes.remove(
                mesh
            )

        bpy.ops.object.select_all(
            action="DESELECT"
        )

        for obj in old_selection:

            if obj.name in bpy.data.objects:

                obj.select_set(
                    True
                )

        if old_active is not None:

            if old_active.name in bpy.data.objects:

                bpy.context.view_layer.objects.active = (
                    old_active
                )


# ============================================================
# JSON EXISTENTE
# ============================================================

def load_existing_json(json_path, model_name):
    """
    Carga el JSON existente.

    Si todavía no existe, crea una estructura compatible.
    """

    if not json_path.exists():

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
                        }
                    },

                    "Page": {}
                },

                "Name": model_name,

                "Tooltip": "",

                "LocalPoints": {},

                "Branches": {},

                "Branches Start": {},

                "Default Branch": [
                    f"./{model_name}.obj"
                ]
            }
        ]

    with open(
        json_path,
        "r",
        encoding="utf-8-sig"
    ) as file:

        data = json.load(file)

    if not isinstance(data, list) or not data:

        raise RuntimeError(
            f"El JSON '{json_path}' "
            f"no contiene una lista válida."
        )

    if not isinstance(data[0], dict):

        raise RuntimeError(
            f"El JSON '{json_path}' "
            f"tiene una estructura inválida."
        )

    return data


# ============================================================
# ACTUALIZAR JSON
# ============================================================

def update_json(
    data,
    model_name,
    local_points,
    branches,
    branches_start
):
    """
    Actualiza exclusivamente los campos generados
    automáticamente por Blender.

    Se conserva información manual como:

        Tooltip
        Description
        Page
        RtG-Format Data
    """

    model_data = data[0]

    # --------------------------------------------------------
    # LocalPoints
    # --------------------------------------------------------

    model_data["LocalPoints"] = (
        local_points
    )

    # --------------------------------------------------------
    # Branches
    # --------------------------------------------------------

    model_data["Branches"] = (
        branches
    )

    # --------------------------------------------------------
    # Branches Start
    # --------------------------------------------------------

    model_data["Branches Start"] = (
        branches_start
    )

    # --------------------------------------------------------
    # Default Branch
    # --------------------------------------------------------

    model_data["Default Branch"] = [
        f"./{model_name}.obj"
    ]

    # --------------------------------------------------------
    # Nombre.
    # --------------------------------------------------------

    if not model_data.get("Name"):

        model_data["Name"] = model_name

    # --------------------------------------------------------
    # Mantener RtG-Preview existente.
    #
    # OJO:
    # Default Branch ya NO está aquí.
    # --------------------------------------------------------

    rtg_format = model_data.setdefault(
        "RtG-Format",
        {}
    )

    preview = rtg_format.setdefault(
        "RtG-Preview",
        {}
    )

    preview.setdefault(
        "Size",
        {
            "default": 1
        }
    )

    return data


def save_json(json_path, data):
    """
    Guarda el JSON.
    """

    json_path.parent.mkdir(
        parents=True,
        exist_ok=True
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


# ============================================================
# PROCESAR MODELO
# ============================================================

def process_model(model_root):
    """
    Procesa un modelo completo.

    Ejemplo:

        Switch
        ├── Switch
        ├── input
        │   └── start
        └── output
            ├── start
            └── Point_2
    """

    model_name = model_root.name

    print("")
    print("=" * 70)
    print(
        f"[RtG] Procesando: {model_name}"
    )
    print("=" * 70)

    # --------------------------------------------------------
    # Descubrir MESH.
    # --------------------------------------------------------

    meshes = get_descendant_meshes(
        model_root
    )

    if not meshes:

        raise RuntimeError(
            f"El modelo '{model_name}' "
            f"no contiene MESH."
        )

    # --------------------------------------------------------
    # Principal.
    # --------------------------------------------------------

    main_mesh = find_main_mesh(
        model_root,
        meshes
    )

    # --------------------------------------------------------
    # Ramas.
    # --------------------------------------------------------

    branches = find_branches(
        main_mesh,
        meshes
    )

    # --------------------------------------------------------
    # Puntos.
    # --------------------------------------------------------

    points = get_descendant_points(
        model_root
    )

    print(
        f"[RtG] Principal: {main_mesh.name}"
    )

    print(
        f"[RtG] Ramas: {len(branches)}"
    )

    print(
        f"[RtG] Puntos: {len(points)}"
    )

    # --------------------------------------------------------
    # Centro del modelo principal.
    # --------------------------------------------------------

    model_center = calculate_main_center(
        main_mesh
    )

    print(
        "[RtG] Centro del modelo: "
        f"{tuple(clean_number(v) for v in model_center)}"
    )

    # --------------------------------------------------------
    # Directorios.
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
    # split/ se crea automáticamente.
    # --------------------------------------------------------

    split_directory.mkdir(
        parents=True,
        exist_ok=True
    )

    # ========================================================
    # EXPORTAR MODELO PRINCIPAL
    # ========================================================

    main_temp = create_main_export_mesh(
        main_mesh,
        model_center
    )

    main_output = (
        model_directory /
        f"{model_name}.obj"
    )

    export_temp_obj(
        main_temp,
        main_output
    )

    print(
        f"[RtG] Principal -> {main_output}"
    )

    # ========================================================
    # BRANCHES
    # ========================================================

    branches_json = {}

    for branch in branches:

        # ----------------------------------------------------
        # Encontrar start.
        # ----------------------------------------------------

        start = find_branch_start(
            branch
        )

        # ----------------------------------------------------
        # Encontrar Point_X.
        # ----------------------------------------------------

        point_id = find_branch_point(
            branch
        )

        # ----------------------------------------------------
        # Ruta.
        # ----------------------------------------------------

        branch_filename = (
            f"{branch.name}.obj"
        )

        branch_path = (
            f"./split/{branch_filename}"
        )

        branch_output = (
            split_directory /
            branch_filename
        )

        # ----------------------------------------------------
        # Crear exportación temporal.
        # ----------------------------------------------------

        branch_temp = (
            create_branch_export_mesh(
                branch,
                start
            )
        )

        # ----------------------------------------------------
        # Exportar.
        # ----------------------------------------------------

        export_temp_obj(
            branch_temp,
            branch_output
        )

        # ----------------------------------------------------
        # Registrar rama.
        # ----------------------------------------------------

        if point_id in branches_json:

            raise RuntimeError(
                f"El ID '{point_id}' "
                f"ya fue asignado a otra rama."
            )

        branches_json[
            point_id
        ] = branch_path

        print(
            f"[RtG] Rama: "
            f"{branch.name} -> {point_id}"
        )

    # ========================================================
    # LOCALPOINTS
    # ========================================================

    local_points = build_local_points(
        points,
        model_center
    )

    # ========================================================
    # BRANCHES START
    # ========================================================

    branches_start = build_branches_start(
        branches,
        model_center
    )

    # ========================================================
    # JSON
    # ========================================================

    json_path = (
        model_directory /
        f"{model_name}.json"
    )

    json_data = load_existing_json(
        json_path,
        model_name
    )

    json_data = update_json(
        json_data,
        model_name,
        local_points,
        branches_json,
        branches_start
    )

    save_json(
        json_path,
        json_data
    )

    print(
        f"[RtG] JSON -> {json_path}"
    )

    print(
        f"[RtG] '{model_name}' terminado."
    )


# ============================================================
# ENCONTRAR MODELOS
# ============================================================

def find_model_roots():
    """
    Busca modelos en la escena.

    Un objeto raíz que contenga al menos un MESH descendiente
    se considera un modelo.

    No depende de una colección específica.
    """

    roots = []

    for obj in bpy.context.scene.objects:

        if obj.parent is not None:
            continue

        # ----------------------------------------------------
        # MESH raíz.
        # ----------------------------------------------------

        if obj.type == "MESH":

            roots.append(obj)

            continue

        # ----------------------------------------------------
        # Buscar MESH descendientes.
        # ----------------------------------------------------

        has_mesh = any(
            child.type == "MESH"
            and is_descendant(child, obj)
            for child in bpy.context.scene.objects
        )

        if has_mesh:

            roots.append(obj)

    return roots


# ============================================================
# MAIN
# ============================================================

def main():
    """
    Ejecuta todo el exportador.
    """

    print("")
    print("=" * 70)
    print("RtG-Format Blender Exporter")
    print("=" * 70)

    OUTPUT_ROOT.mkdir(
        parents=True,
        exist_ok=True
    )

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

    successful = 0

    for model in models:

        try:

            process_model(
                model
            )

            successful += 1

        except Exception as error:

            print("")
            print(
                f"[RtG] ERROR en '{model.name}':"
            )

            print(
                f"       {error}"
            )

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

