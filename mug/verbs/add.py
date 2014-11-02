def run(repo, output, file_names):
    repo_file_name_map = repo.files_by_repo(file_names)
    for repository, file_names in repo_file_name_map.iteritems():
        index = repository.index
        for file_name in file_names:
            index.add(file_name)
        index.write()
