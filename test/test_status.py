import shutil
import pytest
import pygit2
import sys
import os
import mug
from mug.verbs import status, output
from mug import repo

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
        tree = repo.revparse_single('HEAD').tree
        parents.append(tree.oid)
    repo.create_commit('HEAD', author, committer, message, tree_id, parents) 
    index.write()

@pytest.fixture
def simplerepo(request):
    # simple fixture with a project and a mugule
    repo = pygit2.init_repository('ignore/simplerepo')
    contents = {
        'file_a.txt' : 'abc\nabc\n',
        'file_b.txt' : 'xyz\nabc\n',
        '.mugules' : 'mod_a: ignore/mod_a\n',
        '.gitignore' : 'mod_a\n'
    }
    write_and_commit(repo, contents, 'initial commit')
    mod_a = pygit2.init_repository('ignore/simplerepo/mod_a')
    sub_a_contents = {
        'file_a.txt' : 'one\ntwo\nthree\n'
    }
    write_and_commit(mod_a, sub_a_contents, 'initial commit')
    def fin():
        shutil.rmtree('ignore/simplerepo')
        pass
    request.addfinalizer(fin)
    return repo

NO_CHANGES_OUTPUT="""\
nothing to commit, working directory clean
"""

def test_status_output_no_changes(simplerepo):
    st = status.Status()
    repository = repo.MugRepository('ignore/simplerepo')
    o_stream = output.Output()
    st.run(repository, o_stream, [])
    assert o_stream.value() == NO_CHANGES_OUTPUT


MODIFIED_NOT_STAGED_OUTPUT="""\
Changes not staged for commit:
  (use "mug add <file> ..." to update what will be commited)
  (use "mug checkout -- <file> ..." to discard changes in working directory)

    modified: ignore/simplerepo/file_a.txt
"""

def test_status_output_working_tree_modified(simplerepo):
    st = status.Status()
    write(simplerepo.workdir, { 'file_a.txt' : 'one\ntwo\three\four\n' })

    repository = repo.MugRepository('ignore/simplerepo')
    o_stream = output.Output()
    st.run(repository, o_stream, [])
    assert o_stream.value() == MODIFIED_NOT_STAGED_OUTPUT

