import mug
import pygit2


from mug.verbs import commit, output
from mug import repo, utils

UNTRACKED_FILE_OUTPUT="""\
Untracked files:
  (use "mug add <file> ..." to include in what will be committed)

    ignore/simplerepo/untracked.txt

"""

SPLIT_BY_REPOSITORY_OUTPUT="""\
Changes to be committed:
  (use "mug reset HEAD <file> ..." to unstage)

    modified: ignore/simplerepo/file_a.txt
    modified: ignore/simplerepo/mod_a/file_a.txt

ERROR: Files of multiple repositories are staged for commit. Split the
commits by repository.
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
    assert output_stream.value() == 'nothing to commit, working directory clean\n'

def test_commit_all_adds_files_to_index(simplerepo):
    output_stream = output.Output()
    repository = repo.MugRepository('ignore/simplerepo')
    utils.write(simplerepo.workdir, {'file_a.txt' : 'one\n'})
    commit.run(repository, output_stream, ['--all', '-m', 'updating contents of file_a.txt'])
    assert output_stream.value() == ''

def test_commit_aborts_when_files_are_staged_for_multiple_repositories(simplerepo):
    output_stream = output.Output()
    repository = repo.MugRepository('ignore/simplerepo')
    utils.write(simplerepo.workdir, {
        'file_a.txt' : 'one\n', 'mod_a/file_a.txt' : 'xxx\n'})
    commit.run(repository, output_stream, ['--all', '-m', 'updating contents of file_a.txt'])
    assert output_stream.value() == SPLIT_BY_REPOSITORY_OUTPUT


