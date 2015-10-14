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
    for obj in os.listdir(dirname):
        obj_path = os.path.join(dirname, obj)
        if os.path.isdir(obj_path):
            callable(dirname)
            dir_visitor(obj_path, callable)


def replicate_directory_tree(input_dir, output_dir):
    """
    _replicate_directory_tree_

    clone dir structure under input_dir into output dir
    """
    def transplant_dir(target, dirname):
        print "transplant_dir({},{})".format(target, dirname)

    dir_visitor(input_dir, functools.partial(transplant_dir, output_dir))


def find_templates(input_dir):
    """
    _find_templates_

    traverse the input_dir structure and return a list
    of template files ending with .mustache
    """
    pass


if __name__ == '__main__':
    dname = '/Users/david/Documents/work/docker/try_again/test1'
    oname = '/Users/david/Documents/work/docker/try_again/test_output'
    replicate_directory_tree(dname, oname)