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
    └── output
        └── Point_2

REGLAS
------

1. El objeto raíz representa el modelo.
2. El MESH descendiente cuyo nombre coincide con el nombre del
   modelo raíz es el MESH completo.
3. Cualquier otro MESH descendiente directo/indirecto es una rama.
4. Los Empty llamados Point_X representan LocalPoints.
5. Un Point_X perteneciente a una rama debe estar dentro de esa
   rama en la jerarquía de Blender.
6. Una rama sin Point_X recibe "NaN".
7. Una rama con más de un Point_X provoca un error.
8. Los Empty nunca se exportan a OBJ.

CENTRADO
--------

El centro del modelo se calcula utilizando EXCLUSIVAMENTE la
geometría del MESH completo.

Esto es importante porque las ramas (input/output/etc.) son
copias/separaciones de partes del modelo completo y no deben
cambiar el centro por sí mismas.

La geometría se exporta centrada en:

    0, 0, 0

La escena original de Blender NO se modifica.

PUNTOS
------

Las posiciones de los puntos se calculan respecto al centro
geométrico del modelo completo.

Ejemplo:

    Point_2 world = (105, 20, -8)
    Center        = (100, 20, -10)

Resultado:

    Point_2 = (5, 0, 2)

RAMAS
-----

La asociación de una rama con un punto NO se realiza por distancia.

Se utiliza la jerarquía de Blender:

    output
    └── Point_2

significa:

    "2": "./split/output.obj"

Mientras:

    input

sin Point_X significa:

    "NaN": "./split/input.obj"

JSON
----

Si ya existe un JSON, el script lo conserva y únicamente actualiza
los campos que genera automáticamente:

    RtG-Preview.Default Branch
    LocalPoints
    Branches

De esta manera no se pierden Tooltip, Page, metadatos, etc.

SALIDA
------

Modelo completo:

    assets/models/Switch/Switch.obj

Ramas:

    assets/models/Switch/split/input.obj
    assets/models/Switch/split/output.obj

JSON:

    assets/models/Switch/Switch.json
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

# ------------------------------------------------------------
# Carpeta raíz donde están los modelos de RtG-Format.
#
# Cambia esta ruta si tu repositorio está en otra ubicación.
# ------------------------------------------------------------

OUTPUT_ROOT = Path(
    r"C:\Users\User\Desktop\Created programs\Mine\Reverse Engineering\Roblox\RtG Format\assets\models"
)


# ------------------------------------------------------------
# Prefijo utilizado para los Empty de puntos.
#
# Point_1
# Point_2
# Point_3
# ...
# ------------------------------------------------------------

POINT_PREFIX = "Point_"


# ------------------------------------------------------------
# Nombre del objeto principal.
#
# No se fuerza un nombre concreto:
# el script toma el nombre del objeto raíz.
# ------------------------------------------------------------


# ============================================================
# UTILIDADES NUMÉRICAS
# ============================================================

def clean_number(value):
    """
    Limpia números provenientes de Blender para evitar valores
    innecesariamente largos en el JSON.

    Ejemplos:

        1.000000000001 -> 1
        0.000000000001 -> 0
        2.500000000001 -> 2.5
    """

    value = float(value)

    # Evita ruido numérico cercano a cero.
    if abs(value) < 1e-10:
        return 0

    value = round(value, 10)

    if value == int(value):
        return int(value)

    return value


def vector_to_json(vector):
    """
    Convierte un Vector de Blender en una lista JSON limpia.
    """

    return [
        clean_number(vector.x),
        clean_number(vector.y),
        clean_number(vector.z)
    ]


# ============================================================
# OBJETOS Y JERARQUÍA
# ============================================================

def is_point(obj):
    """
    Devuelve True si el objeto es un Empty con nombre Point_X.

    Válidos:

        Point_1
        Point_2
        Point_10

    Inválidos:

        Point
        Point_A
        point_2
    """

    if obj.type != "EMPTY":
        return False

    if not obj.name.startswith(POINT_PREFIX):
        return False

    point_id = obj.name[len(POINT_PREFIX):]

    return point_id.isdigit()


