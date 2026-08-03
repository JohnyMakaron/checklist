import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Adw


class PreferencesWindow(Adw.PreferencesWindow):
    def __init__(self, app):
        super().__init__(application=app)
        self.set_title("Preferences")
        self.set_default_size(460, 520)

        page = Adw.PreferencesPage()
        page.set_name("general")
        page.set_title("General")

        appearance_group = Adw.PreferencesGroup()
        appearance_group.set_title("Appearance")
        page.add(appearance_group)

        behavior_group = Adw.PreferencesGroup()
        behavior_group.set_title("Behavior")
        page.add(behavior_group)

        about_group = Adw.PreferencesGroup()
        about_group.set_title("About")
        page.add(about_group)

        self.add(page)
