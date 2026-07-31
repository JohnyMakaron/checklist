import gi

gi.require_version("Gtk", "4.0")

from gi.repository import Gtk


class TaskRow(Gtk.Box):
    def __init__(self, task, changed_callback, delete_callback):
        super().__init__(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=8,
        )

        self.changed_callback = changed_callback

        self.checkbox = Gtk.CheckButton(
            label=task["text"]
        )
        self.checkbox.set_active(task["completed"])
        self.checkbox.connect("toggled", self.on_toggled)

        self.delete_button = Gtk.Button(label="🗑")
        self.delete_button.connect(
            "clicked",
            lambda button: delete_callback(self)
        )

        self.append(self.checkbox)
        self.append(self.delete_button)

    def on_toggled(self, button):
        self.changed_callback()

    def to_dict(self):
        return {
            "text": self.checkbox.get_label(),
            "completed": self.checkbox.get_active(),
        }