def get_point_id(obj):
    """
    Extrae el ID numérico del nombre del punto.

        Point_2 -> "2"
        Point_10 -> "10"
    """

    return obj.name[len(POINT_PREFIX):]


def is_descendant(obj, root):
    """
    Comprueba si 'obj' está dentro de la jerarquía de 'root'.

    Ejemplo:

        Switch
        └── output
            └── Point_2

    Point_2 es descendiente de Switch.
    Point_2 también es descendiente de output.
    """

    current = obj.parent

    while current is not None:

        if current == root:
            return True

        current = current.parent

    return False


def get_direct_children(root):
    """
    Devuelve únicamente los hijos directos del objeto raíz.
    """

    return [
        obj
        for obj in bpy.context.scene.objects
        if obj.parent == root
    ]


# ============================================================
# DESCUBRIMIENTO DEL MODELO
# ============================================================

def find_meshes(model_root):
    """
    Encuentra todos los MESH descendientes del modelo.
    """

    meshes = []

    for obj in bpy.context.scene.objects:

        if obj.type != "MESH":
            continue

        if is_descendant(obj, model_root):

            meshes.append(obj)

    return meshes


def find_main_mesh(model_root, meshes):
    """
    Encuentra el MESH completo.

    El MESH completo debe tener exactamente el mismo nombre
    que el objeto raíz.

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
            f"Hay múltiples MESH llamados "
            f"'{model_root.name}'."
        )

    return matches[0]


# ============================================================
# PUNTOS
# ============================================================

def find_model_points(model_root):
    """
    Encuentra todos los Point_X pertenecientes al modelo.

    Un punto puede estar:

        directamente bajo una rama,
        bajo un objeto intermedio,
        etc.

    Siempre que sea descendiente del modelo raíz.
    """

    points = []

    for obj in bpy.context.scene.objects:

        if not is_point(obj):
            continue

        if is_descendant(obj, model_root):

            points.append(obj)

    points.sort(
        key=lambda obj: int(get_point_id(obj))
    )

    return points


def find_branch_points(branch):
    """
    Encuentra los Point_X pertenecientes específicamente a una rama.

    Ejemplo:

        output
        └── Point_2

    devuelve:

        [Point_2]

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

    return points


# ============================================================
# RAMAS
# ============================================================

def find_branches(model_root, main_mesh, meshes):
    """
    Todo MESH distinto del MESH completo se considera una rama.

    Ejemplo:

        Switch
        ├── Switch  <- principal
        ├── input   <- rama
        └── output  <- rama

    """

    return [
        mesh
        for mesh in meshes
        if mesh != main_mesh
    ]


def get_branch_point(branch):
    """
    Determina qué Point_X pertenece a una rama.

    Reglas:

    - 0 puntos -> "NaN"
    - 1 punto  -> usar ese ID
    - >1 puntos -> error

    No se utiliza distancia.

    La jerarquía de Blender determina la asociación.
    """

    points = find_branch_points(branch)

    if len(points) == 0:

        return "NaN"

    if len(points) > 1:

        point_names = ", ".join(
            point.name
            for point in points
        )

        raise RuntimeError(
            f"La rama '{branch.name}' tiene múltiples "
            f"Point_X: {point_names}. "
            f"Una rama debe tener como máximo un punto."
        )

    return get_point_id(points[0])


# ============================================================
# GEOMETRÍA Y CENTRADO
# ============================================================

def get_evaluated_mesh_data(obj):
    """
    Obtiene la versión evaluada de la malla.

    Esto permite que los modificadores de Blender sean incluidos
    en la geometría utilizada para calcular el centro y exportar.

    Devuelve:

        evaluated_object
        mesh
        world_matrix
    """

    depsgraph = bpy.context.evaluated_depsgraph_get()

    evaluated_object = obj.evaluated_get(
        depsgraph
    )

    mesh = evaluated_object.to_mesh(
        preserve_all_data_layers=True,
        depsgraph=depsgraph
    )

    world_matrix = (
        evaluated_object.matrix_world.copy()
    )

    return (
        evaluated_object,
        mesh,
        world_matrix
    )


