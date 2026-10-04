import json
import re

json_path = r"d:\Viet Hoa Game\translation_export\ScenarioMessageData_Chapter_1.json"
with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

for i, item in enumerate(data):
    m = re.search(r'"Id":(\d+)', item.get("id", ""))
    if m and int(m.group(1)) == 3:
        print(f"Found index {i}:")
        print("id:", item.get("id"))
        print("en:", item.get("english"))
        print("vn:", item.get("vietnamese"))
