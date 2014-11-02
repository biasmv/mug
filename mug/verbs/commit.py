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
    print opts

def run(repo, output, args):
    opts = parse_args(args)
