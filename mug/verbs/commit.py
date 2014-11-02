import os
import pygit2
import status

from argparse import ArgumentParser

def parse_args(args):
    a = ArgumentParser()
    a.add_argument('-a', '--all', action='store_true', default=False)
    a.add_argument('-m', '--message', default=None)
    a.add_argument('files', nargs='*')
    opts = a.parse_args(args)
    return opts

FILE_OF_MULTIPLE_REPOSITORIES_STAGED_FOR_COMMIT='''\
Files of multiple repositories are staged for commit. Split the
commits by repository.'''
def run(repo, output, args):
    opts = parse_args(args)
    if opts.all:
        for repository in repo.all_repositories:
            index = repository.index
            index.add_all()
            index.write()
    combined_status = status.status_all(repo)
    status_to_be_committed = (
        pygit2.GIT_STATUS_INDEX_MODIFIED, pygit2.GIT_STATUS_INDEX_DELETED, 
        pygit2.GIT_STATUS_INDEX_NEW
    )
    to_be_committed = []
    for st in status_to_be_committed:
        to_be_committed.extend(combined_status[st])
    if len(to_be_committed) == 0:
        return status.write_output(combined_status, output)
    # check that only files of one repository are staged
    by_repo = repo.files_by_repo(to_be_committed)
    if len(by_repo) > 1:
        status.write_output(combined_status, output)
        output.add_separator()
        output.add_error(FILE_OF_MULTIPLE_REPOSITORIES_STAGED_FOR_COMMIT)
        return False
    for repository, file_names in by_repo.iteritems():
        committer = pygit2.Signature(repository.config['user.name'], 
                                     repository.config['user.email'])
        author = committer
        index = repository.index
        tree_id = index.write_tree()
        parents = []
        if not repository.is_empty:
            parents.append(repository.revparse_single('HEAD').oid)
        repository.create_commit('HEAD', author, committer, 
                                 opts.message, tree_id, parents)




