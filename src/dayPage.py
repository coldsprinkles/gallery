from gi.repository import Adw
from gi.repository import Gtk, Gio, Gdk, GObject

class DayPage(Adw.NavigationPage):

    def __init__(self, directory):
        super().__init__(title="Photos")

        gallery = GalleryView(directory)

        self.set_child(gallery)


class Thumbnail(Gtk.Box):
    __gsignals__ = {
        "clicked": (GObject.SignalFlags.RUN_FIRST, None, ())
    }

    def __init__(self, file, size=200):
        super().__init__(orientation=Gtk.Orientation.VERTICAL)
        self.set_size_request(size, size)

        picture = Gtk.Picture.new_for_file(file)
        picture.set_content_fit(Gtk.ContentFit.COVER)
        picture.add_css_class("rounded-picture")

        clamp = Adw.Clamp(maximum_size=size)
        clamp.set_child(picture)

        self.append(clamp)

        click = Gtk.GestureClick()
        click.connect("pressed", lambda *_: self.emit("clicked"))
        self.add_controller(click)


class GalleryView(Gtk.ScrolledWindow):
    __gsignals__ = {
        "image-clicked": (GObject.SignalFlags.RUN_FIRST, None, (int,))
    }

    def __init__(self, directory):
        super().__init__(hexpand=True, vexpand=True)

        self.flowbox = Gtk.FlowBox(
            selection_mode=Gtk.SelectionMode.NONE,
            row_spacing=12,
            column_spacing=12,
            margin_top=12,
            margin_bottom=12,
            margin_start=12,
            margin_end=12,
        )

        self.set_child(self.flowbox)

        # Load images
        self.imageFiles = self.loadImages(directory)
        self.populateThumbnails()

        # Carousel cache
        self.carouselPage = None

    def populateThumbnails(self):
        for i, file in enumerate(self.imageFiles):
            thumb = Thumbnail(file)
            thumb.connect("clicked", lambda _, idx=i: self.onThumbnailClicked(idx))
            self.flowbox.append(thumb)

    def onThumbnailClicked(self, index):
        nav = self.get_ancestor(Adw.NavigationView)
        if nav is None:
            print("GalleryView not inside a NavView")
            return

        if self.carouselPage is None:
            self.carouselPage = CarouselPage(self.imageFiles, index)
            nav.push(self.carouselPage)
        else:
            self.carouselPage.scroll_to(index)
            nav.push(self.carouselPage)

    def loadImages(self, directory):
        parent = Gio.File.new_for_path(directory)
        infos = parent.enumerate_children(
            'standard::name,standard::content-type',
            Gio.FileQueryInfoFlags.NONE,
            None
        )

        imageFiles = [
            parent.get_child(info.get_name())
            for info in infos
            if info.get_content_type().startswith("image")
        ]

        return imageFiles


class CarouselPage(Adw.NavigationPage):
    def __init__(self, imageFiles, startIndex=0):
        super().__init__(title="Photo")

        self.carousel = Adw.Carousel()
        self.pages = []

        for file in imageFiles:
            pic = Gtk.Picture.new_for_file(file)
            self.carousel.append(pic)
            self.pages.append(pic)

        toolbar = Adw.ToolbarView()
        toolbar.add_top_bar(Adw.HeaderBar())
        toolbar.set_content(self.carousel)

        self.set_child(toolbar)
        self.scroll_to(startIndex)

    def scroll_to(self, index):
        if 0 <= index < len(self.pages):
            self.carousel.scroll_to(self.pages[index])

