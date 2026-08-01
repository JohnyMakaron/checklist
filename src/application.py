import gi

gi.require_version("Adw", "1")

from gi.repository import Adw

try:
    from .window import MainWindow
except ImportError:
    from window import MainWindow


class ChecklistApplication(Adw.Application):
    def __init__(self):
        super().__init__(
            application_id="com.misterg.checklist"
        )

    def do_activate(self):
        window = self.props.active_window

        if window is None:
            window = MainWindow(self)

        window.present()
