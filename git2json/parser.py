#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Parse git logs.

These parsing functions expect output of the following command:

    git log --pretty=raw --numstat

"""

import re

__author__ = 'Tavish Armstrong'
__email__ = 'tavisharmstrong@gmail.com'
__version__ = '0.2.1'

PAT_COMMIT = r'''
(
commit\ (?P<commit>[a-f0-9]+)\n
tree\ (?P<tree>[a-f0-9]+)\n
(?P<parents>(parent\ [a-f0-9]+\n)*)
(?P<author>author \s+(.+)\s+<(.*)>\s+(\d+)\s+([+\-]\d\d\d\d)\n)
(?P<committer>committer \s+(.+)\s+<(.*)>\s+(\d+)\s+([+\-]\d\d\d\d)\n)\n
(?P<message>
(\ \ \ \ .*\n)*
)
\n
(?P<numstats>
(^(\d+|-)\s+(\d+|-)\s+(.*)$\n)*
)
)
'''
RE_COMMIT = re.compile(PAT_COMMIT, re.MULTILINE | re.VERBOSE)

# -------------------------------------------------------------------
# Main parsing functions


def parse_commits(data):
    '''Accept a string and parse it into many commits.
    Parse and yield each commit-dictionary.
    This function is a generator.
    '''
    raw_commits = RE_COMMIT.finditer(data)
    for rc in raw_commits:
        full_commit = rc.groups()[0]
        parts = RE_COMMIT.match(full_commit).groupdict()
        parsed_commit = parse_commit(parts)
        yield parsed_commit


def parse_commit(parts):
    '''Accept a parsed single commit. Some of the named groups
    require further processing, so parse those groups.
    Return a dictionary representing the completely parsed
    commit.
    '''
    commit = {}
    commit['commit'] = parts['commit']
    commit['tree'] = parts['tree']
    parent_block = parts['parents']
    commit['parents'] = [
        parse_parent_line(parentline)
        for parentline in
        parent_block.splitlines()
    ]
    commit['author'] = parse_author_line(parts['author'])
    commit['committer'] = parse_committer_line(parts['committer'])
    commit['message'] = "\n".join(
        parse_message_line(msgline)
        for msgline in
        parts['message'].splitlines()
    )
    commit['changes'] = [
        parse_numstat_line(numstat)
        for numstat in
        parts['numstats'].splitlines()
    ]
    return commit


# -------------------------------------------------------------------
# Parsing helper functions


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
    RE_NUMSTAT = r'(\d+|-)\s+(\d+|-)\s+(.*)'
    result = re.match(RE_NUMSTAT, line)
    if result is None:
        return result
    else:
        (sadd, sdel, fname) = result.groups()
        try:
            return (int(sadd), int(sdel), fname)
        except ValueError:
            return (sadd, sdel, fname)
