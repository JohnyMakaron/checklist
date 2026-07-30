import gi

gi.require_version("Gtk", "4.0")

from gi.repository import Gtk


class TaskRow(Gtk.Box):
    def __init__(self, text, delete_callback):
        super().__init__(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=6,
        )

        self.checkbox = Gtk.CheckButton(label=text)

        self.delete_button = Gtk.Button(label="🗑")
        self.delete_button.connect(
            "clicked",
            lambda button: delete_callback(self)
        )

        self.append(self.checkbox)
        self.append(self.delete_button)

    def is_completed(self):
        return self.checkbox.get_active()

    def get_text(self):
        return self.checkbox.get_label()
