# generate_env_json.py
import json

with open("credentials.json", "r", encoding="utf-8") as f:
    data = json.load(f)

converted = json.dumps(data).replace("\n", "\\n")
print(converted)