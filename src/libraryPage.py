# libraryPage.py
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
from gi.repository import Gtk, GLib, Gio
from pathlib import Path
from .dayPage import DayPage


class LibraryPage(Gtk.Box):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.navigationView = Adw.NavigationView()
        self.append(self.navigationView)

        self.switcherPage = Adw.NavigationPage(title="Library")

        self.navigationView.push(self.switcherPage)


        toolbarView = Adw.ToolbarView()
        headerbar = Adw.HeaderBar()

        viewStack = Adw.ViewStack()

        dataDIR = Gio.File.new_for_path(
            "/app/share/sample-images-main"
        )


        dayItem = viewStack.add_titled_with_icon (
            child=DayPage(directory=str(dataDIR.get_child("one").get_path())),
            name="day",
            title="Day",
            icon_name="weather-clear-symbolic"
        )

        monthItem = viewStack.add_titled_with_icon (
            child=Gtk.Label(label="ToDO"),
            name="month",
            title="Month",
            icon_name="x-office-calendar-symbolic"
        )

        yearItem = viewStack.add_titled_with_icon (
            child=Gtk.Label(label="ToDO"),
            name="year",
            title="Year",
            icon_name="view-grid-symbolic"
        )


        viewSwitcher = Adw.ViewSwitcher(
            stack=viewStack,
            policy=Adw.ViewSwitcherPolicy.WIDE
        )

        headerbar.set_title_widget(title_widget=viewSwitcher)
        bottombar = Adw.ViewSwitcherBar(stack=viewStack)

        toolbarView.add_top_bar(widget=headerbar)
        toolbarView.add_bottom_bar(widget=bottombar)
        toolbarView.set_content(content=viewStack)

        self.switcherPage.set_child(child=toolbarView)


