import pygit2
import os

class Verb:
  def __init__(self, name):
    self.name = name
    self._repositories = []




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


