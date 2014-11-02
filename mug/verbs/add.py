import pygit2
import os

def run(repo, output, file_names):
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

