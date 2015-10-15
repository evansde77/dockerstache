#!/usr/bin/env python
"""
_context_

Util for merging JSON files and building the dictionary
for rendering

"""
import os
import json
from . import get_logger


LOGGER = get_logger()


class Context(dict):
    """
    _Context_

    Util wrapper around a dict to load json files in
    precedence and build a dictionary for rendering
    templates

    """
    def __init__(self, jsonfile=None, defaultfile=None):
        super(Context, self).__init__()
        self._defaults = {}
        self._defaults_file = defaultfile
        self._settings_file = jsonfile

    def load(self):
        """
        _load_

        Load the defaults file if specified
        and overlay the json file on top of that

        """
        if self._defaults_file is not None:
            if not os.path.exists(self._defaults_file):
                msg = "Unable to find defaults file: {}".format(self._defaults_file)
                LOGGER.error(msg)
                raise RuntimeError(msg)
            with open(self._defaults_file, 'r') as handle:
                self._defaults = json.load(handle)
                self.update(self._defaults)

        if not os.path.exists(self._settings_file):
                msg = "Unable to find settings file: {}".format(self._settings_file)
                LOGGER.error(msg)
                raise RuntimeError(msg)
        with open(self._settings_file, 'r') as handle:
            settings = json.load(handle)
            self.update(settings)

        return
