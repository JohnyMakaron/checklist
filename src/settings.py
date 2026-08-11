import json
from pathlib import Path

PREFERENCES_DIR = Path(__file__).resolve().parent.parent / "data"
PREFERENCES_FILE = PREFERENCES_DIR / "preferences.json"
FONT_COLOR_OPTIONS = [
    "Default",
    "White",
    "Gray",
    "Black",
    "Blue",
    "Green",
    "Red",
]
DEFAULT_PREFERENCES = {
    "window_opacity": 100,
    "font_color": "Default",
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


def _sanitize_font_color(value):
    if not isinstance(value, str):
        return DEFAULT_PREFERENCES["font_color"]
    if value not in FONT_COLOR_OPTIONS:
        return DEFAULT_PREFERENCES["font_color"]
    return value


def _sanitize_preferences(data):
    if not isinstance(data, dict):
        return dict(DEFAULT_PREFERENCES)

    cleaned = dict(DEFAULT_PREFERENCES)
    opacity = data.get("window_opacity", DEFAULT_PREFERENCES["window_opacity"])
    cleaned["window_opacity"] = _coerce_opacity(opacity)
    font_color = data.get("font_color", DEFAULT_PREFERENCES["font_color"])
    cleaned["font_color"] = _sanitize_font_color(font_color)
    return cleaned


def _read_raw_preferences():
    _get_preferences_dir()

    if not PREFERENCES_FILE.exists():
        return {}

    try:
        with PREFERENCES_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return {}

    return data


def load_preferences():
    """Load application preferences from disk."""
    data = _read_raw_preferences()
    return _sanitize_preferences(data)


def save_preferences(preferences):
    """Persist application preferences to disk."""
    _get_preferences_dir()
    existing = _read_raw_preferences()
    merged = dict(existing)
    merged.update(preferences)
    cleaned = _sanitize_preferences(merged)

    with PREFERENCES_FILE.open("w", encoding="utf-8") as f:
        json.dump(cleaned, f, indent=4)

    return cleaned
