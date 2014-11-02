import pygit2
import verb
import os

class Add(verb.Verb):
    def __init__(self):
        verb.Verb.__init__(self, 'add')
    def run(self, repo, output, file_names):
        sub_repositories = repo.sub_repositories
        main = repo.main_repository
        index = main.index
        for file_name in file_names:
            for sub in sub_repositories:
                rel_path = os.path.relpath(file_name, sub.workdir)
                if rel_path.startswith('..'):
                    continue
                index = sub.index
                break
            else:
                rel_path = os.path.relpath(file_name, main.workdir)
        index.add(rel_path)
        index.write()


def run(repo, output, args):
  verb = Add()
  verb.add(repo, output, args)
