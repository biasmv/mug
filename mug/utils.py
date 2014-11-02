"""
Some utility functions for testing
"""
import sys
import pygit2
import os

def write(base, contents):
    for file_name, data in contents.iteritems():
        full_name = os.path.join(base, file_name)
        dir_name = os.path.dirname(full_name)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        with open(full_name, 'w') as fd:
            fd.write(data)


DEFAULT_COMMITTER = pygit2.Signature('Oskar Brille', 'brillenoski@example.com')
DEFAULT_AUTHOR = pygit2.Signature('Oskar Brille', 'brillenoski@example.com')

def write_and_commit(repo, contents, message, author=DEFAULT_AUTHOR,
                     committer=DEFAULT_COMMITTER):
    """
    Helper function to update contents of files and commit the result
    """
    write(repo.workdir, contents)
    index = repo.index
    for file_name in contents.keys():
        index.add(file_name)
    tree_id = index.write_tree()
    parents = []
    if not repo.is_empty:
        parents.append(repo.revparse_single('HEAD').oid)
    repo.create_commit('HEAD', author, committer, message, tree_id, parents) 
    index.write()

