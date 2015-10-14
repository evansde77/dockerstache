#!/usr/bin/env python
"""
_dockerstache_

"""
import os
import sys
import argparse
import json
from .templates import process_templates


def build_parser():
    """
    _build_parser_

    Set up CLI parser options, parse the
    CLI options an return the parsed results

    """
    parser = argparse.ArgumentParser(
        description='Diesel docker templating util'
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
        print("Context file {} not found".format(opts.context))
        sys.exit(1)

    with open(opts.context, 'r') as handle:
        context = json.load(handle)

    process_templates(
        opts.input,
        opts.output,
        context
        )


if __name__ == '__main__':
    main()
