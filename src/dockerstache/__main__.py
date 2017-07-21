#!/usr/bin/env python
"""
_dockerstache_

"""
import os
import sys
import argparse

from . import get_logger
from .dockerstache import run


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
        default=None
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
        default=None
    )
    parser.add_argument(
        '--defaults', '-d',
        help='JSON file containing default context dictionary to render templates',
        dest='defaults',
        default=None
    )
    parser.add_argument(
        '--inclusive',
        help='include non .mustache files from template',
        default=False,
        action='store_true'
    )
    parser.add_argument(
        '--exclude', '-e',
        help='exclude files from template in this list',
        default=[],
        nargs='+'
    )
    opts = parser.parse_args()
    return vars(opts)


def main():
    """
    _main_

    Create a CLI parser and use that to run
    the template rendering process

    """
    options = build_parser()
    try:
        run(**options)
    except RuntimeError as ex:
        msg = (
            "An error occurred running dockerstache: {} "
            "please see logging info above for details"

        ).format(ex)
        LOGGER.error(msg)
        sys.exit(1)

if __name__ == '__main__':
    main()
