import json
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
DATA_FILE = DATA_DIR / "tasks.json"


def load_tasks():
    """Load tasks from disk."""
    if not DATA_FILE.exists():
        return []

    try:
        with DATA_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)

            if isinstance(data, list):
                return data

    except Exception as e:
        print(f"Error loading tasks: {e}")

    return []


def save_tasks(tasks):
    """Save tasks to disk."""
    DATA_DIR.mkdir(exist_ok=True)

    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=4)