def get_evaluated_world_vertices(obj):
    """
    Devuelve todos los vértices de un objeto evaluado en
    coordenadas mundiales.
    """

    (
        evaluated_object,
        mesh,
        world_matrix
    ) = get_evaluated_mesh_data(obj)

    try:

        for vertex in mesh.vertices:

            yield (
                world_matrix @ vertex.co
            )

    finally:

        evaluated_object.to_mesh_clear()


def calculate_main_mesh_center(main_mesh):
    """
    Calcula el centro del bounding box de TODO el MESH principal.

    IMPORTANTE:

    El centro se calcula solamente con el modelo completo.

    No utilizamos:

        object.location

    ni:

        ramas

    porque las ramas son representaciones separadas de partes
    del mismo modelo.
    """

    vertices = list(
        get_evaluated_world_vertices(
            main_mesh
        )
    )

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
    Genera LocalPoints usando la posición de cada Empty respecto
    al centro del modelo.

    La rotación se obtiene de la matriz mundial del Empty.

    Estructura:

        "2": [
            [x, y, z],
            [rx, ry, rz]
        ]
    """

    local_points = {}

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

        if point_id in local_points:

            raise RuntimeError(
                f"El ID de punto '{point_id}' "
                f"aparece más de una vez."
            )

        local_points[point_id] = [

            vector_to_json(
                local_position
            ),

            vector_to_json(
                rotation
            )
        ]

    return local_points


# ============================================================
# OBJ TEMPORAL
# ============================================================

def create_export_object(source_obj, model_center):
    """
    Crea una copia temporal de la geometría para exportación.

    El objeto original NO se modifica.

    Flujo:

        Blender mesh
            ↓
        aplicar evaluación/modificadores
            ↓
        convertir vértices a world space
            ↓
        restar model_center
            ↓
        objeto temporal con:
            Location = 0,0,0
            Rotation = 0,0,0
            Scale    = 1,1,1

    Así el OBJ final no tiene offset.
    """

    (
        evaluated_object,
        source_mesh,
        world_matrix
    ) = get_evaluated_mesh_data(
        source_obj
    )

    try:

        export_mesh = bpy.data.meshes.new(
            f"__RtGExportMesh_{source_obj.name}"
        )

        export_object = bpy.data.objects.new(
            f"__RtGExport_{source_obj.name}",
            export_mesh
        )

        bpy.context.scene.collection.objects.link(
            export_object
        )

        # ----------------------------------------------------
        # Copiar geometría.
        # ----------------------------------------------------

        export_mesh.from_pydata(
            [
                (
                    world_matrix @ vertex.co
                    - model_center
                )
                for vertex in source_mesh.vertices
            ],
            [
                tuple(
                    polygon.vertices
                )
                for polygon in source_mesh.polygons
            ],
            [
                [
                    loop.vertex_index
                    for loop in polygon.loop_indices
                ]
                for polygon in source_mesh.polygons
            ]
        )

        export_mesh.update()

        # ----------------------------------------------------
        # Resetear completamente la transformación.
        #
        # La transformación ya está horneada en los vértices.
        # ----------------------------------------------------

        export_object.location = (
            0.0,
            0.0,
            0.0
        )

        export_object.rotation_euler = (
            0.0,
            0.0,
            0.0
        )

        export_object.scale = (
            1.0,
            1.0,
            1.0
        )

        return export_object

    finally:

        evaluated_object.to_mesh_clear()


# ============================================================
# EXPORTAR OBJ
# ============================================================

def export_obj(source_obj, output_path, model_center):
    """
    Exporta un objeto MESH como OBJ sin modificar su versión
    original de Blender.
    """

    export_object = create_export_object(
        source_obj,
        model_center
    )

    # --------------------------------------------------------
    # Crear carpeta de destino.
    # --------------------------------------------------------

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    # --------------------------------------------------------
    # Guardar estado de selección.
    # --------------------------------------------------------

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

        export_object.select_set(
            True
        )

        bpy.context.view_layer.objects.active = (
            export_object
        )

        # ----------------------------------------------------
        # Exportación OBJ.
        # ----------------------------------------------------

        bpy.ops.wm.obj_export(
            filepath=str(output_path),
            export_selected_objects=True,
            export_materials=True,
            export_uv=True
        )

    finally:

        # ----------------------------------------------------
        # Eliminar temporal.
        # ----------------------------------------------------

        mesh = export_object.data

        bpy.data.objects.remove(
            export_object,
            do_unlink=True
        )

        if mesh.users == 0:

            bpy.data.meshes.remove(
                mesh
            )

        # ----------------------------------------------------
        # Restaurar selección.
        # ----------------------------------------------------

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

    Si no existe, crea la estructura mínima.

    De esta manera no destruimos información manual como:

        Tooltip
        Page
        Description
        RtG-Format Data
        etc.
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
                        },

                        "Default Branch":
                            f"./{model_name}.obj"
                    },

                    "Page": {}
                },

                "Name": model_name,

                "Description": "",

                "LocalPoints": {},

                "Branches": {}
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
            f"no contiene un array válido."
        )

    if not isinstance(data[0], dict):

        raise RuntimeError(
            f"El JSON '{json_path}' "
            f"tiene una estructura inválida."
        )

    return data


def update_json(data, model_name, local_points, branches):
    """
    Actualiza únicamente los campos generados por Blender.
    """

    model_data = data[0]

    # --------------------------------------------------------
    # Asegurar RtG-Format.
    # --------------------------------------------------------

    rtg_format = model_data.setdefault(
        "RtG-Format",
        {}
    )

    # --------------------------------------------------------
    # Asegurar RtG-Preview.
    # --------------------------------------------------------

    preview = rtg_format.setdefault(
        "RtG-Preview",
        {}
    )

    size = preview.setdefault(
        "Size",
        {}
    )

    # No cambiamos los tamaños existentes.
    if "default" not in size:

        size["default"] = 1

    # --------------------------------------------------------
    # El modelo completo siempre es Default Branch.
    # --------------------------------------------------------

    preview["Default Branch"] = (
        f"./{model_name}.obj"
    )

    # --------------------------------------------------------
    # Actualizar Name solo si falta.
    # --------------------------------------------------------

    if not model_data.get("Name"):

        model_data["Name"] = model_name

    # --------------------------------------------------------
    # Estos sí son generados completamente por el script.
    # --------------------------------------------------------

    model_data["LocalPoints"] = (
        local_points
    )

    model_data["Branches"] = (
        branches
    )

    return data


def save_json(json_path, data):
    """
    Guarda el JSON con indentación legible.
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
# PROCESAR UN MODELO
# ============================================================

