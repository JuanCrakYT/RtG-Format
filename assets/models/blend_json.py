"""
RtG-Format - Blender Model Exporter
===================================

Exportador automático de modelos de Road To Gramby's desde Blender.

ESTRUCTURA DE BLENDER
---------------------

Modelo sin ramas:

    Model
    └── start.Model

Modelo con ramas:

    Model
    ├── branch
    │   └── start.Model.branch
    └── branch
        ├── start.Model.branch
        └── Point_X


REGLAS
------

ROOT
----

El objeto raíz representa el modelo y es un MESH.

El propio ROOT es el MESH principal.

No existe un segundo MESH llamado Model dentro del ROOT.


BRANCHES
--------

Las ramas son MESH hijos directos del ROOT.

Un MESH hijo directo solamente se considera rama si posee
exactamente un Empty start con el nombre:

    start.Model.branch


Los MESH hijos que no tengan un start correspondiente se ignoran.

Esto permite tener copias temporales como:

    Model-clone

sin que sean exportadas como ramas.


START
-----

Los Empty de origen tienen nombres específicos.

Modelo sin ramas:

    start.Model

Modelo con ramas:

    start.Model.branch

Los start de las ramas representan el origen local de cada rama.


POINTS
------

Los puntos son Empty llamados:

    Point_1
    Point_2
    Point_3
    ...


Los puntos pertenecen a la rama dentro de cuya jerarquía aparecen.


CENTRADO
--------

El modelo completo se centra usando únicamente la geometría del
MESH principal.

La escena original de Blender NO se modifica.


JSON
----

Se conserva la información existente del JSON.

El script actualiza:

    LocalPoints
    Branches
    Branches Start
    Default Branch

Los Empty nunca se exportan.
"""

# ============================================================
# IMPORTACIONES
# ============================================================

import bpy
import json

from pathlib import Path

from mathutils import Vector


# ============================================================
# CONFIGURACIÓN
# ============================================================

SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_ROOT = SCRIPT_DIR
POINT_PREFIX = "Point_"

# ============================================================
# UTILIDADES
# ============================================================

def clean_number(value):
    value = float(value)

    if abs(value) < 1e-10:
        return 0

    value = round(value, 10)

    if value == int(value):
        return int(value)

    return value


def vector_to_list(vector):
    return [
        clean_number(vector.x),
        clean_number(vector.y),
        clean_number(vector.z)
    ]


def rotation_to_list(euler):
    return [
        clean_number(euler.x),
        clean_number(euler.y),
        clean_number(euler.z)
    ]


# ============================================================
# POINT_X
# ============================================================

def is_point(obj):
    if obj.type != "EMPTY":
        return False

    if not obj.name.startswith(POINT_PREFIX):
        return False

    point_id = obj.name[len(POINT_PREFIX):]

    return point_id.isdigit()


def get_point_id(obj):
    return obj.name[len(POINT_PREFIX):]


# ============================================================
# JERARQUÍA
# ============================================================

def is_descendant(obj, root):
    current = obj.parent

    while current is not None:

        if current == root:
            return True

        current = current.parent

    return False


def get_descendant_meshes(root):
    meshes = []

    for obj in bpy.context.scene.objects:

        if obj.type != "MESH":
            continue

        if is_descendant(obj, root):
            meshes.append(obj)

    return meshes


def get_descendant_points(root):
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


# ============================================================
# MODELO PRINCIPAL
# ============================================================

def find_main_mesh(model_root):

    if model_root.type != "MESH":
        raise RuntimeError(
            f"El root '{model_root.name}' "
            f"no es un MESH."
        )

    return model_root


# ============================================================
# RAMAS
# ============================================================

def find_branches(model_root):

    branches = []

    for obj in bpy.context.scene.objects:

        if obj.type != "MESH":
            continue

        # Las ramas deben ser hijos directos del ROOT.
        if obj.parent != model_root:
            continue

        expected_start = (
            f"start.{model_root.name}.{obj.name}"
        )

        starts = [
            candidate
            for candidate in bpy.context.scene.objects
            if (
                candidate.type == "EMPTY"
                and candidate.name == expected_start
                and is_descendant(candidate, obj)
            )
        ]

        # Exactamente un start = rama válida.
        if len(starts) == 1:
            branches.append(obj)

    return branches


# ============================================================
# START
# ============================================================

def find_start(empty_name, parent):
    """
    Busca exactamente un Empty con el nombre indicado dentro
    de la jerarquía de parent.
    """

    starts = []

    for obj in bpy.context.scene.objects:

        if obj.type != "EMPTY":
            continue

        if obj.name != empty_name:
            continue

        if is_descendant(obj, parent):
            starts.append(obj)

    if len(starts) == 0:
        raise RuntimeError(
            f"No se encontró '{empty_name}' "
            f"dentro de '{parent.name}'."
        )

    if len(starts) > 1:
        raise RuntimeError(
            f"Se encontraron múltiples objetos "
            f"'{empty_name}' dentro de '{parent.name}'."
        )

    return starts[0]


