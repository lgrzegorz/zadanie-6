import json
from pathlib import Path

DATA_DIR = Path(__file__).parent


def load(name):
    with open(DATA_DIR / name, encoding="utf-8") as f:
        return json.load(f)
