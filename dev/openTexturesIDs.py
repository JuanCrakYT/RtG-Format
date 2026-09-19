import json
import webbrowser
from pathlib import Path
import time

BASE_DIR = Path(__file__).resolve().parent

FILE = BASE_DIR / "textureIDs.json"

with FILE.open("r", encoding="utf-8") as f:
    texture_ids = json.load(f)

for texture_id in texture_ids:
    url = f"https://create.roblox.com/store/asset/{texture_id}"
    print(f"Abriendo: {url}")
    webbrowser.open_new_tab(url)
    time.sleep(0.3)

print(f"\nSe abrieron {len(texture_ids)} texturas.")