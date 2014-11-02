import pygit2
import verb
import os

class Add(verb.Verb):
    def __init__(self):
        verb.Verb.__init__(self, 'add')
    def add(self, file_names):
        submugules = self.all_submugules
        main = self.main_repository
        for file_name in file_names:
            for sub in submugules:
                rel_path = os.path.relpath(file_name, sub.workdir)
                if rel_path.startswith('..'):
                    continue
                index = sub.index
                index.add(rel_path)
                index.write()
                break
            else:
                index = main.index
                index.add(rel_path)
                index.write()


def run(args):
  verb = Add()
  verb.add(args)
