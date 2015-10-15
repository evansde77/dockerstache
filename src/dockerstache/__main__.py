#!/usr/bin/env python
"""
_dockerstache_

"""
import os
import sys
import argparse
import json

from .templates import process_templates
from .context import Context
from . import get_logger

LOGGER = get_logger()


def build_parser():
    """
    _build_parser_

    Set up CLI parser options, parse the
    CLI options an return the parsed results

    """
    parser = argparse.ArgumentParser(
        description='dockerstache templating util'
    )
    parser.add_argument(
        '--output', '-o',
        help='Working directory to render dockerfile and templates',
        dest='output',
        default=os.path.join(os.getcwd(), 'diesel_output')
        )
    parser.add_argument(
        '--input', '-i',
        help='Working directory containing dockerfile and script mustache templates',
        dest='input',
        default=os.getcwd()
        )
    parser.add_argument(
        '--context', '-c',
        help='JSON file containing context dictionary to render templates',
        dest='context',
        required=True
    )
    parser.add_argument(
        '--defaults', '-d',
        help='JSON file containing default context dictionary to render templates',
        dest='defaults',
        default=None
    )

    opts = parser.parse_args()
    return opts


def main():
    """
    _main_

    Create a CLI parser and use that to run
    the template rendering process

    """
    opts = build_parser()
    if not os.path.exists(opts.context):
        msg = "Context file {} not found".format(opts.context)
        LOGGER.error(msg)
        sys.exit(1)
    LOGGER.info(
        (
            "{{dockerstache}}: In: {}\n"
            "{{dockerstache}}: Out: {}\n"
            "{{dockerstache}}: Context: {}\n"
            "{{dockerstache}}: Defaults: {}\n"
        ).format(opts.input, opts.output, opts.context, opts.defaults)
    )
    context = Context(opts.context, opts.defaults)
    context.load()

    process_templates(
        opts.input,
        opts.output,
        context
        )


if __name__ == '__main__':
    main()
