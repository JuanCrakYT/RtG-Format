import json
import time
import webbrowser
from pathlib import Path


# dev/scripts/
BASE_DIR = Path(__file__).resolve().parent

# dev/scripts/assets/AssetID.json
ASSET_IDS_FILE = BASE_DIR / "assets" / "AssetID.json"


def main():
    if not ASSET_IDS_FILE.exists():
        print("ERROR: No se encontró:")
        print(ASSET_IDS_FILE)
        return

    with ASSET_IDS_FILE.open("r", encoding="utf-8") as f:
        asset_ids = json.load(f)

    for asset_id in asset_ids:
        url = f"https://create.roblox.com/store/asset/{asset_id}"

        print(f"Abriendo: {url}")
        webbrowser.open_new_tab(url)

        time.sleep(0.3)

    print(f"\nSe abrieron {len(asset_ids)} assets.")


if __name__ == "__main__":
    main()
