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

        self.add_button = Gtk.Button(label="Add")
        self.add_button.connect("clicked", self.on_add_clicked)

        input_box.append(self.entry)
        input_box.append(self.add_button)

        self.filter_box = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=6,
            margin_bottom=6,
        )

        self.filter_all = Gtk.ToggleButton(label="All")
        self.filter_active = Gtk.ToggleButton(label="Active")
        self.filter_completed = Gtk.ToggleButton(label="Completed")

        self.filter_all.set_group(self.filter_active)
        self.filter_completed.set_group(self.filter_active)
        self.filter_all.connect("toggled", self.on_filter_changed)
        self.filter_active.connect("toggled", self.on_filter_changed)
        self.filter_completed.connect("toggled", self.on_filter_changed)

        self.filter_all.set_active(True)

        self.filter_box.append(self.filter_all)
        self.filter_box.append(self.filter_active)
        self.filter_box.append(self.filter_completed)

        self.task_list = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=6,
        )

        self.empty_state = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=6,
            valign=Gtk.Align.CENTER,
            halign=Gtk.Align.CENTER,
            vexpand=True,
            hexpand=True,
        )

        self.empty_state_icon = Gtk.Label(label="📝")
        self.empty_state_title = Gtk.Label(label="No tasks yet")
        self.empty_state_message = Gtk.Label(label="Add your first task above.")

        self.empty_state.append(self.empty_state_icon)
        self.empty_state.append(self.empty_state_title)
        self.empty_state.append(self.empty_state_message)

        self.task_list.append(self.empty_state)

        scroller = Gtk.ScrolledWindow()
        scroller.set_vexpand(True)
        scroller.set_child(self.task_list)

        main_box.append(input_box)
        main_box.append(self.filter_box)
        main_box.append(scroller)

        toolbar = Adw.ToolbarView()
        toolbar.add_top_bar(header)
        toolbar.set_content(main_box)

        self.set_content(toolbar)

        self.current_filter = "all"
        self._load_saved_tasks()

    def _load_saved_tasks(self):
        tasks = load_tasks()
        for task in tasks:
            self._add_task_row(task, save=False)

        self._update_empty_state()
        self._apply_filter()
        self._save_tasks()

    def _add_task_row(self, task, save=True):
        row = TaskRow(task, self.on_task_changed, self.on_task_deleted)
        self.task_list.append(row)
        self._update_empty_state()

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

    def _update_empty_state(self):
        has_tasks = False
        child = self.task_list.get_first_child()

        while child is not None:
            if isinstance(child, TaskRow):
                has_tasks = True
                break
            child = child.get_next_sibling()

        self.empty_state.set_visible(not has_tasks)

    def _apply_filter(self):
        task_list = self.task_list
        child = task_list.get_first_child()

        while child is not None:
            next_child = child.get_next_sibling()

            if isinstance(child, TaskRow):
                if self.current_filter == "all":
                    child.set_visible(True)
                    child.set_drag_enabled(True)
                elif self.current_filter == "active":
                    child.set_visible(not child.checkbox.get_active())
                    child.set_drag_enabled(False)
                elif self.current_filter == "completed":
                    child.set_visible(child.checkbox.get_active())
                    child.set_drag_enabled(False)

            child = next_child

    def on_add_clicked(self, button):
        text = self.entry.get_text().strip()

        if not text:
            return

        self._add_task_row({"text": text, "completed": False})
        self.entry.set_text("")
        self.entry.grab_focus()

    def on_entry_activate(self, entry):
        self.on_add_clicked(None)

    def on_filter_changed(self, button):
        if button.get_active():
            if button is self.filter_all:
                self.current_filter = "all"
            elif button is self.filter_active:
                self.current_filter = "active"
            elif button is self.filter_completed:
                self.current_filter = "completed"

            self._apply_filter()

    def on_task_changed(self, task_row):
        self._save_tasks()
        self._apply_filter()

    def on_task_deleted(self, task_row):
        self.task_list.remove(task_row)
        self._update_empty_state()
        self._save_tasks()

