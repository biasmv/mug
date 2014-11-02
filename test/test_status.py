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

def test_status_output_working_tree_modified(simplerepo):
    utils.write(simplerepo.workdir, { 'file_a.txt' : 'one\ntwo\three\four\n' })

    repository = repo.MugRepository('ignore/simplerepo')
    o_stream = output.Output()
    status.run(repository, o_stream, [])
    assert o_stream.value() == MODIFIED_NOT_STAGED_OUTPUT

