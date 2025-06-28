# Copyright (C) 2022 - 2025 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from io import StringIO
from gi.repository import Gio, GObject
import ruamel.yaml
import json

import datetime

class ExtendedJSONEncoder(json.JSONEncoder):

    def default(self, value):
        if isinstance(value, datetime.datetime):
            return value.timestamp()
        if isinstance(value, datetime.date):
            return value.strftime("%Y-%m-%d")
        if isinstance(value, ruamel.yaml.comments.CommentedSet):
            return list(value)
        return super().default(value)

class JsonYamlService():

    def __init__(self):
        self._cancellable = Gio.Cancellable()

    def _convert_json_to_yaml_thread(self, task:Gio.Task, source_object:GObject.Object, task_data:object, cancelable:Gio.Cancellable):
        if task.return_error_if_cancelled():
            return
        outcome = self._convert_json_to_yaml(self._input_string, self._input_indents)
        task.return_value(outcome)

    def _convert_yaml_to_json_thread(self, task:Gio.Task, source_object:GObject.Object, task_data:object, cancelable:Gio.Cancellable):
        if task.return_error_if_cancelled():
            return
        outcome = self._convert_yaml_to_json(self._input_string, self._input_indents)
        task.return_value(outcome)

    def _convert_json_to_yaml(self, json_str:str, indents:int) -> str:
        yaml = ruamel.yaml.YAML(typ=['rt'])
        yaml.indent(mapping=indents, sequence=indents, offset=indents)
        stream = StringIO()
        yaml.dump(json.loads(json_str), stream)
        return  stream.getvalue()

    def _convert_yaml_to_json(self, yaml_str:str, indents:int) -> str:
        yaml = ruamel.yaml.YAML(typ='rt')

        return json.dumps(
            yaml.load(yaml_str),
            indent=indents,
            ensure_ascii=False,
            cls=ExtendedJSONEncoder,
        )

    def convert_json_to_yaml_async(self, caller:GObject.Object, callback:callable):
        task = Gio.Task.new(caller, None, callback, self._cancellable)
        task.set_return_on_cancel(True)
        task.run_in_thread(self._convert_json_to_yaml_thread)

    def convert_yaml_to_json_async(self, caller:GObject.Object, callback:callable):
        task = Gio.Task.new(caller, None, callback, self._cancellable)
        task.set_return_on_cancel(True)
        task.run_in_thread(self._convert_yaml_to_json_thread)

    def convert_async_finish(self, result:Gio.AsyncResult, caller:GObject.Object):
        if not Gio.Task.is_valid(result, caller):
            return -1
        self._input_string = None
        self._input_indents = None
        return result.propagate_value().value

    def get_cancellable(self) -> Gio.Cancellable:
        return self._cancellable

    def set_input_string(self, input:str):
        self._input_string = input

    def set_input_indents(self, indents:int=4):
        self._input_indents = indents
