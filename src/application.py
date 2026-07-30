import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Adw

from window import MainWindow


class ChecklistApplication(Adw.Application):
    def __init__(self):
        super().__init__(
            application_id="com.misterg.checklist"
        )

    def do_activate(self):
        window = MainWindow(self)
        window.present()
