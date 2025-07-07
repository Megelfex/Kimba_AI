
import json

def load_identity(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
