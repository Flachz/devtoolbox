# Copyright (C) 2022 - 2025 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gtk, Adw, GObject
from enum import Enum

from ..utils import Utils


class Bases(Enum):
    BINARY = 2
    OCTAL = 8
    DECIMAL = 10
    HEX = 16
    ASCII = 128
    UTF8 = 256


@Gtk.Template(resource_path="/me/iepure/devtoolbox/ui/views/base_converter.ui")
class BaseConverterView(Adw.Bin):
    __gtype_name__ = "BaseConverterView"

    # Template elements
    _toast = Gtk.Template.Child()
    _title = Gtk.Template.Child()
    _decimal = Gtk.Template.Child()
    _binary = Gtk.Template.Child()
    _octal = Gtk.Template.Child()
    _hex = Gtk.Template.Child()
    _ascii = Gtk.Template.Child()
    _utf8 = Gtk.Template.Child()

    def __init__(self):
        super().__init__()

        # Signals
        self._decimal_handler = self._decimal.connect(
            "changed", self._on_decimal_changed)
        self._octal_handler = self._octal.connect(
            "changed", self._on_octal_changed)
        self._hex_handler = self._hex.connect("changed", self._on_hex_changed)
        self._binary_handler = self._binary.connect(
            "changed", self._on_binary_changed)
        self._ascii_handler = self._ascii.connect(
            "changed", self._on_ascii_changed)
        self._utf8_handler = self._utf8.connect(
            "changed", self._on_utf8_changed)

    def _on_decimal_changed(self, user_data: GObject.GPointer):
        self._convert(Bases.DECIMAL)

    def _on_octal_changed(self, user_data: GObject.GPointer):
        self._convert(Bases.OCTAL)

    def _on_hex_changed(self, user_data: GObject.GPointer):
        self._convert(Bases.HEX)

    def _on_binary_changed(self, user_data: GObject.GPointer):
        self._convert(Bases.BINARY)
    
    def _on_ascii_changed(self, user_data: GObject.GPointer):
        self._convert(Bases.ASCII)
        
    def _on_utf8_changed(self, user_data: GObject.GPointer):
        self._convert(Bases.UTF8)

    def _convert(self, starting_base: Bases):
        self._binary.remove_css_class("border-red")
        self._octal.remove_css_class("border-red")
        self._decimal.remove_css_class("border-red")
        self._hex.remove_css_class("border-red")

        decimal_num = 0

        if starting_base in [Bases.ASCII, Bases.UTF8]:
            char_input = self._ascii.get_text() if starting_base == Bases.ASCII else self._utf8.get_text()
            decimal_num = ord(char_input) if len(char_input) == 1 else 0
        else:
            match starting_base:
                case Bases.BINARY:
                    if Utils.is_binary(self._binary.get_text()):
                        try:
                            decimal_num = int(
                                self._binary.get_text(), Bases.BINARY.value)
                        except ValueError:
                            self._binary.add_css_class("border-red")
                            return
                case Bases.OCTAL:
                    if Utils.is_octal(self._octal.get_text()):
                        try:
                            decimal_num = int(
                                self._octal.get_text(), Bases.OCTAL.value)
                        except ValueError:
                            self._octal.add_css_class("border-red")
                            return
                case Bases.DECIMAL:
                    if Utils.is_decimal(self._decimal.get_text()):
                        try:
                            decimal_num = int(
                                self._decimal.get_text(), Bases.DECIMAL.value)
                        except ValueError:
                            self._decimal.add_css_class("border-red")
                            return
                case Bases.HEX:
                    if Utils.is_hex(self._hex.get_text()):
                        try:
                            decimal_num = int(
                                self._hex.get_text(), Bases.HEX.value)
                        except ValueError:
                            self._hex.add_css_class("border-red")
                            return

        octal_num = oct(decimal_num).replace("0o", "")
        hex_num = hex(decimal_num).replace("0x", "").upper()
        binary_num = bin(decimal_num).replace("0b", "")
        
        # Handle ASCII and UTF-8 conversion
        try:
            ascii_char = chr(decimal_num) if 0 <= decimal_num <= 127 else ""
        except ValueError:
            ascii_char = ""
            
        try:
            utf8_char = chr(decimal_num)
        except ValueError:
            utf8_char = ""

        # Block signal to prevent infinite recursion
        self._decimal.handler_block(self._decimal_handler)
        self._octal.handler_block(self._octal_handler)
        self._hex.handler_block(self._hex_handler)
        self._binary.handler_block(self._binary_handler)
        self._ascii.handler_block(self._ascii_handler)
        self._utf8.handler_block(self._utf8_handler)

        # Display result
        self._binary.set_text(binary_num)
        self._octal.set_text(octal_num)
        self._decimal.set_text(str(decimal_num))
        self._hex.set_text(hex_num)
        self._ascii.set_text(ascii_char)
        self._utf8.set_text(utf8_char)

        # Set cursor at the saved positions
        self._binary.set_position(-1)
        self._octal.set_position(-1)
        self._decimal.set_position(-1)
        self._hex.set_position(-1)
        self._ascii.set_position(-1)
        self._utf8.set_position(-1)

        # Unblock signals to allow future changes
        self._decimal.handler_unblock(self._decimal_handler)
        self._octal.handler_unblock(self._octal_handler)
        self._hex.handler_unblock(self._hex_handler)
        self._binary.handler_unblock(self._binary_handler)
        self._ascii.handler_unblock(self._ascii_handler)
        self._utf8.handler_unblock(self._utf8_handler)
