import os
import pygit2
import verb
import collections

UNTRACKED_HEADER = """\
Untracked files:
  (use "mug add <file> ..." to include in what will be committed)
"""
TO_BE_COMMITTED_HEADER = """\
Changes to be committed:
  (use "mug reset HEAD <file> ..." to unstage)
"""

NOT_STAGED_FOR_COMMIT_HEADER = """\
Changes not staged for commit:
  (use "mug add <file> ..." to update what will be commited)
  (use "mug checkout -- <file> ..." to discard changes in working directory)
"""
class Status(verb.Verb):
  def __init__(self):
    verb.Verb.__init__(self, 'status')

  def print_untracked(self, untracked):
    if len(untracked) == 0:
      return
    print UNTRACKED_HEADER
    for u in untracked:
      print '    %s' % os.path.relpath(u, os.getcwd())
    print ''

  def print_modified_or_to_be_committed(self, header, new_status, 
                                        modified_status, deleted_status, 
                                        combined_status):
    
    files = [(f, ' deleted') for f in combined_status[deleted_status]]
    files.extend([(f, 'modified') for f in combined_status[modified_status]])
    if new_status != None:
      files.extend([(f, 'new file') for f in combined_status[new_status]])
    print header
    files = sorted(files) 
    for file_name, status in files:
      print '    %s: %s' %(status, os.path.relpath(file_name, os.getcwd()))
    print ''

  def print_to_be_committed(self, combined_status):
    self.print_modified_or_to_be_committed(TO_BE_COMMITTED_HEADER, 
                                           pygit2.GIT_STATUS_INDEX_NEW,
                                           pygit2.GIT_STATUS_INDEX_MODIFIED,
                                           pygit2.GIT_STATUS_INDEX_DELETED,
                                           combined_status)
  def print_not_staged_for_commit(self, combined_status):
    self.print_modified_or_to_be_committed(NOT_STAGED_FOR_COMMIT_HEADER, 
                                           None,
                                           pygit2.GIT_STATUS_WP_MODIFIED,
                                           pygit2.GIT_STATUS_WP_DELETED,
                                           combined_status)
  def print_all(self, combined_status):
    self.print_to_be_committed(combined_status)
    self.print_untracked(combined_status[pygit2.GIT_STATUS_WT_NEW])
    
  def status(self):
    all_repos = self.all_repositories
    combined_status = collections.defaultdict(list)
    working_dirs = set([r.workdir for r in all_repos])
    for repo in all_repos:
      status = repo.status()
      for name, s in status.iteritems():
        abs_path = os.path.join(repo.workdir, name)
        # skip paths pointing to the submodule. Typically these directories 
        # should be added to gitignore files, but it's better to just not 
        # show the mat all in the status output.
        if abs_path in working_dirs:
          continue
        # we don't care about ignored files or files that are up-to-date
        if s in (pygit2.GIT_STATUS_CURRENT, pygit2.GIT_STATUS_IGNORED):
          continue
        combined_status[s].append(abs_path)
    self.print_all(combined_status)
    


def run(args):
  verb = Status()
  verb.status()