def process_model(model_root):
    """
    Procesa un modelo completo.

    Ejemplo:

        Switch
        ├── Switch
        ├── input
        └── output
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
    # Buscar todos los MESH.
    # --------------------------------------------------------

    meshes = find_meshes(
        model_root
    )

    if not meshes:

        raise RuntimeError(
            f"El modelo '{model_name}' "
            f"no tiene ningún MESH descendiente."
        )

    # --------------------------------------------------------
    # Encontrar MESH completo.
    # --------------------------------------------------------

    main_mesh = find_main_mesh(
        model_root,
        meshes
    )

    # --------------------------------------------------------
    # Encontrar ramas.
    # --------------------------------------------------------

    branches = find_branches(
        model_root,
        main_mesh,
        meshes
    )

    # --------------------------------------------------------
    # Encontrar todos los puntos del modelo.
    # --------------------------------------------------------

    points = find_model_points(
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
    # Calcular centro usando SOLAMENTE la geometría completa.
    # --------------------------------------------------------

    model_center = calculate_main_mesh_center(
        main_mesh
    )

    print(
        "[RtG] Centro:"
        f" {tuple(clean_number(v) for v in model_center)}"
    )

    # --------------------------------------------------------
    # Crear carpetas.
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

    export_obj(
        main_mesh,
        main_output,
        model_center
    )

    print(
        f"[RtG] Exportado: {main_output}"
    )

    # --------------------------------------------------------
    # Construir Branches.
    # --------------------------------------------------------

    branches_json = {}

    for branch in branches:

        point_id = get_branch_point(
            branch
        )

        filename = (
            f"{branch.name}.obj"
        )

        branch_output = (
            split_directory /
            filename
        )

        # ----------------------------------------------------
        # Exportar rama usando EL MISMO centro del modelo.
        # ----------------------------------------------------

        export_obj(
            branch,
            branch_output,
            model_center
        )

        relative_path = (
            f"./split/{filename}"
        )

        if point_id in branches_json:

            raise RuntimeError(
                f"El ID '{point_id}' "
                f"ya está asignado a otra rama."
            )

        branches_json[
            point_id
        ] = relative_path

        print(
            f"[RtG] Rama: "
            f"{branch.name} -> "
            f"{point_id}"
        )

    # --------------------------------------------------------
    # Construir LocalPoints.
    # --------------------------------------------------------

    local_points = build_local_points(
        points,
        model_center
    )

    # --------------------------------------------------------
    # Cargar JSON existente.
    # --------------------------------------------------------

    json_path = (
        model_directory /
        f"{model_name}.json"
    )

    json_data = load_existing_json(
        json_path,
        model_name
    )

    # --------------------------------------------------------
    # Actualizar únicamente los datos automáticos.
    # --------------------------------------------------------

    json_data = update_json(
        json_data,
        model_name,
        local_points,
        branches_json
    )

    # --------------------------------------------------------
    # Guardar.
    # --------------------------------------------------------

    save_json(
        json_path,
        json_data
    )

    print(
        f"[RtG] JSON: {json_path}"
    )

    print(
        f"[RtG] Modelo '{model_name}' terminado."
    )


# ============================================================
# DETECTAR MODELOS
# ============================================================

def find_model_roots():
    """
    Busca objetos raíz que tengan MESH descendientes.

    Un objeto raíz es simplemente un objeto sin parent.

    Esto permite trabajar con:

        Switch
        Tooth
        Part
        etc.

    dentro de la misma escena.
    """

    roots = []

    for obj in bpy.context.scene.objects:

        if obj.parent is not None:
            continue

        # ----------------------------------------------------
        # Si el propio objeto es MESH, puede ser un modelo.
        # ----------------------------------------------------

        if obj.type == "MESH":

            roots.append(obj)

            continue

        # ----------------------------------------------------
        # Buscar descendientes MESH.
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
    Ejecuta el exportador completo.
    """

    print("")
    print("=" * 70)
    print("RtG-Format Blender Exporter")
    print("=" * 70)

    # --------------------------------------------------------
    # Crear carpeta raíz si no existe.
    # --------------------------------------------------------

    OUTPUT_ROOT.mkdir(
        parents=True,
        exist_ok=True
    )

    # --------------------------------------------------------
    # Encontrar modelos.
    # --------------------------------------------------------

    models = find_model_roots()

    if not models:

        print(
            "[RtG] ERROR: "
            "No se encontraron modelos."
        )

        return

    print(
        f"[RtG] Modelos encontrados: "
        f"{len(models)}"
    )

    successful = 0

    # --------------------------------------------------------
    # Procesar uno por uno.
    # --------------------------------------------------------

    for model in models:

        try:

            process_model(
                model
            )

            successful += 1

        except Exception as error:

            print("")
            print(
                f"[RtG] ERROR en "
                f"'{model.name}':"
            )

            print(
                f"       {error}"
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
