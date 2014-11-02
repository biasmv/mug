import mug
import pygit2


from mug.verbs import commit, output
from mug import repo, utils

UNTRACKED_FILE_OUTPUT="""\
Untracked files:
  (use "mug add <file> ..." to include in what will be committed)

    ignore/simplerepo/untracked.txt

"""
def test_commit_with_untracked_files_but_nothing_to_commit_shows_status(simplerepo):
    output_stream = output.Output()
    repository = repo.MugRepository('ignore/simplerepo')
    utils.write(simplerepo.workdir, {'untracked.txt' : 'one\n'})
    commit.run(repository, output_stream, [])
    assert output_stream.value() == UNTRACKED_FILE_OUTPUT

def test_commit_with_nothing_to_commit_shows_status(simplerepo):
    output_stream = output.Output()
    repository = repo.MugRepository('ignore/simplerepo')
    commit.run(repository, output_stream, [])
    output_stream.value() == 'nothing to commit'


