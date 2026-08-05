import json
from pathlib import Path

PREFERENCES_DIR = Path(__file__).resolve().parent.parent / "data"
PREFERENCES_FILE = PREFERENCES_DIR / "preferences.json"
DEFAULT_PREFERENCES = {
    "window_opacity": 100,
}


def _get_preferences_dir():
    PREFERENCES_DIR.mkdir(parents=True, exist_ok=True)
    return PREFERENCES_DIR


def _coerce_opacity(value):
    try:
        numeric_value = float(value)
    except (TypeError, ValueError):
        return DEFAULT_PREFERENCES["window_opacity"]

    if 0.3 <= numeric_value <= 1.0:
        percentage = int(round(numeric_value * 100))
    else:
        percentage = int(round(numeric_value))

    return max(30, min(100, percentage))


def _sanitize_preferences(data):
    if not isinstance(data, dict):
        return dict(DEFAULT_PREFERENCES)

    cleaned = dict(DEFAULT_PREFERENCES)
    opacity = data.get("window_opacity", DEFAULT_PREFERENCES["window_opacity"])
    cleaned["window_opacity"] = _coerce_opacity(opacity)
    return cleaned


def load_preferences():
    """Load application preferences from disk."""
    _get_preferences_dir()

    if not PREFERENCES_FILE.exists():
        return dict(DEFAULT_PREFERENCES)

    try:
        with PREFERENCES_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return dict(DEFAULT_PREFERENCES)

    sanitized = _sanitize_preferences(data)

    if sanitized != data:
        save_preferences(sanitized)

    return sanitized


def save_preferences(preferences):
    """Persist application preferences to disk."""
    _get_preferences_dir()
    cleaned = _sanitize_preferences(preferences)

    with PREFERENCES_FILE.open("w", encoding="utf-8") as f:
        json.dump(cleaned, f, indent=4)

    return cleaned
