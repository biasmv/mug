import pygit2
import os
import collections

class NoRepositoryFound(IOError):
    def __init__(self, initial_dir):
        self.initial_dir = initial_dir
    def __str__(self):
        return 'No mug repository found.'

class NoSuchMuguleFound(IOError):
    def __init__(self, name, path):
        self.name = name
        self.path = path
    def __str__(self):
        return 'No mugule "%s" found at path "%s"' % (self.name, self.path)

class MugRepository:
    """
    A multi-git repository, is a git repository which contains references to
    other git repositories, so-called mugules. Mugules and the main repository 
    are thought to be developed in sync, meaning that branches of the main
    repository and the sub-repository must match.
    """
    def __init__(self, directory):
        self._repo = pygit2.Repository(os.path.join(directory, '.git'))
        mugules = MugRepository.read_mugules_file(directory)
        self._mugules = []
        for repo_name in mugules:
            sub_repo_path = os.path.join(self._repo.workdir, repo_name, '.git')
            try:
                repo = pygit2.Repository(sub_repo_path)
                self._mugules.append(repo)
            except KeyError as error:
                raise NoSuchMuguleFound(repo_name, sub_repo_path)

    @property
    def sub_repositories(self):
        """
        The mugules contained in this mug repository
        """
        return self._mugules
    @property
    def all_repositories(self):
        return [self._repo] + self._mugules

    @property
    def main_repository(self):
        return self._repo

    @staticmethod
    def discover(initial_path):
        """
        Discovers the mug repositories. It recursively walks from the current 
        working directory and looks for a .mugules files. If it does not find 
        such a file an exception is raised.

        Upon success, a MugRepository is returned.
        """
        mugules_root = MugRepository.discover_mugules_root(initial_path)
            
        return MugRepository(mugules_root)

    @staticmethod
    def discover_mugules_root(initial_dir):
        current = initial_dir
        while True:
            mugules_file = os.path.join(current, '.mugules')
            if os.path.exists(mugules_file):
                return current
            next_dir = os.path.dirname(current)
            if next_dir == current:
                raise NoRepositoryFound(initial_dir)
            current = next_dir

    def files_by_repo(self, file_names):
        """
        Associates file names with the correct repository. Returns a map of repo -> 
        relative_filenames. 
        """
        main = self.main_repository
        sub_repositories = self.sub_repositories
        repo_file_name_map = collections.defaultdict(list)
        for file_name in file_names:
            for sub in sub_repositories:
                rel_path = os.path.relpath(file_name, sub.workdir)
                if rel_path.startswith('..'):
                    continue
                repo_file_name_map[sub].append(rel_path)
                break
            else:
                rel_path = os.path.relpath(file_name, main.workdir)
                repo_file_name_map[main].append(rel_path)
        return repo_file_name_map

    @staticmethod
    def read_mugules_file(directory):
        mugules = []
        with open(os.path.join(directory, '.mugules'), 'r') as mf:
            for line in mf:
                line = line.strip()
                if len(line) == 0 or line.startswith('#'):
                    continue
                mugules.append(line.split(':')[0])
        return mugules
    

