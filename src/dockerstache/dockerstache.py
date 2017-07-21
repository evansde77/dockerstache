#!/usr/bin/env python
"""
_dockerstache_

Main function to invoke dockerstache as a lib call

"""
import os

from .dotfile import Dotfile
from .templates import process_templates, process_copies
from .context import Context
from . import get_logger

LOGGER = get_logger()


def run(**options):
    """
    _run_

    Run the dockerstache process to render templates
    based on the options provided

    If extend_context is passed as options it will be used to
    extend the context with the contents of the dictionary provided
    via context.update(extend_context)

    """
    with Dotfile(options) as conf:
        if conf['context'] is None:
            msg = "No context file has been provided"
            LOGGER.error(msg)
            raise RuntimeError(msg)
        if not os.path.exists(conf['context_path']):
            msg = "Context file {} not found".format(conf['context_path'])
            LOGGER.error(msg)
            raise RuntimeError(msg)
        LOGGER.info(
            (
                "{{dockerstache}}: In: {}\n"
                "{{dockerstache}}: Out: {}\n"
                "{{dockerstache}}: Context: {}\n"
                "{{dockerstache}}: Defaults: {}\n"
            ).format(conf['input'], conf['output'], conf['context'], conf['defaults'])
        )
        context = Context(conf['context'], conf['defaults'])
        context.load()
        if 'extend_context' in options:
            LOGGER.info("{{dockerstache}} Extended context provided")
            context.update(options['extend_context'])

        process_templates(
            conf['input'],
            conf['output'],
            context
            )
        if conf['inclusive']:
            process_copies(
                conf['input'],
                conf['output'],
                conf['exclude']
            )
    return dict(conf)
