import mug
import pygit2


from mug.verbs import add, output
from mug import repo, utils

def test_add_in_main_repository(simplerepo):
    utils.write(simplerepo.workdir, { 'file_a.txt' : 'one\ntwo\three\four\n' })
    output_stream = output.Output()
    repository = repo.MugRepository('ignore/simplerepo')
    add.run(repository, output_stream, ['ignore/simplerepo/file_a.txt'])
    assert simplerepo.status_file('file_a.txt') == pygit2.GIT_STATUS_INDEX_MODIFIED




def test_add_in_sub_repository(simplerepo):
    utils.write(simplerepo.workdir, { 'mod_a/file_a.txt' : 'one\ntwo\three\four\n' })
    output_stream = output.Output()
    repository = repo.MugRepository('ignore/simplerepo')
    add.run(repository, output_stream, ['ignore/simplerepo/mod_a/file_a.txt'])
    r = pygit2.Repository('ignore/simplerepo/mod_a/.git')
    assert r.status_file('file_a.txt') == pygit2.GIT_STATUS_INDEX_MODIFIED


