import gi
gi.require_version("Gtk", "3.0")

from gi.repository import Gtk, Gdk
from functions.fileStorage import updateConfig, readConfig, createConfig
from functions.color import setColorRGB

UI_FILE = "ui.glade"

class Example:
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file(UI_FILE)
        self.builder.connect_signals(self)
        
        self.status_icon = Gtk.StatusIcon()
        self.status_icon.set_from_icon_name("AlienLogoDarkIcon")
        self.status_icon.connect("popup-menu", self.right_click_event)

        self.window = self.builder.get_object("window")
        self.window.set_icon_name("AlienLogoDarkIcon")
        self.window.show_all()
        
        
        config = readConfig()
        self.colorZone1 = self.builder.get_object("Zone1")
        self.colorZone2 = self.builder.get_object("Zone2")
        self.colorZone3 = self.builder.get_object("Zone3")
        self.colorZone4 = self.builder.get_object("Zone4")
        self.colorZone1.set_rgba(config[0])
        self.colorZone2.set_rgba(config[1])
        self.colorZone3.set_rgba(config[2])
        self.colorZone4.set_rgba(config[3])

    def button_clicked(self, button):
        zon1 = self.colorZone1.get_rgba()
        zon2 = self.colorZone2.get_rgba()
        zon3 = self.colorZone3.get_rgba()
        zon4 = self.colorZone4.get_rgba()
        updateConfig(zon1, zon2, zon3, zon4)
        setColorRGB(zon1, zon2, zon3, zon4)

    def about_clicked(self, button):
        self.window_label.set_text("This is just an example.")

    def quit_clicked(self, button):
        self.on_window_destroy(self.window)

    def on_window_destroy(self, window):
        Gtk.main_quit()

    def right_click_event(self, icon, button, time):
        self.menu = Gtk.Menu()
        about = Gtk.MenuItem()
        about.set_label("About")
        about.connect("activate", self.show_about_dialog)
        self.menu.append(about)
        quit = Gtk.MenuItem()
        quit.set_label("Quit")
        quit.connect("activate", Gtk.main_quit)
        self.menu.append(quit)
        self.menu.show_all()
        self.menu.popup(None, None, None, self.status_icon, button, time)

    def show_about_dialog(self, widget):
        about_dialog = Gtk.AboutDialog()
        about_dialog.set_destroy_with_parent(True)
        about_dialog.run()
        about_dialog.destroy()

def main():
    app = Example()
    Gtk.main()


if __name__ == "__main__":
    main()
