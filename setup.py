#!/usr/bin/env python

from setuptools import setup, find_packages

requirements_file = open('requirements.txt')
requirements = requirements_file.read().strip().split('\n')

setup(name='dockerstache',
      version='0.0.3',
      description='Dockerfile mustache templating tools',
      author='Dave Evans',
      author_email='evansde77.github@gmail.com',
      url='https://github.com/evansde77/dockerstache',
      install_requires=requirements,
      packages = find_packages('src'),
      package_dir={'': 'src'},
      entry_points = {
        'console_scripts': ['dockerstache=dockerstache.__main__:main'],
      }
     )
