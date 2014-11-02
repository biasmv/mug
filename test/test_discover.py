import shutil
import pytest
import pygit2
import sys
import os
import mug
from mug.repo import MugRepository, NoRepositoryFound

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
    request.addfinalizer(fin)
    return repo

def test_find_mugules_file_in_working_dir(simplerepo):
    repo = MugRepository.discover('ignore/simplerepo')
    assert len(repo.mugules) == 1
    assert os.path.abspath(repo.mugules[0].workdir) == \
           os.path.abspath('ignore/simplerepo/mod_a')

def test_reports_error_when_no_mugules_file_exists(simplerepo):
    with pytest.raises(NoRepositoryFound):
        repo = MugRepository.discover('ignore/simplerepo2')

