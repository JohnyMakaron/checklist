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
        adjustment = Gtk.Adjustment(
            value=preferences["window_opacity"],
            lower=30,
            upper=100,
            step_increment=1,
            page_increment=10,
        )

        self.opacity_row = Adw.SpinRow()
        self.opacity_row.set_title("Window Opacity")
        self.opacity_row.set_subtitle("30–100%")
        self.opacity_row.set_adjustment(adjustment)
        self.opacity_row.connect("changed", self.on_opacity_changed)

        appearance_group.add(self.opacity_row)
        page.add(appearance_group)

        behavior_group = Adw.PreferencesGroup()
        behavior_group.set_title("Behavior")
        page.add(behavior_group)

        about_group = Adw.PreferencesGroup()
        about_group.set_title("About")
        page.add(about_group)

        self.add(page)

    def on_opacity_changed(self, row):
        percentage = int(round(row.get_value()))
        save_preferences({"window_opacity": percentage})

        if self.window is not None:
            self.window.set_opacity(percentage / 100.0)
