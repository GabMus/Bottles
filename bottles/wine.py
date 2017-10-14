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
import apt
import threading
import subprocess
import urllib
import shutil
import tarfile
import time
from pathlib import Path
from softwareproperties.SoftwareProperties import SoftwareProperties
import webbrowser
gi.require_version('Gtk', '3.0')
gi.require_version('Granite', '1.0')
from gi.repository import Gtk, Gdk, Granite, GObject, GLib, GdkPixbuf
try:
    import constants as cn
    import helper as hl
except ImportError:
    import bottles.constants as cn
    import bottles.helper as hl

GLib.threads_init()

class T_Winecfg(threading.Thread):
    cache = apt.Cache()

    def __init__(self, working_prefix_dir):
        threading.Thread.__init__(self)
        self.working_prefix_dir = working_prefix_dir
        
    def run(self):
        subprocess.call("WINEPREFIX="+self.working_prefix_dir+" winecfg", shell=True)

class T_Wintricks(threading.Thread):
    cache = apt.Cache()

    def __init__(self, working_prefix_dir):
        threading.Thread.__init__(self)
        self.working_prefix_dir = working_prefix_dir
        
    def run(self):
        subprocess.call("WINEPREFIX="+self.working_prefix_dir+" winetricks", shell=True)

class T_Console(threading.Thread):
    cache = apt.Cache()

    def __init__(self, working_prefix_dir):
        threading.Thread.__init__(self)
        self.working_prefix_dir = working_prefix_dir
        
    def run(self):
        os.chdir(self.working_prefix_dir)
        subprocess.call("WINEPREFIX="+self.working_prefix_dir+" wineconsole cmd", shell=True)

class T_Monitor(threading.Thread):
    cache = apt.Cache()

    def __init__(self, working_prefix_dir):
        threading.Thread.__init__(self)
        self.working_prefix_dir = working_prefix_dir
        
    def run(self):
        os.chdir(self.working_prefix_dir)
        subprocess.call("WINEPREFIX="+self.working_prefix_dir+" wine taskmgr", shell=True)

class T_Control(threading.Thread):
    cache = apt.Cache()

    def __init__(self, working_prefix_dir):
        threading.Thread.__init__(self)
        self.working_prefix_dir = working_prefix_dir
        
    def run(self):
        os.chdir(self.working_prefix_dir)
        subprocess.call("WINEPREFIX="+self.working_prefix_dir+" wine control", shell=True)

class T_Regedit(threading.Thread):
    cache = apt.Cache()

    def __init__(self, working_prefix_dir):
        threading.Thread.__init__(self)
        self.working_prefix_dir = working_prefix_dir
        
    def run(self):
        os.chdir(self.working_prefix_dir)
        subprocess.call("WINEPREFIX="+self.working_prefix_dir+" wine regedit", shell=True)

class T_Uninstaller(threading.Thread):
    cache = apt.Cache()

    def __init__(self, working_prefix_dir):
        threading.Thread.__init__(self)
        self.working_prefix_dir = working_prefix_dir
        
    def run(self):
        os.chdir(self.working_prefix_dir)
        subprocess.call("WINEPREFIX="+self.working_prefix_dir+" wine uninstaller", shell=True)

class T_Wineboot(threading.Thread):
    cache = apt.Cache()

    def __init__(self, working_prefix_dir):
        threading.Thread.__init__(self)
        self.working_prefix_dir = working_prefix_dir
        
    def run(self):
        os.chdir(self.working_prefix_dir)
        subprocess.call("WINEPREFIX="+self.working_prefix_dir+" wineboot", shell=True)

class Wine:
    HGtk = hl.HGtk()
    working_dir = str(Path.home())+"/.Bottles/"
    wine_icon = Gtk.IconTheme.get_default().load_icon("wine", 16, 0)

    def __init__(self, parent):
        self.parent = parent

    def check_work_dir(self):
        if not os.path.exists(self.working_dir):
            os.mkdir(self.working_dir)
    
    def run_winecfg(self, working_dir):
        T_Winecfg(working_dir).start()
    
    def run_winetricks(self, working_dir):
        T_Wintricks(working_dir).start()
    
    def run_console(self, working_dir):
        T_Console(working_dir).start()
    
    def run_monitor(self, working_dir):
        T_Monitor(working_dir).start()
    
    def run_control(self, working_dir):
        T_Control(working_dir).start()
    
    def run_regedit(self, working_dir):
        T_Regedit(working_dir).start()
    
    def run_uninstaller(self, working_dir):
        T_Uninstaller(working_dir).start()
    
    def run_wineboot(self, working_dir):
        T_Wineboot(working_dir).start()

    # FIXME: I need to include check for special character and clones
    def create_bottle(self, name, arch):
        # log
        print("Creating a bottle with name: "+name+" and arch: "+arch)

        # create dir
        self.working_prefix_dir = self.working_dir+"prefix_"+name
        if not os.path.exists(self.working_prefix_dir):
            os.mkdir(self.working_prefix_dir)
            version_bottle = self.working_prefix_dir+"/version.bottle"
            with open(version_bottle, "w") as f:
                f.write(arch)

            # start winecfg
            self.run_winecfg(self.working_prefix_dir)

        self.detail_bottle(name)
        
        # re-fill list
        lt = self.parent.parent.stack.list_all
        lt.generate_entries(True)

    def list_bottles(self):
        bottles = []
        walk = next(os.walk(self.working_dir))[1]
        for w in walk:
            bottles.append(w)
        return bottles

    # FIXME: I need to include check for special character
    def remove(self, bottle_name):
        shutil.rmtree(self.working_dir+bottle_name, ignore_errors=True)

        # re-fill list
        lt = self.parent.parent.stack.list_all
        lt.generate_entries(True)

    def detail_bottle(self, name):
        # populate detail data
        dt = self.parent.parent.stack.detail
        dt.working_dir = self.working_prefix_dir
        dt.title.set_text(name)
        with open(self.working_prefix_dir+"/version.bottle",'r') as arch_f:
            arch=arch_f.read().replace('\n', '')
        if arch == "32 Bit":
            version = subprocess.check_output(["wine", "--version"])
        else:
            version = subprocess.check_output(["wine64", "--version"])
        version = str(version)
        version = version.replace("b'", "")
        version = version.replace("\\n'", "")
        dt.description.set_text(version+" ("+arch+")")

        # change stack to detail
        self.parent.save.hide()
        self.parent.parent.stack.stack.set_visible_child_name("detail")
        
