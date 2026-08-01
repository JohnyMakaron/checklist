import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Gtk, Adw

try:
    from .task_row import TaskRow
    from .storage import load_tasks, save_tasks
except ImportError:
    from task_row import TaskRow
    from storage import load_tasks, save_tasks


class MainWindow(Adw.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app)

        self.set_title("Checklist")
        self.set_default_size(800, 600)

        header = Adw.HeaderBar()

        title = Gtk.Label(label="Checklist")
        title.add_css_class("title")
        header.set_title_widget(title)

        main_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=12,
            margin_top=12,
            margin_bottom=12,
            margin_start=12,
            margin_end=12,
        )

        input_box = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=6,
        )

        self.entry = Gtk.Entry()
        self.entry.set_placeholder_text("Type a new task...")
        self.entry.connect("activate", self.on_entry_activate)

        self.priority_combo = Gtk.ComboBoxText()
        self.priority_combo.append_text("Low")
        self.priority_combo.append_text("Medium")
        self.priority_combo.append_text("High")
        self.priority_combo.set_active(1)

        self.add_button = Gtk.Button(label="Add")
        self.add_button.connect("clicked", self.on_add_clicked)

        input_box.append(self.entry)
        input_box.append(self.priority_combo)
        input_box.append(self.add_button)

        self.task_list = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=6,
        )

        scroller = Gtk.ScrolledWindow()
        scroller.set_vexpand(True)
        scroller.set_child(self.task_list)

        main_box.append(input_box)
        main_box.append(scroller)

        toolbar = Adw.ToolbarView()
        toolbar.add_top_bar(header)
        toolbar.set_content(main_box)

        self.set_content(toolbar)

        self._load_saved_tasks()

    def _load_saved_tasks(self):
        tasks = load_tasks()
        for task in tasks:
            self._add_task_row(task, save=False)

        self._save_tasks()

    def _add_task_row(self, task, save=True):
        row = TaskRow(task, self.on_task_changed, self.on_task_deleted)
        self.task_list.append(row)

        if save:
            self._save_tasks()

    def _save_tasks(self):
        tasks = []
        child = self.task_list.get_first_child()

        while child is not None:
            next_child = child.get_next_sibling()
            if isinstance(child, TaskRow):
                tasks.append(child.to_dict())
            child = next_child

        save_tasks(tasks)

    def on_add_clicked(self, button):
        text = self.entry.get_text().strip()

        if not text:
            return

        priority = self.priority_combo.get_active_text().lower()
        if priority not in {"low", "medium", "high"}:
            priority = "medium"

        self._add_task_row({"text": text, "completed": False, "priority": priority})
        self.entry.set_text("")
        self.priority_combo.set_active(1)
        self.entry.grab_focus()

    def on_entry_activate(self, entry):
        self.on_add_clicked(None)

    def on_task_changed(self, task_row):
        self._save_tasks()

    def on_task_deleted(self, task_row):
        self.task_list.remove(task_row)
        self._save_tasks()

