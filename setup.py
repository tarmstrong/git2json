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

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='git2json',
    version='0.1.0',
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
