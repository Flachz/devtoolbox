# Copyright (C) 2022 - 2025 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gtk, Adw, GObject


@Gtk.Template(resource_path='/me/iepure/devtoolbox/ui/widgets/file_view.ui')
class FileView(Adw.Bin):
    __gtype_name__ = 'FileView'

    # Template elements
    _file_path_lbl = Gtk.Template.Child()
    _file_size_lbl = Gtk.Template.Child()

    # Properties
    file_path = GObject.Property(type=str, default="")
    file_size = GObject.Property(type=str, default="")

    def __init__(self):
        super().__init__()

        self.set_property("css-name", "fileview")

        # Property binding
        self.bind_property("file_path", self._file_path_lbl, "label", GObject.BindingFlags.SYNC_CREATE)
        self.bind_property("file_size", self._file_size_lbl, "label", GObject.BindingFlags.SYNC_CREATE)

    def get_file_path(self) -> str:
        return self.file_path

    def set_file_path(self, file_path:str):
        self.file_path = file_path

    def get_file_size(self) -> str:
        return self.file_size

    def set_file_size(self, file_size:str):
        self.file_size = file_size
