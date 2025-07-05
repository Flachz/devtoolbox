# Copyright (C) 2022 - 2025 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gio, GObject
from typing import Iterator
import re


class RegexTesterService():

    def __init__(self):
        self._cancellable = Gio.Cancellable()

    def set_regex(self, regex:str):
        self._regex = regex

    def set_text(self, text:str):
        self._text = text

    def get_cancellable(self) -> Gio.Cancellable:
        return self._cancellable

    def async_finish(self, result:Gio.AsyncResult, caller:GObject.Object):
        if not Gio.Task.is_valid(result, caller):
            return -1
        self._text = None
        self._regex = None
        return result.propagate_value().value

    def find_all_matches_async(self, caller:GObject.Object, callback:callable):
        task = Gio.Task.new(caller, None, callback, self._cancellable)
        task.set_return_on_cancel(True)
        task.run_in_thread(self._find_all_matches_thread)

    def _find_all_matches_thread(self, task:Gio.Task, source_object:GObject.Object, task_data:object, cancelable:Gio.Cancellable):
        if task.return_error_if_cancelled():
            return
        outcome = self._find_all_matches(self._regex, self._text)
        task.return_value(outcome)

    def _find_all_matches(self, regex:str, text:str) -> Iterator:
        p = re.compile(r"{}".format(regex))
        return p.finditer(text)
