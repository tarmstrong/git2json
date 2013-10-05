import git2json as g


def test_regex_only():
    commit = (
        'commit 78a7baf74a77055e25914f2d50812c92bd6243bf'
        '\ntree b72a934faf0e0bd3a333a6069cc67dd74114bb9b'
        '\nparent a4d8c6dbab70038b4585f7711873e71f92db47bf'
        '\nparent a4d8c6dbab70038b4585f7711873e71f92db47bf'
        '\nauthor Tavish Armstrong'
        ' <tavisharmstrong@gmail.com> 1380495019 -0400'
        '\ncommitter Tavish Armstrong'
        ' <tavisharmstrong@gmail.com> 1380495019 -0400'
        '\n\n    Start examples section in the README\n'
        '\n9\t0\tREADME.rst\n9\t0\tREADME.rst\n\n'
    )

    from git2json.parser import RE_COMMIT

    matches = RE_COMMIT.findall(commit)
    assert len(matches) > 0


def test_parse_commits():
    commit = (
        'commit 78a7baf74a77055e25914f2d50812c92bd6243bf'
        '\ntree b72a934faf0e0bd3a333a6069cc67dd74114bb9b'
        '\nparent a4d8c6dbab70038b4585f7711873e71f92db47bf'
        '\nparent a4d8c6dbab70038b4585f7711873e71f92db47bf'
        '\nauthor Tavish Armstrong'
        ' <tavisharmstrong@gmail.com> 1380495019 -0400'
        '\ncommitter Tavish Armstrong'
        ' <tavisharmstrong@gmail.com> 1380495019 -0400'
        '\n\n    Start examples section in the README\n'
        '\n9\t0\tREADME.rst\n9\t0\tREADME.rst\n\n'
    )

    parsed = list(g.parse_commits(commit))
    assert len(parsed) > 0
