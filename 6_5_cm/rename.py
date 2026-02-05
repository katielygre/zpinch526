from pathlib import Path
import re

folder = Path(".")

pattern = re.compile(r'^(\d+)(?:_(\d+))?_kV_(.+)$')

for file in folder.glob("*.csv"):
    m = pattern.match(file.name)
    if not m:
        print("SKIP:", file.name)
        continue

    whole = m.group(1)
    frac = m.group(2) or "0"
    rest = m.group(3)

    new_name = f"{whole}_{frac}_kV_{rest}"

    # print(file.name, "→", new_name)
    file.rename(file.with_name(new_name))