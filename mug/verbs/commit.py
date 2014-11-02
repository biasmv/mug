import os
import pygit2
import status

from argparse import ArgumentParser

def parse_args(args):
    a = ArgumentParser()
    a.add_argument('-a', '-all', action='store_true', default=False)
    a.add_argument('-m', '--message', default=None)
    a.add_argument('files', nargs='*')
    opts = a.parse_args(args)

def run(repo, output, args):
    opts = parse_args(args)
    combined_status = status.status_all(repo)
    status_to_be_committed = (
        pygit2.GIT_STATUS_INDEX_MODIFIED, pygit2.GIT_STATUS_INDEX_DELETED, 
        pygit2.GIT_STATUS_INDEX_NEW
    )
    to_be_committed = []
    for st in status_to_be_committed:
        to_be_committed.extend(combined_status[st])
    if len(to_be_committed) == 0:
        status.write_output(combined_status, output)
        return

