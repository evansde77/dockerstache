#!/usr/bin/env python
"""
_dockerstache_

util package for rendering docker files from mustache templates

"""
import sys
import logging
import logging.handlers
__version__ = "0.0.11"


_LOGGER = {
    "logger": None
}


def get_logger():
    """
    _get_logger_

    Get package logger instance

    """
    if _LOGGER['logger'] is None:
        _LOGGER['logger'] = setup_logger()
    return _LOGGER['logger']


def setup_logger():
    """
    setup basic logger
    """
    logger = logging.getLogger('dockerstache')
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setLevel(logging.INFO)
    logger.addHandler(handler)
    return logger
