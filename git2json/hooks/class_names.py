'''
Get class names from every file changed in the commit.
'''

import re
import ast


def mod_commit(executor, commit_data):
    commit_hash = commit_data['commit']
    changed_files = [
        change[2]
        for change in commit_data['changes']
        if re.match(r'.*py$', change[2])
    ]
    file_classes = {}
    for file in changed_files:
        contents = executor.run_git_show(commit_hash, file)
        try:
            tree = ast.parse(contents)
            classes = [e for e in tree.body if type(e) == ast.ClassDef]
            names = [c.name for c in classes]
            file_classes[file] = names
        except SyntaxError:
            file_classes[file] = 'Error'
    commit_data['classes'] = file_classes
    return commit_data
