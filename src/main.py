import sys
import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Gio, Adw, Gdk
from .window import ChobiWindow


class ChobiApplication(Adw.Application):
    """The main application singleton class."""

    def __init__(self):
        super().__init__(application_id='com.riyani.chobi',
                         flags=Gio.ApplicationFlags.DEFAULT_FLAGS,
                         resource_base_path='/com/riyani/chobi')
        self.create_action('quit', lambda *_: self.quit(), ['<control>q'])
        self.create_action('about', self.on_about_action)
        self.create_action('preferences', self.on_preferences_action)
        self.load_css()

    def load_css(self):
        provider = Gtk.CssProvider()
        provider.load_from_data(b"""
        .rounded-picture {
            border-radius: 7px;
        }
        """)
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def do_activate(self):
        """Called when the application is activated.

        We raise the application's main window, creating it if
        necessary.
        """
        win = self.props.active_window
        if not win:
            win = ChobiWindow(application=self)
        win.present()

    def on_about_action(self, *args):
        """Callback for the app.about action."""
        about = Adw.AboutDialog(application_name='chobi',
                                application_icon='com.riyani.chobi',
                                developer_name='riyani',
                                version='0.1.0',
                                developers=['riyani'],
                                copyright='© 2026 riyani')
        # Translators: Replace "translator-credits" with your name/username, and optionally an email or URL.
        about.set_translator_credits(_('translator-credits'))
        about.present(self.props.active_window)

    def on_preferences_action(self, widget, _):
        preferencesDialog =  Adw.PreferencesDialog()
        preferences = Adw.PreferencesPage(

        )

        integrationGroup = Adw.PreferencesGroup(
            title="Integration",
            description="Settings to make this more GNOME"
        )

        addFolder = Gtk.Button.new_from_icon_name("list-add-symbolic")
        addFolder.set_valign(Gtk.Align.CENTER)
        integrationGroup.set_header_suffix(addFolder)

        for i in range(1):
            folderRow = Adw.ActionRow(
                title="Pictures",
                subtitle="/home/riyani/Pictures/home/riyani/Pictures/Images/Documents/2024/harish sir teachers day/"
            )
            removeFolder = Gtk.Button.new_from_icon_name("list-remove-symbolic")
            removeFolder.set_valign(Gtk.Align.CENTER)
            folderRow.add_suffix(removeFolder)
            integrationGroup.add(folderRow)

        immichGroup = Adw.PreferencesGroup(
            title="Immich",
            description="Configure Immich Settings"
        )

        immichServer = Adw.ActionRow(
            title="Server Url",
            subtitle="Immich server url"
        )
        serverEntry = Gtk.Entry()
        serverEntry.set_valign(Gtk.Align.CENTER)
        immichServer.add_suffix(serverEntry)
        immichGroup.add(immichServer)

        preferences.add(integrationGroup)
        preferences.add(immichGroup)
        preferencesDialog.add(preferences)
        preferencesDialog.present(self.props.active_window)

        print("ADD THIS")

    def create_action(self, name, callback, shortcuts=None):
        """Add an application action.

        Args:
            name: the name of the action
            callback: the function to be called when the action is
              activated
            shortcuts: an optional list of accelerators
        """
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)


def main(version):
    """The application's entry point."""
    app = ChobiApplication()
    return app.run(sys.argv)

