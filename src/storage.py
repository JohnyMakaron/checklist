import json
import os
from pathlib import Path

LEGACY_DATA_DIR = Path(__file__).parent.parent / "data"
LEGACY_DATA_FILE = LEGACY_DATA_DIR / "tasks.json"


def _get_xdg_data_home():
    xdg_data_home = os.environ.get("XDG_DATA_HOME")
    if xdg_data_home:
        return Path(xdg_data_home).expanduser()

    return Path.home() / ".local" / "share"


def _get_data_dir():
    return _get_xdg_data_home() / "Checklist"


def _get_data_file():
    data_dir = _get_data_dir()
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir / "tasks.json"


def _migrate_legacy_tasks_if_needed():
    data_file = _get_data_file()
    if data_file.exists():
        return

    if not LEGACY_DATA_FILE.exists():
        return

    try:
        with LEGACY_DATA_FILE.open("r", encoding="utf-8") as f:
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

            with data_file.open("w", encoding="utf-8") as f:
                json.dump(cleaned_tasks, f, indent=4)
    except Exception as e:
        print(f"Error migrating legacy tasks: {e}")


def load_tasks():
    """Load tasks from disk."""
    data_file = _get_data_file()
    _migrate_legacy_tasks_if_needed()

    if not data_file.exists():
        return []

    try:
        with data_file.open("r", encoding="utf-8") as f:
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
    data_file = _get_data_file()

    cleaned_tasks = []
    for item in tasks:
        if isinstance(item, dict):
            cleaned_tasks.append(
                {
                    "text": str(item.get("text", "")).strip(),
                    "completed": bool(item.get("completed", False)),
                }
            )

    with data_file.open("w", encoding="utf-8") as f:
        json.dump(cleaned_tasks, f, indent=4)
