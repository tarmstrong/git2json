#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Generate a json log of a git repository.
"""

from __future__ import print_function
import json
import sys
from .parser import parse_commits

__author__ = 'Tavish Armstrong'
__email__ = 'tavisharmstrong@gmail.com'
__version__ = '0.2.3'

# -------------------------------------------------------------------
# Main


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--git-dir',
        default=None,
        help='Path to the .git/ directory of the repository you are targeting'
    )
    args = parser.parse_args()
    if sys.version_info < (3, 0):
        print(git2json(run_git_log(args.git_dir)))
    else:
        print(git2jsons(run_git_log(args.git_dir)))

# -------------------------------------------------------------------
# Main API functions


def git2jsons(s):
    return json.dumps(list(parse_commits(s)), ensure_ascii=False)


def git2json(fil):
    return json.dumps(list(parse_commits(fil.read())), ensure_ascii=False)


# -------------------------------------------------------------------
# Functions for interfacing with git


def run_git_log(git_dir=None):
    '''run_git_log([git_dir]) -> File

    Run `git log --numstat --pretty=raw` on the specified
    git repository and return its stdout as a pseudo-File.'''
    import subprocess
    if git_dir:
        command = [
            'git',
            '--git-dir=' + git_dir,
            'log',
            '--numstat',
            '--pretty=raw'
        ]
    else:
        command = ['git', 'log', '--numstat', '--pretty=raw']
    raw_git_log = subprocess.Popen(
        command,
        stdout=subprocess.PIPE
    )
    if sys.version_info < (3, 0):
        return raw_git_log.stdout
    else:
        return raw_git_log.stdout.read().decode('utf-8', 'ignore')
