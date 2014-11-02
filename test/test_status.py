import mug
from mug.verbs import status, output
from mug import repo, utils

NO_CHANGES_OUTPUT="""\
nothing to commit, working directory clean
"""

def test_status_output_no_changes(simplerepo):
    repository = repo.MugRepository('ignore/simplerepo')
    o_stream = output.Output()
    status.run(repository, o_stream, [])
    assert o_stream.value() == NO_CHANGES_OUTPUT


MODIFIED_NOT_STAGED_OUTPUT="""\
Changes not staged for commit:
  (use "mug add <file> ..." to update what will be commited)
  (use "mug checkout -- <file> ..." to discard changes in working directory)

    modified: ignore/simplerepo/file_a.txt
"""

UNTRACKED_FILE_OUTPUT="""\
Untracked files:
  (use "mug add <file> ..." to include in what will be committed)

    ignore/simplerepo/file_x.txt

"""
def test_status_output_working_tree_modified(simplerepo):
    utils.write(simplerepo.workdir, { 'file_a.txt' : 'one\ntwo\three\four\n' })
    repository = repo.MugRepository('ignore/simplerepo')
    o_stream = output.Output()
    status.run(repository, o_stream, [])
    assert o_stream.value() == MODIFIED_NOT_STAGED_OUTPUT

def test_status_untracked_files(simplerepo):
    utils.write(simplerepo.workdir, { 'file_x.txt' : 'one\ntwo\three\four\n' })
    repository = repo.MugRepository('ignore/simplerepo')
    o_stream = output.Output()
    status.run(repository, o_stream, [])
    assert o_stream.value() == UNTRACKED_FILE_OUTPUT

def test_status_output_ignored(simplerepo):
    utils.write(simplerepo.workdir, { 'file_x.hidden' : 'one\ntwo\three\four\n' })
    repository = repo.MugRepository('ignore/simplerepo')
    o_stream = output.Output()
    status.run(repository, o_stream, [])
    assert o_stream.value() == NO_CHANGES_OUTPUT

