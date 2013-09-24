#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
git2json.py

Generate a json log of a git repository.
"""

__author__ = 'Tavish Armstrong'
__email__ = 'tavisharmstrong@gmail.com'
__version__ = '0.1.0'


import re
import json
from itertools import cycle


def parse_hash_line(line, name):
    RE_HASH_LINE = name + r' ([abcdef0-9]+)'
    result = re.match(RE_HASH_LINE, line)
    if result is None:
        return result
    else:
        return result.groups()[0]


def parse_commit_line(line):
    return parse_hash_line(line, 'commit')


def parse_parent_line(line):
    return parse_hash_line(line, 'parent')


def parse_tree_line(line):
    return parse_hash_line(line, 'tree')


def parse_person_line(line, name):
    RE_PERSON = name + r' (.+) <(.*)> (\d+) ([+\-]\d\d\d\d)'
    result = re.match(RE_PERSON, line)
    if result is None:
        return result
    else:
        groups = result.groups()
        name = groups[0]
        email = groups[1]
        timestamp = int(groups[2])
        timezone = groups[3]
        d_result = {
            'name': name,
            'email': email,
            'date': timestamp,
            'timezone': timezone,
        }
        return d_result


def parse_committer_line(line):
    return parse_person_line(line, 'committer')


def parse_author_line(line):
    return parse_person_line(line, 'author')


def parse_message_line(line):
    RE_MESSAGE = r'    (.*)'
    result = re.match(RE_MESSAGE, line)
    if result is None:
        return result
    else:
        return result.groups()[0]


def parse_numstat_line(line):
    RE_NUMSTAT = r'(\d+|-)\W+(\d+|-)\W+(.*)'
    result = re.match(RE_NUMSTAT, line)
    if result is None:
        return result
    else:
        (sadd, sdel, fname) = result.groups()
        try:
            return (int(sadd), int(sdel), fname)
        except ValueError:
            return (sadd, sdel, fname)


def parse_blank_line(line):
    if len(line) == 1 and line == '\n':
        return True
    else:
        return None


def parse_commits(lines):
    '''Read lines from the git log one at a time.

    This parser is hand-rolled and shouldn't be.'''
    lines = iter(lines)
    parsers = [
        (parse_commit_line, 1),
        (parse_tree_line, 1),
        (parse_parent_line, 1),
        (parse_author_line, 1),
        (parse_committer_line, 1),
        (parse_blank_line, 1),
        (parse_message_line, 0),
        (parse_blank_line, 1),
        (parse_numstat_line, 0),
    ]
    iparsers = cycle(iter(parsers))
    parsed_lines = []
    prev_line = None
    try:
        line = lines.next()
        for p, c in iparsers:
            if c == 1:
                if prev_line is None:
                    pass
                else:
                    line = prev_line
                    prev_line = None
                #line = prev_line is None and prev_line or lines.next()
                result = p(line)
                if result is None:
                    continue
                parsed_lines.append((p.__name__, result,))
                line = lines.next()
            else:
                cont = False
                while not cont:
                    result = p(line)
                    if result is None:
                        prev_line = line
                        cont = True
                    else:
                        # More lines of the same type (e.g. message lines)
                        parsed_lines.append((p.__name__, result,))
                        line = lines.next()

    except StopIteration:
        pass

    def empty_commit():
        return {
            'changes': [],
            'message': '',
        }
    final_commits = []
    current_commit = None
    for name, data in parsed_lines:
        if name == 'parse_commit_line':
            if current_commit is not None:
                final_commits.append(current_commit)
            current_commit = empty_commit()
            current_commit['commit'] = data
        elif name == 'parse_tree_line':
            current_commit['tree'] = data
        elif name == 'parse_parent_line':
            current_commit['parent'] = data
        elif name == 'parse_author_line':
            current_commit['author'] = data
        elif name == 'parse_committer_line':
            current_commit['committer'] = data
        elif name == 'parse_message_line':
            if 'message' not in current_commit.keys():
                current_commit['message'] = ''
            current_commit['message'] += data
        elif name == 'parse_numstat_line':
            if 'changes' not in current_commit.keys():
                current_commit['changes'] = []
            current_commit['changes'].append(list(data))
    final_commits.append(current_commit)
    return final_commits


def git2jsons(s):
    lines = s.split('\n')
    return json.dumps(parse_commits(lines))


def git2json(fil):
    lines = fil.xreadlines()
    return json.dumps(parse_commits(lines))


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
    return raw_git_log.stdout


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--git-dir',
        default=None,
        help='Path to the .git/ directory of the repository you are targeting'
    )
    args = parser.parse_args()
    print git2json(run_git_log(args.git_dir))
