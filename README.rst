===============================
Git2JSON
===============================

.. image:: https://badge.fury.io/py/git2json.png
    :target: http://badge.fury.io/py/git2json
    
.. image:: https://travis-ci.org/tarmstrong/git2json.png?branch=master
        :target: https://travis-ci.org/tarmstrong/git2json

.. image:: https://pypip.in/d/git2json/badge.png
        :target: https://crate.io/packages/git2json?version=latest


Convert git logs to JSON for easier analysis.

* Free software: BSD license
* Documentation: http://git2json.rtfd.org.

Usage
-----

::

    usage: git2json [-h] [--git-dir GIT_DIR]

    optional arguments:
      -h, --help         show this help message and exit
      --git-dir GIT_DIR  Path to the .git/ directory of the repository you are
                        targeting


The resulting JSON log is printed to standard output.

Example JSON
------------

The following shows the structure of the JSON emitted by the tool.

::

    [{
        "committer": {
            "date": 1379903278,
            "timezone": "-0400",
            "name": "Tavish Armstrong",
            "email": "tavisharmstrong@gmail.com"
        },
        "parent": "e307663594031738c932877c8589552d5aafc953",
        "author": {
            "date": 1379903278,
            "timezone": "-0400",
            "name": "Tavish Armstrong",
            "email": "tavisharmstrong@gmail.com"
        },
        "tree": "bd03127651335e3a51241f507f3bf194d8336485",
        "commit": "d06454c160218b4a782afad2429abda1add54df0",
        "message": "Allow user to specify git-dir on the command line.",
        "changes": [
            [23, 3, "git2json/__init__.py"]
        ]
        },
        // ... More commits
        ]

