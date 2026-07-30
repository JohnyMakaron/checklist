import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Gtk, Adw


class ChecklistApp(Adw.Application):
    def __init__(self):
        super().__init__(application_id="com.misterg.checklist")

    def do_activate(self):
        window = Adw.ApplicationWindow(application=self)
        window.set_default_size(800, 600)

        header = Adw.HeaderBar()

        title = Gtk.Label(label="Checklist")
        title.add_css_class("title")

        header.set_title_widget(title)

        toolbar = Adw.ToolbarView()
        toolbar.add_top_bar(header)

        label = Gtk.Label(label="Hello from Checklist!")
        toolbar.set_content(label)

        window.set_content(toolbar)
        window.present()


app = ChecklistApp()
app.run()
