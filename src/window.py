import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Gtk, Adw

from task_row import TaskRow


class MainWindow(Adw.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app)

        self.set_title("Checklist")
        self.set_default_size(800, 600)

        # Header
        header = Adw.HeaderBar()

        title = Gtk.Label(label="Checklist")
        title.add_css_class("title")
        header.set_title_widget(title)

        # Main layout
        main_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=12,
            margin_top=12,
            margin_bottom=12,
            margin_start=12,
            margin_end=12,
        )

        # Input row
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

        # Task list
        self.task_list = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=6,
        )

        # Scroll area
        scroller = Gtk.ScrolledWindow()
        scroller.set_vexpand(True)
        scroller.set_child(self.task_list)

        # Assemble layout
        main_box.append(input_box)
        main_box.append(scroller)

        toolbar = Adw.ToolbarView()
        toolbar.add_top_bar(header)
        toolbar.set_content(main_box)

        self.set_content(toolbar)

    def on_add_clicked(self, button):
        text = self.entry.get_text().strip()

        if not text:
            return

        row = TaskRow(text, self.remove_task)
        self.task_list.append(row)

        self.entry.set_text("")
        self.entry.grab_focus()

    def on_entry_activate(self, entry):
        self.on_add_clicked(None)

    def remove_task(self, task):
        self.task_list.remove(task)
