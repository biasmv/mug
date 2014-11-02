import shutil
import pytest
import mug.utils
import pygit2
import sys
import os

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
    mug.utils.write_and_commit(repo, contents, 'initial commit')
    mod_a = pygit2.init_repository('ignore/simplerepo/mod_a')
    sub_a_contents = {
        'file_a.txt' : 'one\ntwo\nthree\n'
    }
    mug.utils.write_and_commit(mod_a, sub_a_contents, 'initial commit')
    def fin():
        shutil.rmtree('ignore/simplerepo')
        pass
    request.addfinalizer(fin)
    return repo

