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

    def write_untracked(self, untracked, output):
        if len(untracked) == 0:
            return
        output.add_line(UNTRACKED_HEADER)
        for u in untracked:
            output.add_line('    %s' % os.path.relpath(u, os.getcwd()))
        output.add_separator()

    def write_modified_or_to_be_committed(self, header, new_status, 
                                          modified_status, deleted_status, 
                                          file_stats, output):
        files = [(f, ' deleted') for f in file_stats[deleted_status]]
        files.extend([(f, 'modified') for f in file_stats[modified_status]])
        if new_status != None:
                files.extend([(f, 'new file') for f in file_stats[new_status]])
        if len(files) == 0:
            return
        output.add_separator()
        output.add_line(header)
        files = sorted(files) 
        for file_name, status in files:
            rel_path = os.path.relpath(file_name, os.getcwd())
            output.add_line('    %s: %s' % (status, rel_path))

    def write_to_be_committed(self, combined_status, output):
        self.write_modified_or_to_be_committed(TO_BE_COMMITTED_HEADER, 
                                               pygit2.GIT_STATUS_INDEX_NEW,
                                               pygit2.GIT_STATUS_INDEX_MODIFIED,
                                               pygit2.GIT_STATUS_INDEX_DELETED,
                                               combined_status,
                                               output)
    def write_not_staged_for_commit(self, combined_status, output):
        self.write_modified_or_to_be_committed(NOT_STAGED_FOR_COMMIT_HEADER, 
                                               None,
                                               pygit2.GIT_STATUS_WT_MODIFIED,
                                               pygit2.GIT_STATUS_WT_DELETED,
                                               combined_status, output)
    def write_output(self, combined_status, output):
        if len(combined_status) == 0:
            output.add_line('nothing to commit, working directory clean')
            return
        self.write_to_be_committed(combined_status, output)
        self.write_not_staged_for_commit(combined_status, output)
        self.write_untracked(combined_status[pygit2.GIT_STATUS_WT_NEW], output)
    

    def collect_repo_status(self, repo, working_dirs, combined_status):
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
    def run(self, repo, output, args):
        all_repos = repo.all_repositories
        combined_status = collections.defaultdict(list)
        working_dirs = set([r.workdir for r in all_repos])
        for repo in all_repos:
            self.collect_repo_status(repo, working_dirs, combined_status)
        self.write_output(combined_status, output)
    


def run(repo, output, args):
  verb = Status()
  return verb.run(repo, output)
