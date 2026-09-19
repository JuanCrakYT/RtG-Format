import json
import webbrowser
from pathlib import Path
import time

BASE_DIR = Path(__file__).resolve().parent

FILE = BASE_DIR / "AssetID.json"

with FILE.open("r", encoding="utf-8") as f:
    asset_ids = json.load(f)

for asset_id in asset_ids:
    url = f"https://create.roblox.com/store/asset/{asset_id}"
    print(f"Abriendo: {url}")
    webbrowser.open_new_tab(url)
    time.sleep(0.3)

print(f"\nSe abrieron {len(asset_ids)} assets.")