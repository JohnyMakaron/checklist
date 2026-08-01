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
        self.delete_callback = delete_callback

        self.checkbox = Gtk.CheckButton(label=task["text"])
        self.checkbox.set_active(bool(task["completed"]))
        self.checkbox.connect("toggled", self.on_toggled)

        self.delete_button = Gtk.Button(label="🗑")
        self.delete_button.connect("clicked", self.on_delete_clicked)

        self.append(self.checkbox)
        self.append(self.delete_button)

    def on_toggled(self, button):
        self.changed_callback(self)

    def on_delete_clicked(self, button):
        self.delete_callback(self)

    def to_dict(self):
        return {
            "text": self.checkbox.get_label(),
            "completed": self.checkbox.get_active(),
        }
