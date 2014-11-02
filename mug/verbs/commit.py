import os
import pygit2
import verb
import collections
from argparse import ArgumentParser

class Commit(verb.Verb):
    def __init__(self):
        verb.Verb.__init__(self, 'commit')
    
    def commit(self, args):
        a = ArgumentParser()
        a.add_argument('files', nargs='*')
        opts = a.parse_args(args)
        print opts



def run(args):
  verb = Commit()
  verb.commit(args)
