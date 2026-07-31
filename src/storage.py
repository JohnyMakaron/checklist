import json
import os

DATA_FILE = os.path.join(
    os.path.dirname(__file__),
    "..",
    "data",
    "tasks.json",
)


def load_tasks():
    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except Exception:
        return []


def save_tasks(tasks):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)

    with open(DATA_FILE, "w") as file:
        json.dump(tasks, file, indent=4)
