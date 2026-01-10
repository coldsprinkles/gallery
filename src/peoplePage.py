from gi.repository import Adw, Gtk, GObject, Gdk, Gio
from .dayPage import GalleryView

class PeoplePage(Gtk.Box):
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL)
        self.dataDIR = Gio.File.new_for_path(
            "/app/share/sample-images-main"
        )
        self.navView = Adw.NavigationView()
        self.append(self.navView)


        self.rootPage = Adw.NavigationPage(title="People")
        self.navView.add(self.rootPage)


        self.toolbarView = Adw.ToolbarView()
        self.rootPage.set_child(self.toolbarView)

        headerbar = Adw.HeaderBar()
        self.eyeButton = Gtk.ToggleButton(icon_name="view-reveal-symbolic")
        headerbar.pack_end(self.eyeButton)
        self.toolbarView.add_top_bar(headerbar)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        searchbar = Gtk.SearchBar(key_capture_widget=self)
        searchEntry = Gtk.SearchEntry(
            placeholder_text="Search Person", width_request=400
        )
        searchbar.set_child(searchEntry)

        self.peopleView = PeopleView()
        self.peopleView.connect("person-clicked", self.onPersonClicked)

        scrollable = Gtk.ScrolledWindow(hexpand=True, vexpand=True)
        scrollable.set_child(self.peopleView)

        box.append(searchbar)
        box.append(scrollable)
        self.toolbarView.set_content(box)

        # Bottom bar
        bottombar = Gtk.ActionBar()
        saveButton = Gtk.Button(label="Save")
        saveButton.add_css_class("suggested-action")
        saveButton.connect("clicked", self.onSave)

        cancelButton = Gtk.Button(label="Cancel")
        cancelButton.add_css_class("destructive-action")
        cancelButton.connect("clicked", self.onCancel)

        bottombar.pack_end(saveButton)
        bottombar.pack_start(cancelButton)

        self.toolbarView.add_bottom_bar(bottombar)
        self.toolbarView.set_reveal_bottom_bars(False)


        self.eyeButton.connect("toggled", self.editToggle)

    def onPersonClicked(self, peopleView, index):
        if (self.eyeButton.get_active()):
            return

        directory = ""
        if(index==0):
            directory = self.dataDIR.get_child("fone").get_path()
        else:
            directory = self.dataDIR.get_child("ftwo").get_path()

        galleryView = GalleryView(directory)
        toolbar = Adw.ToolbarView()
        toolbar.add_top_bar(Adw.HeaderBar())
        toolbar.set_content(galleryView)
        galleryPage = Adw.NavigationPage()
        galleryPage.set_child(toolbar)

        self.navView.push(galleryPage)

    def editToggle(self, button):
        active = button.get_active()
        self.peopleView.set_selection_mode(
            Gtk.SelectionMode.MULTIPLE if active else Gtk.SelectionMode.NONE
        )
        self.toolbarView.set_reveal_bottom_bars(active)

    def onSave(self, button):
        selectedChildren = self.peopleView.get_selected_children()
        for child in selectedChildren:
            child = child.get_child()
            child.set_text("Removed")
            child.set_show_initials(True)
        print("Selected: " + str(selectedChildren))
        self.eyeButton.set_active(False)

    def onCancel(self, button):
        self.eyeButton.set_active(False)


class PeopleView(Gtk.FlowBox):
    __gsignals__ = {
        "person-clicked": (GObject.SignalFlags.RUN_FIRST, None, (int,))
    }

    def __init__(self):
        super().__init__(
            selection_mode=Gtk.SelectionMode.NONE,
            row_spacing=12,
            column_spacing=12,
            margin_top=12,
            margin_bottom=12,
            margin_start=12,
            margin_end=12,
            valign=Gtk.Align.START
        )
        self.dataDIR = Gio.File.new_for_path(
            "/app/share/sample-images-main"
        )

        self.imageFiles = []

        """for i in range(100):
            avatar = Adw.Avatar(size=100)
            #texture = Gdk.Texture.new_from_file(Gio.File.new_for_path("/redacted"))
            #avatar.set_custom_image(texture)

            click = Gtk.GestureClick()
            click.connect(
                "pressed",
                lambda _, __, ___, ____, idx=i: self.emit("person-clicked", idx)
            )
            avatar.add_controller(click)
            self.append(avatar)
        """
        avatar = Adw.Avatar(size=100)
        fone = self.dataDIR.get_child("fone.png").get_path()
        texture = Gdk.Texture.new_from_file(Gio.File.new_for_path(fone))
        avatar.set_custom_image(texture)

        click = Gtk.GestureClick()
        click.connect(
            "pressed",
            lambda _, __, ___, ____, idx=0: self.emit("person-clicked", idx)
        )
        avatar.add_controller(click)
        self.append(avatar)

        avatar = Adw.Avatar(size=100)
        ftwo = self.dataDIR.get_child("ftwo.png").get_path()
        texture = Gdk.Texture.new_from_file(Gio.File.new_for_path(ftwo))
        avatar.set_custom_image(texture)

        click = Gtk.GestureClick()
        click.connect(
            "pressed",
            lambda _, __, ___, ____, idx=1: self.emit("person-clicked", idx)
        )
        avatar.add_controller(click)
        self.append(avatar)


