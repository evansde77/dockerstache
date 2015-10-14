#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='dockerstache',
      version='0.0.0',
      description='Dockerfile mustache templating tools',
      author='Dave Evans',
      author_email='evansde77.github@gmail.com',
      url='https://github.com/evansde77/dockerstache',
      packages = find_packages('src'),
      package_dir={'': 'src'},
      entry_points = {
        'console_scripts': ['dockerstache=dockerstache.__main__:main'],
      }
     )
