#!/usr/bin/python3
'''
   Copyright 2017 Mirko Brombin (brombinmirko@gmail.com)

   This file is part of Bottles.

    Bottles is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Bottles is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Bottles.  If not, see <http://www.gnu.org/licenses/>.
'''

import os
import gi
import subprocess
import webbrowser
gi.require_version('Gtk', '3.0')
gi.require_version('Granite', '1.0')
from gi.repository import Gtk, Gdk, Granite, GdkPixbuf
try:
    import constants as cn
    import wine as w
    import helper as hl
except ImportError:
    import bottles.constants as cn
    import bottles.wine as w
    import bottles.helper as hl

class Detail(Gtk.Box):
    status = False
    working_dir = ""

    def __init__(self, parent):
        Gtk.Box.__init__(self, False, 0)
        self.wine = w.Wine(self)
        self.parent = parent
        HGtk = hl.HGtk

        self.set_border_width(15)
        #win.resize(800,400)
        self.set_orientation(Gtk.Orientation.VERTICAL)

        self.title = Gtk.Label("New prefix")
        self.title.set_name('Title')
        HGtk.add_class(self, self.title, "detail_title")
        self.title.set_justify(Gtk.Justification.CENTER)
        self.add(self.title)

        self.description = Gtk.Label("Here you can create a new Wine prefix")
        self.description.set_name('Description')
        self.description.set_justify(Gtk.Justification.CENTER)
        self.add(self.description)

        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(self.vbox)
        
        self.grid_1 = Gtk.Grid()
        self.grid_1.set_column_homogeneous(True)
        self.grid_1.set_column_spacing(20)
        self.vbox.add(self.grid_1)

        # Drive C
        self.button_drive_c = Gtk.Button.new_from_icon_name("folder", Gtk.IconSize.DIALOG)
        self.button_drive_c.connect("clicked", self.on_button_drive_c_clicked)
        self.grid_1.add(self.button_drive_c)
        
        # Winecfg
        self.button_wine_cfg = Gtk.Button.new_from_icon_name("wine-winecfg", Gtk.IconSize.DIALOG)
        self.button_wine_cfg.connect("clicked", self.on_button_wine_cfg_clicked)
        self.grid_1.add(self.button_wine_cfg)
        
        # Winetricks
        self.button_winetricks = Gtk.Button.new_from_icon_name("winetricks", Gtk.IconSize.DIALOG)
        self.button_winetricks.connect("clicked", self.on_button_winetricks_clicked)
        self.grid_1.add(self.button_winetricks)
        
        grid_2 = Gtk.Grid()
        grid_2.set_column_spacing(20)
        grid_2.set_column_homogeneous(True)
        self.vbox.add(grid_2)

        label_drive_c = Gtk.Label("Browse C:")
        HGtk.add_class(self, label_drive_c, "label_cell")
        grid_2.add(label_drive_c)

        label_wine_cfg = Gtk.Label("Configure")
        HGtk.add_class(self, label_wine_cfg, "label_cell")
        grid_2.add(label_wine_cfg)

        label_winetricks = Gtk.Label("Winetricks")
        HGtk.add_class(self, label_winetricks, "label_cell")
        grid_2.add(label_winetricks)
        
        self.grid_3 = Gtk.Grid()
        self.grid_3.set_column_spacing(20)
        self.grid_3.set_column_homogeneous(True)
        self.vbox.add(self.grid_3)
        
        # Terminal
        self.button_terminal = Gtk.Button.new_from_icon_name("utilities-terminal", Gtk.IconSize.DIALOG)
        self.button_terminal.connect("clicked", self.on_button_terminal_clicked)
        self.grid_3.add(self.button_terminal)
        
        # Monitor
        self.button_monitor = Gtk.Button.new_from_icon_name("utilities-system-monitor", Gtk.IconSize.DIALOG)
        self.button_monitor.connect("clicked", self.on_button_monitor_clicked)
        self.grid_3.add(self.button_monitor)
        
        # Settings
        self.button_settings = Gtk.Button.new_from_icon_name("preferences-desktop", Gtk.IconSize.DIALOG)
        self.button_settings.connect("clicked", self.on_button_settings_clicked)
        self.grid_3.add(self.button_settings)

        grid_4 = Gtk.Grid()
        grid_4.set_column_spacing(20)
        grid_4.set_column_homogeneous(True)
        self.vbox.add(grid_4)

        label_terminal = Gtk.Label("Terminal")
        HGtk.add_class(self, label_terminal, "label_cell")
        grid_4.add(label_terminal)

        label_monitor = Gtk.Label("Task manager")
        HGtk.add_class(self, label_monitor, "label_cell")
        grid_4.add(label_monitor)

        label_settings = Gtk.Label("Control panel")
        HGtk.add_class(self, label_settings, "label_cell")
        grid_4.add(label_settings)
        
        self.grid_5 = Gtk.Grid()
        self.grid_5.set_column_spacing(20)
        self.grid_5.set_column_homogeneous(True)
        self.vbox.add(self.grid_5)
        
        # Regedit
        self.button_regedit = Gtk.Button.new_from_icon_name("dialog-password", Gtk.IconSize.DIALOG)
        self.button_regedit.connect("clicked", self.on_button_regedit_clicked)
        self.grid_5.add(self.button_regedit)
        
        # Uninstaller
        self.button_uninstaller = Gtk.Button.new_from_icon_name("wine-uninstaller", Gtk.IconSize.DIALOG)
        self.button_uninstaller.connect("clicked", self.on_button_uninstaller_clicked)
        self.grid_5.add(self.button_uninstaller)
        
        # Reboot
        self.button_reboot = Gtk.Button.new_from_icon_name("system-reboot", Gtk.IconSize.DIALOG)
        self.button_reboot.connect("clicked", self.on_button_reboot_clicked)
        self.grid_5.add(self.button_reboot)

        grid_6 = Gtk.Grid()
        grid_6.set_column_spacing(20)
        grid_6.set_column_homogeneous(True)
        self.vbox.add(grid_6)

        label_regedit = Gtk.Label("Regedit")
        HGtk.add_class(self, label_regedit, "label_cell")
        grid_6.add(label_regedit)

        label_uninstaller = Gtk.Label("Uninstaller")
        HGtk.add_class(self, label_uninstaller, "label_cell")
        grid_6.add(label_uninstaller)

        label_reboot = Gtk.Label("Reboot")
        HGtk.add_class(self, label_reboot, "label_cell")
        grid_6.add(label_reboot)

    def on_button_drive_c_clicked(self, button):
        os.system('xdg-open "%s"' % self.working_dir)

    def on_button_wine_cfg_clicked(self, button):
        self.wine.run_winecfg(self.working_dir)

    def on_button_winetricks_clicked(self, button):
        self.wine.run_winetricks(self.working_dir)

    def on_button_terminal_clicked(self, button):
        self.wine.run_console(self.working_dir)

    def on_button_monitor_clicked(self, button):
        self.wine.run_monitor(self.working_dir)

    def on_button_settings_clicked(self, button):
        self.wine.run_control(self.working_dir)

    def on_button_regedit_clicked(self, button):
        self.wine.run_regedit(self.working_dir)

    def on_button_uninstaller_clicked(self, button):
        self.wine.run_uninstaller(self.working_dir)

    def on_button_reboot_clicked(self, button):
        self.wine.run_wineboot(self.working_dir)