from pathlib import Path
import json

localizationFile = Path('localization.json')

with open(localizationFile, encoding="UTF-8") as f:
    loc = json.load(f)