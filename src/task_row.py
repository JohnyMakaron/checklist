import gi

gi.require_version("Gtk", "4.0")

from gi.repository import Gtk, GLib, Pango


class TaskRow(Gtk.Box):
    def __init__(self, task, changed_callback, delete_callback):
        super().__init__(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=8,
        )

        self.changed_callback = changed_callback
        self.delete_callback = delete_callback
        self.task_text = str(task.get("text", "")).strip()

        self.checkbox = Gtk.CheckButton()
        self.checkbox.set_active(bool(task["completed"]))
        self.checkbox.connect("toggled", self.on_toggled)

        self.task_label = Gtk.Label()
        self.task_label.set_hexpand(True)
        self.task_label.set_xalign(0)
        self.task_label.set_ellipsize(Pango.EllipsizeMode.END)
        self._update_task_label()

        self.delete_button = Gtk.Button(label="🗑")
        self.delete_button.set_valign(Gtk.Align.CENTER)
        self.delete_button.connect("clicked", self.on_delete_clicked)

        self.append(self.checkbox)
        self.append(self.task_label)
        self.append(self.delete_button)

    def _update_task_label(self):
        text = GLib.markup_escape_text(self.task_text)
        if self.checkbox.get_active():
            self.task_label.set_markup(
                f'<span strikethrough="true" alpha="50%">{text}</span>'
            )
        else:
            self.task_label.set_markup(text)

    def on_toggled(self, button):
        self._update_task_label()
        self.changed_callback(self)

    def on_delete_clicked(self, button):
        self.delete_callback(self)

    def to_dict(self):
        return {
            "text": self.task_text,
            "completed": self.checkbox.get_active(),
        }
