import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

FILE = BASE_DIR / "PolaroidPhoto_Organized.json"

OUTPUT = FILE.parent / "textureIDs.json"

with FILE.open("r", encoding="utf-8") as f:
    data = json.load(f)

texture_ids = set()

def scan(value):
    if isinstance(value, dict):
        for key, child in value.items():
            if key.lower() in ("textureid", "textureID".lower()):
                if isinstance(child, str) and child.startswith("rbxassetid://"):
                    texture_ids.add(child.removeprefix("rbxassetid://"))

            scan(child)

    elif isinstance(value, list):
        for child in value:
            scan(child)

scan(data)

texture_ids = sorted(texture_ids, key=int)

with OUTPUT.open("w", encoding="utf-8") as f:
    json.dump(texture_ids, f, indent=4)

print(f"Encontradas {len(texture_ids)} texturas:")
for texture_id in texture_ids:
    print(texture_id)

print(f"\nGuardado en: {OUTPUT}")