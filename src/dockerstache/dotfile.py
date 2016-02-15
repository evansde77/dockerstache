#!/usr/bin/env python
"""
dotfile

Utils for reading the .dockerstache file in a template dir and looking
for config/actions found inside it

"""
import os
import json
import subprocess
from . import get_logger


LOGGER = get_logger()


def execute_command(working_dir, cmd):
    proc = subprocess.Popen(
        cmd,
        cwd=working_dir,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    status = proc.wait()
    stdout, stderr = proc.communicate()
    if status:
        msg = (
            "Non zero {} exit from command {}\n"
            "Stdout: {}\n"
            "Stderr: {}\n"
        ).format(status, cmd, stdout, stderr)
        LOGGER.error(msg)
        raise RuntimeError(msg)
    LOGGER.info(stdout)


class Dotfile(dict):
    """
    object to encapsulate access to the .dockerstache
    file in a template

    """
    def __init__(self, opts):
        super(Dotfile, self).__init__()
        self.opts = opts
        self.template_dir = opts.input
        self.dot_file = os.path.join(self.template_dir, '.dockerstache')
        self.setdefault('pre_script', None)
        self.setdefault('post_script', None)
        self.setdefault('context', None)
        self.setdefault('defaults', None)
        self.setdefault('output', None)

    def exists(self):
        """check dotfile exists"""
        return os.path.exists(self.dot_file)

    def load(self):
        """read dotfile and populate self"""
        if self.exists():
            with open(self.dot_file, 'r') as handle:
                self.update(json.load(handle))
        if self.opts.context is None:
            self.opts.context = self['context']
        if self.opts.defaults is None:
            self.opts.defaults = self['defaults']
        if self.opts.output is None:
            self.opts.output = self['output']

    def __enter__(self):
        self.load()
        self.pre_script()
        return self

    def __exit__(self, *args):
        self.post_script()

    def pre_script(self):
        if self['pre_script'] is None:
            return
        LOGGER.info("Executing pre script: {}".format(self['pre_script']))
        cmd = self['pre_script']
        execute_command(self.template_dir, cmd)

    def post_script(self):
        if self['post_script'] is None:
            return
        LOGGER.info("Executing post script: {}".format(self['post_script']))
        cmd = self['post_script']
        execute_command(self.template_dir, cmd)
