import os
from pathlib import Path

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Adw, Gtk

try:
    from .settings import load_preferences, save_preferences
except ImportError:
    from settings import load_preferences, save_preferences


class PreferencesWindow(Adw.PreferencesWindow):
    def __init__(self, app, window=None):
        super().__init__(application=app)
        self.set_title("Preferences")
        self.set_default_size(460, 520)
        self.window = window

        page = Adw.PreferencesPage()
        page.set_name("general")
        page.set_title("General")

        appearance_group = Adw.PreferencesGroup()
        appearance_group.set_title("Appearance")

        preferences = load_preferences()

        self.opacity_row = Adw.ActionRow()
        self.opacity_row.set_title("Window Opacity")

        self.current_opacity = int(preferences["window_opacity"])

        self.opacity_value_label = Gtk.Label(label=f"{self.current_opacity}%")
        self.opacity_value_label.set_margin_start(6)
        self.opacity_value_label.set_margin_end(6)
        self.opacity_value_label.set_halign(Gtk.Align.CENTER)

        self.opacity_controls = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        self.opacity_controls.set_halign(Gtk.Align.END)

        decrement_button = Gtk.Button(label="-")
        decrement_button.connect("clicked", self.on_opacity_decrement)
        increment_button = Gtk.Button(label="+")
        increment_button.connect("clicked", self.on_opacity_increment)

        self.opacity_controls.append(decrement_button)
        self.opacity_controls.append(self.opacity_value_label)
        self.opacity_controls.append(increment_button)

        self.opacity_row.add_suffix(self.opacity_controls)

        appearance_group.add(self.opacity_row)
        page.add(appearance_group)

        behavior_group = Adw.PreferencesGroup()
        behavior_group.set_title("Behavior")

        self.autostart_path = Path.home() / ".config" / "autostart" / "com.misterg.checklist.desktop"
        self.autostart_row = Adw.SwitchRow()
        self.autostart_row.set_title("Run at startup")
        self.autostart_row.set_subtitle("Launch Checklist automatically when you log in")
        self.autostart_row.set_active(self.autostart_path.exists())
        self.autostart_row.connect("notify::active", self.on_autostart_toggled)
        behavior_group.add(self.autostart_row)

        page.add(behavior_group)

        about_group = Adw.PreferencesGroup()
        about_group.set_title("About")
        page.add(about_group)

        self.add(page)

    def _update_opacity(self, percentage):
        clamped_percentage = max(30, min(100, int(percentage)))
        self.current_opacity = clamped_percentage
        self.opacity_value_label.set_label(f"{self.current_opacity}%")
        save_preferences({"window_opacity": self.current_opacity})

        if self.window is not None:
            self.window.set_opacity(self.current_opacity / 100.0)

    def on_opacity_decrement(self, button):
        self._update_opacity(self.current_opacity - 1)

    def on_opacity_increment(self, button):
        self._update_opacity(self.current_opacity + 1)

    def on_autostart_toggled(self, row, pspec):
        self._set_autostart_enabled(row.get_active())

    def _set_autostart_enabled(self, enabled):
        self.autostart_path.parent.mkdir(parents=True, exist_ok=True)

        if enabled:
            desktop_file = """[Desktop Entry]
Type=Application
Name=Checklist
Exec=checklist
X-GNOME-Autostart-enabled=true
"""
            self.autostart_path.write_text(desktop_file, encoding="utf-8")
        elif self.autostart_path.exists():
            self.autostart_path.unlink()
