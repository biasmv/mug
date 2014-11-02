import pygit2
import os

class Verb:
  def __init__(self, name):
    self.name = name
    self._repositories = []

  def _discover_mugules_root(self):
    current = os.getcwd()
    while True:
      mugules_file = os.path.join(current, '.mugules')
      if os.path.exists(mugules_file):
        return current
      next_dir = os.path.dirname(current)
      if next_dir == current:
        raise ValueError('no such repository')
      current = next_dir
  def _read_mugules_file(self, directory):
    mugules = []
    with open(os.path.join(directory, '.mugules'), 'r') as mf:
      for line in mf:
        line = line.strip()
        if len(line) == 0 or line.startswith('#'):
          continue
        mugules.append(line.split(':')[0])
    return mugules
    

  def _discover(self):
    """
    Discovers the mug repositories. It recursively walks from the current 
    working directory and looks for a .mugules files. If it does not find 
    such a file an exception is raised.

    Upon success, a list of sub repositories is returned.
    """
    mugules_root = self._discover_mugules_root()
    mugules = self._read_mugules_file(mugules_root)
    repositories = [pygit2.Repository(os.path.join(mugules_root, '.git'))]
    for repo_name in mugules:
        sub_repo_path = os.path.join(mugules_root, repo_name, '.git')
        try:
            repo = pygit2.Repository(sub_repo_path)
            repositories.append(repo)
        except KeyError as error:
            raise ValueError('mug module %s (at path \'%s\') does not exists' % (repo_name, sub_repo_path))
        
    return repositories



  @property
  def all_repositories(self):
    """
    Returns the list of pygit2 repositories of which the multi-git
    project is compromised of. 
    """
    if len(self._repositories) == 0:
      self._repositories = self._discover()
    return self._repositories

  @property
  def main_repository(self):
    return self.all_repositories[0]
  @property
  def all_submugules(self):
    return self.all_repositories[1:]


