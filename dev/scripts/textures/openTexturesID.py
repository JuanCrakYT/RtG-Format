import json
import subprocess
import sys
import time
import webbrowser
from pathlib import Path


# dev/scripts/textures/
BASE_DIR = Path(__file__).resolve().parent

# Scripts y archivos
TEXTURE_SCRIPT = BASE_DIR / "TextureId.py"
TEXTURE_IDS_FILE = BASE_DIR / "textureIDs.json"


def update_texture_ids():
    """Ejecuta TextureId.py para actualizar textureIDs.json."""
    print("Actualizando Texture IDs...\n")

    result = subprocess.run(
        [sys.executable, str(TEXTURE_SCRIPT)],
        cwd=BASE_DIR,
    )

    if result.returncode != 0:
        print("\nERROR: TextureId.py terminó con un error.")
        return False

    return True


def open_textures():
    """Abre todas las texturas encontradas en Roblox Creator."""
    if not TEXTURE_IDS_FILE.exists():
        print("ERROR: No se encontró textureIDs.json.")
        return

    with TEXTURE_IDS_FILE.open("r", encoding="utf-8") as f:
        texture_ids = json.load(f)

    for texture_id in texture_ids:
        url = f"https://create.roblox.com/store/asset/{texture_id}"

        print(f"Abriendo: {url}")
        webbrowser.open_new_tab(url)

        time.sleep(0.3)

    print(f"\nSe abrieron {len(texture_ids)} texturas.")


def main():
    if not update_texture_ids():
        return

    print("\n" + "=" * 40)
    print("Abriendo texturas...")
    print("=" * 40 + "\n")

    open_textures()


if __name__ == "__main__":
    main()
