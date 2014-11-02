import pygit2
import os

class Verb:
    def __init__(self, name):
        self.name = name
    def run(self, mug_repo, output):
        raise NotImplemented('run must be implemented by all verbs')


