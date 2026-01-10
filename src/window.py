# window.py
#
# Copyright 2026 riyani
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Adw
from gi.repository import Gtk, Gio

from .peoplePage import PeoplePage
from .libraryPage import LibraryPage
from .favouritesPage import FavouritesPage

class ChobiWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'ChobiWindow'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        navigationSplitView = Adw.NavigationSplitView()
        sidebarPage =  Adw.NavigationPage(title="Sidebar")

        headerBar = Adw.HeaderBar()
        titleWidget = Adw.WindowTitle(title="Chobi")
        headerBar.set_title_widget(titleWidget)
        #Menu Stuff
        menuButtonModel = Gio.Menu()
        menuButtonModel.append(
            label='Preferences',
            detailed_action='app.preferences',
        )
        menuButtonModel.append(
            label='About Chobi',
            detailed_action='app.about',
        )
        menuButton = Gtk.MenuButton(
            primary=True,
            icon_name="open-menu-symbolic",
        )
        menuButton.set_menu_model(menu_model=menuButtonModel)
        headerBar.pack_end(child=menuButton)

        toolbarView = Adw.ToolbarView()
        sidebarPage.set_child(toolbarView)

        #SidebarStuff
        sidebar = Adw.ViewSwitcherSidebar()

        #Stack
        viewStack = Adw.ViewStack()

        libraryItem = viewStack.add_titled_with_icon (
            child=LibraryPage(),
            name="library",
            title="Library",
            icon_name="view-grid-symbolic"
        )

        peopleItem = viewStack.add_titled_with_icon (
            child=PeoplePage(),
            name="people",
            title="People",
            icon_name="avatar-default-symbolic"
        )

        placesItem = viewStack.add_titled_with_icon (
            child=Gtk.Label(label="Places Content"),
            name="places",
            title="Places",
            icon_name="location-services-active-symbolic"
        )

        favouritesItem = viewStack.add_titled_with_icon (
            child=FavouritesPage("/home/riyani/Pictures/Flowers/"),
            name="favourites",
            title="Favourites",
            icon_name="emote-love-symbolic"
        )

        #Albums Stuff
        maldaItem = viewStack.add_titled_with_icon (
            child=Gtk.Label(label="Album Content"),
            name="malda",
            title="Malda",
            icon_name="starred-symbolic"
        )

        screenshotItem = viewStack.add_titled_with_icon (
            child=Gtk.Label(label="Screenshot Album"),
            name="screenshot",
            title="Screenshot",
            icon_name="starred-symbolic"
        )

        WhatsAppItem = viewStack.add_titled_with_icon (
            child=Gtk.Label(label="Album Content"),
            name="whatsapp",
            title="WhatsApp Images",
            icon_name="starred-symbolic"
        )


        libraryItem.set_starts_section(True)
        libraryItem.set_section_title(section_title="Photos")
        favouritesItem.set_needs_attention(True)
        favouritesItem.set_badge_number(12)
        peopleItem.set_needs_attention(True)
        peopleItem.set_badge_number(0)
        maldaItem.set_starts_section(True)
        maldaItem.set_section_title(section_title="Albums")



        sidebar.set_stack(viewStack)

        toolbarView.add_top_bar(headerBar)
        toolbarView.set_content(sidebar)

        contentPage = Adw.NavigationPage(title="Content")
        contentView = Adw.ToolbarView()
        contentView.set_content(viewStack)
        contentPage.set_child(contentView)


        navigationSplitView.set_content(contentPage)
        navigationSplitView.set_sidebar(sidebarPage)

        self.set_content(navigationSplitView)
        self.set_default_size(1170, 650)