def find_main_start(model_root, main_mesh):
    """
    Modelo sin ramas:

        Model
        └── Model
            └── start.Model
    """

    expected_name = f"start.{model_root.name}"

    return find_start(
        expected_name,
        main_mesh
    )


def find_branch_start(model_root, branch):
    """
    Modelo con ramas:

        Model
        └── branch
            └── start.Model.branch
    """

    expected_name = (
        f"start.{model_root.name}.{branch.name}"
    )

    return find_start(
        expected_name,
        branch
    )


# ============================================================
# POINT DE RAMA
# ============================================================

def find_branch_point(branch):
    """
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

    depsgraph = (
        bpy.context.evaluated_depsgraph_get()
    )

    evaluated = obj.evaluated_get(
        depsgraph
    )

    mesh = evaluated.to_mesh(
        preserve_all_data_layers=True,
        depsgraph=depsgraph
    )

    return evaluated, mesh


# ============================================================
# CENTRO DEL MODELO
# ============================================================

def calculate_main_center(main_mesh):

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

def build_local_points(
    points,
    model_center
):

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

def build_branches_start(
    model_root,
    branches,
    model_center
):

    result = {}

    for branch in branches:

        start = find_branch_start(
            model_root,
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
# MALLA PRINCIPAL
# ============================================================

def create_main_export_mesh(
    main_mesh,
    model_center
):

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

        return mesh

    finally:

        evaluated.to_mesh_clear()


# ============================================================
# MALLA DE RAMA
# ============================================================

def create_branch_export_mesh(
    branch,
    start
):

    evaluated, source_mesh = evaluated_mesh(
        branch
    )

    try:

        start_inverse = (
            start.matrix_world.inverted()
        )

        world_matrix = (
            evaluated.matrix_world.copy()
        )

        transform = (
            start_inverse @ world_matrix
        )

        vertices = [
            transform @ vertex.co
            for vertex in source_mesh.vertices
        ]

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

        return mesh

    finally:

        evaluated.to_mesh_clear()


# ============================================================
# EXPORTAR OBJ TEMPORAL
# ============================================================

def export_temp_obj(
    mesh,
    filepath
):

    filepath = Path(filepath)

    filepath.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    temp_object = bpy.data.objects.new(
        "__RtGExportTemp__",
        mesh
    )

    bpy.context.scene.collection.objects.link(
        temp_object
    )

    bpy.context.view_layer.objects.active = (
        temp_object
    )

    temp_object.select_set(True)

    try:

        bpy.ops.wm.obj_export(
            filepath=str(filepath),
            export_materials=False,
            export_uv=False,
            export_normals=True,
            export_smooth_groups=False,
            export_object_groups=False,
            export_material_groups=False,
            export_triangulated=False
        )

    finally:

        temp_object.select_set(False)

        bpy.data.objects.remove(
            temp_object,
            do_unlink=True
        )

        bpy.data.meshes.remove(
            mesh
        )


# ============================================================
# JSON
# ============================================================

def load_existing_json(json_path):

    if json_path.exists():

        with json_path.open(
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        if (
            not isinstance(data, list)
            or len(data) == 0
            or not isinstance(data[0], dict)
        ):

            raise RuntimeError(
                f"El JSON '{json_path}' "
                f"no tiene el formato esperado."
            )

        return data

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
            "Name": json_path.stem,
            "Tooltip": "",
            "LocalPoints": {},
            "Branches": {},
            "Branches Start": {},
            "Default Branch": [
                f"./{json_path.stem}.obj"
            ]
        }
    ]


def update_json(
    data,
    model_name,
    local_points,
    branches_data,
    branches_start,
    default_branch
):

    entry = data[0]

    # --------------------------------------------------------
    # No tocar metadata existente.
    # --------------------------------------------------------

    entry["Name"] = model_name

    entry["LocalPoints"] = local_points

    entry["Branches"] = branches_data

    entry["Branches Start"] = branches_start

    entry["Default Branch"] = [
        default_branch
    ]

    return data


def save_json(
    json_path,
    data
):

    with json_path.open(
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )

        file.write("\n")


# ============================================================
# PROCESAR MODELO
# ============================================================

def process_model(model_root):

    model_name = model_root.name

    print()
    print("=" * 60)
    print(
        f"Procesando modelo: {model_name}"
    )
    print("=" * 60)

    # --------------------------------------------------------
    # Buscar MESH.
    # --------------------------------------------------------

    main_mesh = find_main_mesh(
        model_root
    )
    
    branches = find_branches(
        model_root
    )

    print(
        f"MESH principal: {main_mesh.name}"
    )

    print(
        f"Ramas encontradas: {len(branches)}"
    )

    # --------------------------------------------------------
    # Preparar carpetas.
    # --------------------------------------------------------

    model_dir = (
        OUTPUT_ROOT / model_name
    )

    split_dir = (
        model_dir / "split"
    )

    model_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    if branches:
        split_dir.mkdir(
            parents=True,
            exist_ok=True
        )

    # --------------------------------------------------------
    # Centro.
    # --------------------------------------------------------

    model_center = calculate_main_center(
        main_mesh
    )

    print(
        "Centro del modelo:",
        vector_to_list(model_center)
    )

    # --------------------------------------------------------
    # Points.
    # --------------------------------------------------------

    points = get_descendant_points(
        model_root
    )

    local_points = build_local_points(
        points,
        model_center
    )

    # --------------------------------------------------------
    # Caso SIN RAMAS.
    # --------------------------------------------------------

    if not branches:

        print(
            "Modelo sin ramas."
        )

        # Exigir start.Model
        main_start = find_main_start(
            model_root,
            main_mesh
        )

        print(
            f"Start principal: {main_start.name}"
        )

        branches_data = {}

        branches_start = {}

        # ----------------------------------------------------
        # Exportar modelo principal.
        # ----------------------------------------------------

        main_export_mesh = (
            create_main_export_mesh(
                main_mesh,
                model_center
            )
        )

        main_obj = (
            model_dir /
            f"{model_name}.obj"
        )

        export_temp_obj(
            main_export_mesh,
            main_obj
        )

    # --------------------------------------------------------
    # Caso CON RAMAS.
    # --------------------------------------------------------

    else:

        print(
            "Modelo con ramas."
        )

        branches_data = {}

        branches_start = (
            build_branches_start(
                model_root,
                branches,
                model_center
            )
        )

        # ----------------------------------------------------
        # Registrar cada rama.
        # ----------------------------------------------------

        for branch in branches:

            point_id = find_branch_point(
                branch
            )

            branch_path = (
                f"./split/{branch.name}.obj"
            )

            branches_data[
                point_id
            ] = branch_path

            print(
                f"Rama: {branch.name}"
            )

            print(
                f"  Point: {point_id}"
            )

            print(
                f"  Start: "
                f"start.{model_name}.{branch.name}"
            )

            # ------------------------------------------------
            # Exportar rama.
            # ------------------------------------------------

            start = find_branch_start(
                model_root,
                branch
            )

            branch_mesh = (
                create_branch_export_mesh(
                    branch,
                    start
                )
            )

            branch_obj = (
                split_dir /
                f"{branch.name}.obj"
            )

            export_temp_obj(
                branch_mesh,
                branch_obj
            )

        # ----------------------------------------------------
        # Exportar modelo principal.
        # ----------------------------------------------------

        main_export_mesh = (
            create_main_export_mesh(
                main_mesh,
                model_center
            )
        )

        main_obj = (
            model_dir /
            f"{model_name}.obj"
        )

        export_temp_obj(
            main_export_mesh,
            main_obj
        )

    # --------------------------------------------------------
    # JSON.
    # --------------------------------------------------------

    json_path = (
        model_dir /
        f"{model_name}.json"
    )

    data = load_existing_json(
        json_path
    )

    data = update_json(
        data,
        model_name,
        local_points,
        branches_data,
        branches_start,
        f"./{model_name}.obj"
    )

    save_json(
        json_path,
        data
    )

    print()
    print(
        f"Modelo exportado correctamente: "
        f"{model_dir}"
    )


# ============================================================
# DETECTAR ROOTS
# ============================================================

def find_model_roots():
    roots = []

    for obj in bpy.context.scene.objects:

        if obj.type != "MESH":
            continue

        if obj.parent is not None:
            continue

        roots.append(obj)

    return roots


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print("=" * 60)
    print("RtG-Format Blender Exporter")
    print("=" * 60)

    roots = find_model_roots()

    if not roots:

        print(
            "No se encontraron modelos."
        )

        return

    print(
        f"Modelos encontrados: {len(roots)}"
    )

    for model_root in roots:

        try:

            process_model(
                model_root
            )

        except Exception as error:

            print()
            print(
                f"ERROR en '{model_root.name}':"
            )

            print(
                error
            )

            print()

    print()
    print("=" * 60)
    print("Proceso terminado.")
    print("=" * 60)


# ============================================================
# EJECUTAR
# ============================================================

if __name__ == "__main__":
    main()