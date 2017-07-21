#!/usr/bin/env python
"""
_templates_

Find templates, render templates etc

"""
import os
import functools
import pystache
import shutil
from . import get_logger


LOGGER = get_logger()


def dir_visitor(dirname, visitor):
    """
    _dir_visitor_

    walk through all files in dirname, find
    directories and call the callable on them.

    :param dirname: Name of directory to start visiting,
      all subdirs will be visited
    :param visitor: Callable invoked on each dir visited
    """
    visitor(dirname)
    for obj in os.listdir(dirname):
        obj_path = os.path.join(dirname, obj)
        if os.path.isdir(obj_path):
            dir_visitor(obj_path, visitor)


def replicate_directory_tree(input_dir, output_dir):
    """
    _replicate_directory_tree_

    clone dir structure under input_dir into output dir
    All subdirs beneath input_dir will be created under
    output_dir
    :param input_dir: path to dir tree to be cloned
    :param output_dir: path to new dir where dir structure will
       be created
    """
    def transplant_dir(target, dirname):
        x = dirname.replace(input_dir, target)
        if not os.path.exists(x):
            LOGGER.info('Creating: {}'.format(x))
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

    :param input_dir: Path to start recursive search for
       mustache templates
    :returns: List of file paths corresponding to templates
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


def find_copies(input_dir, exclude_list):
    """
    find files that are not templates and not
    in the exclude_list for copying from template to image
    """
    copies = []

    def copy_finder(copies, dirname):
        for obj in os.listdir(dirname):
            pathname = os.path.join(dirname, obj)
            if os.path.isdir(pathname):
                continue
            if obj in exclude_list:
                continue
            if obj.endswith('.mustache'):
                continue

            copies.append(os.path.join(dirname, obj))

    dir_visitor(
        input_dir,
        functools.partial(copy_finder, copies)
    )
    return copies


def render_template(template_in, file_out, context):
    """
    _render_template_

    Render a single template file, using the context provided
    and write the file out to the location specified

    #TODO: verify the template is completely rendered, no
       missing values

    """
    renderer = pystache.Renderer()
    result = renderer.render_path(template_in, context)
    with open(file_out, 'w') as handle:
        LOGGER.info('Rendering: {} to {}'.format(template_in, file_out))
        handle.write(result)


def copy_file(src, target):
    """
    copy_file

    copy source to target

    """
    LOGGER.info("Copying {} to {}".format(src, target))
    shutil.copyfile(src, target)


def process_templates(input_dir, target_dir, context):
    """
    _process_templates_

    Given the input dir containing a set of template,
    clone the structure under that directory into the target dir
    using the context to process any mustache templates that
    are encountered

    """
    if not target_dir.endswith('/'):
        target_dir = "{}/".format(target_dir)
    if not os.path.exists(target_dir):
        LOGGER.info('Creating: {}'.format(target_dir))
        os.makedirs(target_dir)
    replicate_directory_tree(input_dir, target_dir)
    templates = find_templates(input_dir)
    for templ in templates:
        output_file = templ.replace(input_dir, target_dir)
        output_file = output_file[:-len('.mustache')]
        render_template(templ,  output_file, context)


def process_copies(input_dir, target_dir, excludes):
    """
    _process_copies_

    Handles files to be copied across, assumes
    that dir structure has already been replicated

    """
    copies = find_copies(input_dir, excludes)
    for c in copies:
        output_file = c.replace(input_dir, target_dir)
        copy_file(c,  output_file)

