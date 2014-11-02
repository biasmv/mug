import shutil
import pytest
import pygit2
import sys
import os
import mug
from mug.repo import MugRepository, NoRepositoryFound

def test_find_mugules_file_in_working_dir(simplerepo):
    repo = MugRepository.discover('ignore/simplerepo')
    assert len(repo.mugules) == 1
    assert os.path.abspath(repo.mugules[0].workdir) == \
           os.path.abspath('ignore/simplerepo/mod_a')

def test_reports_error_when_no_mugules_file_exists(simplerepo):
    with pytest.raises(NoRepositoryFound):
        repo = MugRepository.discover('ignore/simplerepo2')

