#!/usr/bin/env python
"""
dotfile

Utils for reading the .dockerstache file in a template dir and looking
for config/actions found inside it

"""
import os
import six
import json
import subprocess
from . import get_logger


LOGGER = get_logger()


def execute_command(working_dir, cmd, env_dict):
    """
    execute_command: run the command provided in the working dir
    specified adding the env_dict settings to the
    execution environment

    :param working_dir: path to directory to execute command
       also gets added to the PATH
    :param cmd: Shell command to execute
    :param env_dict: dictionary of additional env vars to
      be passed to the subprocess environment

    """
    proc_env = os.environ.copy()
    proc_env["PATH"] = "{}:{}:.".format(proc_env["PATH"], working_dir)
    proc_env.update(env_dict)
    proc = subprocess.Popen(
        cmd,
        cwd=working_dir,
        env=proc_env,
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


def absolute_path(p):
    result = p
    if not os.path.isabs(p):
        result = os.path.join(os.getcwd(), p)
    return os.path.normpath(result)


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
        self.setdefault('output_path', None)
        self.setdefault('context_path', None)
        self.setdefault('defaults_path', None)

    def exists(self):
        """check dotfile exists"""
        return os.path.exists(self.dot_file)

    def load(self):
        """
        read dotfile and populate self
        opts will override the dotfile settings,
        make sure everything is synced in both
        opts and this object

        """
        if self.exists():
            with open(self.dot_file, 'r') as handle:
                self.update(json.load(handle))
        if self.opts.context is not None:
            self['context'] = self.opts.context
        else:
            self.opts.context = self['context']
        if self.opts.defaults is not None:
            self['defaults'] = self.opts.defaults
        else:
            self.opts.defaults = self['defaults']
        if self.opts.output is not None:
            self['output'] = self.opts.output
        else:
            if self['output'] is None:
                output = os.path.join(os.getcwd(), 'dockerstache-output')
                self.opts.output = output
                self['output'] = output
            else:
                self.opts.output = self['output']
        self['output_path'] = self.abs_output_dir()
        if self['context'] is not None:
            self['context_path'] = absolute_path(self['context'])
        if self['defaults'] is not None:
            self['defaults_path'] = absolute_path(self['defaults'])

    def __enter__(self):
        self.load()
        self.pre_script()
        return self

    def __exit__(self, *args):
        self.post_script()

    def abs_input_dir(self):
        """
        compute the abs path to the input dir
        """
        return absolute_path(self.template_dir)

    def abs_output_dir(self):
        """compute absolute output path"""
        return absolute_path(self['output'])

    def env_dictionary(self):
        """
        convert the options to this script into an
        env var dictionary for pre and post scripts
        """
        none_to_str = lambda x: str(x) if x else ""
        return {"DOCKERSTACHE_{}".format(k.upper()): none_to_str(v) for k, v in six.iteritems(self)}

    def pre_script(self):
        """
        execute the pre script if it is defined
        """
        if self['pre_script'] is None:
            return
        LOGGER.info("Executing pre script: {}".format(self['pre_script']))
        cmd = self['pre_script']
        execute_command(self.abs_input_dir(), cmd, self.env_dictionary())
        LOGGER.info("Pre Script completed")

    def post_script(self):
        if self['post_script'] is None:
            return
        LOGGER.info("Executing post script: {}".format(self['post_script']))
        cmd = self['post_script']
        execute_command(self.template_dir, cmd, self.env_dictionary())
        LOGGER.info("Post Script completed")
