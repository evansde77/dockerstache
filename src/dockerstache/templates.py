#!/usr/bin/env python
"""
_templates_

Find templates, render templates etc

"""
import os
import functools


def dir_visitor(dirname, callable):
    """
    _dir_visitor_

    walk through all files in dirname, find
    directories and call the callable on them

    """
    callable(dirname)
    for obj in os.listdir(dirname):
        obj_path = os.path.join(dirname, obj)
        if os.path.isdir(obj_path):
            dir_visitor(obj_path, callable)


def replicate_directory_tree(input_dir, output_dir):
    """
    _replicate_directory_tree_

    clone dir structure under input_dir into output dir
    """
    def transplant_dir(target, dirname):
        x = dirname.replace(input_dir, target)
        if not os.path.exists(x):
            os.makedirs(x)

    dir_visitor(
        input_dir,
        functools.partial(transplant_dir, output_dir)
    )


def find_templates(input_dir):
    """
    _find_templates_

    traverse the input_dir structure and return a list
    of template files ending with .mustache
    """
    templates = []

    def template_finder(result, dirname):
        for obj in os.listdir(dirname):
            if obj.endswith('.mustache'):
                result.append(os.path.join(dirname, obj))

    dir_visitor(
        input_dir,
        functools.partial(template_finder, templates)
    )
    return templates

