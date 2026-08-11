import json
import tempfile
import unittest
from pathlib import Path

from src import settings


class SettingsTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.original_preferences_dir = settings.PREFERENCES_DIR
        self.original_preferences_file = settings.PREFERENCES_FILE
        settings.PREFERENCES_DIR = Path(self.temp_dir.name)
        settings.PREFERENCES_FILE = settings.PREFERENCES_DIR / "preferences.json"

    def tearDown(self):
        settings.PREFERENCES_DIR = self.original_preferences_dir
        settings.PREFERENCES_FILE = self.original_preferences_file
        self.temp_dir.cleanup()

    def test_window_opacity_defaults_to_full(self):
        preferences = settings.load_preferences()
        self.assertEqual(preferences["window_opacity"], 100)
        self.assertEqual(preferences["font_color"], "Default")

    def test_save_preferences_isolated_from_tasks(self):
        saved = settings.save_preferences({"window_opacity": 70})
        preferences = settings.load_preferences()

        self.assertEqual(saved["window_opacity"], 70)
        self.assertEqual(preferences["window_opacity"], 70)
        self.assertEqual(preferences["font_color"], "Default")

    def test_load_preferences_merges_defaults_and_sanitizes(self):
        settings.PREFERENCES_FILE.write_text(
            json.dumps({"window_opacity": 0, "font_color": "Purple"}),
            encoding="utf-8",
        )

        preferences = settings.load_preferences()

        self.assertEqual(preferences["window_opacity"], 30)
        self.assertEqual(preferences["font_color"], "Default")

    def test_save_preferences_merges_existing_preferences_without_reading_via_load(self):
        settings.PREFERENCES_FILE.write_text(
            json.dumps({"window_opacity": 50, "font_color": "Blue"}),
            encoding="utf-8",
        )

        saved = settings.save_preferences({"window_opacity": 70})
        self.assertEqual(saved["window_opacity"], 70)
        self.assertEqual(saved["font_color"], "Blue")

        contents = json.loads(settings.PREFERENCES_FILE.read_text(encoding="utf-8"))
        self.assertEqual(contents["window_opacity"], 70)
        self.assertEqual(contents["font_color"], "Blue")

    def test_save_preferences_sanitizes_updates(self):
        saved = settings.save_preferences(
            {"window_opacity": 150, "font_color": "Purple"}
        )
        self.assertEqual(saved["window_opacity"], 100)
        self.assertEqual(saved["font_color"], "Default")


if __name__ == "__main__":
    unittest.main()
