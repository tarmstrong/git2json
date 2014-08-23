#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

with open('README.rst') as file_readme:
    readme = file_readme.read()

with open('HISTORY.rst') as file_history:
    history = file_history.read().replace('.. :changelog:', '')

setup(
    name='git2json',
    version='0.2.3',
    description='Convert git logs to JSON for easier analysis.',
    long_description=readme + '\n\n' + history,
    author='Tavish Armstrong',
    author_email='tavisharmstrong@gmail.com',
    url='https://github.com/tarmstrong/git2json',
    packages=[
        'git2json',
    ],
    package_dir={'git2json': 'git2json'},
    entry_points={'console_scripts': ['git2json = git2json:main']},
    include_package_data=True,
    install_requires=[
    ],
    license="BSD",
    zip_safe=False,
    keywords='git2json',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
    test_suite='tests',
)
