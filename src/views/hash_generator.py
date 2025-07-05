# Copyright (C) 2022 - 2025 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gtk, Adw, GObject, Gio
from gettext import gettext as _

from ..services.hash_generator import HashGeneratorService


@Gtk.Template(resource_path="/me/iepure/devtoolbox/ui/views/hash_generator.ui")
class HashGeneratorView(Adw.Bin):
    __gtype_name__ = "HashGeneratorView"

    # Template elements
    _toast = Gtk.Template.Child()
    _title = Gtk.Template.Child()
    _preference_group = Gtk.Template.Child()
    _type_dropdown = Gtk.Template.Child()
    _check_switch = Gtk.Template.Child()
    _check_entryrow = Gtk.Template.Child()
    _input_area = Gtk.Template.Child()
    _output_area = Gtk.Template.Child()
    _check_box = Gtk.Template.Child()
    _check_icon = Gtk.Template.Child()
    _check_title_lbl = Gtk.Template.Child()
    _check_lbl = Gtk.Template.Child()

    _service = HashGeneratorService()

    def __init__(self):
        super().__init__()

        # Signals
        self._type_dropdown.connect("notify::selected", self._on_type_changed)
        self._check_entryrow.connect("changed", self._on_check_hash_changed)
        self._input_area.connect("text-changed", self._on_input_changed)
        self._input_area.connect("text-loaded", self._on_input_changed)
        self._input_area.connect("file-loaded", self._on_input_changed)
        self._input_area.connect("image-loaded", self._on_input_changed)
        self._input_area.connect("view-cleared", self._on_view_cleared)
        self._input_area.connect("error", self._on_error)

    def _on_type_changed(self, source_widget:GObject.Object, pspec:GObject.ParamSpec):
        self._calculate_hash()

    def _on_input_changed(self, source_widget:GObject.Object):
        self._calculate_hash()

    def _on_check_hash_changed(self, source_widget:GObject.Object):
        self._check_hash()

    def _on_view_cleared(self, source_widget:GObject.Object):
        self._service.get_cancellable().cancel()
        self._output_area.set_spinner_spin(False)
        self._output_area.clear()
        self._check_box.set_visible(False)

    def _on_error(self, source_widget:GObject.Object, error:str):
        self._toast.add_toast(Adw.Toast(title=_("Error: {error}").format(error=error), priority=Adw.ToastPriority.HIGH))

    def _calculate_hash(self):

        # Stop previous tasks
        self._service.get_cancellable().cancel()
        self._output_area.set_spinner_spin(False)
        self._input_area.remove_css_class("border-red")

        # Setup task
        self._output_area.set_spinner_spin(True)
        text = self._input_area.get_text()
        if self._input_area.get_visible_view() == "text-area":
            self._service.set_input(text)
        else:
            self._service.set_input(self._input_area.get_opened_file_path())

        # Call task
        hash_type = self._type_dropdown.get_selected()
        match hash_type:
            case 0: # MD5
                self._calculate_md5(text)
            case 1: # SHA1
                self._calculate_sha1(text)
            case 2: # SHA256
                self._calculate_sha256(text)
            case 3: # SHA512
                self._calculate_sha512(text)
            case 4: # SHA3-256
                self._calculate_sha3_256(text)
            case 5: # SHA3-512
                self._calculate_sha3_512(text)
            case 6: # Adler32
                self._calculate_adler32(text)
            case 7: # CRC32
                self._calculate_crc32(text)

    def _calculate_md5(self, text:str):
        if self._input_area.get_visible_view() == "text-area" and len(text) > 0:
            self._service.hash_text_with_md5_async(self, self._on_async_done)
        elif self._input_area.get_visible_view() == "text-area" and len(text) == 0:
            self._output_area.clear()
        elif self._input_area.get_visible_view() == "image-area" or self._input_area.get_visible_view() == "file-area":
            self._service.hash_file_with_md5_async(self, self._on_async_done)

    def _calculate_sha1(self, text:str):
        if self._input_area.get_visible_view() == "text-area" and len(text) > 0:
            self._service.hash_text_with_sha1_async(self, self._on_async_done)
        elif self._input_area.get_visible_view() == "text-area" and len(text) == 0:
            self._output_area.clear()
        elif self._input_area.get_visible_view() == "image-area" or self._input_area.get_visible_view() == "file-area":
            self._service.hash_file_with_sha1_async(self, self._on_async_done)

    def _calculate_sha256(self, text:str):
        if self._input_area.get_visible_view() == "text-area" and len(text) > 0:
            self._service.hash_text_with_sha256_async(self, self._on_async_done)
        elif self._input_area.get_visible_view() == "text-area" and len(text) == 0:
            self._output_area.clear()
        elif self._input_area.get_visible_view() == "image-area" or self._input_area.get_visible_view() == "file-area":
            self._service.hash_file_with_sha256_async(self, self._on_async_done)

    def _calculate_sha512(self, text:str):
        if self._input_area.get_visible_view() == "text-area" and len(text) > 0:
            self._service.hash_text_with_sha512_async(self, self._on_async_done)
        elif self._input_area.get_visible_view() == "text-area" and len(text) == 0:
            self._output_area.clear()
        elif self._input_area.get_visible_view() == "image-area" or self._input_area.get_visible_view() == "file-area":
            self._service.hash_file_with_sha512_async(self, self._on_async_done)
            
    def _calculate_sha3_256(self, text:str):
        if self._input_area.get_visible_view() == "text-area" and len(text) > 0:
            self._service.hash_text_with_sha3_256_async(self, self._on_async_done)
        elif self._input_area.get_visible_view() == "text-area" and len(text) == 0:
            self._output_area.clear()
        elif self._input_area.get_visible_view() == "image-area" or self._input_area.get_visible_view() == "file-area":
            self._service.hash_file_with_sha3_256_async(self, self._on_async_done)

    def _calculate_sha3_512(self, text:str):
        if self._input_area.get_visible_view() == "text-area" and len(text) > 0:
            self._service.hash_text_with_sha3_512_async(self, self._on_async_done)
        elif self._input_area.get_visible_view() == "text-area" and len(text) == 0:
            self._output_area.clear()
        elif self._input_area.get_visible_view() == "image-area" or self._input_area.get_visible_view() == "file-area":
            self._service.hash_file_with_sha3_512_async(self, self._on_async_done)

    def _calculate_adler32(self, text:str):
        if self._input_area.get_visible_view() == "text-area" and len(text) > 0:
            self._service.hash_text_with_adler32_async(self, self._on_async_done)
        elif self._input_area.get_visible_view() == "text-area" and len(text) == 0:
            self._output_area.clear()
        elif self._input_area.get_visible_view() == "image-area" or self._input_area.get_visible_view() == "file-area":
            self._service.hash_file_with_adler32_async(self, self._on_async_done)

    def _calculate_crc32(self, text:str):
        if self._input_area.get_visible_view() == "text-area" and len(text) > 0:
            self._service.hash_text_with_crc32_async(self, self._on_async_done)
        elif self._input_area.get_visible_view() == "text-area" and len(text) == 0:
            self._output_area.clear()
        elif self._input_area.get_visible_view() == "image-area" or self._input_area.get_visible_view() == "file-area":
            self._service.hash_file_with_crc32_async(self, self._on_async_done)

    def _check_hash(self):
        if self._check_entryrow.get_text() == self._output_area.get_text():
            self._check_box.set_visible(True)
            self._check_icon.set_from_icon_name("check-round-outline")
            self._check_title_lbl.set_text(_("Hashes match!"))
            self._check_lbl.set_wrap(False)
            self._check_lbl.set_text(_("The integrity is verified."))
            self._check_icon.remove_css_class("warning")
            self._check_title_lbl.remove_css_class("warning")
            self._check_icon.add_css_class("success")
            self._check_title_lbl.add_css_class("success")
        else:
            self._check_box.set_visible(True)
            self._check_icon.set_from_icon_name("warning")
            self._check_title_lbl.set_text(_("Warning, integrity cannot be verified!"))
            self._check_lbl.set_wrap(True)
            self._check_lbl.set_text(_("The calculated hash and the provided one do not match. Check again and if this is a file you downloaded from the Internet re-download it."))
            self._check_icon.remove_css_class("success")
            self._check_title_lbl.remove_css_class("success")
            self._check_icon.add_css_class("warning")
            self._check_title_lbl.add_css_class("warning")

    def _on_async_done(self, source_widget:GObject.Object, result:Gio.AsyncResult, user_data:GObject.GPointer):
        self._output_area.set_spinner_spin(False)
        outcome = self._service.async_finish(result, self)

        if len(outcome) > 0:
            self._output_area.set_text(outcome)

        if self._check_switch.get_active() and len(self._check_entryrow.get_text()) > 0:
            self._check_hash()
        else:
            self._check_box.set_visible(False)
