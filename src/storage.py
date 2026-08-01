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
            cleaned_tasks = []
            for item in data:
                if isinstance(item, dict):
                    cleaned_tasks.append(
                        {
                            "text": str(item.get("text", "")).strip(),
                            "completed": bool(item.get("completed", False)),
                        }
                    )
            return cleaned_tasks
    except Exception as e:
        print(f"Error loading tasks: {e}")

    return []


def save_tasks(tasks):
    """Save tasks to disk."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    cleaned_tasks = []
    for item in tasks:
        if isinstance(item, dict):
            cleaned_tasks.append(
                {
                    "text": str(item.get("text", "")).strip(),
                    "completed": bool(item.get("completed", False)),
                }
            )

    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(cleaned_tasks, f, indent=4)
