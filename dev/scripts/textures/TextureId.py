import json
from pathlib import Path


# dev/scripts/textures/
BASE_DIR = Path(__file__).resolve().parent

# dev/PolaroidPhoto_Organized.json
INPUT_FILE = BASE_DIR.parent.parent / "PolaroidPhoto_Organized.json"

# dev/scripts/textures/textureIDs.json
OUTPUT_FILE = BASE_DIR / "textureIDs.json"


def scan(value, texture_ids):
    """Recursively search for TextureID properties."""
    if isinstance(value, dict):
        for key, child in value.items():
            if key.lower() == "textureid":
                if (
                    isinstance(child, str)
                    and child.startswith("rbxassetid://")
                ):
                    texture_ids.add(
                        child.removeprefix("rbxassetid://")
                    )

            scan(child, texture_ids)

    elif isinstance(value, list):
        for child in value:
            scan(child, texture_ids)


def main():
    if not INPUT_FILE.exists():
        print(f"ERROR: No se encontró:")
        print(INPUT_FILE)
        return

    with INPUT_FILE.open("r", encoding="utf-8") as f:
        data = json.load(f)

    texture_ids = set()
    scan(data, texture_ids)

    texture_ids = sorted(texture_ids, key=int)

    with OUTPUT_FILE.open("w", encoding="utf-8") as f:
        json.dump(texture_ids, f, indent=4)

    print(f"Encontradas {len(texture_ids)} texturas:")

    for texture_id in texture_ids:
        print(texture_id)

    print(f"\nGuardado en:")
    print(OUTPUT_FILE)


if __name__ == "__main__":
    main()
