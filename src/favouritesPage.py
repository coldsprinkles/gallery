from gi.repository import Adw
from gi.repository import Gtk, Gio, Gdk, GObject
from .dayPage import GalleryView

class FavouritesPage(Adw.NavigationPage):

    def __init__(self, directory):
        super().__init__(title="Photos")
        self.navView = Adw.NavigationView()
        self.set_child(self.navView)
        self.rootPage = Adw.NavigationPage(title="Favourites")
        self.navView.add(self.rootPage)
        self.toolbarView = Adw.ToolbarView()


        gallery = GalleryView(directory)
        self.rootPage.set_child(gallery)

