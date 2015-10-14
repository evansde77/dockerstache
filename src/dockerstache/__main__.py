#!/usr/bin/env python
"""
_dockerstache_

"""
import os
import argparse


def build_parser():
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

    opts = parser.parse_args()
    return opts

def main():
    opts = build_parser()


if __name__ == '__main__':
    main()
