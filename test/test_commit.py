import mug
import pygit2


from mug.verbs import commit, output
from mug import repo, utils

def test_commit_with_nothing_to_commit_does_not_do_anything(simplerepo):
    output_stream = output.Output()
    repository = repo.MugRepository('ignore/simplerepo')
    commit.run(repository, output_stream, [])


