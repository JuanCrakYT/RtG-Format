import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent

INPUT_FILE = BASE_DIR / "PolaroidPhoto.json"
OUTPUT_FILE = BASE_DIR / "PolaroidPhoto_Organized.json"


def organize_scene_object(object_id, object_data):
    """
    Organiza un objeto de escena sin alterar sus datos.
    """

    organized = {
        "objectId": object_data.get("objectId", object_id),
        "className": object_data.get("className"),
        "props": object_data.get("props", {}),
        "children": object_data.get("children", {}),
    }

    return organized


def organize_photo(photo):
    """
    Organiza una PolaroidPhoto manteniendo la estructura original.
    """

    if not isinstance(photo, list) or len(photo) != 3:
        raise ValueError("La estructura raíz no parece ser una tupla RtG válida.")

    object_type = photo[0]
    connections = photo[1]
    properties = photo[2]

    if object_type != "PolaroidPhoto":
        raise ValueError(
            f"Se esperaba PolaroidPhoto, pero se encontró: {object_type}"
        )

    photo_data = properties.get("PhotoData", {})

    scene_new_objects = photo_data.get("sceneNewObjects", {})
    organized_objects = {}

    for object_id, object_data in scene_new_objects.items():
        organized_objects[str(object_id)] = organize_scene_object(
            object_id,
            object_data
        )

    organized_photo = [
        object_type,
        connections,
        {
            "Phrase": properties.get("Phrase", ""),
            "PhotoData": {
                "cameraCF": photo_data.get("cameraCF"),
                "sceneCullObjects": photo_data.get(
                    "sceneCullObjects",
                    []
                ),
                "sceneNewObjects": organized_objects,
                "sceneUpdateObjects": photo_data.get(
                    "sceneUpdateObjects",
                    []
                )
            }
        }
    ]

    return organized_photo


def main():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"No se encontró:\n{INPUT_FILE}"
        )

    with INPUT_FILE.open("r", encoding="utf-8") as file:
        data = json.load(file)

    # RtG normalmente contiene un array de objetos.
    if not isinstance(data, list):
        raise ValueError("El archivo raíz no contiene un array.")

    organized_data = []

    for index, photo in enumerate(data, start=1):
        try:
            organized_data.append(organize_photo(photo))
        except Exception as error:
            raise ValueError(
                f"Error organizando la Polaroid #{index}: {error}"
            ) from error

    with OUTPUT_FILE.open(
        "w",
        encoding="utf-8",
        newline="\n"
    ) as file:
        json.dump(
            organized_data,
            file,
            ensure_ascii=False,
            indent=4
        )

        file.write("\n")

    print("PolaroidPhoto organizada correctamente.")
    print(f"Entrada:  {INPUT_FILE}")
    print(f"Salida:   {OUTPUT_FILE}")


if __name__ == "__main__":
    main()