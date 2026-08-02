import gi

gi.require_version("Gtk", "4.0")

from gi.repository import Gtk, GLib, Pango, Gdk


class TaskRow(Gtk.Box):
    @staticmethod
    def insert_task_row_at_index(parent, row, index):
        child = parent.get_first_child()
        current_index = 0

        while child is not None:
            if isinstance(child, TaskRow):
                if current_index == index:
                    previous_sibling = child.get_prev_sibling()
                    if previous_sibling is None:
                        parent.prepend(row)
                    else:
                        parent.insert_child_after(row, previous_sibling)
                    return
                current_index += 1
            child = child.get_next_sibling()

        parent.append(row)

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

        self.drag_source = Gtk.DragSource()
        self.drag_source.set_actions(Gdk.DragAction.MOVE)
        self.drag_source.connect("prepare", self.on_drag_prepare)
        self.drag_source.connect("drag-begin", self.on_drag_begin)
        self.drag_source.connect("drag-end", self.on_drag_end)
        self.add_controller(self.drag_source)

        self.drop_target = Gtk.DropTarget.new(type(self), Gdk.DragAction.MOVE)
        self.drop_target.connect("drop", self.on_drop)
        self.add_controller(self.drop_target)

        self.set_drag_enabled(True)

    def set_drag_enabled(self, enabled):
        if enabled:
            self.drag_source.set_actions(Gdk.DragAction.MOVE)
            self.drop_target.set_actions(Gdk.DragAction.MOVE)
        else:
            self.drag_source.set_actions(Gdk.DragAction.NONE)
            self.drop_target.set_actions(Gdk.DragAction.NONE)

    def _update_task_label(self):
        text = GLib.markup_escape_text(self.task_text)
        if self.checkbox.get_active():
            self.task_label.set_markup(
                f'<span strikethrough="true" alpha="50%">{text}</span>'
            )
        else:
            self.task_label.set_markup(text)

    def on_drag_prepare(self, drag_source, x, y):
        return Gdk.ContentProvider.new_for_value(self)

    def on_drag_begin(self, drag_source, drag):
        self.set_cursor_from_name("grabbing")

    def on_drag_end(self, drag_source, drag, delete_data):
        self.set_cursor_from_name("default")

    def on_drop(self, drop_target, value, x, y):
        source_row = value
        parent = self.get_parent()

        if source_row is None or source_row is self or parent is None:
            return False

        if source_row.get_parent() is not parent:
            return False

        source_index = None
        target_index = None
        child = parent.get_first_child()
        index = 0

        while child is not None:
            if isinstance(child, TaskRow):
                if child is source_row:
                    source_index = index
                if child is self:
                    target_index = index
                index += 1
            child = child.get_next_sibling()

        if source_index is None or target_index is None:
            return False

        parent.remove(source_row)

        if source_index < target_index:
            TaskRow.insert_task_row_at_index(parent, source_row, target_index + 1)
        else:
            TaskRow.insert_task_row_at_index(parent, source_row, target_index)

        self.changed_callback(self)
        return True

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
